import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const LoggedInRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await fetch("/api/auth/session-check", {
          credentials: "include",
        });
        const data = await res.json();
        setIsValid(data.success === true);
      } catch {
        setIsValid(false);
      }
    };
    checkSession();
  }, []);

  if (isValid === null) return <div>Loading session...</div>;
  return isValid ? children : <Navigate to="/login" replace />;
};

export default LoggedInRoute;
