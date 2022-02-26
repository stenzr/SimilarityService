'''
@author: Rohit Kumar [stenzr]
Project: Similarity Service
Description: A REST API to detect similarity between two sentences 
'''

# Install required libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

# Initialize flask app
app = Flask(__name__)
api = Api(app)

# Connect with mongoDB, create database and collection
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

# Class to implement utitlity methods used by different endpoint specific methods


class Utility:
    # Contructor to initialize the Response dictionary
    def __init__(self):
        self.response = {}

    # Method to check if user already exists in the database
    def UserExist(self, username):
        if users.count_documents({"Username": username}) == 0:
            return False
        else:
            return True

    # Method to verify the password of the user
    def verifyPw(self, username, password):
        if not self.UserExist(username):
            return False

        hashed_pw = users.find({
            "Username": username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False

    # Method to count user specific token numbers
    def countTokens(self, username):
        tokens = users.find({
            "Username": username
        })[0]["Tokens"]

        return tokens

    # Method to create the response json structure
    def get_response_json(self, status=501, msg="Internal Error", similarity=None, currentTokens=None, username=None):
        self.response["status"] = status
        self.response["msg"] = msg
        self.response["userInformation"] = {}
        self.response["userInformation"]["username"] = username
        self.response["userInformation"]["currentTokens"] = currentTokens
        self.response["results"] = {}
        self.response["results"]["similarity"] = similarity

        return self.response

# Class to handle call to endpoint "/register"


class Register(Resource):
    def post(self):
        utility = Utility()

        # Get the data from request json
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        # Check if user already exists
        if utility.UserExist(username):
            retJson = utility.get_response_json(
                status=305, msg="Username Already Exists", username=username)
            return jsonify(retJson)

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        # Add user to database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = utility.get_response_json(
            status=200, msg="Sign up Successful", currentTokens=utility.countTokens(username), username=username)
        return jsonify(retJson)

# Class to handle call to endpoint "/detect"


class Detect(Resource):
    def post(self):
        utility = Utility()

        # Get data from request json
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        # Validate the existence of user in database
        if not utility.UserExist(username):
            retJson = utility.get_response_json(
                status=301, msg="Invalid Username", username=username)
            return jsonify(retJson)

        correct_pw = utility.verifyPw(username, password)

        # Authenticate the user
        if not correct_pw:
            retJson = utility.get_response_json(
                status=302, msg="Invalid Password", username=username)
            return jsonify(retJson)

        # Validate if the user has enough token for transaction
        num_tokens = utility.countTokens(username)

        if num_tokens <= 0:
            retJson = utility.get_response_json(
                status=303, msg="You have run out of tokens. Please refill", currentTokens=num_tokens, username=username)
            return jsonify(retJson)

        # Get the similarity score of the texts
        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)
        similarity_score = ratio*100

        # Update the token after transaction fees
        current_tokens = utility.countTokens(username)

        users.update_one({
            "Username": username,
        }, {
            "$set": {
                "Tokens": current_tokens - 1
            }
        })

        retJson = utility.get_response_json(
            status=200, msg="Success", similarity=similarity_score, currentTokens=utility.countTokens(username), username=username)

        return jsonify(retJson)

# Class to handle call to endpoint "/refill"


class Refill(Resource):
    def post(self):
        utility = Utility()

        # Get the data from input json
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]

        # Validate the presence of user in the database
        if not utility.UserExist(username):
            retJson = utility.get_response_json(
                status=301, msg="Invalid Username", username=username)
            return jsonify(retJson)

        # Validate the administrator password
        correct_pw = utility.verifyPw(username="admin", password=password)

        if not correct_pw:
            retJson = utility.get_response_json(
                status=304, msg="Invalid Admin Password", username=username)
            return jsonify(retJson)

        # Update the user specific token
        current_tokens = utility.countTokens(username)
        updated_tokens = current_tokens + refill_amount

        users.update_one({
            "Username": username,
        }, {
            "$set": {
                "Tokens": updated_tokens
            }
        })

        retJson = utility.get_response_json(
            status=200, msg="Success", currentTokens=updated_tokens, username=username)
        return jsonify(retJson)


# Add resource to the api, endpoint info
api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
