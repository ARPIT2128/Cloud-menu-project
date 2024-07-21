from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
import requests
import io
from PIL import Image
from transformers import AutoTokenizer
import uuid

app = Flask(__name__)

recognizer = sr.Recognizer()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HEADERS = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
}

tokenizer = AutoTokenizer.from_pretrained("gpt2")

def generate_cover_art(input_text):
    try:
        input_text_with_suffix = f"Album Cover,Art,music album cover,{input_text}___{uuid.uuid4()}"
        tokenized_input = tokenizer(input_text_with_suffix, return_tensors="pt")
        input_str = tokenizer.decode(tokenized_input["input_ids"][0])

        payload = {"inputs": input_str}
        response = requests.post(API_URL, headers=HEADERS, json=payload, stream=True)
        response.raise_for_status()

        if response.content:
            image = Image.open(io.BytesIO(response.content))
            buf = io.BytesIO()
            image.save(buf, format='PNG')
            buf.seek(0)
            return buf
        else:
            return None
    except requests.RequestException as e:
        print(f"Error in making request to Hugging Face API: {str(e)}")
        return None

@app.route('/generate_cover_art', methods=['POST'])
def generate_cover_art_endpoint():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    audio_data = audio_file.read()

    try:
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return jsonify({"error": "Google Web Speech API could not understand the audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results from Google Web Speech API; {e}"}), 500

    image_buffer = generate_cover_art(text)
    if image_buffer:
        return send_file(image_buffer, mimetype='image/png')
    else:
        return jsonify({"error": "Empty response from Hugging Face API"}), 500

if __name__ == '__main__':
    app.run(port=8080)
