import requests


api_endpoint = 'http://localhost:5001/api/account'
headers = {
    'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyODY3Mzg5LCJpYXQiOjE2OTI4NjU1ODksImp0aSI6IjE3MTU5NzgwYWIxMDQ3ZWRiNDA3YzFjZWY4OTkxNmFmIiwidXNlcl9pZCI6ImNlNWI2MzhmLTM0MGItNGQ4Ni04OTNhLWJlNDUyODM2NmYzNiJ9.rsm9fj7_fzFMFbCN1W9ZMyLdlEvo24Mg3m0k8h9UPAk',
}
data = {
    'password':'testing12'
}
response = requests.patch(f'{api_endpoint}/b13292ac-6c2e-4419-b125-cb834a929c5c/',data=data,headers=headers)
print(response.text)