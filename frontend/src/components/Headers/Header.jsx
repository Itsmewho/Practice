import { useNavigate } from "react-router-dom";
import styles from "./Header.module.css";

const Header = () => {
  return (
    <>
      <div className={styles.headerContainer}>
        <div className={styles.headerMenu}></div>
      </div>
    </>
  );
};

export default Header;
