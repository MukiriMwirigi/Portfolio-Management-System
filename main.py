import pandas as pd
from pandas.core.base import DataError
import sklearn 
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
# configs
from configs.configurations import Development, Testing, Production
import pickle

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
model1 = pickle.load(open('mdl.pkl', 'rb'))
model = pickle.load(open('mod.pkl', 'rb'))
le_loaded = pickle.load(open("le.obj", "rb"))

# models
from models.inventory import Inventory
from models.stock import Stock
from models.sales import Sales

# services
from services.inventory import InventoryService

Gender_to_int = {'Male':1, 'Female':0}
Married_to_int = {'Yes':1, 'No':0}
Education_to_int = {'Graduate':1, 'Not Graduate':0}
Self_Employed_to_int = {'Yes':1, 'No':0}
Property_Area_to_int = {'Urban':1, 'Rural':0}

# error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404


@app.before_first_request
def create():
    db.create_all()


@app.context_processor
def utility_processor():
    def compute_quanity(inventoryID: int):
        # find an inventory that matches the id
        inv = Inventory.get_inventory_byID(id=inventoryID)
        if inv is not None:
            # get the the stock quanity
            total_stock = list(map(lambda obj: obj.quantity, inv.stock))
            total_sales = list(map(lambda obj: obj.quantity, inv.Sales))
            return sum(total_stock) - sum(total_sales)
            
    return dict(compute_quanity=compute_quanity)
"""
@app.context_processor
def utility_processor():
    def compute_revenue(inventoryID: int):
        if sales is not None:
            total_sales = list(map(lambda obj:revenue, inv.Sales))
            return (total_sales * sp)
            
    return dict(compute_revenue=compute_revenue)

@app.context_processor
def utility_processor():
    def compute_profit(inventoryID: int):
        if sales is not None:
            total_sales = list(map(lambda obj:revenue, inv.Sales))
            return(compute_revenue-(total_sales*bp))

    return dict(compute_profit=compute_profit)

@app.context_processor
def utility_processor():
    def compute_loss(inventoryID: int):
        if sales is not None:
            total_sales = list(map(lambda obj:revenue, inv.Sales))
            return(compute_revenue-(total_sales*bp))

    return dict(compute_loss=compute_loss)

"""
@app.route('/')
def index():
    return render_template('/landing/index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    total_inventories = len(Inventory.fetch_all())

    return render_template('/admin/dashboard.html', ti=total_inventories)


@app.route('/mlmodel')
def mlmodel():
    return render_template('/landing/mlmodel.html')

@app.route('/pred', methods=['POST'])
def pred():
    if request.method == 'POST':
        
        Gender = request.form['Gender']
        Married = request.form['Married']
        Education = request.form['Education']
        Self_Employed = request.form['Self_Employed']
        Property_Area = request.form['Property_Area'] 
        Dependents = request.form.get('Dependents')
        ApplicantIncome = request.form.get('ApplicantIncome')
        CoapplicantIncome = request.form.get('CoapplicantIncome')
        LoanAmount = request.form.get('LoanAmount')
        Loan_Amount_Term = request.form.get('Loan_Amount_Term')
        Credit_History =  request.form.get('Credit_History')
        
        feature_list=['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
        
        data = pd.DataFrame(index=[1])
        data['Gender'] = Gender_to_int[Gender]
        data['Married'] = Married_to_int[Married]
        data['Education'] = Education_to_int[Education]
        data['Self_Employed'] = Self_Employed_to_int[Self_Employed]
        data['Property_Area'] = Property_Area_to_int[Property_Area]
        data['Dependents'] = Dependents 
        data['ApplicantIncome'] = ApplicantIncome
        data['CoapplicantIncome'] = CoapplicantIncome
        data['LoanAmount'] = LoanAmount
        data['Loan_Amount_Term'] = Loan_Amount_Term
        data['Credit_History'] = Credit_History
        
        for i in data:
            if i == np.NaN :
                data.fillna(inplace=True)
            else:
                return i 

        pred = model1.predict(data)

        if pred == 1:
            return 1
        else: 
            return 0

        #output = round(pred[0], 0)
        output = pred

        return render_template('/landing/mlmodel.html', pred_text='Loan_Status {}'.format(output))

@app.route('/pred_api', methods=['POST'])
def pred_api():
    
    #For direct API calls throughout request
    data = request.get_json(force=True)
    pred = model1.predict(data)
    
    output = pred [0]
    return jsonify(output)
 
######################################################################################################
@app.route('/salary')
def salary():
    return render_template('/landing/salary.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Rendering results on HTML GUI

    int_features = [int(x) for x in request.form.values()]
    final_features= [np.array(int_features)]
    
    
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('/landing/salary.html', prediction_text='Salary {}'.format(output))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    
    #For direct API calls throughout request
    
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    
    output = prediction [0]
    return jsonify(output)

############################################################################################################
@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    return InventoryService.inventories()


@app.route("/inventories/<int:inv_id>/restock", methods=['POST'])
def restock(inv_id):
    if request.method == 'POST':
        qty = request.form['qty']
        
        r = Stock(quantity=qty,inventoryId=inv_id)
        r.create_record()
        flash("New stock successfully added", "success")

        return redirect(url_for('inventories'))

@app.route("/inventories/<int:inv_id>/make-sale", methods=['POST'])
def make_sale(inv_id):
    if request.method == "POST":
        qty = request.form['qty']

        s = Sales(quantity=qty, inventoryId=inv_id)
        s.create_record()
        flash("Sale successfully recorded", "success")
        return redirect(url_for('inventories'))


@app.route('/inventories/<int:inv_id>/edit', methods=['POST'])
def edit_inventory(inv_id):
    if request.method == 'POST':
        name:str = request.form['name']
        itype:str = request.form['category']
        bp = request.form['bp']
        sp = request.form['sp']

        u = Inventory.edit_inventory(
            inv_id=inv_id,
            name=name,
            itype=itype,
            bp=bp,
            sp=sp
        )
        flash("Inventory record successfully updated", "success")
        return redirect(url_for('inventories'))


#######################################################################################################
"""Stock"""
@app.route('/stock')
def stock():
    all_stock = Stock.fetch_all()
    return render_template('admin/stock.html', all_stock=all_stock)

############################################################################################################
"""Sales"""
@app.route('/sales')
def sales():
    all_sales = Sales.fetch_all()
    return render_template('admin/sales.html', all_sales=all_sales)


"""
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
"""