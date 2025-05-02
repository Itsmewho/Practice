import styles from "./styles/RegisterSuccess.module.css";

const RegisterSuccessScreen = () => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Almost there!</h1>
      <p className={styles.message}>
        Please check your email to verify your account.
      </p>
    </div>
  );
};

export default RegisterSuccessScreen;
