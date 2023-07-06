from flask import Flask

app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def api_data():
    """
    查询数据的api，对接metroview的驱动
    :return:
    """
    
    return 200


@app.route('/api/control', methods=['POST'])
def api_control():
    """
    下发控制的api
    :return:
    """

    return 200


if __name__ == '__main__':
    from configparser import ConfigParser
    cfg = ConfigParser()
    cfg.read('../config.ini')
    port = cfg.get('api', 'port')

    app.run(port=int(port))
