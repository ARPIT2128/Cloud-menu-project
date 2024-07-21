import base64
import boto3
import json
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS


load_dotenv("menu/Secret.env")

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="ap-south-1",aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),)

# Set the model ID, e.g., Titan Image Generator G1.
model_id = "amazon.titan-image-generator-v1"

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # Get the prompt from the request
    data = request.get_json()
    prompt = data.get('prompt', "A stylized picture of a cute old steampunk robot.")
    
    # Generate a random seed.
    seed = random.randint(0, 2147483647)

    # Format the request payload using the model's native structure.
    native_request = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "cfgScale": 8.0,
            "height": 512,
            "width": 512,
            "seed": seed,
        },
    }

    # Convert the native request to JSON.
    request_payload = json.dumps(native_request)

    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request_payload)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract the image data.
    base64_image_data = model_response["images"][0]

    # Save the generated image to a local folder.
    i, output_dir = 1, "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    while os.path.exists(os.path.join(output_dir, f"titan_{i}.png")):
        i += 1

    image_data = base64.b64decode(base64_image_data)
    image_path = os.path.join(output_dir, f"titan_{i}.png")
    with open(image_path, "wb") as file:
        file.write(image_data)

    return jsonify({"message": f"The generated image has been saved to {image_path}", "image_url": image_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
