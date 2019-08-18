from flask import Flask
from . import models, resources
from flask import jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from models import db
# from app import app


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/appdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# db = SQLAlchemy(app)
jwt = JWTManager(app)

def init_db():
    models.db.init_app(app)
    models.db.app = app
    models.db.create_all()


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.BankDetailsResource, '/bankifsc')
api.add_resource(resources.BranchesDetailsResource, '/branchesquery')
api.add_resource(resources.AllBranches, '/branches')
api.add_resource(resources.AllBanks, '/banks')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

# if __name__=='__main__'  and __package__ is None:
#     from os import sys, path
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#     app.run(host='127.0.0.1', port=8080, debug=True)
