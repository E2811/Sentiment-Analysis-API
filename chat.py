from pymongo import MongoClient, InsertOne
from bson.json_util import dumps
from errorHandler import error_handler
from bson.objectid import ObjectId
import datetime
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient("mongodb://localhost:27017/")
db =client['chatgroup']
users = db['users']
chat = db['chat']

@error_handler
def chat__list_create(users_id):
    ''' Create a conversation to load messages for a bunch of users '''
    query =[]
    chat_new_id = uniqueId()
    chat_id = str(chat.insert_one({"chat_id": chat_new_id}).inserted_id)
    for user in users_id:
        query = list(users.find({'user_id':int(user)}, {"_id":0}))
        if not query:
            raise ValueError('user_id not found')
        chat.update_one({'_id':ObjectId(chat_id)}, {"$push": {"users": {"user_id": query[0]['user_id'], "username": query[0]['username'] }  } } )
    return json.dumps({"chat_id":chat_new_id})


@error_handler
def add_user(chat_id, user_id):
    ''' Add user to a chat '''
    user_info = list(users.find({'user_id':int(user_id)},{'_id':0}))
    print(user_info)
    if not user_info:
        raise ValueError("user not created")
    query = list(chat.find_one({'chat_id':int(chat_id)}))
    if not query:
        raise ValueError('chat not found')
    chat.update_one({'chat_id':int(chat_id)}, {"$push":{'users':{"user_id":user_info[0]['user_id'],"username": user_info[0]['username'] }}})
    return json.dumps({"chat_id":chat_id})


@error_handler
def add_message(chat_id, user_id, message):
    ''' Add message to a chat '''
    query = chat.find_one({"$and":[{'chat_id':int(chat_id)}, {"users.user_id": user_id}]})
    if not query:
        raise ValueError("user not found in this chat")
    chat.update_one({'chat_id':int(chat_id)} , { "$push": { "messages": {"user_id": message['user_id'],"message": message['text'],"time": datetime.datetime.now()}}})
    return json.dumps({"chat_id":chat_id})

@error_handler
def chat_list(chat_id):
    ''' Get all message from chat_id '''
    query = list(chat.find({'chat_id':int(chat_id)},{'_id':0,'messages':1}))
    if not query:
        raise ValueError('chat not found')
    return { "messages": query[0]['messages']}


def uniqueId():
    ''' Create new ID ''' 
    chat_exist = list(chat.find({'chat_id':{'$exists':True}}))
    if not chat_exist:
        return 1
    chat_id =[e['chat_id'] for e in list(chat.find({},{'_id':0, 'chat_id':1}))]
    return max(chat_id) +1


def sentiment_chat(chat_id):
    ''' Get the sentiments score for messages of a selected chat. Return an average score for the chat and a individual score for each message '''
    messages = chat_list(chat_id)['messages']
    sia = SentimentIntensityAnalyzer()
    compounds = []
    text =[]
    for m in messages:
        info ={}
        info['message']=m['message']
        info['time']=m['time']
        info['user_id']=m['user_id']
        compound = sia.polarity_scores(m['message'])['compound']
        info['sentiment']=compound
        compounds.append(compound)
        text.append(info)
    chat.update_one({'messages':m} , {"$set": {"messages":text}})
    average = sum(compounds)/len(compounds)
    chat.update_one({'chat_id':int(chat_id)} , { "$push": { "sentiment_average[-1,1]":average}})
    return {"chat_id":chat_id, "sentiment_average[-1,1]":average, "messages":text} 
