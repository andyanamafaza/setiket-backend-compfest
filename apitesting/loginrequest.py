import requests

api_endpoint = 'http://localhost:5001/api/auth/'
data = {
    'username':'rara',
    'password':'rara'
}
response = requests.post(api_endpoint,data=data)
print(response.json())