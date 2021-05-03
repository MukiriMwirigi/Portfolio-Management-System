from main import db
from sqlalchemy import func

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    inventoryId = db.Column(db.Integer, db.ForeignKey('inventories.id'), nullable=False)

    # create
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

   
    def compute_quanity(salesID: int):
        if inv is not None:
            # get the the stock quanity
            total_stock = list(map(lambda obj: obj.quantity, inv.stock))
            total_sales = list(map(lambda obj: obj.quantity, inv.Sales))
            return sum(total_stock) - sum(total_sales)
            
            return dict(compute_quanity=compute_quanity)


"""
    def add_column(database_name:str, table_name:str, column:int, default=None):
        ret = False

add_column('cryptos', 'sales', 'revenue')
add_column('cryptos', 'sales', 'profit')
add_column('cryptos', 'sales', 'loss')
"""