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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
    'username' : fields.String(required=True),
    'email' : fields.String(required=True)
    }
)


resp = {200: 'Success', 400: 'user already in db', 400: 'Content not allowed', \
    400: 'Payload too large', 500: 'Server Error'}

# manage responses

@users.route('')
class Users(Resource):

    #GET all users
    #GET a user based on ID
    def get(self):
        return 'ciao'


    @users.expect(userModel, validate=True)
    @users.doc(responses=resp)
    def post(self):
        '''create a new user MODIFIED'''
        #create a new record in the DB
        try:
            data = request.get_json()
            username_request = data.get("username")
            email_request = data.get("email")

        #checking if user exists
            if(User.query.filter( (User.username==username_request) | (User.email==email_request)).count() > 0):
                return 'user already in DB', 400

            u = User(username=username_request, email=email_request)
            app.logger.info(type(u))
            db.session.add(u)
            db.session.commit()
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

        # return the user and 200
        return jsonify(u.asDict())

    #crete PUT
    #create DELETE




if __name__ == '__main__':
    app.run(debug=True)
    # write tests
    # show test coverage
