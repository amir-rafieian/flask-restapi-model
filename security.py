# =============================================================================
# Import Libraries
# =============================================================================
from models.user import UserModel

# =============================================================================
# JWT = Jason Web Token is for logging & authentication.
# When user register, server get the unique ID as JWT and pass it to client, so
# Any request from now on should come with JWT, which means client previously
# authenticated.
# =============================================================================


# =============================================================================
# Functions
# =============================================================================
#Function to authenticate the user. given a username/pass it will select the correct username
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user
    
    
def identity(payload): #payload is the content of the JWT token
    user_id = payload['identity']
    #retrieve user
    return UserModel.find_by_id(user_id)




























