from  fastapi import FastAPI ,Depends , HTTPException
from starlette.middleware.cors import CORSMiddleware

from auth import AuthHandeler
from view import AuthDetails , tweet

import model
auth_handler = AuthHandeler()
app=FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # This allows all origins, you can replace it with specific origins if needed
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],  # You can specify the HTTP methods allowed
#     allow_headers=["*"],  # You can specify the headers allowed
# )

# /feeds
@app.get('/')
def index(username=Depends(auth_handler.auth_wrapper)):
    result = model.getNewsFeedData(username)
    return result


@app.post('/register')
async def register(auth:AuthDetails):
    print(AuthDetails)
    users = model.searchUser(auth.username)
    if users:
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth.password)
    model.insertUser(auth.username, hashed_password)
    return {"message":"account created successfully"}


@app.post('/login')
async def login(auth:AuthDetails):
    u = model.searchUser(auth.username)
    print(u)
    if u == None:
        if  not auth_handler.verify_password(auth.password, u['password']):
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(u.name)
    return {'token': token}


@app.get('/follow/{user_id}')
async def follow(user_id:int,username=Depends(auth_handler.auth_wrapper)):
     return model.follow(username,user_id)


@app.get('/search/')
async def search(search:str ,username=Depends(auth_handler.auth_wrapper)):
    return model.search(search)


@app.post('/post/')
async def post(tweet:tweet ,username=Depends(auth_handler.auth_wrapper)):
    if model.postTweet(tweet, username):
        return  {'message':'successfully tweet posted'}


@app.get('/myprofile')
def index(username=Depends(auth_handler.auth_wrapper)):
    result = model.getmytweetData(username)
    return result

