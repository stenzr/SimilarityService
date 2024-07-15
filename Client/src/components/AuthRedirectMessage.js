// AuthRedirectMessage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const AuthRedirectMessage = () => {
  const navigate = useNavigate();

  React.useEffect(() => {
    // Redirect after a short delay to allow the message to be displayed
    const timer = setTimeout(() => {
      navigate('/register');
    }, 5000); // Delay of 3 seconds

    return () => clearTimeout(timer); // Cleanup timer on unmount
  }, [navigate]);

  return (
    <div>
      <h1>You need to be authenticated to access this page.</h1>
      <p>Redirecting you to the registration page...</p>
    </div>
  );
};

export default AuthRedirectMessage;
