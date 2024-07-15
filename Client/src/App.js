import React from 'react';
import Register from './components/Register';
import Detect from './components/Detect';
import Refill from './components/Refill';

const App = () => {
  return (
    <div>
      <h1>Similarity Service</h1>
      <Register />
      <Detect />
      <Refill />
    </div>
  );
};

export default App;
