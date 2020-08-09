// File:        App.js
// Author:      Jeremy Evans
//
// Description: Primary component of the application, containing both the form and the
//              graph (this is done to address the issue of sharing state across
//              the two without the use of ES6 classes for the sake of time).
//           
// ===================================================================================

import React from 'react';
import * as d3 from "d3"
import './TwForm.css';
import './TwGraph.css';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            filter: '',
            processing: false,
            error: null,
            data: []
        };

        // Bindings: TwForm
        this.addData = this.addData.bind(this);
        this.clearData = this.clearData.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCallToFlask = this.handleCallToFlask.bind(this);
    }

    // ===============================================================================
    // TWFORM
    // ===============================================================================

    addData(result) {
        var tweetText = "";
        for (var sentence of result.sentences) {
            tweetText = tweetText.concat(sentence.text.content + " ");
        }

        return {
            "documentSentiment" : result.documentSentiment,
            "text" : tweetText
        };
    }

    clearData() {
        this.setState({data: []});
    }

    // Alters the "filter" state upon change
    handleChange(event) {
        this.setState({filter: event.target.value});
    }

    // Simulates a submission by sending dummy JSON data to TwGraph
    handleSubmit(event) {
        if (!this.state.processing) {
            this.setState({processing: true});
            this.clearData();
            this.handleCallToFlask();
        }
        event.preventDefault();
    }

    // Repeatedly calls flask until flasks returns processing: false
    handleCallToFlask() {
        fetch("http://127.0.0.1:5000/get_test_data")
        .then(res => res.json())
        .then(
            // On success
            (result) => {
                this.setState({
                    processing: result.processing,
                    data: this.state.data.concat(this.addData(result))
                });
                console.log(this.state.data);

                if (this.state.processing) {
                    this.handleCallToFlask();
                }
            },
            // On failure
            (error) => {
                this.setState({
                    error
                });
                console.log(error);
            }
        )   
    }

    // ===============================================================================
    // TWGRAPH
    // ===============================================================================

    // ===============================================================================
    // RENDER
    // ===============================================================================

    render() {
        return (
            <section id="tw-form">
                <div id="tw-form-container">
                    <h3>Filter Input</h3>
                    <form onSubmit={this.handleSubmit}>
                        <div className="tw-form-box">
                            <input type="text" value={this.state.filter} onChange={this.handleChange} placeholder="e.g. Fortnite" required/>
                            <label>Filter</label>
                        </div>
                        <input type="submit" value="Submit"/>
                    </form>
                </div>
            </section>
        );
    }
}

export default App;
