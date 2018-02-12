//imports
import {actionCreators as userActions} from 'redux/modules/user';

//actions
const SET_FEED = "SET_FEED";

//action creators
function setFeed(feed){
    return {
        type: SET_FEED,
        feed
    }
}

//API Actions
function getFeed(){
    return (dispatch, getState) => { //thunk 덕택에 새로운 function 이름은 getState가 있다.(말그대로 현재 state를 가져온다.)
//이 경우 state에 토큰을 저장해서, API request를 만들때마다 state를 다시 가져오는것. 그래서 getState를 사용한다.
        const {user: {token} } = getState();
        fetch("images/", {
            headers:{
                Authorization: `JWT ${token}`
            }
        })
        .then(response => {
            if (response.status ===401 ){
                dispatch(userActions.logout());
            } //status가 401이면 logout function실행
            return response.json(); //아니라면, response.json() 해서 작업을 계속함
        })
        .then(json => dispatch(setFeed(json)));
    };
};


//initial state
const initialState = {
    
};


//reducer

function reducer(state = initialState, action){
    switch (action.type) {
        case SET_FEED:
        return applySetFeed(state, action);
        default : 
        return state;
    }
}

//reducer function
function applySetFeed(state, action){
    const { feed } = action;
    return {
        ...state,
        feed
    }
}


//exports

const actionCreators = {
    getFeed
};

export {actionCreators};

//default reducer export

export default reducer;