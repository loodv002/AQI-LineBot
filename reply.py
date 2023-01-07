from linebot.models import TextSendMessage, ImageSendMessage
import re
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

from model import *
from utils import *
from db import *


def replySites(event, session):
    sites = getSites(session)
    reply = '\n'.join('%d %s'%(site.siteId, site.locationInfo()) for site in sites)

    line_bot_api.push_message(
        userIdOf(event),
        TextSendMessage(reply)
    )

def replyLatestRecord(event, session):
    message = messageOf(event)
    siteId = int(re.match('^(\d+)$', message).groups()[0])
    userId = userIdOf(event)
    site = getSite(session, siteId)

    if not site:
        line_bot_api.push_message(
            userId,
            TextSendMessage('測站編號不存在\n用"sites"查詢測站編號')
        )
        return
    
    user = getUser(session, userId)
    updateLastSiteId(session, user, siteId)
    latestRecord = getLatestRecord(session, siteId)

    reply = '%s\n%s'%(site.locationInfo(), latestRecord.simpleInfo())
    line_bot_api.push_message(
        userId, 
        TextSendMessage(reply)
    )

def replyLastSite(event, session):
    userId = userIdOf(event)
    user = getUser(session, userId)
    if user.lastSiteId == None:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('沒有查尋紀錄')
        )
        return

    site = getSite(session, user.lastSiteId)
    latestRecord = getLatestRecord(session, user.lastSiteId)

    reply = '%d %s\n%s'%(site.siteId, site.locationInfo(), latestRecord.simpleInfo())
    line_bot_api.push_message(
        userId, 
        TextSendMessage(reply)
    )

def replyCommands(event):
    s = \
'''➤ help: 開啟此提示
➤ sites: 查看所有測站與測站編號
➤ <測站編號>: 查看該測站最新數據
➤ last: 查看上筆查詢數據
➤ schedules: 查看設置的提醒
➤ schedule <測站編號> <時間(時)>:
     設置定時測站提醒
➤ delete <測站編號> <時間(時)>:
     刪除定時測站提醒
➤ graph <測站編號>:
     該測站24小時內數據圖表
➤ 傳送位置: 查看最近測站數據'''

    line_bot_api.push_message(
        userIdOf(event), 
        TextSendMessage(s)
    )

def replySchedules(event, session):
    userId = userIdOf(event)
    schedule_site = getScheduleWithSite(session, userId)

    if schedule_site:
        reply = '目前已設置\n' + '\n'.join('%d-%s 於 %d時'%(site.siteId, site.locationInfo(), schedule.time) for schedule, site in schedule_site)
    else:
        reply = '目前無設置提醒'

    line_bot_api.push_message(
        userId, 
        TextSendMessage(reply)
    )

def replyGraph(event, session):
    userId = userIdOf(event)
    message = messageOf(event)

    siteId = int(re.match('^graph\s+(\d+)$', message).groups()[0])
    site = getSite(session, siteId)

    if not site:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('測站編號不存在\n用"sites"查詢測站編號')
        )
        return
    
    line_bot_api.push_message(
        userId, 
        TextSendMessage('處理中，請稍後...')
    )
    
    timeLimit = datetime.now() - timedelta(days=1) + timedelta(hours=8)
    records = getRecordsAfter(session, siteId, timeLimit)
    
    aqi = [record.aqi for i, record in enumerate(records) if record.aqi]
    aqiX = [i for i, record in enumerate(records) if record.aqi]
    pm2_5 = [record.pm2_5 for i, record in enumerate(records) if record.pm2_5]
    pm2_5X = [i for i, record in enumerate(records) if record.pm2_5]
    timeMark = [record.publishTime.strftime('%m/%d %H:00') for record in records]
    
    fileName = '/tmp/%d.png'%siteId
    
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    
    fig, ax1 = plt.subplots()

    ax1.set_ylabel('AQI')
    ax1.plot(aqiX, aqi, 'r')
    ax1.tick_params(axis='y', labelcolor='red')
    
    plt.xticks(list(range(24)), timeMark, rotation='vertical')
    plt.title(site.locationInfo() + ' 24小時 AQI、pm2.5 變化')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('pm2.5')
    ax2.plot(pm2_5X, pm2_5, 'b')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.subplots_adjust(bottom = 0.2)
    plt.savefig(fileName)
    
    link = uploadImage(fileName)

    line_bot_api.push_message(
        userId, 
        ImageSendMessage(link, link)
    )

def replyLocation(event, session):
    userId = userIdOf(event)
    lo, la = locationOf(event)

    sites = getSites(session)
    
    nearestSite = min(sites, key=lambda site:distance(lo, la, float(site.longitude), float(site.latitude)))
    latestRecord = getLatestRecord(session, nearestSite.siteId)

    dis = distance(lo, la, float(nearestSite.longitude), float(nearestSite.latitude))
    if dis >= 0.7:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('您與最近的測站距離過遠，不具參考價值')
        )
        return

    user = getUser(session, userId)
    updateLastSiteId(session, user, nearestSite.siteId)

    line_bot_api.push_message(
        userId, 
        TextSendMessage('離您最近的是%d %s\n%s'%(
            nearestSite.siteId,
            nearestSite.locationInfo(),
            latestRecord.simpleInfo()
        ))
    )


def replyAddSchedule(event, session):
    userId = userIdOf(event)
    message = messageOf(event)
    siteId, hour = map(int, re.match('^schedule\s+(\d+)\s+(\d+)$', message).groups())
    site = getSite(session, siteId)
    if not site:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('測站編號不存在\n用"sites"查詢測站編號')
        )
        return
    if hour < 0 or hour > 23:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('時間應在0~23之間')
        )
        return
    if getSchedule(session, userId, siteId, hour):
        line_bot_api.push_message(
            userId, 
            TextSendMessage('提醒已存在')
        )
        return

    addSchedule(session, userId, siteId, hour)

    reply = '成功建立提醒，系統將於每日%d時15分傳送%s的量測記錄'%(hour, site.locationInfo())
    line_bot_api.push_message(
        userId, 
        TextSendMessage(reply)
    )

def replyDeleteSchedule(event, session):
    userId = userIdOf(event)
    message = messageOf(event)
    siteId, hour = map(int, re.match('^delete\s+(\d+)\s+(\d+)$', message).groups())
    site = getSite(session, siteId)
    if not site:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('測站編號不存在\n用"sites"查詢測站編號')
        )
        return
    if hour < 0 or hour > 23:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('時間應在0~23之間')
        )
        return
    
    schedule = getSchedule(session, userId, siteId, hour)
    if not schedule:
        line_bot_api.push_message(
            userId, 
            TextSendMessage('刪除提醒失敗，該提醒不存在。\n用"schedules"查詢現存提醒')
        )
        return
    session.delete(schedule)
    session.commit()

    reply = '成功刪除每日%d時15分 %s 的提醒'%(hour, site.locationInfo())
    line_bot_api.push_message(
        userId, 
        TextSendMessage(reply)
    )
