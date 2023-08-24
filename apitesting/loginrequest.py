import requests

api_endpoint = 'http://localhost:5001/api/auth/login/'
data = {
    'username':'testing12',
    'password':'testing12'
}
response = requests.post(api_endpoint,data=data)
print(response.json())