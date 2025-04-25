import React, { useState } from "react";
import Toast from "../Toast/ToastPopup";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../api/login_api";
import styles from "./styles/Login.module.css";

const LoginScreen = () => {
  const [attempts, setAttempts] = useState(0);
  const [toast, setToast] = useState(null);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const showToast = (message, type) => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const sanitizeInput = (value) => {
    return value.replace(/[<>]/g, ""); // Prevent basic HTML injection
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const sanitized = sanitizeInput(value);
    setFormData((prev) => ({
      ...prev,
      [name]: sanitized,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      showToast("Please fill out all fields", "error");
      return;
    }

    if (attempts >= 5) {
      showToast("Too many login attempts. Please wait.", "error");
      return;
    }

    const result = await loginUser(formData);

    showToast(result.message, result.success ? "success" : "error");

    if (result.success) {
      setTimeout(() => navigate("/2Fa"), 1500);
    } else {
      setAttempts((prev) => prev + 1);
    }
  };

  return (
    <div className={styles.login_container}>
      <h1 className={styles.title}>Login</h1>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div>
          <label className={styles.label}>Email:</label>
          <input
            className={styles.input}
            type="email"
            name="email"
            required
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div>
          <label className={styles.label}>Password:</label>
          <input
            className={styles.input}
            type="password"
            name="password"
            required
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className={styles.center}>
          <button className={styles.login_btn} type="submit">
            Login
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
