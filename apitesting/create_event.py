import requests
import time

with open('Twibbon.png', 'rb') as image_file:
    image_data = image_file.read()

endpoint = 'http://localhost:5001/api'
login_data = {
    'username':'rizq',
    'password':'rizq'
}
login = requests.post(f'{endpoint}/auth/',data=login_data)

if login.status_code == 200:
    login = login.json()
    print(login['access'])
    headers = {
        'Authorization':'Bearer '+login['access']
    }
    for i in range(2):
        data = {
            'title': 'Event Baru',
            'date': '2023-08-20',
            'ticket_quantity': 100,
            'description': 'Event Baru nich',
            'status': 'approved',
        }
        files = {'image': ('image.jpg', image_data)}
        response = requests.post(f'{endpoint}/event/create/',data=data,headers=headers,files=files)
        if response.status_code != 201:
            print('asking refresh token')
            refresh_token = login['refresh']
            refresh_request = requests.post(f'{endpoint}/auth/refresh/',data={'refresh':refresh_token})
            print(refresh_request.json())
            headers['Authorization'] ='Bearer '+refresh_request.json()['access']
        print(response.json())
