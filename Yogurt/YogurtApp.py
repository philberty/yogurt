import os
import json

from . import AppCache

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask (__name__)

@app.errorhandler (404)
def not_found (error=None):
    message = { 'status': 404,
                'message': 'Not Found: ' + request.url,
            }
    resp = jsonify (message)
    resp.status_code = 404
    return resp

@app.route ("/")
def index ():
    return app.send_static_file ('index.html')

@app.route ("/api/<path:key>")
def Yogurt_RestApi (key):
    try:
        data = AppCache.CacheServer.get (key)
        data = json.loads (data)
    except:
        data = None
    finally:
        if data is not None:
            data ['status'] = 200
            return jsonify (data)
        return not_found ()

@app.route ("/<path:path>")
def statics (path):
    return app.send_static_file (path)
 
