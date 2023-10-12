import LocalAuth from "./LocalAuth";
import React, { useEffect } from "react";

const LocalRegisterSSO = (props) => {
    
    useEffect(() => {
        async function register_sso(name, scope){
            // API 호출
            const resp_sso = await fetch(`${props.url}/auth/register_sso`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `name=${name}&scope=${scope}`,
            })

            if(resp_sso.status !== 200){
                alert("토큰발급요청을 실패하였습니다.");
                return;
            }
            const json_sso = await resp_sso.json();

            if(json_sso.status !== true){
                alert("토큰발급요청을 실패하였습니다.");
                return;
            }
            //props.setToken();
            props.setStatus(LocalAuth.STATUS_SIGNIN);
            return json_sso;
        }    

        const name = props.title;
        const scope = "user";
        register_sso(name, scope).then((data) => {
            console.log(`json_register_sso: ${JSON.stringify(data)}`);
        });
    }, [props]);

    return (
        <div className="center-element"></div>
    );
};

export default LocalRegisterSSO;