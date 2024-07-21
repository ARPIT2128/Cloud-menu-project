"""import requests
import json

url = "http://127.0.0.1:5000/createbucket"  # Adjust if your Flask app runs on a different host/port
payload = {"name": "testbucket"}  
headers = {
"Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
"""
"""
import requests
import json

url = "http://localhost:5000/generate_image"
payload = {"prompt": "A stylized picture of a cute old steampunk robot."}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print("Test passed.")
    print("Response:", response.json())
else:
    print("Test failed.")
    print("Response Code:", response.status_code)
    print("Response:", response.text)

"""
import os
image_path = os.path.join('output', f"titan_1.png")
print(image_path)