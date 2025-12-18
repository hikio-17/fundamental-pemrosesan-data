import requests

url = "https://quote-api.dicoding.dev/list"
response = requests.get(url)

print(response.json())