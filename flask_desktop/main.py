from flask import Flask, render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, FlaskWebGUI!</h1>'

if __name__ == '__main__':
    try:
        # Initialize FlaskUI with explicit flask_mode and optional browser path
        ui = FlaskUI(app=app, server='flask', port=5000, width=800, height=600, browser_path=r"C:\Program Files\Google\Chrome\Application\chrome_proxy.exe")
        # Run the application with FlaskUI
        ui.run()
    except Exception as e:
        print(f"Error: {e}")
