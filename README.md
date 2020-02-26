# Sentiment-Analysis-API

The aim of this project is to create an API in Falsk to create conversation between different users in chat. In the SRC folder, you can find different files with the necessary code to implement the API. 
  - api.py: File which connect the API and created the endpoints
  - user.py: code to insert the users in the users collection with its corresponding username and users_id
  - chat.py: code to create the chats
  - errorhandler: function to control possible errors when making requests to the API 
  -recommender: code to implement a recommendation system for the users
  -test_api.ipynb: to test the api and observe some examples of requests
  
## API endpoints

### 1. User endpoints 

- (GET) `/user/create/<username>`
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** `user_id`
  
- (GET) `/user/<user_id>/recommend`
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with the user_id of the users ordered from most similar to less 
  
- (GET) `/user/<user_id>/recommendation`
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with top user_id. The similarity is based on similar wording. The analysis was performed using the cosine distance 
  
### 2. Chat endpoints:

- (GET) `/chat/create`
  - **Purpose:** Create a conversation to load messages
  - **Params:** An array of users ids `[user_id]`
  - **Returns:** `chat_id`
 
- (GET) `/chat/<chat_id>/adduser`
  - **Purpose:** Add a user to a chat
  - **Params:** `user_id`
  - **Returns:** `chat_id`
- (GET) `/chat/<chat_id>/addmessage`
  - **Purpose:** Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
  - **Params:**
    - `user_id`: the user that writes the message
  - **Body:**
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `chat_id`
  
- (GET) `/chat/<chat_id>/list`
  - **Purpose:** Get all messages from `chat_id`
  - **Returns:** json array with all messages from this `chat_id`
  
- (GET) `/chat/<chat_id>/sentiment`
  - **Purpose:** Analyze messages from `chat_id`using`NLTK` sentiment analysis package. Introduce in de database the score sentiment of each message
  - **Returns:** json with an average of sentiments from messages in the chat and all messages with sentiment score. 
  
#### Deployed at HEROKU still in process
