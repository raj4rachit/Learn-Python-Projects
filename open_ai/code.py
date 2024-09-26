from judini import CodeGPTPlus
codegpt = CodeGPTPlus(api_key="c614c589-6925-4c0d-bfa0-ccdfb0315d1f", org_id="c614c589-6925-4c0d-bfa0-ccdfb0315d1f")

AGENT_ID = "1668861c-1edc-4f57-b9d4-ace305bda119"
messages = [{"role": "user", "content": "What is the meaning of life?"}]

# No streaming
chat = codegpt.chat_completion(agent_id=AGENT_ID, messages=messages)
print(chat)

# Streaming
for chunk in codegpt.chat_completion(agent_id=AGENT_ID, messages=messages,stream=True):
    print(chunk, end="")