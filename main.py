import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# _____________ Setting up MongoDB ____________________#
mongo_uri: str = os.getenv('CONNECTION_STRING')
mongo_client: MongoClient = MongoClient(mongo_uri)

# _____________ testing up MongoDB ____________________#
database = mongo_client.get_database('Users_Database')
collection = database.get_collection('Users')

# Testing my MongoDB connection
"""user = {
    'name': 'folarin',
    'email': 'abe@gmail.com',
    'password': '12452145'
}
collection.insert_one(user)"""
