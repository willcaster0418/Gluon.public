import React, { useEffect, useRef, useState } from "react";

const WebSocketProc = (props) => {
    const url = `${props.url}`;
    const ws = useRef(undefined);
    const [item, setItem] = useState({});
    const [time, setTime] = useState(0);

    async function AddItem(){
        const keyword = document.querySelector("#add-item").value;
        const key = "add";
        setItem(item => ({...item, [keyword]: undefined}))
        ws.current.send(JSON.stringify({key, keyword}))
    }
    useEffect(() => {
        if(props.token === undefined 
            && ws.current !== undefined
            && ws.current.readyState !== WebSocket.CLOSED){
            console.log("close websocket");
            ws.current.close();
        }
    }, [props.token]);

    useEffect(() => {
        if(ws.current === undefined || ws.current.readyState === WebSocket.CLOSED){
            ws.current = new WebSocket(url);
            ws.current.onopen = () => {
                ws.current.send(props.token);
            };

            ws.current.onmessage = (event) => {
                let data = JSON.parse(event.data);
                console.log(data);
                if(data.key === "time"){
                    setTime(data.value);
                }
                if(data.key === "item"){
                    setItem(item => ({...item, [data.code]: JSON.stringify(data)}))
                }
            };

            ws.current.onclose = () => {
            };
        }
        return () => {
        }
    });

    return (
        <div>
            <div>time : {time}</div>
            <input id="add-item"
                type="text"
                placeholder="keyword"></input>
            <button onClick={()=>{AddItem()}}>ADD</button>
            <ul>
                {Object.keys(item).map((key) => {
                    return <li key={key}>{key} : {item[key]}
                            <button onClick={()=>{
                                const key = "del";
                                ws.current.send(JSON.stringify({key, keyword:key}))
                                alert("del");
                            }}>DEL</button></li>
                })}
            </ul>
        </div>
    );
};

export default WebSocketProc;