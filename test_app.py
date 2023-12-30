"""
request_processor.py

This script sends a POST request to a Flask application running at http://localhost:5000/process_request.
It includes a JSON payload with a specified query type to simulate processing a write request.

Usage:
    1. Ensure that the Flask application is running and accessible at http://localhost:5000.
    2. Modify the 'data' dictionary to include the desired query type.
    3. Run the script to send the POST request and receive a response.

Example:
    - If the Flask application is configured to handle 'write' queries:
        data = {"query_type": "write"}
    - If the Flask application is configured to handle 'read' queries:
        data = {"query_type": "read"}

Note:
    - Adjust the 'url' variable if the Flask application is running at a different endpoint.
    - Review and modify the 'headers' and 'data' variables as needed for your specific use case.
"""
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
