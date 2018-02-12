import React, { Component } from "react";
import PropTypes from 'prop-types';
import SignupForm from "./presenter";

class Container extends Component {
  state = {
    email: "",
    name: "",
    username: "",
    password: ""
  };
  static PropTypes = {
    facebookLogin:PropTypes.func.isRequired, //새로운 props가 생겼으므로 type을 설정
    createAccount:PropTypes.func.isRequired
  }
  render() {
    const { email, name, username, password } = this.state;
    return (
      <SignupForm
        emailValue={email}
        nameValue={name}
        usernameValue={username}
        passwordValue={password}
        handleInputChange={this._handleInputChange}
        handleSubmit={this._handleSubmit}
        handleFacebookLogin={this._handleFacebookLogin}
      />
    );
  }
  _handleInputChange = event => {
    const { target: { value, name } } = event;
    this.setState({
      [name]: value
    });
  };
  _handleSubmit = event => {
    const {email, name, password, username } = this.state;
    const { createAccount } = this.props;
    event.preventDefault();
    createAccount(username, password, email, name)

  };
  _handleFacebookLogin = response => { //누군가 facebook을 누르면, handleFacebookLogin 작동
    const { facebookLogin } = this.props;
    facebookLogin(response.accessToken) //response에는 accessToken이 있다.
  };
}

export default Container;
