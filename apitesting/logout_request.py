import requests
endpoint = 'http://localhost:5001/api'
data = {
    'refresh_token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MjU0NzU1MywiaWF0IjoxNjkyNDYxMTUzLCJqdGkiOiI5MDljNjdmMmMxNzY0ZjNiYTBlMDJhMWYyZWIzN2UzYiIsInVzZXJfaWQiOiJmZDk3ZjlkNi0wNzg1LTRjYzktOTRjMy0xY2UxOTc4ZDU1YjEifQ.ceJRSte3_Ffw_wlRVYEd4Z4YJ0KZMHsda1j8BJMdmKU'
}
request_logout = requests.post(f'{endpoint}/auth/logout/',data=data)
print(request_logout.text)