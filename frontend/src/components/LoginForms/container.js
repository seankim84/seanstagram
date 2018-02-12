import React, { Component } from 'react';
import PropTypes from 'prop-types';
import LoginForm from './presenter';

class Container extends Component{
    state = {
        username:"",
        password:""
    }
    static propTypes = {
        facebookLogin:PropTypes.func.isRequired,
        usernameLogin:PropTypes.func.isRequired
    }
    render(){
        const {username, password} = this.state;
        return <LoginForm 
            handleInputChange={this._handleInputChange} 
            handleSubmit={this._handleSubmit}  
            handleFacebookLogin={this._handleFacebookLogin}
            usernameValue={username}  
            passwordValue={password} 
                />;
    }
    _handleInputChange = event => {
        const { target : {value, name} } = event; //const value = event.target.value;
        this.setState({
            [name]:value  //여기서 [name]은 위의 name argument를 의미한다. 그냥 name으로 작성하면, variable이다!
        });
    };
    _handleSubmit = event => {
        const { usernameLogin } = this.props;
        const { username, password } = this.state;
        event.preventDefault(); //preventDefault는 브라우저(구글,크롬,사파리 등등이 디폴트 작업을 하지 않는것)
        usernameLogin(username, password);
    };
    _handleFacebookLogin = response => {
        const { facebookLogin } = this.props;// 나중에 redux action 위치
        facebookLogin(response.accessToken);
    };
}

export default Container;