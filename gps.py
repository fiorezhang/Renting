#coding=utf-8

import pymysql
from scipy import stats
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *
import numpy as np
import os
import platform
import csv
import codecs
import geocoder

if 'Windows' in platform.platform():
    PATH_SOURCE = "E:\BigData\Source"
    PATH_WORK = "E:\BigData\Work"
    PATH_CHART = "E:\BigData\Chart"
    USER = 'root'
    PSWD = '102038Fs'
else:
    PATH_SOURCE = '/home/fiore/Projects/BigData/ForFlash/Source'
    PATH_WORK = '/home/fiore/Projects/BigData/ForFlash/Work'
    PATH_CHART = '/home/fiore/Projects/BigData/ForFlash/Chart'
    USER = 'root'
    PSWD = '123456'

AK_BAIDU = 'OPmzYDQ3FDrcip6S02xtR7cbXsGgbCgG'
    
DATABASE = 'RENTING'
TABLE_FULL = 'full'
TABLE_DISTINCT = 'distinct'
TABLE_GPS = 'gps'
VARCHAR_MAX = 40

mpl.rcParams['font.sans-serif'] = ['SimHei']

def sql_select(str_table, str_fields, str_conditions):
    connection = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PSWD, db=DATABASE, charset='utf8')
    cursor = connection.cursor()

    cmd = "SELECT "+str_fields+" FROM `"+str_table+"` "+str_conditions+" ;"

    cursor.execute(cmd)
    ret = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return ret
    
def sql_update(str_table, str_fields, str_conditions):
    connection = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PSWD, db=DATABASE, charset='utf8')
    cursor = connection.cursor()

    cmd = "UPDATE `"+str_table+"` SET "+str_fields+" "+str_conditions+" ;"

    cursor.execute(cmd)
    ret = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return ret    

def getCommunityList():
    list_community = sql_select(TABLE_DISTINCT, "`city`, `community`, COUNT(*) AS `count_community`", "WHERE `class`='出租房' AND `money`!='NULL' AND `area`!='NULL' GROUP BY `city`, `community` ORDER BY `count_community` DESC LIMIT 2000")
    list_community = np.array(list_community)
    list_community = [record[0]+' '+record[1] for record in list_community]
    return list_community
    
def getGeoInfo(strCommunity):
    try:
        g = geocoder.baidu(strCommunity, key=AK_BAIDU)
        if g.quality != '城市':
            r = geocoder.baidu(g.latlng, key=AK_BAIDU, method="reverse")
            print("检索【"+strCommunity+"】，坐标："+str(g.latlng)+"，城市："+r.city+"，区域："+r.district+"，地址："+r.address)
            return [g.lat, g.lng, r.city, r.district, r.address]
        else:
            print("检索【"+strCommunity+"】，找不到！")
            return None
    except Exception as e:
        print("检索【"+strCommunity+"】，出错了！")
        return None

def updateGpsTable(strCommunity, infoCommunity):
    city, community = str.split(strCommunity, ' ')
    lat, lng, _, district, address = infoCommunity
    print(city, district, community, address, lat, lng)
    sql_update(TABLE_GPS, "`district`='"+district+"', `address`='"+address+"', `lat`="+str(lat)+", `lng`="+str(lng), "WHERE `city`='"+city+"' AND `community`='"+community+"'")

def ifCommunityUpdated(strCommunity):
    city, community = str.split(strCommunity, ' ')
    record = sql_select(TABLE_GPS, "`city`, `community`, `lat`, `lng`", "WHERE `city`='"+city+"' AND `community`='"+community+"'")
    return record[0][2] is None or record[0][3] is None
    
if __name__ == '__main__':
    list = getCommunityList()
    for community in list:
        if ifCommunityUpdated(community):
            info = getGeoInfo(community)
            if info != None:
                updateGpsTable(community, info)

'''    
city = '上海' 
place = '平南一村'
name = city+place
key = 'OPmzYDQ3FDrcip6S02xtR7cbXsGgbCgG'
url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&address=' % (key)
 
url = url + name
r = requests.get(url)
res = r.json()
print(res)
 
if res.get('result', None) and res['result']['comprehension'] == 100:
    loc = res['result']['location']
    print(loc)
else:
    print("NOT FOUND")
'''    