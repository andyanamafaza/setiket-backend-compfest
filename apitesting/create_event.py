import requests
import time
endpoint = 'http://localhost:5001/api'
login_data = {
    'username':'rizqi',
    'password':'rizqi'
}
login = requests.post(f'{endpoint}/auth/',data=login_data)

if login.status_code == 200:
    login = login.json()
    print(login['access'])
    headers = {
        'Authorization':'Bearer '+login['access']
    }
    for i in range(5):
        data = {
        'title':f'Event Baru{i+1}',
        'date':'2023-08-20',
        'ticket_quantity':100,
        'description':'Event Baru nich',
        'status':'approved'
        }
        response = requests.post(f'{endpoint}/event/create/',data=data,headers=headers)
        if response.status_code != 201:
            print('asking refresh token')
            refresh_token = login['refresh']
            refresh_request = requests.post(f'{endpoint}/auth/refresh/',data={'refresh':refresh_token})
            print(refresh_request.json())
            headers['Authorization'] ='Bearer '+refresh_request.json()['access']
        print(response.json())
        time.sleep(5)