# =============================================================================
# Import Libraries
# =============================================================================
from db import db
#import logging
#logging.basicConfig(level=logging.DEBUG)

# =============================================================================
# Classes
# =============================================================================
class ItemModel(db.Model):
    
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True)
    price = db.Column(db.Float(precision=2)) #2decimal places
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') 
    #Its like a join functionality, and it can find the stores in db that matches 
    #wih store id. its a single store (Each Item can belong to one store only, but one
    #store can have many items)

    def __init__(self, name, price, store_id):
        #self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id
        
    def json_rep(self):
        '''
        This method returns the json representation of the model
        '''
        return {'name': self.name, 'price':self.price}
    
    @classmethod
    def find_by_name(cls,name):
        return ItemModel.query.filter_by(name=name).first() #select * from items where name = name limit 1
        
        
    def save_to_db(self): 
        #when we retrieve an object from db, we can change th pgject name and add it 
        #to session again, sqlalchemy will do the update instead of insert. so this method
        #is upsert
        db.session.add(self)
        db.session.commit()
        
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    
    @classmethod
    def get_all(cls):
        return ItemModel.query.all()
    