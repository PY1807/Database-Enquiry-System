import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({ otpsent, children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!otpsent) {
      navigate("/login");
    }
  }, [navigate]);

  // If the user is not logged in, do not render children
  if (!otpsent) {
    return null;
  }

  // Render children if the user is logged in
  return children;
};

export default ProtectedRoute;
