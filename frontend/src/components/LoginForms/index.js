import { connect } from 'react-redux';
import Container from './container';
import { actionCreators as userActions } from "redux/modules/user";

//Action을 Reducer에게 Dispatch하는 방법(redux state를 변경하는 방법은 reducer에게 액션을 dispatch한다.)

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        facebookLogin: (access_token) => {
            dispatch(userActions.facebookLogin(access_token));
        },
        usernameLogin:(email, password) => {
            dispatch(userActions.usernameLogin(email, password));
        }
    };
};

export default connect(null, mapDispatchToProps)(Container);