import requests

response = requests.get('https://airportgap.dev-tester.com/api/airports')
print(response.status_code)
print(response.text) 
    