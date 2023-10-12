# -*- coding: utf-8 -*
from pkg.query import Query

import flask
from flask import request, jsonify

import logging
import datetime
from flask_cors import CORS

query = None
def initialize():
    global query
    nstr = datetime.datetime.now().strftime("%Y%m%d")
    try:
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.QueryDaemon.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(QueryDaemon.py >> initialize) : {str(e)}")
        
    try:
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != "CoinTrader"]
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)
            # log logger name
            logging.info(f"Logger {logger.name} set to CRITICAL")
    except Exception as e:
        logging.info(f"Error(QueryDaemon.py >> initialize) : {str(e)}")


    logging.info("---*--- Query Daemon ---*---")
    query = flask.Flask(__name__)

import json
def item():
    param = request.get_json()
    logging.info(json.dumps(param))
    param['price'] = 0
    return jsonify(param)

initialize()
query.add_url_rule('/query/item'  , 'item'  , item, methods = ['GET'])