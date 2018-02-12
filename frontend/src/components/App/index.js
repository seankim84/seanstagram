import { connect } from 'react-redux';
import Container from './container';

const mapStateToProps = (state, ownProps) => { //state를 통해, logged in prop을 container component로 보낸다.(mapStateToProps 덕분)
  const { user, routing : {location} } = state;
  return { isLoggedIn: user.isLoggedIn,
           pathname: location.pathname // 이렇게 작업을 하면, 나의 app component는 new prop의 존재를 알게된다.그리고 해당 prop이 바뀌면 앱컴포넌트는 렌더를 다시 하게 된다.       
  }; //user.js에 store 안에 있는 variable을 얻고자 한다.
};

export default connect(mapStateToProps)(Container); //container.js와 연결