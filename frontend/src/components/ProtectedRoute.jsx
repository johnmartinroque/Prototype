// src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ user, children }) {
  if (!user) {
    // if no user, redirect to authentication
    return <Navigate to="/authentication" replace />;
  }
  return children;
}

export default ProtectedRoute;
