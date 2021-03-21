env="DEV"
API_NAME="Flask Todo API"
APP_VERSION="1.0"
API_KEY="cléTodoArthurLeclercq"
HASH_SALT="sardocheleroidusel"

class Config():
    DEBUG=True
    SWAGGER_URL="/api/docs"

class ConfigDev(Config):
    DATA_SWAGGER="http://127.0.0.1:5001/swagger"

class ConfigProd(Config):
    DEBUG=False
    DATA_SWAGGER="http://localhost:5001/swagger"
   