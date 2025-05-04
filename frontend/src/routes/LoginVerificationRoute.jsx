import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const LoginVerificationRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    const checkLoginCookie = async () => {
      try {
        const res = await fetch("/api/auth/verify-login-cookie", {
          credentials: "include",
        });
        const data = await res.json();
        setIsValid(data.success === true);
      } catch {
        setIsValid(false);
      }
    };
    checkLoginCookie();
  }, []);

  if (isValid === null) return <div>Verifying login...</div>;
  return isValid ? children : <Navigate to="/" replace />;
};

export default LoginVerificationRoute;
