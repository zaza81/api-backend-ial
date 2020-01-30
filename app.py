from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy


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

db.create_all()

userModel = users.model('userModel', {
    'username' : fields.String(),
    'email' : fields.String()
    }
)


# manage status codes
# manage responses
#

@users.route('')
class Users(Resource):

    #GET all users
    #GET a user based on ID
    def get(self):
        return 'ciao'

    @users.expect(userModel)
    def post(self):
        '''create a new user'''
        #create a new record in the DB
        # return the user and 200
        return ''
    #crete PUT
    #create DELETE




if __name__ == '__main__':
    app.run(debug=True)
    # write tests
    # show test coverage
