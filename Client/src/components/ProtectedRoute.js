// ProtectedRoute.js
import React from 'react';
import { useAuth } from '../context/AuthContext';
import AuthRedirectMessage from './AuthRedirectMessage';

const ProtectedRoute = ({ element }) => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? element : <AuthRedirectMessage />;
};

export default ProtectedRoute;
