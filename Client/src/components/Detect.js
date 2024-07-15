import React, { useState } from 'react';
import axios from 'axios';

const Detect = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [similarity, setSimilarity] = useState('');
  const [message, setMessage] = useState('');

  const handleDetect = async () => {
    try {
      const response = await axios.post('http://localhost:5000/detect', {
        username,
        password,
        text1,
        text2,
      });
      setSimilarity(response.data.results.similarity);
      setMessage(response.data.msg);
    } catch (error) {
      setMessage('Detection failed');
    }
  };

  return (
    <div>
      <h2>Detect Similarity</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <textarea
        placeholder="Text 1"
        value={text1}
        onChange={(e) => setText1(e.target.value)}
      ></textarea>
      <textarea
        placeholder="Text 2"
        value={text2}
        onChange={(e) => setText2(e.target.value)}
      ></textarea>
      <button onClick={handleDetect}>Detect</button>
      <p>{message}</p>
      {similarity && <p>Similarity: {similarity}</p>}
    </div>
  );
};

export default Detect;
