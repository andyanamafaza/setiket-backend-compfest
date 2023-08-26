import requests

api_endpoint = 'http://localhost:5001/api/auth/login/'
data = {
    'username':'admin',
    'password':'admin'
}
login = requests.post(api_endpoint,data=data)
print(login.status_code)
if login.status_code == 200:
    login_data = login.json()
    print(login_data['access'])
    headers = {
        'Authorization':'Bearer '+login_data['access']
    }
    api_endpoint = 'http://localhost:5001/api/event-users/ee6751c1-7077-4586-9017-2cc9daf56d5b/'
    
    response = requests.get(api_endpoint, headers=headers)
    print(response.json())