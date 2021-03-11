from flask import render_template,request, redirect, url_for, flash
# models
from models.inventory import Inventory
from models.stock import Stock
from models.sales import Sales

class InventoryService:

    @classmethod
    def inventories(cls):
        # get all inventories
        all_inventories = Inventory.fetch_all()
        
        if request.method == 'POST':
            name:str = request.form['name']
            itype:str = request.form['category']
            bp = request.form['bp']
            sp = request.form['sp']

            # check if the inventory name exists
            inv = Inventory.check_inventory_exists(name)

            if inv is not None:
                flash('Inventory name already exists', 'danger')
                return redirect(url_for('inventories'))
            else:
                record = Inventory(name=name.title(),itype= itype.title(),bp = bp,sp=sp)
                record.create_record()
                flash('Successfully added', 'success')
                return redirect(url_for('inventories'))
            
        return render_template('/admin/inventories.html', inventories=all_inventories)
