import requests
 
# Get data on only confirmed cases
api_response = requests.get('https://covid19api.herokuapp.com/confirmed')
api_response_deaths = requests.get('https://covid19api.herokuapp.com/deaths')
 
# Print latest data for location ID 100: California, USA
print(api_response.json()['locations'][223]['latest'])
print(api_response_deaths.json()['locations'][223]['latest'])
