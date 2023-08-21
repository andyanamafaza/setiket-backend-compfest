import requests
import random
import string

api_endpoint = 'http://localhost:5001/api/auth/register/'
roles = ['customer', 'event_organizer', 'administrator']

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_phone_number():
    return '08' + ''.join(random.choice(string.digits) for _ in range(10))

for _ in range(10):
    data = {
        'username': generate_random_string(8),
        'password': 'faza1234',
        'email': generate_random_string(8) + '@gmail.com',
        'phone_number': generate_random_phone_number(),
        'role': random.choice(roles)
    }
    
    response = requests.post(api_endpoint, data=data)
    print(response.json())

# data = {
#     'username': 'admintesting',
#     'password': 'faza1234',
#     'email': 'admintesting@gmail.com',
#     'phone_number': '0812209138920',
#     'role': 'administrator'
# }
# response = requests.post(api_endpoint, data=data)
# print(response.json())
# print(response.status_code)