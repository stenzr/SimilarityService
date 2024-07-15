import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './components/Register';
import Detect from './components/Detect';
import Refill from './components/Refill';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <div>
          <nav>
            <ul>
              <li>
                <Link to="/register">Register</Link>
              </li>
              <li>
                <Link to="/detect">Detect Similarity</Link>
              </li>
              <li>
                <Link to="/refill">Refill Tokens</Link>
              </li>
            </ul>
          </nav>

          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/detect" element={<ProtectedRoute element={<Detect />} />} />
            <Route path="/refill" element={<ProtectedRoute element={<Refill />} />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
