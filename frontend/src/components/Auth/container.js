import React, { Component } from 'react';
import Auth from "./presenter";
//Sign up 과 Login 사이엔 두개의 state변화가 있다.(state변화는 container에 입력한다!! 중요!!)
class Container extends Component{
    state = {
        action : "login" // state에는 action이 있고, 그 action의 이름은 login
    };
    render(){
        const {action} = this.state; 
        return <Auth action = {action} changeAction={this._changeAction} />;
    } //Signup, Login 사이의 state 변화가 있을 것을 정의
    _changeAction = () => {
        this.setState(prevState => { //여기에 새로운 state를 넣으면 state를 변화시킬 수 있다.(근데 current state가 뭔지 알아야 한다.)
            const { action } = prevState;
            if( action === 'login'){ // 현재 state가 login이면 회원가입으로 변경시키고
                return{
                    action : "signup"
                };
            }
            else if(action === 'signup'){ //현재 state가 signup이면 login으로 변경시킨다.
                return{
                    action: "login"
                };
            }
        });
    };
}

export default Container;