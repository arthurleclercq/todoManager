from flask import request
from flask_restful import Resource,reqparse,abort
import  json, os
from app.services.bdd import BDD
from app.services.jwt import decodeToken
from datetime import datetime

class TodosResource(Resource):

    def get(self,listName):
        """Return all todos in a list
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
            liste=BDD.extract(f"app/resources/bdd/{user}/{listName}.json")                      
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
        return ({"status":0,"message":"Todo lists returned successully","data":liste})
    
    def put(self,listName):
        
        """Add a todo in a todo list
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
              description: The name and description of the todo
              schema:
                  type: object
                  properties:
                      nom:
                          type: string
                      description:
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
                description: Todo with new name already exists in list"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        parser=reqparse.RequestParser()
        parser.add_argument("nom",type=str,required=True,help="Missing todo name")
        parser.add_argument("description",type=str,required=True,help="Missing todo description")
        args=parser.parse_args(strict=True)    
        nom=args["nom"]
        description=args["description"]        
        try:
            liste=BDD.extract(f"app/resources/bdd/{user}/{listName}.json")  
            if any(t["name"]==nom for t in liste):
                return ({"status":2,"message":"Todo with this name already exists"},409) 
            liste.append({"name":nom,"description":description,"lastModif":datetime.now().strftime("%d %b %Y, %H:%M:%S")})                
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
        
        BDD.dump(f"app/resources/bdd/{user}/{listName}.json",liste)
        return ({"status":0,"message":"Todo created successully"})
        