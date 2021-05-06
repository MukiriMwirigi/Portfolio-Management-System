import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'Gender':Male, 'Married':No, 'Dependents':0, 'Education':Graduate, 'Self_Empl0yed':No, 'ApplicantIncome':20000, 'CoapplicantIncome':200, 'LoanAmount':30000, 'Loan_Amount_Term':180, 'Credit_History':1, 'Property_Area':Urban})

print(r.json())