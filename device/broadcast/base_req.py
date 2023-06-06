def get_token():
    import requests
    url = "http://172.16.11.26:8001/api/v29+/auth?name=admin&password=123456"
    r = requests.get(url)
    import json
    j = {}
    j = json.loads(r.content)
    return j["token"]


def get_terminal_status(token):
    import json
    broadcast_status_list = json.loads("{}")
    url = "http://172.16.11.26:8001/api/v29+/ws/forwarder"
    body = json.loads("{}")
    body["company"] = "BL"
    body["actioncode"] = "c2ls_get_server_terminals_status"
    body["token"] = token
    body["data"] = ""
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"
    import requests
    r1 = requests.put(url, data=body)
    j1 = None
    try:
        j1 = json.loads(r1.content)
    except json.JSONDecodeError:
        pass
    if j1 is not None:
        points = j1["data"]["EndPointsArray"]
        for point in points:
            item = "BROADCAST_" + str(point["EndpointID"])
            broadcast_status_list[item] = {}
            broadcast_status_list[item]["status"] = point["Status"]
    return broadcast_status_list
