import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { verifyEmailToken } from "../api/VerifyEmail_api";
import Toast from "../components/Toast/ToastPopup";
import styles from "./styles/Verify.module.css";

const VerifyEmail = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [token, setToken] = useState(null);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tokenFromURL = params.get("token");

    if (!tokenFromURL) {
      setToast({ message: "Missing token.", type: "error" });
    } else {
      setToken(tokenFromURL);
    }
  }, [location.search]);

  const handleVerify = async () => {
    if (!token) return;

    const result = await verifyEmailToken(token);
    setToast({
      message: result.message,
      type: result.success ? "success" : "error",
    });

    if (result.redirectImmediately) {
      setTimeout(() => navigate("/register"), 0);
    } else if (result.success) {
      setTimeout(() => navigate("/"), 2000);
    }
  };

  return (
    <div className={styles.verifyContainer}>
      <h1 className={styles.title}>Verify Your Email</h1>
      <button onClick={handleVerify} className={styles.verifyBtn}>
        Verify
      </button>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default VerifyEmail;
