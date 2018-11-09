#coding: utf-8

import os
import platform
import pymysql
import csv
import codecs

if 'Windows' in platform.platform():
    PATH_SOURCE = "E:\BigData\Source"
    PATH_WORK = "E:\BigData\Work"
    USER = 'root'
    PSWD = '102038Fs'
else:
    PATH_SOURCE = '/home/fiore/Projects/BigData/ForFlash/Source'
    PATH_WORK = '/home/fiore/Projects/BigData/ForFlash/Work'
    USER = 'root'
    PSWD = '123456'

FOLDER_ORIGINAL = "ORG"
FOLDER_CLEAN = "CLN"

DATABASE = 'RENTING'
TABLE = 'full'
VARCHAR_MAX = 40

def readCsvToSql(filename, database, table):
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        #head = next(reader) #没有head行
        conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PSWD, db=database, charset='utf8')
        cur = conn.cursor()
        sql = 'insert into '+table+' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for item in reader:
            #if item[1] is None or item[1] == '':  # item[1]作为唯一键，不能为null
            #    continue
            args = tuple(item)
            #设置两次重试，如果没有问题直接跳出，如果第一次出错，极可能1406字符串过长，尝试裁剪重试，如果再次出错，放弃这一行
            retry = 2
            while retry:
                try:
                    cur.execute(sql, args)
                    break #没有错误就break，完成当前数据的处理流程
                except Exception as e:
                    #打印错误
                    print(e)
                    print(args)
                    #尝试修复 1：把原始数据长度裁剪到表格限定长度
                    item = [item[i][:VARCHAR_MAX] for i in range(len(item))]
                    args = tuple(item)
                retry -= 1

        conn.commit()
        cur.close()
        conn.close()

def importData():
    for dirWork in os.listdir(PATH_WORK):
        print(dirWork)
        for file in os.listdir(PATH_WORK+os.sep+dirWork+os.sep+FOLDER_CLEAN):
            print('-'*10+file)
            readCsvToSql(PATH_WORK+os.sep+dirWork+os.sep+FOLDER_CLEAN+os.sep+file, DATABASE, TABLE)

if __name__ == '__main__':
    importData()


#附上SQL创建表格的代码，需要在执行导入python脚本之前创建好表    
'''
CREATE DATABASE IF NOT EXISTS `RENTING`;
USE RENTING;
#DROP TABLE `rent`;
CREATE TABLE IF NOT EXISTS `rent`(
	`company`    varchar(40),
    `class`      varchar(40),
    `date`       varchar(40),
    `time`       varchar(40),
    `province`   varchar(40),
    `city`       varchar(40),
    `district`   varchar(40),
    `community`  varchar(40),
    `money`      varchar(40),
    `room`       varchar(40),
    `area`       varchar(40),
    `direction`  varchar(40),
    `floor`      varchar(40),
    `decoration` varchar(40),
    `old`        varchar(40)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
SELECT * FROM `rent` LIMIT 100;
SELECT COUNT(*) FROM `rent`;
SELECT COUNT(*) FROM `rent` WHERE `money` != 'NULL';
SELECT `class`, COUNT(*) AS `count_class` FROM `rent` GROUP BY `class` ORDER BY `count_class` DESC;
SELECT `company`, COUNT(*) AS `count_company` FROM `rent` GROUP BY `company` ORDER BY `count_company` DESC;
SELECT `province`, COUNT(*) AS `count_province` FROM `rent` GROUP BY `province` ORDER BY `count_province` DESC;
SELECT `city`, COUNT(*) AS `count_city` FROM `rent` GROUP BY `city` ORDER BY `count_city` DESC;
SELECT `district`, COUNT(*) AS `count_district` FROM `rent` WHERE `district` != 'NULL' GROUP BY `district` ORDER BY `count_district` DESC LIMIT 100;
SELECT `money`, COUNT(*) AS `count_money` FROM `rent` WHERE `money` != 'NULL' AND `money` != 'NOVA' GROUP BY `money` ORDER BY `money` DESC LIMIT 100;
'''    