import { useEffect } from "react";
import styles from "./styles/Toast.module.css";

const Toast = ({ message, type = "info", onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`${styles.toast} ${styles[type]}`}>
      <div className={styles.fadeIn}>{message}</div>
    </div>
  );
};

export default Toast;
