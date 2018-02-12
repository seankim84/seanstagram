//configureStore는 나의 Store를 설정/구성한다.

import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { routerReducer, routerMiddleware } from 'react-router-redux';
import createHistory from 'history/createBrowserHistory'; //여러 history 종류가 있다.  hashHistory 등등.
import { composeWithDevTools } from 'redux-devtools-extension';
import user from 'redux/modules/user';
import photos from 'redux/modules/photos'
import { i18nState } from 'redux-i18n';
import Reactotron from 'ReactotronConfig'; //NODE_PATH 덕분에 src에서 PATH를 받음

const env = process.env.NODE_ENV;

const history = createHistory() //history는 middleware, router 와  연결한다.

const middlewares = [thunk, routerMiddleware(history)]; // []이 뜻은 전체 적용(development, production 둘다), 미들웨어 array. local과 prod를 구분하기 위해. 여기서 middleware를 불러온다.
//router middleware는 리액트 router redux인데 history와 싱크되어야 한다.
if(env === "development"){
    const { logger } = require("redux-logger"); //package.json에 dev로 있기때문에 import를 할 필요 없다.
    middlewares.push(logger); //middlewares가 array이기 때문에 logger 추가 가능, dev가 아닐 경우, 그냥 [thunk] array이다.
    //logger = 우리가 리덕스를 위해 한 작업을 log한다.
}

const reducer = combineReducers({ //여기서 리듀서를 합친다.(라우팅, 미들웨어 등도 여기에 입력)
    user,
    photos,
    routing : routerReducer, // reducer에 routerReducer 추가
    i18nState //reducer에 i18nState 추가. 실제 생성하진 않았지만 combineReducers에 assign 함으로써 사용하고 있다.
});

let store;

if(env === "development"){
    store = initialState => 
    Reactotron.createStore(
        reducer, 
        composeWithDevTools(applyMiddleware(...middlewares))
     );
     //dev환경이라면, Reactotron과 store를 생성하고 else는 prd환경이므로 store를 normal redux와 생성한다.
}
else {
    store = initialState =>
    createStore(reducer, applyMiddleware(...middlewares));//기본적으로 array로 작성해야 하나, array(middleware)를 unpack하기 위해서 ...사용
}

export {history}; //라우터를 생성할건데, 라우터는 history object가 필요하기 때문에 export한다.
export default store();