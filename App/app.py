from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]


class Utility:
    def UserExist(self, username):
        if users.find({"Username": username}).count() == 0:
            return False
        else:
            return True

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

    def countTokens(self, username):
        tokens = users.find({
            "Username": username
        })[0]["Tokens"]

        return tokens


class Register(Resource):
    def post(self):
        utility = Utility()
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if utility.UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }

            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "Sign up Successful"
        }


class Detect(Resource):
    def post(self):
        utility = Utility()
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not utility.UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }

            return jsonify(retJson)

        correct_pw = utility.verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid Password"
            }

            return jsonify(retJson)

        num_tokens = utility.countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "You have run out of tokens. Please refill"
            }

            return jsonify(retJson)

        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "similarity": ratio*100,
            "msg": "Success"
        }

        current_tokens = utility.countTokens(username)

        users.update_one({
            "Username": username,
        }, {
            "$set": {
                "Tokens": current_tokens - 1
            }
        })

        return jsonify(retJson)

class Refill(Resource):
    def post(self):
        utility = Utility()
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]

        if not utility.UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }

            return jsonify(retJson)

        correct_pw = utility.verifyPw(username="admin", password=password)

        if not correct_pw:
            retJson = {
                "status": 304,
                "msg": "Invalid Admin Password"
            }

            return jsonify(retJson)

        current_tokens = utility.countTokens(username)

        updated_tokens = current_tokens + refill_amount

        users.update_one({
            "Username": username,
        }, {
            "$set": {
                "Tokens": updated_tokens
            }
        })

        retJson = {
            "status": 200,
            "currentTokens": updated_tokens,
            "msg": "Success"
        }        

        return jsonify(retJson)

api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    

