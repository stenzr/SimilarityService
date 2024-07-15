import React, { useState } from 'react';
import axios from 'axios';

const Refill = () => {
  const [username, setUsername] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [refillAmount, setRefillAmount] = useState('');
  const [message, setMessage] = useState('');

  const handleRefill = async () => {
    try {
      const response = await axios.post('http://localhost:5000/refill', {
        username,
        admin_pw: adminPassword,
        refill: parseInt(refillAmount, 10),
      });
      setMessage(response.data.msg);
    } catch (error) {
      setMessage('Refill failed');
    }
  };

  return (
    <div>
      <h2>Refill Tokens</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Admin Password"
        value={adminPassword}
        onChange={(e) => setAdminPassword(e.target.value)}
      />
      <input
        type="number"
        placeholder="Refill Amount"
        value={refillAmount}
        onChange={(e) => setRefillAmount(e.target.value)}
      />
      <button onClick={handleRefill}>Refill</button>
      <p>{message}</p>
    </div>
  );
};

export default Refill;
