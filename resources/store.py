# =============================================================================
# Import Libraries
# =============================================================================
from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import JWT, jwt_required
from flask_restful import reqparse

# =============================================================================
# Functions
# =============================================================================
def generate_status_code(status,msg):
    retJson = {
            "status":status,
            "msg":msg
            }
    return retJson


    
# =============================================================================
# Define Resources
# Resources are what we are offering (addition, subtraction, multiplication, division)
# =============================================================================
class Store(Resource):
    
    #With the parser, we can examine the request whether it has the item 
    #we are looking for or not:
    #parser = reqparse.RequestParser() #Its a class variable, so we call it like Item.parser
    #parser.add_argument('name',
    #                   type=str,
    #                   required=True,
    #                   help = "This field is compulsory")
    
    @jwt_required()
    def get(self, name):
        '''
        it will be called when we use get method
        we reach here when resource Add was requested using get method
        '''
        store = StoreModel.find_by_name(name)
        if store is not None:
            return store.json_rep()
        else:
            return generate_status_code(301, '{} Not Found'.format(name))  #flask-restful doesn`t require jasonify
    
   
    def post(self, name):
        '''
        Create Item when post method is used
        '''
        #check if the item already exists:
        if StoreModel.find_by_name(name):
            return generate_status_code(302, '{} already exists'.format(name)), 400
        
        store = StoreModel(name)
        
        try:
            store.save_to_db()
            return generate_status_code(201, '{} has been successfully added'.format(name)), 201 #flask-restful doesn`t require jasonify
        except:
            return generate_status_code(500, '{} insertion error'.format(name)), 500 #flask-restful doesn`t require jasonify
    


    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return generate_status_code(204, '{} has been deleted'.format(name))
        else:
            return generate_status_code(301, '{} does not exists'.format(name))



class StoreList(Resource):
    @jwt_required()
    def get(self):
        
        return {'stores': [store.json_rep() for store in StoreModel.get_all()]}



