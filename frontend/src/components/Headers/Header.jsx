import { useNavigate } from "react-router-dom";
import styles from "./Header.module.css";

const Header = () => {
  const navigate = useNavigate();

  const handleIconClick = () => {
    if (location.pathname === "/Register") {
      navigate("/");
    } else {
      navigate("/Register");
    }
  };

  return (
    <>
      <div className={styles.headerContainer}>
        <div className={styles.headerMenu} onClick={handleIconClick}>
          <div className={styles.tooltip}>
            <div className={styles.icon}>
              <span className={styles.tooltiptext}>
                {location.pathname === "/Register" ? "Login" : "Register"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Header;
