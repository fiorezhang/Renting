#coding=utf-8

import pymysql
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

DATABASE = 'RENTING'
TABLE_FULL = 'full'
TABLE_DISTINCT = 'distinct'
VARCHAR_MAX = 40

mpl.rcParams['font.sans-serif'] = ['SimHei']


def sql_select(str_fields, str_conditions):
    connection = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PSWD, db=DATABASE, charset='utf8')
    cursor = connection.cursor()

    cmd = "SELECT "+str_fields+" FROM `"+TABLE_DISTINCT+"` "+str_conditions+" ;"

    cursor.execute(cmd)
    ret = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return ret
    
def sk_labels(data, cluster):
    kmeans = KMeans(n_clusters=cluster).fit(data)
    labels = kmeans.labels_
    return labels

def plt_draw_1D(data, str_t, str_x):
    plt.figure(figsize=(7,7))
    plt.hist(data, bins=100, color='steelblue')
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.show()

def plt_draw_1D_s(data, str_t, str_x):
    fig, axes = plt.subplots(1, 2)
    sns.distplot(data, ax=axes[0], bins=20, kde=True, rug=True) #kde密度曲线 rug边际毛毯
    sns.kdeplot(data, ax=axes[1], shade=True) #shade阴影
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.show()

def plt_draw_1D_c(data_0, data_1, str_t, str_x):
    sns.kdeplot(data_0, color='r', shade=False) #shade阴影
    sns.kdeplot(data_1, color='b', shade=False) #shade阴影
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.show()

def plt_draw_2D(data, str_t, str_x, str_y):
    index = [str_x, str_y]    
    diction = {index[i]:data[:,i] for i in range(2)}
    sns.JointGrid(str_x, str_y, diction).plot(sns.regplot, sns.distplot)
    plt.xlim((None, None))
    plt.ylim((None, None))
    plt.show()

def plt_draw_3D(data, labels, str_t, str_x, str_y, str_z):
    colors = ['#E4846C', '#19548E', '#E44B4E', '#197D7F', '#0282C9']
    c_list = [colors[labels[i]] for i in range(data.shape[0])]

    plt.figure(figsize=(12,7))
    ax1 = plt.subplot(111,projection='3d')
    x,y,z = data[:,0], data[:,1], data[:,2]
    ax1.scatter(x,y,z,s=15,color=c_list)
    ax1.set_title(str_t)
    ax1.set_xlabel(str_x)
    ax1.set_ylabel(str_y)
    ax1.set_zlabel(str_z)
    plt.show()

def plt_draw_bar(data, str_t, str_x, str_y):
    X=[str(data[i][0]) for i in range(len(data))]
    Y=[data[i][1] for i in range(len(data))]
    fig = plt.figure()
    plt.bar(X,Y,0.5,color="green")
    plt.xlabel(str_x)
    plt.ylabel(str_y)
    plt.title(str_t)
    plt.savefig(PATH_CHART+os.sep+str_t+"_BarChart.png")
    plt.show()  
    
def analysis_company_num():
    content = sql_select("`company`, COUNT(*) AS `count_company`", "GROUP BY `company` ORDER BY `count_company` DESC LIMIT 8")
    print(content)
    plt_draw_bar(content, '主要房产公司分布', '公司名', '信息条数')
    
def analysis_class_num():
    content = sql_select("`class`, COUNT(*) AS `count_class`", "GROUP BY `class` ORDER BY `count_class` DESC")
    print(content)
    plt_draw_bar(content, '租赁类型分布', '租赁类型', '信息条数')
    
def analysis_province_num():
    content = sql_select("`province`, COUNT(*) AS `count_province`", "GROUP BY `province` ORDER BY `count_province` DESC")
    print(content)
    plt_draw_bar(content, '省份分布', '省份', '信息条数')
    
def analysis_city_num():
    content = sql_select("`city`, COUNT(*) AS `count_city`", "GROUP BY `city` ORDER BY `count_city` DESC")
    print(content)
    plt_draw_bar(content, '城市分布', '城市', '信息条数')    

def analysis_district_num():
    content = sql_select("`district`, COUNT(*) AS `count_district`", "WHERE `district` != 'NULL' GROUP BY `district` ORDER BY `count_district` DESC LIMIT 12")
    print(content)
    plt_draw_bar(content, '最多城区分布', '城区', '信息条数')    
 
def analysis_direction_num():
    content = sql_select("`direction`, COUNT(*) as `count_direction`", "WHERE `direction` != 'NULL' GROUP BY `direction` ORDER BY `count_direction` DESC LIMIT 11")
    print(content)
    plt_draw_bar(content, '朝向分布', '朝向', '信息条数')    
    
def analysis_decoration_num():
    content = sql_select("`decoration`, COUNT(*) AS `count_decoration`", "WHERE `decoration` != 'NULL' GROUP BY `decoration` ORDER BY `count_decoration` DESC LIMIT 6")
    print(content)
    plt_draw_bar(content, '装修分布', '装修情况', '信息条数')    

def analysis_old_num():
    content = sql_select("ROUND(CONVERT(`old`, UNSIGNED)/5)*5 AS `num_old`, COUNT(*) AS `count_old`", "WHERE `old` != 'NULL' GROUP BY `num_old` HAVING `num_old` < 2025 AND `num_old` >1950 ORDER BY `num_old` DESC")
    print(content)
    plt_draw_bar(content, '房龄分布', '房龄', '信息条数')    
    
'''    
def analysis_1D():
    content = sql_select('weight_kg', 'league LIKE "%English Premier%" ') 
    content = np.array(content).flatten()
    print(content.shape[0])
    plt_draw_1D_s(content, 'English', 'Weight')

def analysis_1D_c():
    compare = 'eur_value'
    objects = ['English Premier', 'Spanish Primera', 'German Bundesliga', 'French Ligue 1', 'Italian Serie A']
    objects_a = objects[0]
    objects_b = objects[3]

    content_0 = sql_select(compare, 'league LIKE "%'+objects_a+'%" ') 
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select(compare, 'league LIKE "%'+objects_b+'%" ') 
    content_1 = np.array(content_1).flatten()
    print(content_1.shape[0])
    plt_draw_1D_c(content_0, content_1, objects_a+' vs '+objects_b, compare)

def analysis_2D():
    content = sql_select('potential, eur_wage', 'league LIKE "%English Premier%" AND prefers_st = "True"') 
    content = np.array(content)
    print(content.shape[0])
    plt_draw_2D(content, 'English ST', 'Potential', 'Wage')

def analysis_3D():
    content = sql_select('height_cm, weight_kg, eur_value', 'league LIKE "%English Premier%" AND prefers_cb = "True"') 
    content = np.array(content)
    print(content.shape[0])
    labels = sk_labels(content, 5)
    plt_draw_3D(content, labels, 'English CB', 'Height', 'Weight', 'Value')
'''
    
if __name__ == '__main__':
    #analysis_company_num()
    #analysis_class_num()
    #analysis_province_num()
    #analysis_city_num()
    #analysis_district_num()
    #analysis_direction_num()
    #analysis_decoration_num()
    analysis_old_num()