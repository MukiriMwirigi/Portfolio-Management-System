import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'experience':3, 'test_score':10, 'interview_score':10})

print(r.json())

url = 'http://localhost:5000/pred_api'
r = requests.post(url,json={'Gender':Male, 'Married':Yes, 'Dependents':10, 'Education':Graduate, 'Self_Employed':No, 'ApplicantIncome':200000, 'CoapplicantIncome':20000, 'LoanAmount':300000, 'Loan_Amount_Term':360, 'Credit_History':1, 'Property_Area':Urban})

print(r.json())