import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import Dropout
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

requiredObjects = {}

def train_model():
    ggl_review_data = pd.read_csv("googleplaystore_user_reviews.csv")
    azn_food_review_data = pd.read_csv("Reviews.csv")
    rst_review_data=pd.read_csv('Restaurant_Reviews.tsv',delimiter='\t',encoding='utf-8')
    
    ggl_review_data = ggl_review_data.dropna(how='any')
    ggl_review_data = ggl_review_data[ggl_review_data['Sentiment'] != 'Neutral']
    azn_food_review_data = azn_food_review_data[azn_food_review_data['Score'] != 3]

    ggl_review_Text_Data = ggl_review_data['Translated_Review']
    ggl_sentiment_Text_Data = ggl_review_data['Sentiment'].tolist()

    azn_review_Text_Data = azn_food_review_data['Text']
    azn_sentiment_Text_Data = azn_food_review_data['Score'].tolist()

    rst_review_Text_Data = rst_review_data['Review']
    rst_sentiment_Text_Data = rst_review_data['Liked'].tolist()

    frames = [ggl_review_Text_Data, azn_review_Text_Data, rst_review_Text_Data]
    result = pd.concat(frames)
    requiredObjects['result'] = result


    tokenizer_obj = Tokenizer()
    requiredObjects['tokenizer_obj'] = tokenizer_obj
    tokenizer_obj.fit_on_texts(result)
    max_length = max([len(s.split()) for s in result])
    requiredObjects['max_length'] = max_length



    #define vocabulary size
    vocab_size = len(tokenizer_obj.word_index) + 1
    X_train_tokens = tokenizer_obj.texts_to_sequences(result)

    sentiment_output_matrix = []
    ## Google
    for i in range (0, len(ggl_sentiment_Text_Data)):
        if ggl_sentiment_Text_Data[i] == 'Positive':
            sentiment_output_matrix.append(1)
        else:
            sentiment_output_matrix.append(0)
    

    ## Amazon
    for i in range (0, len(azn_sentiment_Text_Data)):
        if int(azn_sentiment_Text_Data[i]) > 3:
            sentiment_output_matrix.append(1)
        if int(azn_sentiment_Text_Data[i]) < 3 :
            sentiment_output_matrix.append(0)

    ## Restaurant
    sentiment_output_matrix = sentiment_output_matrix + rst_sentiment_Text_Data

    X_train_tokens_pad = sequence.pad_sequences(X_train_tokens, maxlen=max_length)

    embedding_vecor_length = 64
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_vecor_length, input_length=max_length))
    model.add(Dropout(0.3))
    model.add(LSTM(100))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train_tokens_pad, sentiment_output_matrix, epochs=1, batch_size=128)
    print(model.summary())

    requiredObjects['model'] = model

    return requiredObjects

