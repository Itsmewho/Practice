import React, { useEffect } from "react";
import styles from "./styles/Toast.module.css";

const Toast = ({ message, type = "info", onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 2000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return <div className={`${styles.toast} ${styles[type]}`}>{message}</div>;
};

export default Toast;
