from pkg.crawl.crawl_naver import CrawlNaver
from pkg.dbwrapper.mariadb import MariaDBWrapper
import time, sysv_ipc, struct, datetime, logging, os, json
from gandan.GandanPub import *
import socket

MEMORY_UNIT = 64 * (20 + 3)
if "MEMORY_UNIT" in os.environ:
    MEMORY_UNIT = int(os.environ["MEMORY_UNIT"])

if __name__ == "__main__":
    nstr = datetime.datetime.now().strftime("%Y%m%d")
    try:
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.crawl_naver.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(crawl_naver.py >> initialize) : {str(e)}")
 
    db = MariaDBWrapper("localhost", "oms" , None, "OMS")
    max_seq = db.select("select max(seq) as max_seq from ITEM")[0]['max_seq']
    items = db.select("select * from ITEM")
    memory = sysv_ipc.SharedMemory(1, flags=sysv_ipc.IPC_CREAT, size=max_seq * MEMORY_UNIT) 
    memory_dict = {item['id'] : item['seq'] for item in items}   

    c = CrawlNaver()
    p = GandanPub(os.environ.get('MW_URL'), int(os.environ.get('MW_PORT')))

    multicast_group = '224.1.1.1'
    port = 7000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(('multicast_group', port))

    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        #receive market data from server.py instead of crawl_naver.py
        data_recv, _addr = sock.recvfrom(16384)
        if len(data_recv) > 16384: #check extra large data
            print(len(data_recv)) 
        data_recv = data_recv.split(b'\n')
        for data_ in data_recv:
            time_len, tr_len=9, 5 #timestamp len : 9, tr len : 5 (of MKT_DATA)
            if len(data_) >= time_len+tr_len:
                tr = data_[time_len : time_len+2]
                if tr.decode() == "A3": #defined only when tr starts with A3
                    dict_={}
                    ticker = data_[time_len+8 : time_len+14].decode()
                    if ticker in memory_dict.keys():
                        try:
                            seq = memory_dict[ticker]
                            dict_['key'] = "item"
                            dict_['code'] = ticker

                            #used timestamp of MKT_DATA
                            data = struct.pack('d', float(data_[:time_len].decode())) 
                            memory.write(data, offset = seq * MEMORY_UNIT + 64 * 0) 

                            dict_['price'] =float(data_[time_len+34:time_len+43].decode())
                            data = struct.pack('d', dict_['price'])
                            memory.write(data, offset = seq * MEMORY_UNIT + 64 * 1)

                            dict_['volume']=float(data_[time_len+43:time_len+53].decode())
                            data = struct.pack('d', dict_['volume'])
                            memory.write(data, offset = seq * MEMORY_UNIT + 64 * 2)

                            p.pub("PUB_MKT"+ticker, json.dumps(dict_))
                        except:
                            #print("parse error", ticker)
                            continue

    time.sleep(5)
    sock.close()