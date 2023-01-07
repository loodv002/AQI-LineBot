from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP


Base = declarative_base()
class Site(Base):
    __tablename__ = 'site'

    siteId       = Column('siteid', Integer, primary_key=True)
    siteName     = Column('sitename', String(10))
    county       = Column(String(5))
    longitude    = Column(Numeric(7, 4))
    latitude     = Column(Numeric(7, 4))

    def locationInfo(self):
        return '%s %s測站'%(self.county, self.siteName)

    def __str__(self):
        return 'Site(%d, %s, %s)'%(
            self.siteId,
            self.siteName,
            self.county
        )
    def __repr__(self):
        return self.__str__()
    
class Record(Base):
    __tablename__ = 'record'

    siteId = Column('siteid', Integer, primary_key=True)
    aqi = Column(Integer)
    status = Column(Integer)
    so2 = Column(Numeric(4, 1))
    co = Column(Numeric(5, 2))
    o3 = Column(Numeric(4, 1))
    o3_8hr = Column(Numeric(4, 1))
    pm10 = Column(Integer)
    pm2_5 = Column(Integer)
    no2 = Column(Numeric(4, 1))
    nox = Column(Numeric(4, 1))
    no = Column(Numeric(4, 1))
    windSpeed = Column('wind_speed', Numeric(4, 1))
    windDirec = Column('wind_direc', Integer)
    publishTime = Column('publishtime', TIMESTAMP, primary_key=True)
    co_8hr = Column(Numeric(4, 1))
    pm2_5_avg = Column(Integer)
    pm10_avg = Column(Integer)
    so2_avg = Column(Integer)

    def statusString(self):
        return {
            1: '良好',
            2: '普通',
            3: '對敏感族群不健康',
            4: '對所有族群不健康',
            5: '非常不健康',
            6: '危害',
        }.get(self.status, '<無資料>')

    def simpleInfo(self):
        return '量測時間: %s\nAQI: %s\npm2.5: %s (微克/立方公尺)\n狀態: %s'%(
            str(self.publishTime),
            str(self.aqi) if self.aqi else '<無資料>',
            str(self.pm2_5) if self.pm2_5 else '<無資料>',
            self.statusString()
        )

    def __str__(self):
        return 'Record(%d, %s)'%(
            self.siteId,
            str(self.publishTime)
        )
    def __repr__(self):
        return self.__str__()

class User(Base):
    __tablename__ = 'user_'
    userId = Column('userid', String(33), primary_key=True)
    lastSiteId = Column('lastsiteid', Integer)

class Schedule(Base):
    __tablename__ = 'schedule'

    userId = Column('userid', String(33), primary_key=True)
    siteId = Column('siteid', Integer, primary_key=True)
    time = Column('time_', Integer, primary_key=True)

    def __str__(self):
        return 'Schedule(%s, %d, %d)'%(self.userId, self.siteId, self.time)
    def __repr__(self):
        return self.__str__()