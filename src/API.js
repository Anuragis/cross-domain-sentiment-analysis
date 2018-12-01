// const api = process.env.REACT_APP_CONTACTS_API_URL || 'http://localhost:8080'
const url = 'http://localhost:1234';
// const url = 'http://www.surveyape.ga:8080';
const axios = require("axios");
// import axios from 'axios';

const headers = {
    'Accept': 'application/json'
};

axios.defaults.withCredentials = true;

// export const predictSentimentDummy = (payload) =>{
//     console.log(payload);
//     return payload;
// };


export const predictSentiment = (payload) =>{
    console.log("In requewst...", payload)
    return axios.post(url + '/predict', payload)
        .then(function (response) {
            console.log(response);
            return response;
        })
        .catch(function (error) {
            console.log(error);
            return error;
        });
};
