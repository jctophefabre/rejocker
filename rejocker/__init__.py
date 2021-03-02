# -*- coding: utf-8 -*-

__license__ = "Apache-2.0"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


import os
import sys
import json
from flask import Flask, abort, request, make_response

from . import rejocker


######################################################


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REJOCKER_DATA_SOURCE = os.environ.get("REJOCKER_DATA_SOURCE", default=os.path.join(BASE_DIR,"resources","example.json"))


######################################################


if REJOCKER_DATA_SOURCE.startswith("http://") or REJOCKER_DATA_SOURCE.startswith("https://"):
    print("Loadind data from URL is not currently supported")
    sys.exit(127)
else:
    try:
        with open(REJOCKER_DATA_SOURCE) as json_file:
            JSON_DATA = json.load(json_file)
    except:
        print("Error loading json data from {}".format(REJOCKER_DATA_SOURCE))
        sys.exit(127)


ENDPOINTS = rejocker.Rejocker(JSON_DATA)


if os.environ.get("FLASK_ENV") == "development":
    print("Using data from {}".format(REJOCKER_DATA_SOURCE))
    print("Endpoints:")
    for k,v in ENDPOINTS.get_all_endpoints().items():
        print("-",k,v)


######################################################


app = Flask(__name__)


@app.route('/',methods=rejocker.Rejocker.METHODS)
@app.route('/<path:subpath>',methods=rejocker.Rejocker.METHODS)
def subpath(subpath=""):

    subpath_norm = rejocker.Rejocker.normalize_url_path(subpath)

    endpobj = ENDPOINTS.get_endpoint(subpath_norm)

    if not endpobj:
        abort(404)
   
    methodobj = endpobj.get_method(request.method)
    if not methodobj:
        abort(405)

    if not methodobj.check_expected_headers(request.headers):
        abort(406)

    if not methodobj.check_parameters(request.args):
        abort(400)

    if not methodobj.check_expected_body(str(request.data, 'utf-8')):
        abort(400)
 

    data = methodobj.get_returned_body()
    
    res = make_response()
    res.headers = methodobj.get_returned_headers()
    res.headers["Content-Type"] = "text/plain"

    if data is not None:
        if isinstance(data,(dict,list,tuple)):
            data = json.dumps(data)
            res.headers["Content-Type"] = "application/json"
        res.data = data

    return  res
