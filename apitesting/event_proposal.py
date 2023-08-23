import requests
import time
import random
import string
import webbrowser


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


endpoint = 'http://localhost:5001/api'
login_data = {
    'username': 'event',
    'password': 'faza1234',
}

with open('Twibbon.png', 'rb') as image_file:
    image_data = image_file.read()

if __name__ == "__main__":
    login = requests.post(f'{endpoint}/auth/login/', data=login_data)

    if login.status_code == 200:
        login = login.json()
        print(login['access'])
        headers = {
            'Authorization': 'Bearer '+login['access']
        }

        for i in range(2):
            data = {
                'name': generate_random_string(10),
                'description': generate_random_string(50),
                'category': random.choice(['seminar', 'workshop', 'concert']),
                'status': random.choice(['pending', 'approved', 'rejected']),
                'location': generate_random_string(20),
            }

            files = {
                'banner': ('banner.jpg', image_data),
                'proposal': ('proposal.pdf', open('produk.pdf', 'rb')),
            }

            response = requests.post(
                f'{endpoint}/event-organizer-proposal/create', data=data, headers=headers, files=files)

            if response.status_code != 201:
                print('Error:', response.status_code)
                error_filename = 'error_response.html'
                with open(error_filename, 'w') as error_file:
                    error_file.write(response.text)
                print(f"Saved error response to '{error_filename}'")

                webbrowser.open_new_tab(error_filename)

                print('Asking refresh token')
                refresh_token = login['refresh']
                refresh_request = requests.post(
                    f'{endpoint}/auth/refresh/', data={'refresh': refresh_token})
                print(refresh_request.json())
                headers['Authorization'] = 'Bearer ' + \
                    refresh_request.json()['access']
            else:
                print('Success:', response.status_code)
                print(response.json())
