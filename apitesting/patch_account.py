import requests


api_endpoint = 'http://localhost:5001/api/account'
headers = {
    'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyODE5NDM5LCJpYXQiOjE2OTI4MTc2MzksImp0aSI6ImNmNmQ2MTlkYjFhZDQ5OWRhNjhlZGVlOTBhOWI5YTg5IiwidXNlcl9pZCI6ImNlNWI2MzhmLTM0MGItNGQ4Ni04OTNhLWJlNDUyODM2NmYzNiJ9.NR_qZvnX-qYBJw3QRj716h5Q7DlB4jpwlBNDgsGzwrg',
}
data = {
    'username':'testing12'
}
response = requests.put(f'{api_endpoint}/b13292ac-6c2e-4419-b125-cb834a929c5c/',data=data,headers=headers)
print(response.text)