//여기서 Authorization 리덕스 스토어에 연결

import { connect }  from 'react-redux'; // redux를 불러오는 이유는, 인덱스에서 로그인,회원가입,이메일 등의 액션을 하기 때문.
import Container from './container';

// Add all the actions for:
// Log in
// Sign Up
// Recover password
// Check Username
// Check password
// Check Email



export default connect()(Container);
