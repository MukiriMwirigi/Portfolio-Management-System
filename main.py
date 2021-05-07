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
def predict():
    # Rendering results on HTML GUI
    def convert():
        Gender = request.form['Gender']
        if Gender == 'Male':
            return 0
        else:
            return 1
        
        Married = request.form['Married']
        if Married == 'Yes':
            return 0
        else:
            return 1

        Education = request.form['Education']
        if Education == 'Graduate':
            return 0
        else:
            return 1

        Self_Employed = request.form['Self_Employed']
        if Self_Employed == 'Yes':
            return 0
        else:
            return 1

        Property_Area = request.form['Property_Area']
        if Property_Area == 'Urban':
            return 0
        else:
            return 1

        Dependents = request.form['Dependents']
        ApplicantIncome = request.form['ApplicantIncome']
        CoapplicantIncome = request.form['CoapplicantIncome']
        LoanAmount = request.form['LoanAmount']
        Loan_Amount_Term = request.form['Loan_Amount_Term']
        Credit_History = request.form['Credit_History']


    final_features= [np.array(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area)]
    
    prediction = model1.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('/landing/mlmodel.html', prediction_text='Loan_Status {}'.format(output))


@app.route('/pred_api', methods=['POST'])
def predict_api():
    
    #For direct API calls throughout request
    
    data = request.get_json(force=True)
    prediction = model1.predict([np.array(list(data.values()))])
    
    output = prediction [0]
    return jsonify(output)




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