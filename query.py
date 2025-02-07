import requests

url = 'http://192.168.27.64:6060/'

x = requests.get(url)

print(x.json())