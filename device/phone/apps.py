import requests
from base64 import b64encode,b64decode
import json


class ExternalPhone:

    def __init__(self, token:str, addr:str):
        base64_value = b64encode(token.encode()).decode('utf-8')
        self.token = base64_value
        self.addr = addr
        with open("./post_body.json", "r") as f:
            j = json.load(f)
        self.get_endpoint_list_body = j["get_endpoint_list"]["body"]

    def login(self, path):
        path = "/control/20140901/infs/login.json"
        url = "".join(["http://", self.addr, path])
        headers = {
            'Authorization': self.token,
            "Content-Type": "application/json; charset=utf-8"
        }
        r = requests.get(url, headers=headers)
        j = json.loads(r.content.decode('utf-8'))
        return j

    def get_endpoint_list(self):
        path = "/control/api_v2.2.5/employee/query/queryAll.json"
        url = "".join(["http://", self.addr, path])
        headers = {
            'Authorization': self.token,
            "Content-Type": "application/json; charset=utf-8"
        }
        r = requests.post(url, headers=headers, json=self.get_endpoint_list_body)
        j = json.loads(r.content.decode('utf-8'))
        return j
