from flask import request
from flask_restful import Resource,reqparse,abort
import json
from app.services.jwt import encodeToken
from app.services.users import users
from app import config, hashing
class LoginResource(Resource):

            
    def post(self):
        """Create a user
        ---
        tags:
            - User API
        parameters:
            - in: body
              name: attributes
              description: User name and password
              schema:
                  type: object
                  properties:
                      user:
                          type: string
                      password:
                          type: string
        responses:
            200:
                description: Success
            401:
                description: Bad login info"""
        parser=reqparse.RequestParser()
        parser.add_argument("user",type=str,required=True,help="Missing user login")
        parser.add_argument("password",type=str,required=True,help="Missing user password")
        args=parser.parse_args(strict=True)        
        user=args["user"]
        password=args["password"]
        return login(user, password)
        


def login(user, mdp):
    if any(e["user"]==user and hashing.check_value(e["password"], mdp, salt=config.HASH_SALT) for e in users.local):        
        token=encodeToken(user)
        return({"status":0,"message":"Login successful","token":token})
    else:
        return({"status":1,"message":"Login error"},401)
    


    
