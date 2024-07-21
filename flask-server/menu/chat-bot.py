import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("menu/Secret.env")

# Configure the API key
gemini_key = os.getenv('GEMINI_KEY')

genai.configure(api_key=gemini_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def chat_with_model(prompt):
    # Start a chat session
    chat_session = model.start_chat(history=[])

    # Send the prompt to the model and get the response
    response = chat_session.send_message(prompt)
    return response.text

