import requests
from flask import Flask, request, jsonify, send_from_directory, Response

app = Flask(__name__, static_url_path='', static_folder='.')

# Set your Merlin API key
MERLIN_API_KEY = 'merlin-test-3b7d-4bad-9bdd-2b0d7b3dcb6d'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')

    url = f'https://api.getmerlin.in/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-merlin-key': f'{MERLIN_API_KEY}'
    }

    payload = {
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
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify({"response": response.json()['choices'][0]['text'].strip()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
