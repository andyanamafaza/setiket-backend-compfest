import requests

endpoint = 'http://localhost:5001/api'
login_data = {
    'username':'rarara',
    'password':'rarara'
}
login = requests.post(f'{endpoint}/auth/',data=login_data)
if login.status_code == 200:
    headers = {
        'Authorization':'Token '+login.json()['access']
    }
    data = {
        'title':'Event Baru',
        'date':'2023-08-20',
        'ticket_quantity':100,
        'description':'Event Baru',
        'status':'approved'
    }
    response = requests.put(f'{endpoint}/event/update/21/',data=data,headers=headers)
    print(response.json())