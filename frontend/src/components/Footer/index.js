import React from 'react';
import PropTypes from 'prop-types';
import styles from './styles.scss';

const Footer = (props, context) => ( //stateless componet에는 context를 argument로 줘야한다.
  <footer className={styles.footer}>
    <div className={styles.column}>
    <nav className={styles.nav}>
      <ul className={styles.list}>
        <li className={styles.listItem}>{context.t("About Us")}</li>
        <li className={styles.listItem}>{context.t("Support")}</li>
        <li className={styles.listItem}>{context.t("Blog")}</li>
        <li className={styles.listItem}>{context.t("Press")}</li>
        <li className={styles.listItem}>{context.t("API")}</li>
        <li className={styles.listItem}>{context.t("Jobs")}</li>
        <li className={styles.listItem}>{context.t("Privacy")}</li>
        <li className={styles.listItem}>{context.t("Terms")}</li>
        <li className={styles.listItem}>{context.t("Directory")}</li>
        <li className={styles.listItem}>{context.t("Language")}</li>
      </ul>
      </nav>
    </div>
    <div className={styles.column}>
      <span className={styles.copyright}>@ 2018 Sean</span>
    </div>
  </footer>
); //context = 해당 Text를 translations할때(리덕스를 사용해서) 사용하는것

Footer.contextTypes = { // stateless로 context 주는법 
  t : PropTypes.func.isRequired //명확하게 함수를 정의
}; 

export default Footer;