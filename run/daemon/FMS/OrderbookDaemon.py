# -*- coding: utf-8 -*
from pkg.query import Query

import flask
from flask import request, jsonify
import sysv_ipc, struct, sys, os
from pkg.dbwrapper.mariadb import MariaDBWrapper

import logging
import datetime
from flask_cors import CORS

MEMORY_UNIT = 64 * (20 + 3)
if "MEMORY_UNIT" in os.environ:
    MEMORY_UNIT = int(os.environ["MEMORY_UNIT"])

orderbook, item_dict, memory = None, {}, None
def _scan(id, data_type ='d', loc = 0):
    global memory, item_dict, MEMORY_UNIT
    i = item_dict[id]
    v = memory.read(byte_count = 8, offset = MEMORY_UNIT * i + loc*64)
    v = struct.unpack(data_type, v)
    return v

def initialize():
    global orderbook, item_dict, memory
    nstr = datetime.datetime.now().strftime("%Y%m%d")
    try:
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.OrderbookDaemon.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(OrderbookDaemon.py >> initialize) : {str(e)}")
        
    try:
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != "CoinTrader"]
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)
            # log logger name
            logging.info(f"Logger {logger.name} set to CRITICAL")
    except Exception as e:
        logging.info(f"Error(OrderbookDaemon.py >> initialize) : {str(e)}")


    logging.info("---*--- Orderbook Daemon ---*---")
    db = MariaDBWrapper("localhost", "oms" , None, "OMS")
    items = db.select("select * from ITEM")

    for item in items:
        item_dict[item['id']] = item['seq']

    memory = sysv_ipc.SharedMemory(1, flags=sysv_ipc.IPC_CREAT) 
    orderbook = flask.Flask(__name__)
    return orderbook

def item():
    # get parameters from request
    # get item from db
    # return item
    name = request.args.get('name', default=None, type=str)
    logging.info(f"OrderbookDaemon.py >> item >> name : {name}")
    try:
        result = {"timestamp" : _scan(name, loc=0, data_type='d'), 
                  "price"  : _scan(name, loc = 1, data_type='d'),
                  "amount" : _scan(name, loc = 2, data_type='d'),
                  "status" : True}
    except Exception as e:
        result = {"status" : False}
    return jsonify(result)

initialize()
orderbook.add_url_rule('/orderbook/item', 'item', item, methods = ['GET'])