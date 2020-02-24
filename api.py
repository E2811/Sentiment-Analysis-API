#!/usr/local/bin/python3
from flask import Flask, request
import os
from dotenv import load_dotenv
load_dotenv()
import users as U
import chat as C


app = Flask(__name__)

@app.route("/user/create/<username>", methods=['GET'])
def create_user(username):
    return U.createUser(username) 


@app.route("/chat/create")
def create_chat():
    users_id = request.args.get('users_id')
    def comma_separated_params_to_list(param):
        param =param[1:-1]
        result = []
        for val in param.split(','):
            if val:
                result.append(val)
        return result
    users_id = comma_separated_params_to_list(users_id)
    return C.chat__list_create(users_id)

@app.route("/chat/<chat_id>/adduser")
def add_user_chat(chat_id):
    user_id = request.args.get('user_id')
    return C.add_user(chat_id,user_id)

@app.route("/chat/<chat_id>/addmessage")
def addMessage(chat_id):
    user_id = int(request.args.get('user_id'))
    message = request.get_json()
    return C.add_message(chat_id, user_id, message)

@app.route("/chat/<chat_id>/list")
def chatList(chat_id):
    return C.chat_list(chat_id)

@app.route("/user/<user_id>/recommend")
def recommendUser(user_id):
    return U.userRecommend(user_id)

@app.route("/user/<user_id>/recommendation")
def recommend_user(user_id):
    return U.userRecommendWord(user_id)

@app.route("/chat/<chat_id>/sentiment")
def sentimentScore(chat_id):
    return C.sentiment_chat(chat_id)

app.run("0.0.0.0", os.getenv("PORT"), debug=True)