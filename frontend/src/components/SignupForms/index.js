import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as userActions } from "redux/modules/user";

const mapDispatchToProps = (dispatch, ownProps) => { // action을 reducer에게 dispatch하는 방법
    return {//위 함수를 불렀을때, userActions facebookLogin을  dispatch한다.(userActions=actionCreators)
            //actionCreators는 facebookLogin이라는 argument 하나만 있다.(user.js참조)
        facebookLogin: (access_token) => { //이 함수는 access token이 필요하다.
            dispatch(userActions.facebookLogin(access_token)); //access_token을 전달한다.
        },
        createAccount: (username, password, email, name) => {
            dispatch(userActions.createAccount(username, password, email, name));
        }
    };
};

export default connect(null, mapDispatchToProps)(Container); // 첫번째 argument는 mapStateToProps인데, 이경우는 없기 때문에, null로 한다.