import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/Login_api";
import { handleLoginSubmit } from "../utils/loginSubmitHandler";
import { handleInput } from "../utils/sanitizerHelper";
import Toast from "../components/Toast/ToastPopup";
import styles from "./styles/Login.module.css";

const LoginScreen = () => {
  const navigate = useNavigate();
  const emailRef = useRef(null);
  const passwordRef = useRef(null);
  const [attempts, setAttempts] = useState(0);
  const [toast, setToast] = useState(null);
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [inputStatus, setInputStatus] = useState({ email: "", password: "" });

  const isLocked = attempts >= 3;

  const handleChange = (e) => {
    handleInput({
      e,
      formData,
      setFormData,
      setInputStatus,
      setToast,
    });
  };

  const handleSubmit = (e) => {
    handleLoginSubmit({
      e,
      formData,
      setInputStatus,
      setToast,
      emailRef,
      passwordRef,
      loginUser,
      setAttempts,
      attempts,
      navigate,
    });
  };

  return (
    <div className={styles.loginContainer}>
      <h1 className={styles.title}>Login</h1>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div>
          <label className={styles.label}>Email:</label>
          <input
            className={`${styles.input} ${
              inputStatus.email === "error" ? styles.error : ""
            } ${inputStatus.email === "success" ? styles.success : ""}`}
            ref={emailRef}
            name="email"
            placeholder="Your@Email.com"
            value={formData.email}
            autoComplete="email"
            onChange={(e) => {
              handleChange(e);
            }}
          />
        </div>
        <div>
          <label className={styles.label}>Password:</label>
          <input
            className={`${styles.input} ${
              inputStatus.password === "error" ? styles.error : ""
            } ${inputStatus.password === "success" ? styles.success : ""}`}
            ref={passwordRef}
            name="password"
            type="password"
            placeholder="Password"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className={styles.center}>
          <button
            className={`${styles.loginBtn} ${
              isLocked ? styles.disabledBtn : ""
            }`}
            type="submit"
          >
            {isLocked ? "Locked" : "Login"}
          </button>
        </div>
      </form>
      {/* Toast msg */}
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

export default LoginScreen;
