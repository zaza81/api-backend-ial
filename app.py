from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
import traceback


app = Flask(__name__)
api = Api(app,
       version='0.1',
       title='The perfect api',
       description='enpoints for class project at ial',
       endpoint='api')

users = api.namespace('users', description ='CRUD operation for users')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fquomdafsccwnn:f88e57b335f0a76e981deeceed9ae3b24653a4f1070758f3d9b4be87a7a70079@ec2-54-247-125-38.eu-west-1.compute.amazonaws.com:5432/d6dr18mde9cgog'

db = SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable = False)
    email = db.Column(db.String(80), unique=True)

    def asDict(self):
        return {
            'id': self.id,
            'username' : self.username,
            'email': self.email
        }

db.create_all()

userModel = users.model('userModel', {
    'username' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True)
    }
)

userModelPut = users.model('userModelPut', {
    'id' : fields.Integer(required=True, validate=True),
    'username' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True)
    }
)


resp = {200: 'Success', 400: 'user already in db', 400: 'Content not allowed', \
    400: 'Payload too large', 500: 'Server Error'}


@users.route('')
class Users(Resource):
    #GET a user based on ID
    def get(self):
        '''get all users'''
        users = User.query.all()
        j = {}
        j['data'] = []
        j['metadata'] = {}
        j['metadata']['n_results'] = User.query.count()
        j['metadata']['n_page'] = 1

        for user in users:
            j['data'].append(user.asDict())
        return jsonify(j)

    @users.expect(userModel, validate=True)
    @users.doc(responses=resp)
    def post(self):
        '''create a new user'''
        #create a new record in the DB
        try:
            data = request.get_json()
            username_request = data.get("username")
            email_request = data.get("email")

            #checking if user exists
            if(User.query.filter( (User.username==username_request) | (User.email==email_request)).count() > 0):
                return 'user already in DB', 400

            u = User(username=username_request, email=email_request)
            db.session.add(u)
            db.session.commit()
            return jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500


    @users.expect(userModelPut, validate=True)
    @users.doc(responses=resp)
    def put(self):
        '''create a new user'''
        try:
            data = request.get_json()
            id_request = data.get("id")
            username_request = data.get("username")
            email_request = data.get("email")

            #checking if user exists
            u = User.query.filter_by(id = id_request).first()
            if(u is None):
                return 'user not in DB', 404

            u.username = username_request
            u.email = email_request
            db.session.commit()
            return jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500


@users.route('/<int:user_id>')
class UsersId(Resource):
    @users.expect(validate=True)
    @users.doc(responses=resp)
    def get(self, user_id):
        '''gets a user '''
        try:
            u = User.query.filter_by(id = user_id).first()
            if (u is None):
                return 'User not found', 404
            return  jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

    @users.expect(validate=True)
    @users.doc(responses=resp)
    def delete(self, user_id):
        '''deletes a user '''
        try:
            u = User.query.filter_by(id = user_id).first()
            if (u is None):
                return 'User not found', 404
            db.session.delete(u)
            db.session.commit()
            return  204
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500




def create_app():
    return app


if __name__ == '__main__':
    app.run(debug=True)
