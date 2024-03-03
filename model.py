from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from view import tweet as tweetview
from view import user as Userobj

Base = declarative_base()
class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    def __str__(self):
        return  self.name

class followers_mapping(Base):
    __tablename__ = 'followers_mapping'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    follow = Column(String)


class tweet(Base):
    __tablename__ ='tweet'
    id = Column(Integer,primary_key=True)
    user = Column(Integer)
    text = Column(String)


engine = create_engine('sqlite:///test.db',echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)


def rawQuery(raw):
    try:
        db = Session()
        result = db.execute(text(raw))
        print(result)
        db.close()
        return result
    except  Exception  as e:
        print("couldn't connect to DB")
        print(e)

def addObjectToDB(obj):
    # try:
        db = Session()
        db.add(obj)
        db.commit()
        db.close()
        return True
    # except Exception  as e:
    #     print("couldn't add obj to db")
        # print(e)

        return False
def getNewsFeedData(username):
    data = rawQuery(f"SELECT * FROM tweets where tweets.user in ( select follow from followers_mapping where user=(select id from user where name={username}))")
    print(data)
    if data == None :
        return []
    dataToJson=[tweetview(*i).dict() for i in data]
    return dataToJson



def follow(username,user_id ):
    print('\n\n\n\n',username,user_id)
    user_id = rawQuery(f'select id from user where id={user_id};')
    current_id = rawQuery(f"select id from user where name='{username}';")
    if user_id and current_id:
        print('test')
        follow= followers_mapping(user = current_id.all()[0][0] , follow = user_id.all()[0][0] )
        addObjectToDB(follow)
        return  {'message':'followed the user'}
    else:
        return 'invalid request'

    return None


def search(search):
    data= rawQuery(f"select * from user where name like '%{search}%';")
    tweetdata= rawQuery(f"select * from tweet where text like '%{search}%';")
    dataToJson=[]
    if data == None and tweetdata == None :
        return {'message':'no data found'}


    dataToJson=[]
    if data  != None:
        for i in data:
            print(i,type(i))
            dataToJson.append({'id':i[0],'name' : i[1]})
    tweets=[]
    for i in tweetdata:
        tweets.append({'id':i[0],'text':i[1],'user':i[2]})
    return {'tweets':tweets,'users':dataToJson}


def insertUser(username, hashed_password):
    usr = user(name=username,password = hashed_password)
    addObjectToDB(usr)
    return None


def searchUser(username):
    name = rawQuery(f"select * from user where name ='{username}' limit 1;")
    print(str(name) + 'this is farhan')

    if name!=None:
        for i in name:
            print(i)
            return user(id=i[0], name=i[1], password=i[2])
            # return user(*i)
    return None


def postTweet(t,username):
    newTweet = tweet(text=t.text,user=username)
    addObjectToDB(newTweet)
    return True


def getmytweetData(username):
    data = rawQuery(
        f"SELECT * FROM tweet where user = '{username}'")
    print(data)
    if data == None:
        return []
    dataToJson = [tweetview(id=i[0],text=i[1],user=i[2]).dict() for i in data]
    return dataToJson