import json


def core_endpoint_status(json_ret:dir):
    endpoints = json_ret["data"]["list"]
    list = {}
    for endpoint in endpoints:
        item = ''.join(["PHONE", "_", str(endpoint["id"])])
        list[item] = {}
        status = endpoint["status"]
        if status == "OffLine":
            list[item]["status"] = 0
        elif status == "Idle":
            list[item]["status"] = 1
        elif status == "Talking":
            list[item]["status"] = 2
        elif status == "Ringing":
            list[item]["status"] = 3

    return json.dumps(list)