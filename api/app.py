from flask import Flask

app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def api_data():

    return 200


@app.route('/api/control', methods=['POST'])
def api_control():

    return 200


if __name__ == '__main__':
    from configparser import ConfigParser
    cfg = ConfigParser()
    cfg.read('../config.ini')
    port = cfg.get('api', 'port')

    app.run(port=int(port))
