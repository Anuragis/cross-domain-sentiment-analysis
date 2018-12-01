from flask import Flask, jsonify, request
import json
from train import *
import pickle, os
from flask_cors import CORS, cross_origin

d = {}
pickle_file = "trained_model"
if os.path.isfile(pickle_file):
    infile = open(pickle_file, 'rb')
    d = pickle.load(infile)
    infile.close()
    print("File loaded from pickle...")
else:
    print("Pickle not found training the model...")
    d = train_model()
    out_file = open(pickle_file, 'wb')
    pickle.dump(d, out_file)
    out_file.close()
    print("Model saved to pickle...")


def predict(tempList):
    test_samples = tempList
    X_test_tokens = d['tokenizer_obj'].texts_to_sequences(test_samples)
    X_test_tokens_pad = sequence.pad_sequences(X_test_tokens, maxlen=d['max_length'])
    resultArray = d['model'].predict(x=X_test_tokens_pad)
    return resultArray


app = Flask(__name__)
# CORS(app, supports_credentials = True)
CORS(app, resources={r"/": {"origins": ""}})


# @app.route("/")
# def hello():
#     global d
#     return jsonify(d)



@app.route("/predict", methods=['POST'])
@cross_origin(supports_credentials=True)
def predictResult():
    request_data = request.get_json()
    print(request_data)
    print(request_data['list'])
    
    finalArray = predict(request_data['list'])
    
    finalArray = finalArray.tolist()

    print("finalArray:", finalArray)
    new_list = []
    cnt = 0
    for i in finalArray:
        tempList = []
        if i[0] > 0.75:
            tempList.append(request_data['list'][cnt])
            tempList.append('positive sentiment')
            new_list.append(tempList)
        if i[0] < 0.35:
            tempList.append(request_data['list'][cnt])
            tempList.append('negative sentiment')
            new_list.append(tempList)
        if i[0] > 0.35 and i[0]<0.40:
            tempList.append(request_data['list'][cnt])
            tempList.append('Neutral with a more negative sense')
            new_list.append(tempList)
        if i[0] > 0.40 and i[0]<0.50:
            tempList.append(request_data['list'][cnt])
            tempList.append('Neutral')
            new_list.append(tempList)
        if i[0] > 0.50 and i[0] < 0.60:
            tempList.append(request_data['list'][cnt])
            tempList.append('Neutral with slight positive sense')
            new_list.append(tempList)
            #new_list.append('Neutral with slight positive sense')
        if i[0] > 0.60 and i[0] < 0.75:
            tempList.append(request_data['list'][cnt])
            tempList.append('Neutral with more positive sense')
            new_list.append(tempList)
            #new_list.append('Neutral with more positive sense')
        cnt += 1
    print("new_list:", new_list)
    tempDict = {
        "final_output": new_list
    }
    return jsonify(tempDict)


app.run(port=1234)