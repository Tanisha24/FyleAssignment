from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)



import models

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

parser2 = reqparse.RequestParser()
parser2.add_argument('ifsc', help = 'This field cannot be blank', required = True)

parser3 = reqparse.RequestParser()
parser3.add_argument('name', help = 'This field cannot be blank', required = True)
parser3.add_argument('city', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if models.UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}
        new_user=models.UserModel(
            username=data['username'],
            password=data['password']
        )
        try:
            new_user.save_to_db()
            access_token=create_access_token(identity=data['username'])
            refresh_token=create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500
        return data

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = models.UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if data['password'] == current_user.password:
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token}
        else:
            print(str(data['password']))
            print(len(data['password']))
            print(str(current_user.password))
            print(len(current_user.password))
            return {'message': 'Wrong credentials'}
        return data

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = models.RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = models.RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return models.UserModel.return_all()

    def delete(self):
        return models.UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

class BankDetailsResource(Resource):
    @jwt_required
    def get(self):
        data=parser2.parse_args()
        ifsc=data['ifsc']
        branch_details=models.BranchModel.find_by_ifsc(data['ifsc'])
        print(branch_details)
        if branch_details is None:
            return {'message': 'Ifsc {} doesn\'t exist'.format(data['ifsc'])}
        else:
            print(branch_details)
            bank_details=models.BankModel.find_by_id(branch_details.bank_id)
            return {
                'ifsc': branch_details.ifsc,
                'bank_id':branch_details.bank_id,
                'bank':bank_details.name,
                'branch':branch_details.branch,
                'address':branch_details.address,
                'city':branch_details.city,
                'state':branch_details.state
            }


class BranchesDetailsResource(Resource):
    @jwt_required
    def get(self):
        data=parser3.parse_args()
        bank_detail=models.BankModel.find_by_name(data['name'])
        print(bank_detail.id)
        if not bank_detail:
            return {'message':'Bank {} doesn\'t exist'.format(data['name'])}
        else:
            branch_details=models.BranchModel.find_by_id_city(bank_detail.id,data['city'],data['name'])
            return branch_details

class AllBanks(Resource):
    def get(self):
        return models.BankModel.return_all()

class AllBranches(Resource):
    def get(self):
        return models.BranchModel.return_all()
