import styles from "./Footer.module.css";

const Footer = () => {
  return (
    <>
      <footer>
        <div className={styles.footer_container}>
          <p className={styles.footer_text}>
            © 2025 JMT - Algo Stock Trading - All rights reserved.
          </p>
        </div>
      </footer>
    </>
  );
};

export default Footer;
