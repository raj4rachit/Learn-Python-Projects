import json

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# OpenAI API URL and key
OPENAI_API_URL = 'https://endpoints.getmerlin.in/chat/completions'
API_KEY = 'API_KEY'  # Replace with your actual API key

def generate_blog_content(prompt):
    url = OPENAI_API_URL

    payload = json.dumps({
        "model": "gpt-3.5-turbo",  # Adjust model as needed
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "max_tokens": 1200,
        "presence_penalty": 0,
        "frequency_penalty": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-merlin-key': f'{API_KEY}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    response = generate_blog_content(prompt)
    print(response)  # Print the response for debugging purposes
    if 'choices' in response:
        return jsonify(response['choices'][0]['message']['content'])
    elif 'error' in response:
        return jsonify({'error': response['error']['message']}), 500
    else:
        return jsonify({'error': 'An unknown error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
