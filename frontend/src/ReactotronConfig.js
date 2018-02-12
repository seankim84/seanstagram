import Reactotron from 'reactotron-react-js';
import {reactotronRedux} from 'reactotron-redux'; 

Reactotron.configure({ name: "Sean" }) //reactotron을 plugin 
.use(reactotronRedux())
.connect();

export default Reactotron;