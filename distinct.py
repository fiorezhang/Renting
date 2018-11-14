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

DATABASE = 'RENTING'
TABLE_FULL = 'full'
TABLE_DISTINCT = 'distinct'
VARCHAR_MAX = 40

def distinctFromFull(database, tableFull, tableDistinct):
    conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PSWD, db=database, charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE `"+tableFull+"` ADD id INT AUTO_INCREMENT PRIMARY KEY")
    except Exception as e:
        print(e)
    try:
        cur.execute("ALTER TABLE `"+tableDistinct+"` ADD id INT")
    except Exception as e:
        print(e)
    cur.execute("INSERT INTO `"+tableDistinct+"` SELECT * FROM `"+tableFull+"` WHERE `id` IN (SELECT MAX(`id`) FROM `"+tableFull+"` WHERE `community` != 'NULL' AND `area` != 'NULL' AND `floor` != 'NULL' GROUP BY `community`, `area`, `floor`")

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    distinctFromFull(DATABASE, TABLE_FULL, TABLE_DISTINCT)


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
CREATE TABLE IF NOT EXISTS `distinct`(
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
'''    
