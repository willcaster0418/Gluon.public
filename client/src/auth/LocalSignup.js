import "./Login.css"
import React from "react";
import { useState } from "react";
import {sha256} from 'js-sha256'

function LocalSignup(props) {
    const [uid, setID] = useState(undefined);
    const [name, setName] = useState(undefined);
    const [password1, setPassword1] = useState(undefined);
    const [password2, setPassword2] = useState(undefined);
    const [role, setRole] = useState("user");

    async function signup () {
        if(uid === undefined || password1 === undefined){
            return
        }
        if(password1 !== password2){
            alert("password not match");
            return;
        }
        //await fetch
        const resp_signup = await fetch(props.url + "/auth/signup", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `uid=${uid}&password=${sha256(password1)}&name=${name}`
        })

        const json_signup = await resp_signup.json();
        console.log(`json_signup: ${JSON.stringify(json_signup)}`)

        // wait for session then do register_sso with it
        //console.log(sessionStorage.stringify());
        if(resp_signup.status !== 200
            || json_signup.status !== true){
            return;
        }

        const resp_sso = await fetch(props.url + "/auth/register_sso", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `uid=${uid}&name=${props.title}&scope=${role}`
        })

        if(resp_sso.status === 200){
            resp_sso.json().then((data) => {
                console.log(`json_register_sso: ${JSON.stringify(data)}`);
                props.setStatus(0);
            });
        }
    }

    return (
        <div className="center-element">
            <div className="login-form">
            <p>{props.title}</p>
            <input
                className="login-form"
                type="text"
                placeholder="user name"
                onChange={(event) => setName(event.target.value)}
            />
            <input
                className="login-form"
                type="text"
                placeholder="user id"
                onChange={(event) => setID(event.target.value)}
            />
            <input
                className="login-form"
                type="password"
                placeholder="password enter"
                onChange={(event) => {setPassword1(event.target.value)}}
            />
            <input
                className="login-form"
                type="password"
                placeholder="password re-enter"
                onChange={(event) => {setPassword2(event.target.value)}}
            />
            <select
                className="login-form"
                onChange={(event) => {setRole(event.target.value)}}
            >
                <option value="user">일반 사용자</option>
                <option value="admin">관리자</option>
            </select>
            <button className="login-button"
                onClick={() => {signup()}}>
                Sign-Up User 🚀
            </button>
            </div> 
        </div>
	);
}
export default LocalSignup;