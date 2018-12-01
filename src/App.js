import React, { Component } from 'react';
import './App.css';
import * as API from './API.js';

import Dropzone from 'react-dropzone';
import { CSVLink, CSVDownload } from "react-csv";
import { Col, Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';

class App extends Component {

    constructor() {
        super()
        this.state = {
            files: [],
            strings: '',
            responseData: '',
            sentimentString: '',
            resultSentiment: 'tesr',
            isHidden: true
        }
    }

    onSubmitSentimentString = () => {
        var string = [this.state.sentimentString]
        var payload = {
            "list" : string
        }

        API.predictSentiment(payload)
            .then((res) => {
                console.log("String to show:"+res.data.final_output[0][1]);
                this.setState({
                    resultSentiment: res.data.final_output[0][1],
                    isHidden: false
                })
            })
    }
        onDrop = (acceptedFiles) => {
        console.log("In dropzone");
        acceptedFiles.forEach(file => {
            const reader = new FileReader();
            reader.onload = () => {

                var inputCSVText = reader.result;
                var strings = inputCSVText.split("\n");

                this.setState({
                    strings: strings
                });

                var payload = {
                    "list": this.state.strings
                }

                API.predictSentiment(payload)
                    .then((res) => {
                        this.setState({
                            responseData: res.data.final_output
                        })
                    })

            };

            reader.onabort = () => console.log('file reading was aborted');
            reader.onerror = () => console.log('file reading has failed');

            reader.readAsBinaryString(file);
        });
    }

    onCancel() {
        this.setState({
            files: []
        });
    }

  render() {
    return (
      <div className="App">
        <header className="App-header">
            <h2 style={{position: "relative", bottom: "50px"}}>Generalized Sentiment Analyser</h2>
            <FormGroup className="col-lg-4">
                {/*<Label for="sentimentString">Email</Label>*/}
                <Input type="sentimentString"
                       onChange={(event) => {
                           this.setState({
                               sentimentString: event.target.value
                           });
                       }}
                       name="sentimentString" id="inputString" placeholder="Enter your input string here" />
            </FormGroup>
            <FormGroup check row>
                <Col sm={{ size: 10, offset: 2 }}>
                    <Button className="btn btn-primary" onClick={() => {
                        this.onSubmitSentimentString();
                    }}>Submit</Button>
                </Col>
            </FormGroup>
            <FormText color="white" hidden={this.state.isHidden}>
                Sentiment: {this.state.resultSentiment}
            </FormText>
            <br/>OR
            <section>
                <div className="dropzone">
                    <Dropzone
                        // style={{cursor: 'pointer'}}
                        onDrop={this.onDrop.bind(this)}
                        onFileDialogCancel={this.onCancel.bind(this)}
                    >
                        <p>Drop your csv file here, or click to select a file to upload.</p>
                    </Dropzone>
                </div>
                <br/>
                <CSVLink
                    data={this.state.responseData}
                    filename={"sentiment-report.csv"}
                    className="btn btn-primary"
                    target="_blank"
                >
                    Download Report
                </CSVLink>
            </section>
        </header>
      </div>
    );
  }
}

export default App;
