import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    const checkToken = async () => {
      try {
        const res = await fetch("/api/auth/verify-cookie", {
          credentials: "include",
        });
        const data = await res.json();
        setIsValid(data.success === true);
      } catch {
        setIsValid(false);
      }
    };
    checkToken();
  }, []);
  if (isValid === null) return <div>Loading...</div>;
  return isValid ? children : <Navigate to="/register" replace />;
};

export default ProtectedRoute;
