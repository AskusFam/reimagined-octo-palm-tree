import requests

#endpoints = 'http://httpbin.org/cookies/set'
endpoints = 'http://localhost:8000/api'
params = {
    'freeform':'134'
}
respomse = requests.get(endpoints)
print (respomse.json()['message'])
