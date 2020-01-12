# =============================================================================
# Import libraries
# =============================================================================
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
    
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
# End points   
# =============================================================================
class UserRegister(Resource):
    
    parser = reqparse.RequestParser() #Its a class variable, so we call it like Item.parser
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help = "This field is compulsory")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help = "This field is compulsory")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        #Check if the user exists:
        if UserModel.find_by_username(data['username']):
            return generate_status_code(302, "User {} already exists".format(data['username'])), 400
        
        
        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        
        
        return generate_status_code(201, "User has been created successfully"), 201






























