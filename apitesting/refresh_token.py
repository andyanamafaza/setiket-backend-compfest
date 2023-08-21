import requests

api_endpoint = 'http://localhost:5001/api/auth/refresh/'
data = {
    'refresh':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NTExMTY3NCwiaWF0IjoxNjkyNTE5Njc0LCJqdGkiOiJmMmYwNTNlNGQ2OGI0ZDliYWRiMWU4NGU0ZTVmOGNkMSIsInVzZXJfaWQiOiI2M2ViNTljZi02MTMwLTQ5NGQtYjczOC01ZTViYThjMjc2MWEifQ.4jXJ55qWuhtyy_GnLRSaiqKW_ltDmQdhihFvKkXpcyc'
}
response = requests.post(api_endpoint,data=data)
print(response.json())