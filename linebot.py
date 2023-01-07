from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage

import json
import re

from model import *
from config import *
from utils import *
from reply import *
from db import *


def lambda_handler(event, context):
    session = createDBsession()

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        message = messageOf(event)
        userId = userIdOf(event)

        try:
            if firstUsage(session, userId):
                replyCommands(event)
                addUser(session, userId)
            elif re.match('^sites$', message):
                replySites(event, session)
            elif re.match('^\d+$', message):
                replyLatestRecord(event, session)
            elif re.match('^last$', message):
                replyLastSite(event, session)
            elif re.match('^help$', message):
                replyCommands(event)
            elif re.match('^schedule\s+\d+\s+\d+$', message):
                replyAddSchedule(event, session)
            elif re.match('^delete\s+\d+\s+\d+$', message):
                replyDeleteSchedule(event, session)
            elif re.match('^schedules$', message):
                replySchedules(event, session)
            elif re.match('^graph\s+\d+$', message):
                replyGraph(event, session)
            else:
                line_bot_api.push_message(
                    userId,
                    TextSendMessage('指令無法識別\n用"help"查詢指令')
                )
        except Exception as err:
            line_bot_api.push_message(TESTER_ID, TextSendMessage(str(err)))
            
    @handler.add(MessageEvent, message=LocationMessage)
    def handle_location(event):
        replyLocation(event, session)
        
    session.close()
    


    # ! below are official suggestion. DO NOT MODIFY.

    signature = event['headers']['x-line-signature']
    body = event['body']
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'signature': json.dumps(signature),
        'body': json.dumps(body)
        }