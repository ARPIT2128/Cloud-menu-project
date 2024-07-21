from menu import AWS_functions,Message_functions

from flask import Flask, Response ,request,render_template, jsonify, send_file,send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import io
from PIL import Image
from base64 import b64encode
import os
from dotenv import load_dotenv
import boto3
import base64
import json
import random
from cvzone.HandTrackingModule import HandDetector  

import requests
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError
from gtts import gTTS

load_dotenv("menu/Secret.env")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

"""
CAMERA MODULE
"""

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['frame']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Read image file from request
    image_stream = io.BytesIO(file.read())
    image = Image.open(image_stream)
    
    # Convert PIL image to numpy array
    frame = np.array(image)
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray_frame, 100, 200)
    
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    processed_image = Image.fromarray(edges)  # Convert numpy array (edges) back to PIL Image
    
    processed_image_path = 'processed_frame.png'
    processed_image.save(processed_image_path)
    
    # Send processed image file to frontend (alternative approach)
    # return send_file(processed_image_path, mimetype='image/png')
    
    # Alternatively, send processed data as base64 encoded image
    buffered = io.BytesIO()
    processed_image.save(buffered, format="PNG")
    buffered.seek(0)
    img_str = "data:image/png;base64," + b64encode(buffered.getvalue()).decode()

    return jsonify({'success': True, 'processed_image': img_str}), 200




# hand detection cam
cap = cv2.VideoCapture(0)
detector = HandDetector(staticMode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5)
finger_count = 0  # Variable to store finger count
camera_running = True  # Variable to control the camera

def count_fingers():
    global finger_count, camera_running
    while camera_running:
        success, img = cap.read()
        if not success:
            break
        
        hands, img = detector.findHands(img, draw=True, flipType=True)
        finger_count = 0
        if hands:
            for hand in hands:
                fingers = detector.fingersUp(hand)
                finger_count += fingers.count(1)

        # Convert image to JPEG format to stream
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global camera_running
    camera_running = True
    return Response(count_fingers(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_camera')
def stop_camera():
    global camera_running
    camera_running = False
    cap.release()
    return jsonify({'status': 'Camera stopped'})

@app.route('/finger_count')
def get_finger_count():
    global finger_count
    return jsonify({'finger_count': finger_count})


# AWS Cloud related callings 

@app.route('/terminate_instances', methods=['POST'])
def terminate_instances_route():
    try:
        data = request.json
        instance_ids = data.get('instance_ids')
        if not instance_ids:
            return jsonify({'error': 'Instance IDs are required'}), 400    
    
        response = AWS_functions.Driver_terminate_instances(
            region_name='ap-south-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            instance_ids=instance_ids
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/initiate_instance', methods=['POST'])
def initiate_instance_route():
    try:
        response = AWS_functions.Driver_initiate_instance(
            region_name='ap-south-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



 

# Set AWS credentials as environment variables


@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    bucket_name = request.form.get('bucket_name')
    if bucket_name:
        try:
            s3 = boto3.client('s3', region_name='ap-south-1')
            s3.create_bucket(
                Bucket=bucket_name,
                ACL='private',
                CreateBucketConfiguration={
                    'LocationConstraint': 'ap-south-1'
                },
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            return jsonify({'message': 'Bucket created successfully!'})
        except Exception as e:
            return jsonify({'error': f'Error creating bucket: {str(e)}'})
    else:
        return jsonify({'error': 'Bucket name not provided'})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    bucket_name = request.form.get('bucket_name')
    file = request.files['file']
    if bucket_name and file:
        try:
            s3 = boto3.client('s3', region_name='ap-south-1',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            s3.upload_fileobj(file, bucket_name, file.filename)
            return jsonify({'message': 'File uploaded successfully!'})
        except Exception as e:
            return jsonify({'error': f'Error uploading file: {str(e)}'})
    else:
        return jsonify({'error': 'Bucket name or file not provided'})

@app.route('/list_files', methods=['POST'])
def list_files():
    bucket_name = request.form.get('bucket_name')
    if bucket_name:
        try:
            s3 = boto3.client('s3', region_name='ap-south-1',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            response = s3.list_objects_v2(Bucket=bucket_name)
            files = [content['Key'] for content in response.get('Contents', [])]
            return jsonify({'files': files})
        except Exception as e:
            return jsonify({'error': f'Error listing files: {str(e)}'})
    else:
        return jsonify({'error': 'Bucket name not provided'})



""" BEDROCK API """
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

@app.route('/output/<path:path>')
def serve_image(path):
    return send_from_directory('output', path)


"""
S3 CODES
"""
@app.route('/createbucket', methods=['POST'])
def createbucket():
    region = 'ap-south-1'
    data = request.json
    name = data['name']
    s3_client = boto3.client(
        's3',
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name=region
    )
    bucket_name = 'bucket89484-' + name
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    print(f"Bucket '{bucket_name}' created successfully.")
    return jsonify({'bucket_name': bucket_name})


@app.route('/chat_gemini', methods=['POST'])
def call_gemini():
    request_data = request.json
    if 'message' not in request_data:
        return jsonify({'error': 'Message not provided in JSON body'}), 400
    
    message = request_data['message']
    response_text = Message_functions.chat_with_model(message)
    
    return jsonify({'response': response_text})



"""
AUDIO
"""
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = Recognizer()
    with Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        
        audio_data = recognizer.listen(source)
        print("Recognizing...")
        
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {text}")
            return jsonify({'text': text}), 200
        except UnknownValueError:
            return jsonify({'error': 'Google Web Speech API could not understand the audio'}), 400
        except RequestError as e:
            return jsonify({'error': f'Could not request results from Google Web Speech API; {e}'}), 500

@app.route('/text_to_speech', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text', '')
    processed_text = text.upper()  
    return jsonify({'processed_text': processed_text})


"""
UTILS
"""

def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
    except Exception as e:
        return None, None, None, None

@app.route('/location', methods=['GET'])
def get_location():
    lat, long, city, state = locationCoordinates()
    if lat is not None and long is not None:
        return jsonify({
            'latitude': lat,
            'longitude': long,
            'city': city,
            'state': state
        })
    else:
        return jsonify({'error': 'Unable to fetch location data'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



