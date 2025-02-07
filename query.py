import requests

url = 'http://192.168.27.251:7000/feedback_dump/'
obj={'order_id':'ORD121999',
     'feedback':'good',
     'rating':1}
x = requests.post(url, json=obj)

print(x.json())