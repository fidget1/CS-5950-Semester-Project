// File:        App.js
// Author:      Jeremy Evans
//
// Description: Primary component of the application, containing both the form and the
//              graph (this is done to address the issue of sharing state across
//              the two without the use of ES6 classes for the sake of time).
//           
// ===================================================================================

import React from 'react';
import TwGraph from './TwGraph'
import './TwForm.css';
import './TwGraph.css';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            filter: '',
            processing: false,
            error: null,
            data: [],
            sentiments: {"positive" : 0, "mixed" : 0, "neutral" : 0, "negative" : 0}
        };

        // Bindings: TwForm
        this.addData = this.addData.bind(this);
        this.clearData = this.clearData.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCallToFlask = this.handleCallToFlask.bind(this);

        // Bindings: TwGraph
        this.addSentiment = this.addSentiment.bind(this);
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
        this.setState({
            data: [],
            sentiments: {"positive" : 0, "mixed" : 0, "neutral" : 0, "negative" : 0}
        });
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
                let newData = this.addData(result);
                this.setState({
                    processing: result.processing,
                    data: this.state.data.concat(newData),
                    sentiments: this.addSentiment(newData.documentSentiment)
                });
                console.log(this.state.sentiments);

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

    // Determines a sentiment based on a given score. Each sentiment is given a
    // number and defined as:
    //
    // Positive (4): score in [0.4, 1.0]
    //
    // Mixed (3): score in (-0.4, 0.4) & magnitude in [3.0, inf)
    //
    // Neutral (2): score in (-0.4, 0.4) & magnitude in [0, 3.0)
    // 
    // Negative(1): score in [-1.0, -0.4]
    addSentiment(documentSentiment) {
        let posScoreMin = 0.4;
        let negScoreMax = -0.4;
        let mixedMagMin = 3.0;

        let updatedSentiments = this.state.sentiments;

        // If the sentiment is positive
        if (documentSentiment.score >= posScoreMin) {
            updatedSentiments.positive += 1;
        }

        // ...is negative
        else if (documentSentiment.score <= negScoreMax) {
            updatedSentiments.negative += 1;
        }

        else {
            // ...is mixed
            if (documentSentiment.magnitude >= mixedMagMin) {
                updatedSentiments.mixed += 1;
            }

            // ...is neutral
            else {
                updatedSentiments.neutral += 1;
            }
        }

        return updatedSentiments;
    }
    // ===============================================================================
    // RENDER
    // ===============================================================================

    render() {
        return (
            <div>
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
                <TwGraph data={[
                    this.state.sentiments.positive, 
                    this.state.sentiments.mixed,
                    this.state.sentiments.neutral,
                    this.state.sentiments.negative]}
                    width={500}
                    height={500} />  
            </div>
        );
    }
}

export default App;
