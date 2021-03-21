from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS     
from flask_hashing import Hashing

app=Flask(__name__)

hashing = Hashing(app)
api=Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

from app import config, routes

if config.env=="DEV":
    conf=config.ConfigDev
else:
    conf=config.ConfigProd

app.config.from_object(conf)

@app.route("/swagger")

def swaggerController():
    swag=swagger(app)
    swag["info"]["version"]=config.APP_VERSION
    swag["info"]["title"]=config.API_NAME
    return jsonify(swag)

blueprint=get_swaggerui_blueprint(
    conf.SWAGGER_URL,
    conf.DATA_SWAGGER,
    config={
        "app_name":"Flask Todo API"
    },
)

app.register_blueprint(blueprint,url_prefix=conf.SWAGGER_URL)