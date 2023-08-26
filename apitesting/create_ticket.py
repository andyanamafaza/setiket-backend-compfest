import requests
import webbrowser

endpoint = 'http://localhost:5001/api'
login_data = {
    'username': 'admin',
    'password': 'admin'
}
login_response = requests.post(f'{endpoint}/auth/login/', data=login_data)
print(login_response.status_code)

if login_response.status_code == 200:
    login_data = login_response.json()
    print(login_data['access'])
    headers = {
        'Authorization': 'Bearer ' + login_data['access']
    }
    event_data = {
        'title': '2023 LE SSERAFIM TOUR FLAME RISES IN JAKARTA',
        'event_id': '6a6bcee1-5c3f-4177-943d-7ffa7fe709e9',
        'start_date': '2023-09-10',
        'end_date': '2023-09-12',
        'start_time': '15:00',
        'end_time': '23:00',
        'ticket_quantity': 1500,
        'ticket_type': 'paid',
        'description': 'Join us for a weekend of live music and fun in the sun!',
        'price': 9999.00
    }
    response = requests.post(f'{endpoint}/ticket/create/', data=event_data, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print(response.json())
        print(response.status_code)
    else:
        error_html = f"<html><body><h1>Error Code: {response.status_code}</h1><p>{response.text}</p></body></html>"
        with open("error_output.html", "w") as html_file:
            html_file.write(error_html)
        
        webbrowser.open("error_output.html")
else:
    print("Login failed.")

# import requests


# api_endpoint = 'http://localhost:5001/api/auth/register/'


# data = {
#     'title': '2023 LE SSERAFIM TOUR ‘FLAME RISES’ IN JAKARTA',
#     'event_id': '6a6bcee1-5c3f-4177-943d-7ffa7fe709e9',
#     'start_date': '2023-09-10',
#     'end_date': '2023-09-12',
#     'start_time': '15:00',
#     'end_time': '23:00',
#     'ticket_quantity': 1500,
#     'ticket_type': 'paid',
#     'description': 'Join us for a weekend of live music and fun in the sun!',
#     'price': '12235.99'
# }
# response = requests.post(api_endpoint, data=data)
# print(response.json())
# print(response.status_code)