import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
import streamlit as st
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the queries"),
    ("user", "Question:{question}"),
])

# Streamlit configuration
st.set_page_config(
    page_title="Chatbot",
    page_icon=":robot:"
)

# Display header
st.header("Chatbot")

# Text input for user query
input_text = st.text_input("Search the topic you want")

# Initialize the LLM model
llm = ChatOllama(model="llama3")  # Use a smaller model if possible gemma2:27b, llama3
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Placeholder for streaming response
output_placeholder = st.empty()


# Asynchronous function to handle streaming response
def display_streamed_response(input_text):
    partial_response = ""

    # Stream response with controlled update frequency
    for i, response_chunk in enumerate(chain.stream({"question": input_text})):  # Using synchronous for-loop
        print(response_chunk)  # Debug line to inspect response_chunk

        # Check if the response_chunk is a dictionary
        if isinstance(response_chunk, dict) and 'message' in response_chunk:
            partial_response += response_chunk['message']['content']
        else:
            # If it's a string, append directly (adjust as needed)
            partial_response += response_chunk

        # Update display only every few chunks
        if i % 5 == 0:
            output_placeholder.text(partial_response)
            time.sleep(0.1)  # Synchronous delay for smoother display updates

    # Final update with the complete response
    output_placeholder.text(partial_response)

# Run the function if there's input
if input_text:
    with st.spinner("Generating response..."):
        display_streamed_response(input_text)

