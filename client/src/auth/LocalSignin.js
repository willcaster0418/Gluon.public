import LocalAuth from "./LocalAuth";
import "./Login.css"
import React from "react";
import { useState } from "react";
import { sha256 } from "js-sha256";

function LocalSignin(props) {
    const [uid, setID] = useState(undefined);
    const [password, setPassword] = useState(undefined);

    const signup = () => {
        props.setStatus(LocalAuth.STATUS_SIGNUP);
    }

    async function signin() {
        if(uid === undefined || password === undefined){
            return
        }
        const resp_signin = await fetch(props.url + "/auth/signin", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `uid=${uid}&password=${sha256(password)}`
        })
        const json_signin = await resp_signin.json();
        console.log(JSON.stringify(json_signin))

        if(resp_signin.status !== 200
            || json_signin.status !== true){
            alert("로그인에 실패하였습니다.");
            return {status: false}
        }
        return json_signin;
    }

    async function listsso(){
        const resp_listsso = await fetch(props.url + "/auth/list_sso", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `name=${props.title}`
        })
        console.log(resp_listsso);
        const json_listsso = await resp_listsso.json();
        console.log(json_listsso);

        if(resp_listsso.status !== 200
            || json_listsso.status !== true
            || json_listsso.client.length === 0){
            alert("SSO 목록을 불러오는데 실패하였습니다.");
            return {status: false}
        }
        const client_id = json_listsso.client[0].client_id;
        const client_secret = json_listsso.client[0].client_secret;

        return {client_id: client_id, client_secret: client_secret, status: true};
    }

    async function token(client_id, client_secret){
        // curl -u <client_id>:<client_secret> -d grant_type=client_credentials http://localhost:3001/auth/token
        console.log({client_id, client_secret, password, uid})
        const resp_token = await fetch(props.url + "/auth/token", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization" : `Basic ${btoa(`${client_id}:${client_secret}`)}`,
            },
            body: `username=${uid}&password=${sha256(password)}&scope=${"user"}&grant_type=${"password"}`
        })

        const json_token = await resp_token.json();
        console.log(json_token);

        if(resp_token.status !== 200
            || json_token.access_token === undefined){
            alert("토큰을 발급받는데 실패하였습니다.");
            return {status: false}
        }
        return json_token;
    }

    return (
        <div className="center-element">
            <div className="login-form">
            <p>{props.title}</p>
            <input
                className="login-form"
                type="text"
                placeholder="username"
                onChange={(event) => setID(event.target.value)}
            />
            <input
                className="login-form"
                type="password"
                placeholder="password"
                onChange={(event) => {setPassword(event.target.value)}}
            />
            <button className="login-button"
                onClick={() => {
                    signin().then((signin_data) => {
                        if(signin_data.status){
                            console.log(signin_data);
                            props.setUid(signin_data.uid);
                            props.setUname(signin_data.uname);
                            listsso().then((sso_data) => {
                                if(sso_data.status){
                                    console.log(sso_data);
                                    token(sso_data.client_id, sso_data.client_secret).then((token_data) => {
                                        console.log(token_data);
                                        props.setToken(token_data.access_token);
                                    });
                                }
                            })
                        }
                    });
                }}>
                Sign in 🚀
            </button>
            <button className="login-button"
                onClick={() => signup()}>
                Sign up 🚀
            </button>
            </div> 
        </div>
	);
}
export default LocalSignin;