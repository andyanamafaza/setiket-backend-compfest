import requests

api_base_url = 'http://localhost:5001/api'

# Login data
login_data = {
    'username': 'admintesting',
    'password': 'faza1234'
}

# Perform login
login_response = requests.post(f'{api_base_url}/auth/', data=login_data)

# Debug: Print login response for troubleshooting
print("Login response:", login_response.status_code, login_response.json())

if login_response.status_code == 200:
    access_token = login_response.json()['access']
    print("Access token:", access_token)
    
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Debug: Print headers for troubleshooting
        print("Headers:", headers)

        overview_response = requests.get(f'{api_base_url}/admin/overview/', headers=headers)
        
        # Debug: Print overview response for troubleshooting
        print("Overview response:", overview_response.status_code)
        
        if overview_response.status_code == 200:
            overview_data = overview_response.json()
            print("Admin Overview Data:")
            print(overview_data)
        else:
            print("Failed to fetch admin overview:", overview_response.status_code)
    else:
        print("Access token not found in login response")
else:
    print("Login failed:", login_response.status_code, login_response.json())
