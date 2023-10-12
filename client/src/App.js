import './App.css'
import LocalRegisterSSO from './auth/LocalReigsterSSO';
import LocalAuth from './auth/LocalAuth';
//import GoogleLogin from './login/GoogleLogin';
import LocalSignin from './auth/LocalSignin';
import LocalSignup from './auth/LocalSignup';
import {useState, useEffect} from 'react';
import Home from './page/Home';

const App = () => {
    /*
        sign-in : 0
        sign-up : 1
        sign-in with SSO : 2
        use application with token : 3
    */
    const [status, setStatus] = useState(LocalAuth.STATUS_SIGNIN);
    const [uid, setUid] = useState(undefined);
    const [uname, setUname] = useState(undefined);
    const [token, setToken] = useState(undefined);
    const [clientID, setClientID] = useState(undefined);
    const [clientSecret, setClientSecret] = useState(undefined);

    const url = "";
    const appName = "Order Management System";

    if(token === undefined){
        if(status === LocalAuth.STATUS_SIGNIN){
            return <LocalSignin title={appName}
                                setStatus={setStatus}
                                url={url}
                                setUid={setUid}
                                setUname={setUname}
                                setClientID={setClientID}
                                setClientSecret={setClientSecret}
                                setToken={setToken}
                    />;
        }
        else if(status === LocalAuth.STATUS_SIGNUP){
            return <LocalSignup title={appName}
                                setStatus={setStatus}
                                url={url}
                    />;
        }
        else if(status === LocalAuth.STATUS_SSO){
            return <LocalRegisterSSO title={appName}
                                     setStatus={setStatus}
                                     setToken={setToken}
                                     url={url}
                    />;
        }
    }
    else{
        return <Home title={appName}
                     setStatus={setStatus}
                     clientID={clientID}
                     clientSecret={clientSecret}
                     setToken={setToken}
                     token={token}
                     url={url}
                     uid={uid}
                     uname={uname}
                />;
    }
}
export default App;