import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'experience':3, 'test_score':10, 'interview_score':10})

print(r.json())