from flask import request, jsonify
import logging, json

class Query:
    marketManager = None
    connection = None
    def __init__(self):
        pass

    @staticmethod
    # @query.route('/query/hello', methods=['GET'])
    def hello():
        # get parameters
        result = {"value" : "hello world!!!!"}
        return jsonify(result)