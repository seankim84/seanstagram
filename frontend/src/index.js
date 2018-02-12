import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { ConnectedRouter } from 'react-router-redux';
import store, { history } from './redux/configureStore'; //default로 store도 받지만, history도 받고자 한다.
import App from './components/App';
import I18n from"redux-i18n";
import { translations } from 'translations';

ReactDOM.render( //Router의 history object가 나의 middleware history object와 같아야 한다.
    <Provider store={store}>
     <I18n translations={translations} initialLang="en" fallbackLang="en">
        <ConnectedRouter history = {history}>
        <App />
        </ConnectedRouter>
     </I18n>
    </Provider>,
    document.getElementById("root") //i18n을 component에 연결(14,16)
    //fallbackLang= 만약 한글을 요청했는데 못찾는다면 default로 된 en을 준다.
);