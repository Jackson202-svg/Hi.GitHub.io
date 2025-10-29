from flask import Flask, redirect, url_for, session, request, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from flask_session import Session
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# OAuth setup (example: Google)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory('.', 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/data')
def get_data():
    if 'user' not in session:
        return jsonify({"error": "unauthorized"}), 401
    # Example dynamic server data
    data = {
        "player_count": random.randint(0, 100),
        "server_status": "Online"
    }
    return jsonify(data)

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
