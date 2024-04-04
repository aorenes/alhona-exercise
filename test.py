from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_json_content():
    try:
        with open('plc.log.json', 'r') as file:
            json_data = file.read()
        return jsonify(json_data)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)