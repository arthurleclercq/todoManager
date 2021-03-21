from flask import request
from flask_restful import Resource,reqparse,abort
import  os
from app.services.bdd import BDD
from app.services.jwt import decodeToken

class ListsResource(Resource):

    def get(self):
        """Return all todo lists
        ---
        tags:
            - Todo API
        parameters:            
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            200:
                description: Success
            401:
                description: Missing or invalid token"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        res=[]
        for fichier in os.listdir(f"app/resources/bdd/{user}"):
            res.append({"name":fichier[:-5],"todos":BDD.extract(f"app/resources/bdd/{user}/{fichier}")})
        return ({"status":0,"message":"Todo lists returned successully","data":res})
    
    def put(self):
        """Create an empty todo list
        ---
        tags:
            - Todo API
        parameters:            
            - in: body
              name: attributes
              description: The name of the list
              schema:
                  type: object
                  properties:
                      nom:
                          type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            200:
                description: Success
            401:
                description: Missing or invalid token
            409:
                description: List already exists"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        parser=reqparse.RequestParser()
        parser.add_argument("nom",type=str,required=True,help="Missing list name")
        args=parser.parse_args(strict=True)    
        nom=args["nom"]
        if f"{nom}.json" in  os.listdir(f"app/resources/bdd/{user}"):
            return ({"status":2,"message":"List already exists"},409)
        BDD.dump(f"app/resources/bdd/{user}/{nom}.json",[])
        return ({"status":0,"message":"Todo lists created successully"})
    
        

        
        


            

        
        
