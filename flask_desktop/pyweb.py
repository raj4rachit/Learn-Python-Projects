import webview
from flask import Flask, render_template_string, request, redirect, url_for, session
from threading import Thread
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Login HTML template
login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <form method="POST" action="/login">
        <label for="username">Email:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <button type="submit">Login</button>
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# Home HTML template
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <h1>Welcome, {{ username }}!</h1>
    <a href="/logout">Logout</a>
</body>
</html>
"""


@app.route('/')
def index():
    if 'username' in session:
        return render_template_string(home_page, username=session['username'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate username is an email address
        if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
            error = 'Invalid email address. Please enter a valid email.'
            return render_template_string(login_page, error=error)

        response = requests.post('https://hrms.schedulesoftware.net/api/login', data={
            'username': username,
            'password': password
        })
        print(response.text)
        if response.status_code == 200:
            # Assuming the API response contains user info in JSON
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template_string(login_page, error=error)
    return render_template_string(login_page)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def start_flask():
    app.run()


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the pywebview window
    webview.create_window('Flask App', 'http://127.0.0.1:5000', width=800, height=600)
    webview.start()
