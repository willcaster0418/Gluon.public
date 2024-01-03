import asyncio
import websockets
import logging, datetime, json, os
from flask import session
from flask import Flask
import requests

from gandan import MMAP
from gandan.GandanSub import *
market_req = MMAP(f"/dev/shm/MARKET_REQ.que", 128*4096, 128)

# create handler for each connection
app = Flask(__name__)
async def handler(websocket, path):
    global app, market_req
    token = None
    while token is None:
        try:
            async with asyncio.timeout(1):
                data = await websocket.recv()
                token = data
        except Exception as e:
            logging.info(f"token loop : {str(e)}")
            pass

    logging.info(f"token recieved as:  {token}")
    # request to auth server
    try:
        r = requests.post("https://127.0.0.1:80/auth/validate_token"
                                , headers = {"Authorization" : f"Bearer {token}"}
                                , verify = False)
        logging.info(f"request to auth server as:  {str(r.text)}!")
        if r.status_code == 200:
            logging.info(f"token validated as:  {token}!")
        else:
            logging.info(f"token validation failed as:  {token}!")
            await websocket.send("failed")
            return
    except Exception as e:
        logging.info(f"token validation failed as:  {token} with {str(e)}")
        return
    
    market_rep = MMAP(f"/dev/shm/{token}.que", 128*4096, 128)
    try:
        market_req.writep(json.dumps({"token" : token}).encode("utf-8"))
    except Exception as e:
        return

    def sub_callback(_h):
        return str(_h.dat_)
    subscription_dict = {}
    t = []
    while True:
        try:
            for key in t:
                subscription_dict[rquery['keyword']] = GandanSub(os.environ["MW_URL"]
                                                   , int(os.environ["MW_PORT"])
                                                   , f"SUB_MKT{key}", 0.01)
            t = []
            for key in subscription_dict.keys():
                result = subscription_dict[key].sub(sub_callback)
                if type(result) == str:
                    logging.info(f"sub_callback : {result}")
                    await websocket.send(result)
            async with asyncio.timeout(1):
                # websocket non-blocking recv
                data = await websocket.recv()
                try:
                    rquery = json.loads(data)
                    if rquery['key'] == "add":
                        t.append(rquery['keyword'])
                        await websocket.send(json.dumps(rquery))
                    if rquery['key'] == "del":
                        logging.info(f"rquery delete : ${data}")
                        del t[rquery['keyword']]
                except Exception as e1:
                    logging.info(str(e1))
                    pass
            datas = market_rep.readp()
            for data in datas:
                logging.info(f"Data : {str(data, 'utf-8')}")
        except asyncio.TimeoutError:
            reply = json.dumps({"status": True, "key" : "time"
                                , "value" : datetime.datetime.now().strftime("%Y%m%d%H%M%S")})
            await websocket.send(reply)
            pass
        except Exception as e:
            logging.info(f"Error(RealTimeDaemon.py >> handler) : {str(e)}")
            break
        finally:
            await asyncio.sleep(0.1)
 

if __name__ == "__main__":
    try:
        nstr = datetime.datetime.now().strftime("%Y%m%d")
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.RealTimeDaemon.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(QueryDaemon.py >> initialize) : {str(e)}")

    que_management = {}
    start_server = websockets.serve(handler, "0.0.0.0", 81)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()