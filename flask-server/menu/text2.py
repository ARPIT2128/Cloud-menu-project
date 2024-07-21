
import requests
import json

# Replace with your actual EC2 public IP
API_URL = "http://65.0.170.245:5000/get_dockerfile"

def test_get_dockerfile(query_text):
    headers = {"Content-Type": "application/json"}
    payload = {"query": query_text}
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())
    else:
        print("Failed with status code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    query_text = "mujhe dockerfile bana ke dijiye jis mai centos:7 ki image hoe"
    test_get_dockerfile(query_text)
