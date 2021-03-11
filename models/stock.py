from main import db
from sqlalchemy import func

class Stock(db.Model):
    __tablename__ = 'stock'
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