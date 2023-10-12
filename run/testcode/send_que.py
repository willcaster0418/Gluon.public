from gandan import MMAP
import time, sys
from datetime import datetime as dt

_id = sys.argv[1]
m = MMAP(f"/dev/shm/{_id}.que", 128*4096, 128)

_latency = float(sys.argv[2])

cnt = 0
while True:
    n = dt.now().timestamp()
    m.writep(bytes(str(_id) + "|" + str(cnt)+"|"+str(n), 'ascii'))
    cnt += 1
    time.sleep(_latency)