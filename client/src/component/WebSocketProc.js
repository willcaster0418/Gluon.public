import React, { useEffect, useRef, useState } from "react";
import ItemList from "./ItemList";

const WebSocketProc = (props) => {
    const url = `${props.url}`;
    const ws = useRef(undefined);
    const [items, setItems] = useState([]);
    const [time, setTime] = useState(0);
    const [updateItem, setUpdateItem] = useState([]);

    const AddItem = () =>{
        const keyword = document.querySelector("#add-item").value;
        const key = "add";
        const new_item={"code":keyword, "price":'...', "volume":'...'};
        if(!items.some(i => i.code === keyword)){ //check if it is new item
            setItems(_ => {return [..._, new_item]});
            ws.current.send(JSON.stringify({key, keyword}));
        }
    }
    const RemoveItem = (code) => {
        const key = "del";
        setItems(items.filter(i => i.code !== code));
        ws.current.send(JSON.stringify({key, keyword:code}));
    }

    useEffect(() => {
        const updated_item=items.map(i => {
            if (i.code !== updateItem.code){
                return i;
            }else{
                return{
                    ... i,
                    price: updateItem.price,
                    volume: updateItem.volume
                };
            }
        })
        setItems(updated_item);
    }, [updateItem]);

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
                    setUpdateItem(data);
                }
            };

            ws.current.onclose = () => {
            };
        }
        return () => {
        }
    }, [ws]);

    return (
        <div>
            <div>time : {time}</div>
            <input id="add-item"
                type="text"
                placeholder="keyword"></input>
            <button onClick={()=>{AddItem()}}>ADD</button>
            <ul>
                <ItemList items={items} onRemove={RemoveItem}/>
            </ul>
        </div>
    );
};

export default WebSocketProc;