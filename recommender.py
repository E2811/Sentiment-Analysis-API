from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import chat as C
from errorHandler import error_handler
from pymongo import MongoClient
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import dbURL

client = MongoClient(dbURL)
db =client['chatgroup']
chat = db['chat']
users = db['users']

@error_handler
def obtain_info(user_id):
    ''' Obtain chats where a user_id is involved '''
    lista_chats = list(chat.find({"users.user_id": int(user_id)}, {"_id":0, "chat_id":1}))
    if not lista_chats:
        raise ValueError(f'{user_id} not found')
    data =[]
    for c in lista_chats:
        info_chat = C.chat_list(c['chat_id'])
        data.append(info_chat['messages'])
    return [d for sublist in data for d in sublist]

def recommend_sentiment(user_id):
    ''' Recommend a friend based on most similar sentiments expressed on messages ''' 
    data = obtain_info(user_id)
    data_df =pd.DataFrame(data)
    sentiment = data_df.pivot_table(columns='user_id',values='sentiment')
    distances = pd.DataFrame(1/(1 + squareform(pdist(sentiment.T, 'euclidean'))), 
                         index=sentiment.columns, columns=sentiment.columns)
    similarities = distances[int(user_id)].sort_values(ascending=False)[1:]
    return {'users': dict(similarities)}


def recommend_similar(user_id):
    ''' Recommend a friend based on similarity in word messages based on cosine similarity '''
    data = obtain_info(user_id)
    data_df =pd.DataFrame(data)
    message_users = data_df.groupby(['user_id']).agg({'message':'sum'})
    stop_words=set(stopwords.words('english'))
    for i,m in enumerate(message_users['message']):
        words = word_tokenize(m)
        filtered =[w for w in words if w.lower() not in stop_words]
        message_users.iloc[i]=' '.join(filtered)
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(message_users['message'])
    m = sparse_matrix.todense()
    df = pd.DataFrame(m, columns=count_vectorizer.get_feature_names(), index=message_users.T.columns)
    similarity_matrix = cosine_similarity (df,df)
    similarity_df = pd.DataFrame(similarity_matrix, columns=message_users.T.columns, index=message_users.T.columns)
    np.fill_diagonal(similarity_df.values, 0) 
    similars = dict(similarity_df.idxmax())
    name = list(users.find({'user_id':int(similars[user_id])}, {'_id':0, 'username':1}))
    return {'user_id':str(similars[user_id]), 'username':name[0]['username']}
