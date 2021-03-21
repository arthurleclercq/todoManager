from flask import request
from flask_restful import Resource,reqparse,abort
from os import mkdir
import json
from app.services.users import users
from app import config, hashing
class AccountResource(Resource):

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
            409:
                description: User with name already exists"""
        parser=reqparse.RequestParser()
        parser.add_argument("user",type=str,required=True,help="Missing user login")
        parser.add_argument("password",type=str,required=True,help="Missing user password")
        args=parser.parse_args(strict=True)    
        user=args["user"]
        password=args["password"]
        return create(user, password)
        

def create(user, mdp):
    
    if any(e["user"]==user for e in users.local):
        return ({"status":2,"message":"Account already exists"},409)
    else:
        hashed=hashing.hash_value(mdp, salt=config.HASH_SALT)
        users.local.append({"user":user,"password":hashed})
        users.save()
        mkdir("app/resources/bdd/{0}".format(user))
            
        return ({"status":0,"message":"Account created successfully"})
    


    

    