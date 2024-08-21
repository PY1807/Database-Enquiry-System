import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({ otpver, children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!otpver) {
      navigate("/login");
    }
  }, [navigate]);

  // If the user is not logged in, do not render children
  if (!otpver) {
    return null;
  }

  // Render children if the user is logged in
  return children;
};

export default ProtectedRoute;
