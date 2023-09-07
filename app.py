from flask import Flask
from flask_graphql import GraphQLView
from graphql import GraphQLError
from graphene import ObjectType, String, Schema
import bcrypt
import jwt
import main

app = Flask(__name__)

main.load_dotenv()
secret_key = main.os.getenv('SECRET_KEY')


# _____________ GraphQL Schema ____________________#
class Query(ObjectType):
    signup = String(name=String(), email=String(), password=String())
    login = String(email=String(), password=String())

    def resolve_signup(self, info, name, password, email):
        # Check if the user already exists
        existing_user = main.collection.find_one({'name': name})
        if existing_user:
            raise GraphQLError('Username already exists.')

        # _____________ Hashing Password ____________________#
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # _____________ Hashing Password ____________________#
        main.collection.insert_one(
            {
                'name': name,
                'email': email,
                'password': hashed_password
            }
        )

        return "Signup Successful"

    def resolve_login(self, info, email, password):
        # _____________ Hashing Password ____________________#
        user = main.collection.find_one({'email': email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            token = jwt.encode({'email': email}, secret_key, algorithm='HS256')
            return f'This User exists, here is the {token}'
        else:
            raise GraphQLError('Invalid username or password')


schema = Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
