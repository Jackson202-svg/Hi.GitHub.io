from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/data')
def get_data():
    data = {
        "player_count": 42,
        "server_status": "Online"
    }
    return jsonify(data)

@app.route('/login/<provider>', methods=['POST'])
def login(provider):
    email = request.json.get('email')
    return jsonify({"status": "success", "provider": provider.capitalize(), "email": email})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
