from main import db
from sqlalchemy import func

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    itype = db.Column(db.String, nullable=False)
    bp = db.Column(db.Float, nullable=False)
    sp = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    stock = db.relationship('Stock', backref='inventory', lazy=True)
    Sales = db.relationship('Sales', backref='inventory', lazy=True)

    # create
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # select * from inventories
    @classmethod
    def fetch_all(cls):
        return cls.query.all()


    @classmethod
    def get_inventory_byID(cls, id:int):
        return cls.query.filter_by(id=id).first()

    # check if inventory name exists
    @classmethod
    def check_inventory_exists(cls,inventory_name:str):
        return cls.query.filter_by(name=inventory_name).first()

    @classmethod
    def edit_inventory(cls, inv_id, name, itype, bp, sp):
        record = cls.query.filter_by(id=inv_id).first()
        if record:
            record.name = name
            record.itype= itype
            record.bp = bp
            record.sp = sp
            db.session.commit()
            return record
        return record
       