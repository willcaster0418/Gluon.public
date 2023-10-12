from pkg.crawl.crawl_naver import CrawlNaver
from pkg.dbwrapper.mariadb import MariaDBWrapper
import time, sysv_ipc, struct, datetime, logging, os, json
from gandan.GandanPub import *

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

    while True:
        _dict = c.snap_krx(page=1, filter={"현재가": "price", "거래량": "volume"})
        for ticker in _dict.keys():
            if ticker in memory_dict.keys():
                seq = memory_dict[ticker]
                data = struct.pack('d', datetime.datetime.now().timestamp())
                memory.write(data, offset = seq * MEMORY_UNIT + 64 * 0)
                data = struct.pack('d', _dict[ticker]['price'])
                memory.write(data, offset = seq * MEMORY_UNIT + 64 * 1)
                data = struct.pack('d', _dict[ticker]['volume'])
                memory.write(data, offset = seq * MEMORY_UNIT + 64 * 2)

                _dict[ticker]['key'] = "item"
                _dict[ticker]['code'] = ticker
                p.pub("PUB_MKT"+ticker, json.dumps(_dict[ticker]))

        logging.info(f"crawl_naver.py >> {datetime.datetime.now()} >> {len(_dict)}")
        time.sleep(10)