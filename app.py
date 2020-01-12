# =============================================================================
# Install flask-restful
# pip install Flask-RESTful
# pip install Flask-JWT 
# pip install Flask-SQLAlchemy
# =============================================================================

# =============================================================================
# JWT = Jason Web Token is for logging & authentication.
# When user register, server get the unique ID as JWT and pass it to client, so
# Any request from now on should come with JWT, which means client previously
# authenticated.
# =============================================================================

# =============================================================================
# Official API codes
# https://restfulapi.net/http-status-codes/
# 200 OK
# 201 CREATED
# 202 ACCEPTED  #when there is a delay in creating an object for example
# 400 BAD REQUEST
# 404 NOT FOUND
# 415 UNSUPPORTED MEDIA TYPE
# 500 INTERNAL SERVER ERROR
# =============================================================================


# =============================================================================
# Import Libraries
# =============================================================================
from flask import Flask
from flask_restful import Api #Api works with resources, and every resource has to be a class
from flask_jwt import JWT
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# =============================================================================
# Initializing
# =============================================================================
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This is just to supress some warning messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#standard format for db URI: [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
#for postgres: 'postgresql://postgres:postgres@localhost/dreamteam_db'

app.secret_key = 'api_course' #shouldn`t share this with public
api = Api(app)


#Before the first request into this app, we create the tables:
@app.before_first_request
def create_tables():
    db.create_all()
    
    

jwt = JWT(app, authenticate, identity) #functions we defined in security.py
#jwt creates a new end point (/auth), when we call this end point we send a
#username/password. JWT will send it to the authenticate function and returns a 
#JWT token.  so client will send this token with next request and JWT uses identity
#function to get user id.

#In postman, we creat the POST call:
#http://127.0.0.1:5000/auth
#and set json content as:
#{
#	"username":"user1",
#	"password":"abcxyz"
#}
#username & pass must be as same as what we have in database.
#it returns an access token:
#{
#    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Nzc5NTA5MzYsImlhdCI6MTU3Nzk1MDYzNiwibmJmIjoxNTc3OTUwNjM2LCJpZGVudGl0eSI6MX0.9TU-XC7OwpahaNT-yTQe5K2Qr8xuU_43VWjANqt4M_g"
#}
#we set these token value in "Headers" in postman:
#Key: Authorization
#Value: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Nzc5NTA5MzYsImlhdCI6MTU3Nzk1MDYzNiwibmJmIjoxNTc3OTUwNjM2LCJpZGVudGl0eSI6MX0.9TU-XC7OwpahaNT-yTQe5K2Qr8xuU_43VWjANqt4M_g

    

# =============================================================================
# After defining resources, we need to do mapping (url)
# =============================================================================
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item,"/item/<string:name>") #http://127.0.0.1/item/name
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register")


#we put the  __name__ == "__main__" condition to make sure app will run when we
#run this script as main script, if we import app.py to other script and run that
#script, app wouldn`t be run.
if __name__ == "__main__": 
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)









