from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers import ConfigController
import config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/postConfig', methods=['POST'])
def create_data():
    try:
        table_name = request.args.get('table')
        data = request.get_json()
        result = ConfigController.create_data(table_name, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getConfig', methods=['GET'])
def read_data():
    try:
        table_name = request.args.get('table')
        instancename = request.args.get('instancename')
        result = ConfigController.read_data(table_name, instancename)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/updateConfig', methods=['POST'])
def update_data():
    try:
        table_name = request.args.get('table')
        data = request.get_json()
        instancename = data.pop('instancename')
        result = ConfigController.update_data(table_name, instancename, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteConfig', methods=['DELETE'])
def delete_data():
    try:
        table_name = request.args.get('table')
        instancename = request.args.get('instancename')
        if not instancename:
            return jsonify({'error': 'Instance name (instancename) is required in the request'}), 400
        result = ConfigController.delete_data(table_name, instancename)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host=config.FLASK_RUN_HOST, port=int(config.FLASK_RUN_PORT), debug=True)