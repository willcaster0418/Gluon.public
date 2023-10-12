import logging, datetime
import threading
import time, json
import sysv_ipc, struct, sys, os
from pkg.dbwrapper.mariadb import MariaDBWrapper

nstr = datetime.datetime.now().strftime("%Y%m%d")
try:
    logging.basicConfig(
        filename = f"/gluon/log/{nstr}.fake.log",
        format ='%(asctime)s:%(levelname)s:%(message)s',
        datefmt ='%m/%d/%Y %I:%M:%S %p',
        level = logging.INFO
    )
except Exception as e:
    logging.info(f"Error(fake.py >> initialize) : {str(e)}")

db = MariaDBWrapper("localhost", "oms" , None, "OMS")
items = db.select("select * from ITEM")

item_dict = {}
for item in items:
    item_dict[item['name']] = item['seq']

MEMORY_UNIT = 64 * (20 + 3)
if "MEMORY_UNIT" in os.environ:
    MEMORY_UNIT = int(os.environ["MEMORY_UNIT"])

memory = sysv_ipc.SharedMemory(1, flags=sysv_ipc.IPC_CREAT) 
def _scan(id, data_type ='d', loc = 0):
    global memory, item_dict, MEMORY_UNIT
    i = item_dict[id]
    v = memory.read(byte_count = 8, offset = MEMORY_UNIT * i + loc*64)
    v = struct.unpack(data_type, v)
    return v

monitoring_dict = {}

def thread_loop():
    global monitoring_dict
    while True:
        for que_name in monitoring_dict.keys():
            data = {}
            for i in range(0, len(monitoring_dict[que_name])):
                try:
                    result = {"timestamp" : _scan(monitoring_dict[que_name][i], loc = 0, data_type='d'), 
                              "price"     : _scan(monitoring_dict[que_name][i], loc = 1, data_type='d'),
                              "amount"    : _scan(monitoring_dict[que_name][i], loc = 2, data_type='d')}
                    data.update(result)
                    fpath = f"/dev/shm/{que_name}.que"
                    if os.path.isfile(fpath):
                        mmap = MMAP(fpath, 128*4096, 128)
                        mmap.writep(json.dumps(data).encode("utf-8"))
                        mmap.close()
                except Exception as e:
                    pass
        time.sleep(1)

t = threading.Thread(target=thread_loop)
t.start()

from gandan import MMAP
m_in = MMAP(f"/dev/shm/ORDER_FAKE.que", 128*4096, 128)
while True:
    try:
        datas = m_in.readp()
        for data in datas:
            logging.info(f"Data : {str(data, 'utf-8')}")
            data = json.loads(str(data, "utf-8"))
            if 'que_name' in data.keys() and 'item_name' in data.keys():
                if 'command' in data.keys() and data['command'] == 'stop':
                    monitoring_dict[data['que_name']] = []
                    pass
                if not data['que_name'] in monitoring_dict.keys():
                    monitoring_dict[data['que_name']] = []
                if not data['item_name'] in monitoring_dict[data['que_name']]:
                    monitoring_dict[data['que_name']].append(data['item_name'])
    except Exception as e:
        logging.info(f"Error(fake.py >> handler) : {str(e)}")
        time.sleep(1)