from pprint import pprint

import requests

response = requests.get('https://airportgap.com/api/airports')
print(response.status_code)
print(response.text)
print("\n")
pprint(response.json())