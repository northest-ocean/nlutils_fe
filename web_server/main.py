import re
import gc
import demjson
import logging
import os
import copy
from flask import Flask, request
from flask_cors import *
import json

from utils import request_args_to_folder, PWJSONParser

app = Flask(__name__)
parser = PWJSONParser()

CORS(app, supports_credentials=True)

@app.route('/params', methods=['POST'])
def test():
    gc.collect()
    if request.method == 'POST':
        data = request.get_data(as_text=False)
        print(data.decode('utf-8'))
        data_dict = json.loads(data)
        fetch_path = request_args_to_folder(data_dict)
        # print(data_dict)
        response = dict()
        response['status'] = 200
        try:
            response['data'] = parser.parse_folder(fetch_path)
            gc.collect()
        except Exception as e:
            logging.exception('Exception occured while handling data')
            response['status'] = 503
        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")