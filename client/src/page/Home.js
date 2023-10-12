import "./Home.css"
import React from "react";
import {useEffect} from "react";
import WebSocketProc from "../component/WebSocketProc";

function Home(props) {
    const search = (e) => {
        e.preventDefault();
        let input = document.getElementById("input").value;
        let url = `${props.url}/orderbook/item?name=` + input;
        fetch(url)
        .then(res => res.json())
        .then(res => {
            let result = `${input} price : ${res.price}`;
            result += `\n${input} amount : ${res.amount}`;
            result += `\n${input} timestamp : ${res.timestamp}`;

            document.getElementById("output").value = result;
        })
        .catch(err => console.log(err));

        url = `${props.url}/query/order?que_name=${props.uid}&item_name=${input}`;
        fetch(url)
        .then(res => res.json())
        .then(res => {
            console.log(res);
        })
    }

    return (
        <div className="container">
            <div className="top">
                <div style={{"textAlign" : "center"}}>
                    <h3> This is Top : {props.uname} </h3>
                    <button id="logout" 
                            type="button" 
                            onClick={() => {
                                        props.setStatus(0); 
                                        props.setToken(undefined);
                                    }}>Logout</button>
                </div>
            </div>

            <div className="mid">
                <div style={{"textAlign" : "center"}}>
                    <WebSocketProc 
                        url="wss://localhost:3000/socket.io"
                        uid={props.uid}
                        token={props.token}
                    />
                </div>
            </div>

            <div className="bottom">
                <div style={{"textAlign" : "center"}}>
                    <h3> This is Bottom </h3>
                </div>
            </div>
        </div>
    );
}

export default Home;