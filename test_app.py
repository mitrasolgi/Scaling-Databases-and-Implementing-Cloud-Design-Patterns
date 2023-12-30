import requests
import json

url = "http://localhost:5000/process_request"
headers = {"Content-Type": "application/json"}

data = {"query_type": "write"}
json_data = json.dumps(data)

response = requests.post(url, headers=headers, data=json_data)

if response.status_code == 200:
    print("Request successfully processed")
    # You can access the response content using response.text or response.json()
    print("Response:", response.text)
else:
    print("Error processing the request. Status code:", response.status_code)
    print("Response:", response.text)
