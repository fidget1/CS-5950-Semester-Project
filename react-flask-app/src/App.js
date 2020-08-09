import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [tweets, setTweets] = useState(0)
  useEffect(() => {
    fetch('/hello').then(res => res.json()).then(data => {
      setTweets(data.tweets);
    });
  }, []);
  console.log({tweets})
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
	<p>The current time is {tweets}.</p>
      </header>
    </div>
  );
}

export default App;
