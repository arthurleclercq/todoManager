from flask import request
from flask_restful import Resource,reqparse,abort
import  json, os
from app.services.bdd import BDD
from app.services.jwt import decodeToken

class ListByNameResource(Resource):

    def get(self,listName):
        """Return a todo list
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
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
            404:
                description: Invalid list id"""

        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        try:
            res={"name":listName,"todos":BDD.extract(f"app/resources/bdd/{user}/{listName}.json")}
            return ({"status":0,"message":"Todo list returned successully","data":res})
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)

        
    
    def delete(self,listName):
        """Delete a todo list
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
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
            404:
                description: Invalid list id"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        try:
            os.remove(f"app/resources/bdd/{user}/{listName}.json")
            return ({"status":0,"message":"Todo list deleted successully"})
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
    
        
    def patch(self,listName):
        """Modify a todo list's name
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
              type: string
            - in: body
              name: attributes
              description: The new name and description of the todo
              schema:
                  type: object
                  properties:
                      newName:
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
            404:
                description: Invalid list id
            409:
                description: List with new name already exists"""
        
        token=request.headers.get("token")
        parser=reqparse.RequestParser()
        parser.add_argument("newName",type=str,required=True,help="Missing new list name")
        args=parser.parse_args(strict=True)    
        newName=args["newName"]
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        if f"{newName}.json" in  os.listdir(f"app/resources/bdd/{user}"):
            return ({"status":2,"message":"List with new name already exists"},409)
        try:
            
            os.rename(f"app/resources/bdd/{user}/{listName}.json",f"app/resources/bdd/{user}/{newName}.json")
            return ({"status":0,"message":"Todo list renamed successully"})
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
    
        
