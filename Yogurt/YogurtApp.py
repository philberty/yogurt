import os
import json

from flask import Flask
from flask import jsonify
from flask import request

from . import AppCache

sfolder = os.path.join(os.path.dirname(os.path.abspath (__file__)), 'www')
app = Flask(__name__, static_folder=sfolder)

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404,
               'message': 'Not Found: ' + request.url,
               'error': str(error)}
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route("/api/<path:key>")
def Yogurt_RestApi(key):
    try:
        data = AppCache.CacheServer.get(key).decode("utf-8")
        data = json.loads(data)
    except Exception:
        data = None
    finally:
        if data is not None:
            data ['status'] = 200
            return jsonify(data)
        return not_found(error='Invalid key')

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/<path:path>")
def statics(path):
    return app.send_static_file(path)
 
