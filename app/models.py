# import app
from sqlalchemy import and_, or_, not_
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class UserModel(db.Model):
    __tablename__='users'
    username=db.Column(db.String(120), primary_key= True, nullable=False)
    password=db.Column(db.String(120),nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class BankModel(db.Model):
    __tablename__ ='banks'
    id=db.Column(db.BigInteger, primary_key=True, nullable=False)
    name=db.Column(db.String(49))

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def return_all(cls,page,page_size):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name
            }
        query= BankModel.query
        print(page)
        # page_size=20
        if page and page_size:
            query = query.limit(page_size)
            query = query.offset(int(page)*int(page_size))
        query=query.all()
        return {'banks': list(map(lambda x: to_json(x), query))}

class BranchModel(db.Model):
    __tablename__ ='branches'
    ifsc=db.Column(db.String(11), primary_key=True, nullable=False)
    bank_id = db.Column(db.BigInteger, db.ForeignKey('banks.id'))
    branch=db.Column(db.String(74))
    address=db.Column(db.String(195))
    city=db.Column(db.String(50))
    district=db.Column(db.String(50))
    state=db.Column(db.String(26))

    @classmethod
    def find_by_ifsc(cls, ifsc):
        print(ifsc)
        return cls.query.filter_by(ifsc = ifsc).first()

    @classmethod
    def find_by_id_city(cls, id,city,name,page,page_size):
        idInt=int(id)
        def to_json(x):
            return {
                'ifsc': x.ifsc,
                'bank_id': x.bank_id,
                'branch': x.branch,
                'address': x.address,
                'city': x.city,
                'district': x.district,
                'state': x.state

            }
        query= BranchModel.query.filter_by(bank_id=idInt).filter_by(city=city)
        # page_size=20
        if page and page_size:
            query = query.limit(page_size)
            query = query.offset(int(page)*int(page_size))
        return {
            "bank_name":name,
            "city":city,
            "branch_details": list(map(lambda x: to_json(x), query))
        }
        # return {name: list(map(lambda x: to_json(x), BranchModel.query.filter_by(bank_id=idInt).filter_by(city=city)))}

    @classmethod
    def return_all(cls,page,page_size):
        def to_json(x):
            return {
                'ifsc': x.ifsc,
                'bank_id': x.bank_id,
                'branch': x.branch,
                'address': x.address,
                'city': x.city,
                'district': x.district,
                'state': x.state

            }
        query= BranchModel.query
        # page_size=20
        # if page_size:
        #     query = query.limit(page_size)
        if page and page_size:
            query = query.limit(page_size)
            query = query.offset(int(page)*int(page_size))
        query=query.all()
        return {'Branches': list(map(lambda x: to_json(x), query))}
        # return cls.query.filter_by(name = name).first()   filter(and_(bank_id == idInt, city=city))))}
