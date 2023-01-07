import json
from requests import get
import psycopg2
from psycopg2.extras import RealDictCursor

from config import *

def handler(event, content):
    url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=%s'%API_KEY

    rsp = get(url)
    records = json.loads(rsp.text)['records']

    host = DB_HOST
    username = DB_USER
    password = DB_PASSWORD
    database = DB_NAME

    statusConvert = {
        '良好': 1,
        '普通': 2,
        '對敏感族群不健康': 3,
        '對所有族群不健康': 4,
        '非常不健康': 5,
        '危害': 6,
        None: None
    }

    def null(v):
        if v in ['-', '']: return None
        return v

    conn = psycopg2.connect(
        host = host,
        database = database,
        user = username,
        password = password
    )

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    for record in records:
        for k, v in record.items():
            record[k] = null(v)
        
        siteid = record['siteid']
        aqi = record['aqi']
        status = statusConvert[record['status']]
        so2 = record['so2']
        co = record['co']
        o3 = record['o3']
        o3_8hr = record['o3_8hr']
        pm10 = record['pm10']
        pm2_5 = record['pm2.5']
        no2 = record['no2']
        nox = record['nox']
        no = record['no']
        wind_speed = record['wind_speed']
        wind_direc = record['wind_direc']
        publishtime = record['publishtime']
        co_8hr = record['co_8hr']
        pm2_5_avg = record['pm2.5_avg']
        pm10_avg = record['pm10_avg']
        so2_avg = record['so2_avg']
            
        cursor.execute('insert into record values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (
            siteid,
            aqi,
            status,
            so2,
            co,
            o3,
            o3_8hr,
            pm10,
            pm2_5,
            no2,
            nox,
            no,
            wind_speed,
            wind_direc,
            publishtime,
            co_8hr,
            pm2_5_avg,
            pm10_avg,
            so2_avg
        ))

        conn.commit()
    return 'ok'
