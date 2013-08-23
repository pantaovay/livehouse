# -*- coding: utf-8 -*-
import MySQLdb
import datetime

def fans_rank():
    conn = MySQLdb.connect(host='localhost', user='pogo', passwd='dbpasswd', charset='utf8', db='bigdata')
    cursor = conn.cursor()

    now = datetime.datetime.now()
    weekday = now.isoweekday()

    if weekday <= 5:
        mDay = datetime.timedelta(days = -2 - weekday)
        update_time = now + mDay
    else:
        mDay = datetime.timedelta(days = 5 - weekday)
        update_time = now + mDay
    try:
        cursor.execute(""" SELECT * FROM SiteFollowTable WHERE date=%s ORDER BY increase DESC """, (update_time.date(),))
        results = cursor.fetchall()
    except Exception, e:
        print e
        results = ()
    return results, update_time
