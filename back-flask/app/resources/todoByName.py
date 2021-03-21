from flask import request
from flask_restful import Resource,reqparse,abort
from app.services.bdd import BDD
from app.services.jwt import decodeToken
from datetime import datetime

class TodoByNameResource(Resource):
    def get(self,listName,todoName):
        """Return a todo
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
              type: string
            - in: path
              name: todoName            
              description: The todo name
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
                description: Invalid list id or todo id"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        try:
            liste=BDD.extract(f"app/resources/bdd/{user}/{listName}.json")                      
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
        
        for t in liste:
            if t["name"]==todoName:
                return ({"status":0,"message":"Todo returned successully","data":t})

        return({"status":4,"message":"Todo doesn't exist"},404)
    
    
    def delete(self,listName,todoName):
        """Delete a todo
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
              type: string
            - in: path
              name: todoName            
              description: The todo name
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
                description: Invalid list id or todo id"""
        token=request.headers.get("token")
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        try:
            liste=BDD.extract(f"app/resources/bdd/{user}/{listName}.json")                      
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
        todo=None
        for t in liste:
            if t["name"]==todoName:
                liste.remove(t)
                BDD.dump(f"app/resources/bdd/{user}/{listName}.json",liste)
                return ({"status":0,"message":"Todo deleted successully"})
        return({"status":4,"message":"Todo doesn't exist"},404)
    
        
    def patch(self,listName,todoName):
        """Modify a todo's name and content
        ---
        tags:
            - Todo API
        parameters:
            - in: path
              name: listName
              description: The todo list name
              required: true
              type: string
            - in: path
              name: todoName            
              description: The todo name
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
                      newDesc:
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
                description: Invalid list id or todo id
            409:
                description: Todo with new name already exists in list"""
        
        token=request.headers.get("token")
        parser=reqparse.RequestParser()
        parser.add_argument("newName",type=str,required=True,help="Missing new todo name")
        parser.add_argument("newDesc",type=str,required=True,help="Missing new todo description")
        args=parser.parse_args(strict=True)    
        newName=args["newName"]
        newDesc=args["newDesc"]
        user=decodeToken(token)
        if user is None:
            return ({"status":3,"message":"Bad authentication token"},401)
        try:
            liste=BDD.extract(f"app/resources/bdd/{user}/{listName}.json")                      
        except Exception as e:
            print(e)
            return({"status":4,"message":"List doesn't exist"},404)
        todo=None
        
        if  (todoName!= newName) and any(t["name"]==newName  for t in liste):
            return ({"status":2,"message":"Todo with this name already exists"},409)

        for t in liste:
            if t["name"]==todoName:
                t["name"]=newName
                t["description"]=newDesc
                t["lastModif"]=datetime.now().strftime("%d %b %Y, %H:%M:%S")
                BDD.dump(f"app/resources/bdd/{user}/{listName}.json",liste)
                return ({"status":0,"message":"Todo modified successully"})
        return({"status":4,"message":"Todo doesn't exist"},404)