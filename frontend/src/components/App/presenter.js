import React from "react";
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import "./styles.scss";
import Auth from "components/Auth";
import Footer from "components/Footer";
import Navigation from "components/Navigation";
import Feed from 'components/Feed';
/*
class App extends Component {
  render() { // "/"겹치기 때문에 /login에서도 'hello'를 보여준다. 그래서 Switch로 둘중 하나를 정확히 보여주도록 한다. 
    return ( //Switch가 없으면, 두 문이 겹친다.
    <div className={styles.App}>
    <Switch>
        <Route path="/" render={() => "hello!"} />
        <Route path="/login" render={() => "login !"} />
    </Switch>
        <Footer />
      </div>
    );
  }
}
*/

const App = props => [
  //Nav
  props.isLoggedIn ? <Navigation key={1} />: null, 

  //Route,
  props.isLoggedIn ? <PrivateRoutes key={2}/> : <PublicRoutes key={2} />, //Priv : // Public(isLoggedIn이 참이면 PrivateRoute 출력, false면 PublicRoute출력)
  <Footer key={3} />
  //react는 array를 리턴할 때마다 키의 숫자가 필요하다.
];

App.PropTypes = { //property와 import 하는 대소문자 구분 중요!!
  isLoggedIn: PropTypes.bool.isRequired // 참,거짓이 isRequired 되어야 한다.
}; //(true or false가 반드시 되야한다. redux/user/initial state에서 값을 받는다.)

const PrivateRoutes = props => (
  <Switch>
    <Route exact path = "/" component={Feed} />
    <Route exact path = "/explore" render={() => "explore"} />
  </Switch>
);

const PublicRoutes = props =>(
  <Switch>
    <Route exact path = "/" component={Auth} />
    <Route exact path = "/recover" render={() => "recover password"} />
  </Switch>
);

export default App;
