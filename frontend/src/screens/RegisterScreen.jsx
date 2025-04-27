import { useState, useRef } from "react";
import { handleInput } from "../utils/sanitizerHelper";
import { handleRegisterSubmit } from "../utils/registerSubmitHandler";
import { registerUser } from "../api/Register_api";
import Toast from "../components/Toast/ToastPopup";
import styles from "./styles/Register.module.css";

const RegisterScreen = () => {
  const emailRef = useRef(null);
  const nameRef = useRef(null);
  const passwordRef = useRef(null);
  const confirmPasswordRef = useRef(null);

  const [toast, setToast] = useState(null);
  const [attempts, setAttempts] = useState(0);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [inputStatus, setInputStatus] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

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
    handleRegisterSubmit({
      e,
      formData,
      setFormData,
      setInputStatus,
      setToast,
      registerUser,
      setAttempts,
      attempts,
    });
  };

  return (
    <div className={styles.registerContainer}>
      <h1 className={styles.title}>Register</h1>
      <form className={styles.form} onSubmit={handleSubmit} autoComplete="off">
        <div>
          {/* Name */}
          <label className={styles.label}>Name</label>
          <input
            className={`${styles.input} ${
              inputStatus.name === "error" ? styles.error : ""
            } ${inputStatus.name === "success" ? styles.success : ""}`}
            ref={nameRef}
            value={formData.name}
            name="name"
            placeholder="Yourname"
            autoComplete="off"
            onChange={handleChange}
          />
          {/* Email */}
          <label className={styles.label}>Email:</label>
          <input
            className={`${styles.input} ${
              inputStatus.email === "error" ? styles.error : ""
            } ${inputStatus.email === "success" ? styles.success : ""}`}
            ref={emailRef}
            value={formData.email}
            name="email"
            placeholder="Your@Email.com"
            autoComplete="off"
            onChange={handleChange}
          />

          {/* Password */}
          <label className={styles.label}>Password:</label>
          <input
            className={`${styles.input} ${
              inputStatus.password === "error" ? styles.error : ""
            } ${inputStatus.password === "success" ? styles.success : ""}`}
            ref={passwordRef}
            value={formData.password}
            name="password"
            type="password"
            placeholder="min 6 characters"
            autoComplete="new-password"
            onChange={handleChange}
          />

          {/* Confirm Password */}
          <label className={styles.label}>Confirm Password:</label>
          <input
            className={`${styles.input} ${
              inputStatus.confirmPassword === "error" ? styles.error : ""
            } ${
              inputStatus.confirmPassword === "success" ? styles.success : ""
            }`}
            ref={confirmPasswordRef}
            value={formData.confirmPassword}
            name="confirmPassword"
            type="password"
            autoComplete="new-password"
            onChange={handleChange}
          />
        </div>

        <div className={styles.center}>
          <button
            className={`${styles.registerBtn} ${
              isLocked ? styles.disabledBtn : ""
            }`}
            type="submit"
            disabled={isLocked}
          >
            {isLocked ? "Locked" : "Register"}
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

export default RegisterScreen;
