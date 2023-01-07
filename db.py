from model import *

def getLatestRecord(session, siteId):
    return session.query(Record).filter_by(siteId=siteId).order_by(Record.publishTime.desc()).first()
    # select * from record where siteid = {siteId} order by publishtime desc limit 1;

def addUser(session, userId):
    user = User(userId=userId, lastSiteId=None)
    session.add(user)
    session.commit()
    # insert into user_ values ({userId}, null);

def getUser(session, userId):
    return session.query(User).filter_by(userId=userId).first()
    # select * from user_ where userid = {userId} limit 1;

def getSite(session, siteId):
    return session.query(Site).filter_by(siteId=siteId).first()
    # select * from site where siteid = {siteId} limit 1;

def getSites(session):
    return session.query(Site).order_by(Site.siteId.asc()).all()
    # select * from site order by siteid;

def existSite(session, siteId):
    return session.query(session.query(Site).filter_by(siteId=siteId).exists()).scalar()
    # select {siteId} in (select siteid from site);

def getRecordsAfter(session, siteId, timeLimit):
    return session.query(Record).filter_by(siteId=siteId).filter(Record.publishTime >= timeLimit).order_by(Record.publishTime.asc()).all()
    # select * from record where siteid = {siteId} and publishtime >= {timeLimit} order by publishtime;

def getSchedule(session, userId, siteId, hour):
    return session.query(Schedule).filter_by(userId=userId, siteId=siteId, time=hour).first()
    # select * from schedule where userid = {userId} and siteid = {siteId} and time_ = hour limit 1;

def addSchedule(session, userId, siteId, hour):
    schedule = Schedule(userId=userId, siteId=siteId, time=hour)
    session.add(schedule)
    session.commit()
    # insert into schedule values ({userId}, {siteId}, {hour});

def getScheduleWithSite(session, userId):
    return session.query(Schedule, Site).join(Site, Schedule.siteId == Site.siteId) \
                                                .filter(Schedule.userId == userId) \
                                                .order_by(Schedule.time.asc()).all()
    # select * from schedule as sc natural join site as si where sc.userid = {userId} order by sc.time_;