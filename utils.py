from linebot import LineBotApi, WebhookHandler

import pyimgur

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *
from db import *

def createDBsession():
    engine = create_engine('postgresql://{db_user}:{db_password}@{db_host}/{db_name}'.format( 
        db_user=DB_USER, 
        db_password=DB_PASSWORD, 
        db_host=DB_HOST, 
        db_name=DB_NAME)
    )
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return session

def createLineSession():
    return LineBotApi(CHANNEL_TOKEN), WebhookHandler(CHANNEL_SECRET)

def userIdOf(event):
    return event.source.user_id
def locationOf(event):
    return (
        event.message.longitude,
        event.message.latitude
    )
def messageOf(event):
    return event.message.text

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def uploadImage(filePath):
    im = pyimgur.Imgur(IMGUR_ID)
    image = im.upload_image(filePath, title='filePath')
    return image.link

def updateLastSiteId(session, user, siteId):
    user.lastSiteId = siteId
    session.commit()

def firstUsage(session, userId):
    return getUser(session, userId) == None

line_bot_api, handler = createLineSession()