import requests
import json

url = "https://api.getmerlin.in/chat/completions"

payload = json.dumps({
  "model": "gpt-3.5-turbo", # Adjust model as needed
  "messages": [
    {
      "role": "user",
      "content": "Who won the world series in 2020?"
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
  'x-merlin-key': 'merlin-test-3b7d-4bad-9bdd-2b0d7b3dcb6d',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

