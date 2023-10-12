import os
from gandan.Gandan import *
import datetime

if __name__ == '__main__':
    url = os.environ.get('MW_URL')
    port = int(os.environ.get('MW_PORT'))
    mw = Gandan((url, port), "/dev/shm/", 512*128, 512)
    mw.setup_log("/gluon/log/" + datetime.datetime.now().strftime('%Y%m%d') + '.mw.log')
    mw.start()
