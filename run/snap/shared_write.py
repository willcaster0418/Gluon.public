import sysv_ipc, struct, os
from pkg.dbwrapper.mariadb import MariaDBWrapper

db = MariaDBWrapper("localhost", "oms" , None, "OMS")
items = db.select("select * from ITEM")

MEMORY_UNIT = 64 * (20 + 3)
if "MEMORY_UNIT" in os.environ:
    MEMORY_UNIT = int(os.environ["MEMORY_UNIT"])

memory = sysv_ipc.SharedMemory(1, flags=sysv_ipc.IPC_CREAT, size=len(items) * MEMORY_UNIT) 

#쓰기
for item in items:
    data = struct.pack('d', item['price'])
    memory.write(data, offset = (item['seq']) * MEMORY_UNIT + 64 * 1)