import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { sanitizeTwoFaCode } from "../utils/sanitizerTwoFa";
import { handleTwoFaSubmit } from "../utils/handleTwoFaSubmit";
import Toast from "../components/Toast/ToastPopup";
import styles from "./styles/TwoFaScreen.module.css";

const TwoFaScreen = () => {
  const [code, setCode] = useState("");
  const [toast, setToast] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const sanitized = sanitizeTwoFaCode(e.target.value);
    setCode(sanitized);
  };

  const handleSubmit = (e) => {
    handleTwoFaSubmit({
      e,
      code,
      setCode,
      setToast,
      navigate,
    });
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Authentication</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="text"
          value={code}
          onChange={handleChange}
          maxLength={6}
          inputMode="numeric"
          pattern="\d*"
          placeholder="Enter 6-digit code"
          className={styles.input}
        />
        <button
          type="submit"
          className={styles.verifyBtn}
          disabled={code.length !== 6}
        >
          Verify
        </button>
      </form>
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

export default TwoFaScreen;
