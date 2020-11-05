# -*- coding: utf-8 -*-

__license__ = "Apache-2.0"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


import json


######################################################


class RejockerMethod:

    def __init__(self):
        self._expected_headers = dict()
        self._expected_params = dict()
        self._accepted_params = dict()
        self._expected_body = None
        self._returned_headers = dict()
        self._returned_body = None


    def check_expected_headers(self,headers):
        for k,v in self._expected_headers.items():
            found_value = headers.get(k)
            if found_value is None or found_value != v:
                return False 
        return True


    def check_parameters(self,args):
        for k,v in self._expected_params.items():
            found_value = args.get(k)
            if found_value is None or found_value not in v:
                return False
        
        for k,v in self._accepted_params.items():
            found_value = args.get(k)
            if found_value is not None and found_value not in v:
                return False

        return True


    def check_expected_body(self,body):
        if self._expected_body is None:
            return True
        elif isinstance(self._expected_body,str):
            return self._expected_body == body
        elif isinstance(self._expected_body,(dict,list,tuple)):
            try:
                tmp_body = json.dumps(json.loads(body),sort_keys=True)
                tmp_expectedbody = json.dumps(self._expected_body,sort_keys=True)
                return tmp_body == tmp_expectedbody
            except:
                return False
        return False 
    

    def get_returned_headers(self):
        return self._returned_headers


    def get_returned_body(self):
        return self._returned_body


######################################################


class RejockerEndpoint:

    def __init__(self):
       self. _methods = dict()

    
    def get_method(self,method):
        if method in self._methods:
            return self._methods[method]
        return None


######################################################


class Rejocker:

    METHODS = ["GET","POST","PUT","PATCH","DELETE"]

    def __init__(self, json_data):

        self._endpoints = dict()        

        # Import of configuration

        for set in json_data:
            prefix = ""
            expected_headers = dict()

            if "prefix" in set and set["prefix"] is not None:
                prefix = set["prefix"]
            if "expected" in set and "headers" in set["expected"] and set["expected"]["headers"]:
                expected_headers = set["expected"]["headers"].copy()
           
            if "endpoints" in set:
                for endpdef in set["endpoints"]:
                    endpobj = RejockerEndpoint()

                    for method in Rejocker.METHODS:
                        method_lowcase = method.lower()
                        if method_lowcase in endpdef:
                            methobj = RejockerMethod()

                            methobj._expected_headers = expected_headers.copy()
                            if "expected" in endpdef[method_lowcase]:
                                if "headers" in endpdef[method_lowcase]["expected"]:
                                    for k,v in endpdef[method_lowcase]["expected"]["headers"].items():
                                        methobj._expected_headers[k] = v
                                if "parameters" in endpdef[method_lowcase]["expected"]:
                                    for k,v in endpdef[method_lowcase]["expected"]["parameters"].items():
                                        methobj._expected_params[k] = v
                                if "body" in endpdef[method_lowcase]["expected"]:
                                    methobj._expected_body = endpdef[method_lowcase]["expected"]["body"]
                            
                            if "accepted" in endpdef[method_lowcase]:
                                if "parameters" in endpdef[method_lowcase]["accepted"]:
                                    for k,v in endpdef[method_lowcase]["accepted"]["parameters"].items():
                                        methobj._accepted_params[k] = v
                            
                            if "returned" in endpdef[method_lowcase]:
                                if "headers" in endpdef[method_lowcase]["returned"]:
                                    for k,v in endpdef[method_lowcase]["returned"]["headers"].items():
                                        methobj._returned_headers[k] = v
                                if "body" in endpdef[method_lowcase]["returned"]:
                                    methobj._returned_body = endpdef[method_lowcase]["returned"]["body"]

                            endpobj._methods[method.upper()] = methobj

                    self._endpoints[Rejocker.compose_url_path(prefix,endpdef["path"])] = endpobj


    def get_endpoint(self,endpoint):
        if endpoint in self._endpoints:
            return self._endpoints[endpoint]
        return None


    def get_all_endpoints(self):
        endpoints = dict()
        for k,v in self._endpoints.items():
            endpoints[k] = list(v._methods.keys())
        return endpoints


    @staticmethod
    def normalize_url_path(path):
        normpath = path
        
        if not normpath.startswith("/"):
            normpath = "/"+normpath
        if not normpath.endswith("/"):
            normpath = normpath+"/"

        normpath = normpath.replace("//","/")

        return normpath


    @staticmethod
    def compose_url_path(prefix,subpath):
        return Rejocker.normalize_url_path(prefix+"/"+subpath)