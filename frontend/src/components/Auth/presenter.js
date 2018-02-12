import React from "react";
import styles from "./styles.scss";
import LoginForm from 'components/LoginForms';
import SignupForm from 'components/SignupForms';

const Auth = (props, context) => ( //img가 필요한땐 require입력!(.png입력 잊지 말것!), context = 리덕스를 사용해, 해당 text를 번역할때 사용!
  <main className={styles.auth}>
    <div className={styles.column}>
      <img src={require("images/phone.png")} alt="Checkout our app. Is cool" /> 
    </div>
    <div className={styles.column}>
    <div className={`${styles.whiteBox} ${styles.formBox}`}>
     <img src={require("images/sean.png")} alt="Logo" />
      {props.action === "login" && <LoginForm />}
      {props.action === "signup" && <SignupForm />}
    </div>
      <div className={styles.whiteBox}>
        {props.action === 'login' && (
            <p>Don't have an account?{" "}
                <span onClick={props.changeAction} className={styles.changeLink}>
                    Sign up
                </span>
             </p>
            )}
        {props.action === 'signup' && (
            <p>Have an account?{" "}
                <span onClick={props.changeAction} className={styles.changeLink}>
                    Log in
                </span>
            </p>
            )}
      </div>
      <div className={styles.appBox}>
        <span>Get the app</span>
        <div className={styles.appstores}>
          <img
            src={require("images/ios.png")}
            alt="Download it on the Apple Appstore"
          />
          <img
            src={require("images/android.png")}
            alt="Download it on the Apple Android store"
          />
        </div>
      </div>
    </div>
  </main>
);
export default Auth;
