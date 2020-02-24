from pymongo import MongoClient, InsertOne
from bson.json_util import dumps
from errorHandler import error_handler
import recommender as R
from config import dbURL

client = MongoClient(dbURL)
db =client['chatgroup']
users = db['users']

@error_handler
def createUser(username):
    ''' Create users in mongodb and return the user_id '''
    query = list(users.find({'username':username}, {'_id':1}))
    if query:
        raise ValueError(f'username alredy exists {query}')
    user_id = uniqueID()
    users.insert_one({'user_id':user_id, 'username':username})
    return {'user_id': str(user_id), 'username':username}


def userRecommend(user_id):
    ''' Recommend friends to this user based on chat sentiments '''
    return R.recommend_sentiment(int(user_id))

def userRecommendWord(user_id):
    ''' Recommend friends to this user based on chat similar words used '''
    return R.recommend_similar(int(user_id))


def uniqueID():
    ''' Create new ID ''' 
    user_id =[e['user_id'] for e in list(users.find({},{'_id':0, 'user_id':1}))]
    if not user_id:
        return 1
    return max(user_id) +1
