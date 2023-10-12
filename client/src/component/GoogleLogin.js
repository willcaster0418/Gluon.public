import "./Login.css"
import React from "react";
import { useGoogleLogin } from '@react-oauth/google';

function GoogleLogin(props) {
    //get values by name
    const login = useGoogleLogin({
        onSuccess: (codeResponse) => {
            props.setToken(codeResponse.access_token);
            props.setUid(codeResponse.googleId);
            props.setStatus(true);
        },
        onError: (error) => console.log('Login Failed:', error),
        scope : 'https://www.googleapis.com/auth/drive.readonly',
    });

    return (
        <div className="center-element">
            <button className="login-button" 
                    onClick={() => login()}>
                        Sign in with Google 🚀 
            </button>
        </div>
	);
}

export default GoogleLogin;