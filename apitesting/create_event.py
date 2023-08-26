import requests
import time
import json
# with open('Twibbon.png', 'rb') as image_file:
#     image_data = image_file.read()
# image_data = requests.get('https://s-light.tiket.photos/t/01E25EBZS3W0FY9GTG6C42E1SE/rsfit186124gsm/events/2023/08/02/ff4c5662-d5bd-449d-b6b4-01c37a99008b-1690966599921-4a247221e400d984241103db40ac30e6.jpg').content
endpoint = 'http://localhost:5001/api'
login_data = {
    'username':'admin',
    'password':'admin'
}
login = requests.post(f'{endpoint}/auth/login/',data=login_data)
print(login.status_code)
if login.status_code == 200:
    login = login.json()
    print(login['access'])
    headers = {
        'Authorization':'Bearer '+login['access']
    }
    with open('data.json','r') as f:
        datas = json.load(f)
    datas = datas['data']
    for i in range(len(datas)):
        data = {
            'title': datas[i]['translations'][0]['title'],
            'start_date':'2023-08-24',
            'end_date':'2023-08-25',
            'start_time':'00:00:00',
            'end_time':'01:00:00',
            'place_name': datas[i]['translations'][0]['area'],
            'city': datas[i]['translations'][0]['city'],
            'full_address': datas[i]['translations'][0]['region'],
            'location': datas[i]['translations'][0]['area'],
            'category':'babakanciamis',
            'description': 'mau nonton konser asik? cuma disini tempatnya',
        }
        image = requests.get(datas[i]['images'][0]['urlMedium']).content
        files = {'image': ('image.jpg', image)}
        response = requests.post(f'{endpoint}/event/create/',data=data,headers=headers,files=files)
        if response.status_code != 201:
            print('asking refresh token')
            refresh_token = login['refresh']
            refresh_request = requests.post(f'{endpoint}/auth/refresh/',data={'refresh':refresh_token})
            print(refresh_request.json())
            headers['Authorization'] ='Bearer '+refresh_request.json()['access']
        print(response.json())