# coding=utf-8
import json

import requests

class BroadcastExterior:
    def __init__(self):
        pass

    def get_endpoints_status(self):
        url = ""
        headers = {}
        body = {"TNumber": 2}
        r = requests.post(url, headers=headers, json=body)

        return json.loads(r.content)
