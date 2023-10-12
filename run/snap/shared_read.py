import sysv_ipc, struct, sys, os
from pkg.dbwrapper.mariadb import MariaDBWrapper

db = MariaDBWrapper("localhost", "oms" , None, "OMS")
items = db.select("select * from ITEM")

item_dict = {}
for item in items:
    item_dict[item['name']] = item['seq']

memory = sysv_ipc.SharedMemory(1, flags=sysv_ipc.IPC_CREAT) 

MEMORY_UNIT = 64 * (20 + 3)
if "MEMORY_UNIT" in os.environ:
    MEMORY_UNIT = int(os.environ["MEMORY_UNIT"])

def _scan(id):
    global memory, item_dict, MEMORY_UNIT
    i = item_dict[id]
    result = []
    for i in range(0, 3):
        v = memory.read(byte_count = 8, offset = MEMORY_UNIT * i)
        v = struct.unpack('d', v)
        result.append(v)
    return result

print(_scan(sys.argv[1]))