from linebot.models import TextSendMessage
from datetime import datetime, timedelta
from sqlalchemy import and_, extract

from utils import *
from model import *

def lambda_handler(event, context):
    curHour = (datetime.now().hour + 8) % 24
    session = createDBsession()
    schedules = session.query(Schedule).filter_by(time=curHour).all()

    for schedule in schedules:
        time = datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            datetime.now().hour,
            0,
            0
        ) + timedelta(hours=8)
        site = session.query(Site).filter_by(siteId=schedule.siteId).first()
        record = session.query(Record).filter(and_(Record.siteId == schedule.siteId, Record.publishTime == time)).first()

        if record:
            reply = '%s\n%s'%(site.locationInfo(), record.simpleInfo())
        else:
            reply = '查無%s %d時的紀錄'%(site.locationInfo(), schedule.time)
        line_bot_api.push_message(
            schedule.userId,
            TextSendMessage(reply)
        )
    'ok'