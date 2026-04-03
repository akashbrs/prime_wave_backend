import urllib.request
import json

url = 'http://127.0.0.1:8005/api/contact/'
data = json.dumps({
    'full_name': 'Test User',
    'email': 'primewavelifestyle@gmail.com',  # Replace with a test email you can check
    'message': 'This is a test from the API debugger'
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print(f"Response: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"Error Code: {e.code}")
    print(f"Error Body: {e.read().decode()}")
except Exception as e:
    print(f"Connection Error: {e}")
