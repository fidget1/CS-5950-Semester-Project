import * as d3 from "d3"
import logo from './logo.svg';
import React from 'react';
import './App.css';

// =========================================================================================
// Form
//
// Simple form consisting of a text area that allows the user to enter a set of search
// filters (current: 1). Upon submission, it builds a request in the form of JSON containing
// the filters and sends it to the backend.

class TwForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: '',
      error: null,
      data: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmitTest = this.handleSubmitTest.bind(this);
  }

  // Alters the "filter" state upon change
  handleChange(event) {
    this.setState({filter: event.target.value})
  }

  // Simulates a submission by sending dummy JSON data to TwGraph
  handleSubmitTest(event) {
    fetch("http://127.0.0.1:5000/get_test_data")
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          data: result.items
        });
        console.log(this.data);
      },
      (error) => {
        this.setState({
          error
        });
        console.log(error);
      }
    )
    event.preventDefault();
  }

  render() {
    return (
      <section id="tw-form">
        <div id="tw-form-container">
          <h3>Filter Input</h3>
          <form onSubmit={this.handleSubmitTest}>
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

// =========================================================================================
// Display (Graph)

class TwGraph extends React.Component {
  render() {
    return (
      <section id="tw-graph">
        <div id="tw-graph-container">

        </div>
      </section>
    );
  }
}

// =========================================================================================
// Render (esentially a "main")

function App() {
  return (
    <div className="App">
      <TwForm/>
      {/* <TwGraph/> */}
    </div>
  );
}

export default App;
