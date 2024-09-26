import webview
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from threading import Thread
import requests
import re
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Dummy in-memory store for authenticated sessions
authenticated_users = {}
favicon_path = 'favicon.ico'


@app.route('/')
def index():
    token = request.cookies.get('token')
    if token in authenticated_users:
        user_data = authenticated_users[token]
        return render_template('home.html', user=user_data)
    return redirect(url_for('login_page'))


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        loginData = request.get_json()
        logging.info(f"Received data: {loginData}")
    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        return jsonify({'error': 'Invalid JSON input.'}), 400

    username = loginData.get('username')
    password = loginData.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    # Validate username is an email address
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        return jsonify({'error': 'Invalid email address. Please enter a valid email.'}), 400

    response = requests.post('https://hrms.schedulesoftware.net/api/login', data={'email': username, 'password': password})

    try:
        data = response.json()
        logging.info(f"Response from external API: {data}")
    except requests.exceptions.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from external API: {e}")
        return jsonify({'error': 'Failed to decode response from the server.'}), 500

    if response.status_code == 200 and data.get('status') == True:
        data = data.get('data')
        token = data.get('token')
        if token:
            authenticated_users[token] = {
                'user': data.get('user'),
                'task': data.get('task'),
                'token': token,
                'time_sheet': data.get('time_sheet'),
                'logo': data.get('company_logo')
            }
            resp = make_response(jsonify({'success': True, 'token': token}))
            resp.set_cookie('token', token)
            return resp
        else:
            return jsonify({'error': 'Token is missing from the response.'}), 500
    else:
        return jsonify({'error': data.get('error','Unknown error')}), 400

@app.route('/logout')
def logout():
    token = request.cookies.get('token')
    if token and token in authenticated_users:
        del authenticated_users[token]
    response = redirect(url_for('login_page'))
    response.delete_cookie('token')
    return response


def start_flask():
    app.run()


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the pywebview window
    webview.create_window('HRMS - Human Resources Management System', 'http://127.0.0.1:5000', width=900, height=700)
    webview.start()
