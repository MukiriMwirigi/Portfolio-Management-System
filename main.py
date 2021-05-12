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
model1 = pickle.load(open('model.pkl', 'rb'))
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
        '''
        if Gender == 'Male':
            Gender = 1
        else:
            Gender = 0
    '''
        Married = request.form['Married']
        '''
        if Married == 'Yes':
            Married = 1
        else:
            Married = 0
    '''
        Education = request.form['Education']
        '''
        if Education == 'Graduate':
            Education = 1
        else:
            Education = 0
        '''
        Self_Employed = request.form['Self_Employed']
        '''
        if Self_Employed == 'Yes':
            Self_Employed = 0
        else:
            Self_Employed = 1
'''
        Property_Area = request.form['Property_Area']
        '''
        if Property_Area == 'Rural':
            Property_Area = 1
        else:
            Property_Area = 0
         '''   
        Dependents = request.form['Dependents']
        ApplicantIncome = request.form['ApplicantIncome']
        CoapplicantIncome = request.form['CoapplicantIncome']
        LoanAmount = request.form['LoanAmount']
        Loan_Amount_Term = request.form['Loan_Amount_Term']
        Credit_History =  request.form['Credit_History']
        
        """
        new_array = [Gender, Married, Education, Self_Employed, Property_Area, Dependents, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History]
        
        data = np.array([new_array])
        #np.where(data[] >= np.finfo(np.float64).max)
        pred = int(model1.predict(data))
        
        output = round(pred[0])
        """
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

        pred = model1.predict(data)
        output = round(pred[0])

        return render_template('/landing/mlmodel.html', prediction_text='Loan_Status {}'.format(output))

"""
@app.route('/pred_api', methods=['POST'])
def pred_api():
    
    #For direct API calls throughout request
    js= json.loads(data.decode("utf-8"))
    json_ = request.get_json(force=True)
    query = pd.get_dummies(pd.DataFrame(json_))
    pred = model1.predict(query)
    
    output = pred [0]
    return jsonify(output)
"""

"""
def pred():
    # Rendering results on HTML GUI
    new_array = list()
    if request.method == 'POST':
        
        Gender = request.form['Gender']
        if Gender == 'Male':
            new_array = new_array + [1,0]
        elif Gender == 'Female':
            new_array == new_array + [0,1]
    
        Married = request.form['Married']
        if Married == 'Yes':
            new_array = new_array + [1,0]
        elif Married == 'No':
            new_array = new_array + [0,1]
    
        Education = request.form['Education']
        if Education == 'Graduate':
            new_array = new_array + [1,0]
        elif Education == "Not Graduate":
            new_array = new_array + [0,1]
        
        Self_Employed = request.form['Self_Employed']
        if Self_Employed == 'Yes':
            new_array = new_array + [1,0]
        elif Self_Employed == 'No':
            new_array = new_array + [0,1]

        Property_Area = request.form['Property_Area']
        if Property_Area == 'Rural':
            new_array = new_array + [1,0]
        elif Property_Area == 'Urban':
            new_array = new_array + [0,1]
            
        Dependents = int(request.form.get('Dependents'))
        ApplicantIncome = int(request.form.get('ApplicantIncome'))
        CoapplicantIncome = int(request.form.get('CoapplicantIncome'))
        LoanAmount = int(request.form.get('LoanAmount'))
        Loan_Amount_Term = int(request.form.get('Loan_Amount_Term'))
        Credit_History = float(request.form.get('Credit_History'))
        
        new_array = new_array + [Dependents, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History]
        
        data = np.array([new_array])
        
        pred = int(model1.predict(data))
        
        output = round(pred[0])
        
        return render_template('/landing/mlmodel.html', prediction_text='Loan_Status {}'.format(output))


@app.route('/pred_api', methods=['POST'])
def pred_api():
    
    #For direct API calls throughout request
    
    data = request.get_json(force=True)
    pred = model1.predict([np.array(list(data.values()))])
    
    output = pred [0]
    return jsonify(output)

    """


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


#################################################################
"""Stock"""
@app.route('/stock')
def stock():
    all_stock = Stock.fetch_all()
    return render_template('admin/stock.html', all_stock=all_stock)

######################################################################
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