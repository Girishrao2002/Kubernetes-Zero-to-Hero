import React, {useEffect, useState} from 'react';
import axios from 'axios';
import './App.css';

function App(){
  const [message, setMessage] = useState('Loading...');
  useEffect(()=>{
    axios.get('/api/message')
      .then(res=> setMessage(res.data.message))
      .catch(()=> setMessage('Failed to fetch'));
  },[]);
  return (
    <div className="App">
      <header className="App-header">
        <h1>Ingress Demo</h1>
        <p>Backend message: {message}</p>
      </header>
    </div>
  );
}

export default App;
