//import

//actions
const SAVE_TOKEN =  "SAVE_TOKEN";
const LOGOUT = "LOGOUT";

//action creators(redux state 바꿀 때 사용)
function saveToken(token){ //토큰을 받을 때마다, saveToken이라는 액션을 dispatch한다.(지금 받은 token과 함께)
    return {
        type : SAVE_TOKEN,//그리고 해당 action을 reducer에서 실행
        token
    }
};

function logout(){
    return {
        type: LOGOUT
    };
}


//API actions(API를 부를때 사용)
function facebookLogin(access_token){
    return function(dispatch) {
        fetch("/users/login/facebook/", { //user/url에서 가져온다.(config/urls에 이렇게 설정되어있다.)
            method: "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                access_token
            }) //body에선 json을 string으로 변환 그리고 JSON은 access_token이다.
        })
            .then(response => response.json())
            .then(json => {
                if (json.token) { //만약 json이 token이 있다면, saveToken을 dispatch 한다.(json.token 키와 함께)
                    dispatch(saveToken(json.token));
                }
            }) //.then문은 작업이 완료된 후 실행
            .catch(err => console.log(err))  // 에러발생시 실행
    };
}

function usernameLogin(username, password){ //username,password는 container에서 미리 만들어 놓은것
    return function(dispatch){
        fetch("/rest-auth/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({
                username,
                password
            })
        })
        .then(response => response.json())
        .then(json =>{
            if(json.token){
                dispatch(saveToken(json.token))
            }
        })
        .catch(err => console.log(err))
    }
}

function createAccount(username, password, email, name){
    return function(dispatch){
        fetch("/rest-auth/registration/", {
            method:"POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                username,
                password1: password,
                password2: password,
                email,
                name
            })
        })
        .then(response => response.json())
        .then(json => {
            if(json.token){
                dispatch(saveToken(json.token))
            }
        })
        .catch(err => console.log(err));
    }
}

//initial state
const initialState = {
    isLoggedIn: localStorage.getItem("jwt") ? true : false,//브라우저에 저장하는 쿠키 같은것 but 쿠키와는 다른점이 내 웹에서만 가능하다.
    //로컬스토리지 안에 jwt(token)를 찾는다,true or false로 응답. 없으면 false, 있다면 isLoggedin = true 상태가 된다. App/presenter에서 bool로 isRequired되어있기 때문에 true or false만 가능!
    token: localStorage.getItem('jwt') //App실행시, localStorage에 있는 jwt를 가져오고, 없다면 null로 결정(null=false)
};

// reducer

function reducer(state=initialState,action){ 
    switch(action.type){
        case SAVE_TOKEN: //위에서 받아온 token을 리듀서에서 실행
            return applySetToken(state, action); //applySetToken 함수 실행
        case LOGOUT:
            return applyLogout(state, action); 
        default:
            return state;
    }
}


// reducer functions

function applySetToken(state, action){
    const { token } = action;
    localStorage.setItem("jwt", token); //action에서 온 token
    return {
        ...state,
        isLoggedin:true, //리듀서가 isLoggedin은 참이라하고, token을 state에 저장한다.
        token : token
    }
}

function applyLogout(state, action){ //작동하지 않는 토큰 삭제
    localStorage.removeItem("jwt");
    return{
        isLoggedin:false
    };
}

//exports

const actionCreators = {
    facebookLogin,
    usernameLogin,
    createAccount,
    logout
    
};

export { actionCreators };

//reducer exports
export default reducer;