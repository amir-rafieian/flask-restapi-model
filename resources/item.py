# =============================================================================
# Import Libraries
# =============================================================================
from flask_restful import Resource #Api works with resources, and every resource has to be a class
from flask_jwt import JWT, jwt_required
from flask_restful import reqparse
from models.item import ItemModel


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
class Item(Resource):
    
    #With the parser, we can examine the request whether it has the item 
    #we are looking for or not:
    parser = reqparse.RequestParser() #Its a class variable, so we call it like Item.parser
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help = "This field is compulsory")
    
    
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help = "This field is compulsory")
     
    #it will process the input and select the valid fields in data, if it does not
    #have the 'price' field, it will return 400 BAD REQUEST code and the help message.
    #we don`t need to run the following try/except block anymore when we use reqparse.
    
    #try:
    #    data = request.get_json() 
    #except:
    #    return generate_status_code(415, 'Only JSON format is acceptable'), 415
    
            
    
    
    @jwt_required()
    def get(self, name):
        '''
        it will be called when we use get method
        we reach here when resource Add was requested using get method
        '''
        item = ItemModel.find_by_name(name)
        if item is not None:
            return item.json_rep()
        else:
            return generate_status_code(301, '{} Not Found'.format(name))  #flask-restful doesn`t require jasonify
    
    
        
        
    def post(self, name):
        '''
        Create Item when post method is used
        '''
        #check if the item already exists:
        if ItemModel.find_by_name(name):
            return generate_status_code(302, '{} already exists'.format(name)), 400
        
        
        data = Item.parser.parse_args()
        print("Hereee", flush=True)
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
            return generate_status_code(201, '{} has been successfully added'.format(name)), 201 #flask-restful doesn`t require jasonify
        except:
            return generate_status_code(500, '{} insertion error'.format(name)), 500 #flask-restful doesn`t require jasonify
    
    
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return generate_status_code(204, '{} has been deleted'.format(name))
        else:
            return generate_status_code(301, '{} does not exists'.format(name))
        
    
    @jwt_required()
    def put(self, name):
        '''
        Put is to create or update the item, we can call it any number of time,
        and its 
        '''
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        #check if the item already exists:
        if item is not None:
            item.price = data['price']
                
        else:
            #create the item
            item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
            return generate_status_code(204, '{} has been successfully updated'.format(name)), 200 #flask-restful doesn`t require jasonify
        except:
            return generate_status_code(500, '{} update error'.format(name)), 500 #flask-restful doesn`t require jasonify
    
                
                        
        
class ItemList(Resource):
    @jwt_required()
    def get(self):
        
        return {'items': [item.json_rep() for item in ItemModel.get_all()]}






















