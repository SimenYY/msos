from protocol.deviceProtocol import DeviceProtocol, web_client


@web_client
class PhoneProtocol(DeviceProtocol):

    def __init__(self):
        pass

    def execute(self, device_code_list, content):
        print(device_code_list, content)
