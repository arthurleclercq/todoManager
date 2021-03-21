from app import api

from app.resources.login import LoginResource
from app.resources.account import AccountResource
from app.resources.lists import ListsResource
from app.resources.listByName import ListByNameResource
from app.resources.todos import TodosResource
from app.resources.todoByName import TodoByNameResource


api.add_resource(LoginResource,"/api/login")
api.add_resource(AccountResource,"/api/account")
api.add_resource(ListsResource,"/api/lists")
api.add_resource(ListByNameResource,"/api/list/<string:listName>")
api.add_resource(TodosResource,"/api/lists/todos/<string:listName>")
api.add_resource(TodoByNameResource,"/api/lists/todos/<string:listName>/<string:todoName>")