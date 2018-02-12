import React from 'react';
import App from './presenter';

const Container = props => <App {...props} />
//Container Component는  props를 받아서 presenter안에 있는 App Componet를 준다.
export default Container;