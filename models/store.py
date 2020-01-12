# =============================================================================
# Import Libraries
# =============================================================================
from db import db
#import logging
#logging.basicConfig(level=logging.DEBUG)

# =============================================================================
# Classes
# =============================================================================
class StoreModel(db.Model):
    
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True)
    
    #back reference is doing the opposite of relationship in ItemModel. It lets
    #up now about the items in a database. One store can have many items.
    #lazy defines how the data will be loaded from the database; in this case it will be 
    #loaded dynamically, which is ideal for managing large collections:
    items = db.relationship('ItemModel', lazy='dynamic') #This is a list of ItemModels
    

    def __init__(self, name):
        #self.id = _id
        self.name = name
        
    def json_rep(self):
        '''
        This method returns the json representation of the model
        '''
        #we use self.items.all() instead of self.items() becaue of using lazy=dynamice and
        #self.items would be a list of items but a query builder
        return {'name': self.name, 'items':[item.json_rep() for item in self.items.all()]}
        
    
    @classmethod
    def find_by_name(cls,name):
        return StoreModel.query.filter_by(name=name).first() #select * from stores where name = name limit 1
        
        
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
        return StoreModel.query.all()
    