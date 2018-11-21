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
    data = [int(data[i]) for i in range(len(data))]
    plt.figure(figsize=(7,7))
    plt.hist(data, bins=100, color='steelblue')
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.show()

def plt_draw_1D_s(data, str_t, str_x):
    data = [int(data[i]) for i in range(len(data))]
    fig, axes = plt.subplots(1, 2)
    #fig, axes = plt.subplots(1, 1)
    sns.kdeplot(data, ax=axes[0], shade=True) #shade阴影
    plt.title(str_t)
    plt.xlabel(str_x)
    sns.distplot(data, ax=axes[1], bins=20, kde=True, rug=True) #kde密度曲线 rug边际毛毯
    #sns.kdeplot(data, ax=axes, shade=True) #shade阴影
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.savefig(PATH_CHART+os.sep+str_t+"_KdeDistChart.png")
    plt.show()

def plt_draw_1D_c2(data_0, data_1, str_t, str_x):
    sns.kdeplot(data_0, color='b', shade=False) #shade阴影
    sns.kdeplot(data_1, color='r', shade=False) #shade阴影
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.xlim((0, None))
    plt.show()

def plt_draw_1D_c3(data_0, data_1, data_2, str_0, str_1, str_2, str_t, str_x):
    sns.kdeplot(data_0, color='b', shade=True) #shade阴影
    sns.kdeplot(data_1, color='g', shade=True) #shade阴影
    sns.kdeplot(data_2, color='r', shade=True) #shade阴影
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel('Ratio')
    plt.xlim((0, None))
    plt.legend([str_0, str_1, str_2], loc='upper right', fontsize=10)
    plt.savefig(PATH_CHART+os.sep+str_t+"_KdeChart.png")
    plt.show()

def plt_draw_2D(data, str_t, str_x, str_y):
    index = [str_x, str_y]    
    diction = {index[i]:data[:,i] for i in range(2)}
    sns.JointGrid(x=str_x, y=str_y, data=diction, space=1).plot(sns.regplot, sns.distplot)
    plt.xlim((None, None))
    plt.ylim((None, None))
    plt.title(str_t)
    plt.savefig(PATH_CHART+os.sep+str_t+"_JointChart.png")
    plt.show()

def plt_draw_2D_s(data, str_t, str_x, str_y):
    index = [str_x, str_y]    
    diction = {index[i]:data[:,i] for i in range(2)}
    g = sns.JointGrid(x=str_x, y=str_y, data=diction, space=0.8)
    g = g.plot_joint(sns.kdeplot, cmap="Blues_d")
    g = g.plot_joint(sns.regplot, marker="", color="steelblue")
    plt.xlim((0, None))
    plt.ylim((0, None))
    plt.title(str_t)
    plt.xlabel(str_x)
    plt.ylabel(str_y)
    g = g.plot_marginals(sns.kdeplot, shade=True)
    g = g.annotate(stats.pearsonr, loc='upper left')
    plt.savefig(PATH_CHART+os.sep+str_t+"_JointChart.png")
    #plt.show()

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

def plt_draw_box(data, str_t, str_x, str_y):
    index = [str_x, str_y]    
    diction = {index[i]:data[:,i] for i in range(2)}
    diction[str_y] = diction[str_y].astype(float)
    sns.boxplot(x=str_x, y=str_y, data=diction, color='steelblue')
    plt.xlim((None, None))
    plt.ylim((0, None))
    plt.title(str_t)
    plt.savefig(PATH_CHART+os.sep+str_t+"_BoxChart.png")
    plt.show()    
    
def plt_draw_bar(data, str_t, str_x, str_y):
    X=[str(data[i][0]) for i in range(len(data))]
    Y=[data[i][1] for i in range(len(data))]
    fig = plt.figure()
    plt.bar(X,Y,0.5,color="steelblue")
    plt.xlabel(str_x)
    plt.ylabel(str_y)
    plt.title(str_t)
    plt.savefig(PATH_CHART+os.sep+str_t+"_BarChart.png")
    plt.show()  
    
#########################################################################################

def analysis_company_count():
    content = sql_select("`company`, COUNT(*) AS `count_company`", "GROUP BY `company` ORDER BY `count_company` DESC LIMIT 8")
    print(content)
    plt_draw_bar(content, '主要房产公司分布', '公司名', '信息条数')
    
def analysis_class_count():
    content = sql_select("`class`, COUNT(*) AS `count_class`", "GROUP BY `class` ORDER BY `count_class` DESC")
    print(content)
    plt_draw_bar(content, '租赁类型分布', '租赁类型', '信息条数')

def analysis_month_count():
    content = sql_select("DATE_FORMAT(CONVERT(`date`, DATE), '%y-%m') AS `num_month`, COUNT(*) AS `count_month`", "WHERE `date` != 'NULL' GROUP BY `num_month` ORDER BY `num_month`")
    print(content)
    plt_draw_bar(content, '月份分布', '月份', '信息条数')    
 
def analysis_hour_count():
    content = sql_select("TIME_FORMAT(CONVERT(`time`, TIME), '%H') AS `num_hour`, COUNT(*) AS `count_hour`", "WHERE `time` != 'NULL' GROUP BY `num_hour` ORDER BY `num_hour`")
    print(content)
    plt_draw_bar(content, '时间分布', '小时', '信息条数')    
     
def analysis_province_count():
    content = sql_select("`province`, COUNT(*) AS `count_province`", "GROUP BY `province` ORDER BY `count_province` DESC")
    print(content)
    plt_draw_bar(content, '省份分布', '省份', '信息条数')
    
def analysis_city_count():
    content = sql_select("`city`, COUNT(*) AS `count_city`", "GROUP BY `city` ORDER BY `count_city` DESC")
    print(content)
    plt_draw_bar(content, '城市分布', '城市', '信息条数')    

def analysis_district_count():
    content = sql_select("`district`, COUNT(*) AS `count_district`", "WHERE `district` != 'NULL' GROUP BY `district` ORDER BY `count_district` DESC LIMIT 12")
    print(content)
    plt_draw_bar(content, '最多城区分布', '城区', '信息条数')    

def analysis_room_count():
    content = sql_select("`room`, COUNT(*) as `count_room`", "WHERE `room` != 'NULL' GROUP BY `room` ORDER BY `count_room` DESC LIMIT 6")
    print(content)
    plt_draw_bar(content, '房型分布', '房型', '信息条数')        
    
def analysis_floor_count():
    content = sql_select("LEFT(`floor`, 1) AS `height`, COUNT(*) AS `count_height`", "GROUP BY `height` ORDER BY `count_height` DESC LIMIT 3")
    print(content)
    plt_draw_bar(content, '楼层分布', '楼层', '信息条数')      
    
def analysis_direction_count():
    content = sql_select("`direction`, COUNT(*) as `count_direction`", "WHERE `direction` != 'NULL' GROUP BY `direction` ORDER BY `count_direction` DESC LIMIT 11")
    print(content)
    plt_draw_bar(content, '朝向分布', '朝向', '信息条数')    
    
def analysis_decoration_count():
    content = sql_select("`decoration`, COUNT(*) AS `count_decoration`", "WHERE `decoration` != 'NULL' GROUP BY `decoration` ORDER BY `count_decoration` DESC LIMIT 6")
    print(content)
    plt_draw_bar(content, '装修分布', '装修情况', '信息条数')    

def analysis_old_count():
    content = sql_select("ROUND(CONVERT(`old`, UNSIGNED)/5)*5 AS `num_old`, COUNT(*) AS `count_old`", "WHERE `old` != 'NULL' GROUP BY `num_old` HAVING `num_old` < 2025 AND `num_old` >1950 ORDER BY `num_old` DESC")
    print(content)
    plt_draw_bar(content, '房龄分布', '房龄', '信息条数')    
    
def analysis_money_num_divbyclass():
    content_0 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '出租房' HAVING `num_money` < 100000 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '写字楼出租房' HAVING `num_money` < 100000 ORDER BY RAND() LIMIT 1000")
    content_1 = np.array(content_1).flatten()
    print(content_1.shape[0])
    content_2 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '商铺出租房' HAVING `num_money` < 100000 ORDER BY RAND() LIMIT 1000")
    content_2 = np.array(content_2).flatten()
    print(content_2.shape[0])
    str_0, str_1, str_2 = '出租房', '写字楼出租房', '商铺出租房'
    plt_draw_1D_c3(content_0, content_1, content_2, str_0, str_1, str_2, '房屋租金-类型', '租金区间')
    #单独为出租房拉一下数据，缩小范围
    content_0 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/100)*100 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '出租房' HAVING `num_money` < 15000 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])    
    plt_draw_1D_s(content_0, '房屋租金-出租房', '租金区间')

def analysis_money_num_divbyfloor():
    content_0 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND LEFT(`floor`, 1) = '高' HAVING `num_money` < 50000 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND LEFT(`floor`, 1) = '中' HAVING `num_money` < 50000 ORDER BY RAND() LIMIT 1000")
    content_1 = np.array(content_1).flatten()
    print(content_1.shape[0])
    content_2 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND LEFT(`floor`, 1) = '低' HAVING `num_money` < 50000 ORDER BY RAND() LIMIT 1000")
    content_2 = np.array(content_2).flatten()
    print(content_2.shape[0])
    str_0, str_1, str_2 = '高', '中', '低'
    plt_draw_1D_c3(content_0, content_1, content_2, str_0, str_1, str_2, '房屋租金-楼层', '租金区间')
    #单独为出租房拉一下数据，缩小范围
    content_0 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '高' HAVING `num_money` < 10000 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '中' HAVING `num_money` < 10000 ORDER BY RAND() LIMIT 1000")
    content_1 = np.array(content_1).flatten()
    print(content_1.shape[0])
    content_2 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/1000)*1000 AS `num_money`", "WHERE `money` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '低' HAVING `num_money` < 10000 ORDER BY RAND() LIMIT 1000")
    content_2 = np.array(content_2).flatten()
    print(content_2.shape[0])
    str_0, str_1, str_2 = '高', '中', '低'
    plt_draw_1D_c3(content_0, content_1, content_2, str_0, str_1, str_2, '房屋租金-楼层-出租房', '租金区间')

def analysis_unitmoney_num_divbyfloor():
    #单独为出租房拉一下数据，缩小范围
    content_0 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/CONVERT(`area`, UNSIGNED)) AS `num_unitmoney`", "WHERE `money` != 'NULL' AND `area` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '高' AND CONVERT(`money`, UNSIGNED) < 50000 AND CONVERT(`area`, UNSIGNED) > 5 HAVING `num_unitmoney` < 200 ORDER BY RAND() LIMIT 5000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/CONVERT(`area`, UNSIGNED)) AS `num_unitmoney`", "WHERE `money` != 'NULL' AND `area` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '中' AND CONVERT(`money`, UNSIGNED) < 50000 AND CONVERT(`area`, UNSIGNED) > 5 HAVING `num_unitmoney` < 200 ORDER BY RAND() LIMIT 5000")
    content_1 = np.array(content_1).flatten()
    print(content_1.shape[0])
    content_2 = sql_select("ROUND(CONVERT(`money`, UNSIGNED)/CONVERT(`area`, UNSIGNED)) AS `num_unitmoney`", "WHERE `money` != 'NULL' AND `area` != 'NULL' AND `class` = '出租房' AND LEFT(`floor`, 1) = '低' AND CONVERT(`money`, UNSIGNED) < 50000 AND CONVERT(`area`, UNSIGNED) > 5 HAVING `num_unitmoney` < 200 ORDER BY RAND() LIMIT 5000")
    content_2 = np.array(content_2).flatten()
    print(content_2.shape[0])
    str_0, str_1, str_2 = '高', '中', '低'
    plt_draw_1D_c3(content_0, content_1, content_2, str_0, str_1, str_2, '租金单价-楼层-出租房', '单价区间')
    
def analysis_area_num_divbyclass():
    content_0 = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/10)*10 AS `num_area`", "WHERE `area` != 'NULL' AND `class` = '出租房' HAVING `num_area` < 1000 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    content_1 = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/10)*10 AS `num_area`", "WHERE `area` != 'NULL' AND `class` = '写字楼出租房' HAVING `num_area` < 1000 ORDER BY RAND() LIMIT 1000")
    content_1 = np.array(content_1).flatten()
    print(content_0.shape[0])
    content_2 = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/10)*10 AS `num_area`", "WHERE `area` != 'NULL' AND `class` = '商铺出租房' HAVING `num_area` < 1000 ORDER BY RAND() LIMIT 1000")
    content_2 = np.array(content_2).flatten()
    print(content_0.shape[0])
    str_0, str_1, str_2 = '出租房', '写字楼出租房', '商铺出租房'
    plt_draw_1D_c3(content_0, content_1, content_2, str_0, str_1, str_2, '房屋面积-类型', '面积区间')
    #单独为出租房拉一下数据，缩小范围
    content_0 = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/3)*3 AS `num_area`", "WHERE `area` != 'NULL' AND `class` = '出租房' HAVING `num_area` < 200 ORDER BY RAND() LIMIT 1000")
    content_0 = np.array(content_0).flatten()
    print(content_0.shape[0])
    plt_draw_1D_s(content_0, '房屋面积-出租房', '面积区间')

def analysis_money_area_num_divbyclass():
    for name_class in ("出租房", "写字楼出租房", "商铺出租房"):
        content = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/1)*1 AS `num_area`, ROUND(CONVERT(`money`, UNSIGNED)/100)*100 AS `num_money`", 
                             "WHERE `money` != 'NULL' AND `area` != 'NULL' AND `class` = '"+name_class+"' HAVING `num_area` < 200 AND `num_money` < 20000 ORDER BY RAND() LIMIT 1000")
        content = [[int(content[i][0]), int(content[i][1])] for i in range(len(content))]
        content = np.array(content)
        print(content.shape[0])
        print(content)
        plt_draw_2D_s(content, '租金和面积关系-'+name_class, '面积', '租金')

def analysis_money_area_num_divbyclass_divbydistrict():
    for name_class in ("出租房", "写字楼出租房", "商铺出租房"):
        list_district = sql_select("`district`, COUNT(*) AS `count_district`", "WHERE `class`='"+name_class+"' AND `money`!='NULL' AND `area`!='NULL' AND `floor`!='NULL' GROUP BY `province`, `district` ORDER BY `count_district` DESC LIMIT 12");
        list_district= np.array(list_district)
        list_district = list_district[:, 0]
        for name_district in list_district:
            content = sql_select("ROUND(CONVERT(`area`, UNSIGNED)/1)*1 AS `num_area`, ROUND(CONVERT(`money`, UNSIGNED)/100)*100 AS `num_money`", 
                                 "WHERE `money`!='NULL' AND `area`!='NULL' AND `class`='"+name_class+"' AND `district`='"+name_district+"' HAVING `num_area`<200 AND `num_money`<20000 ORDER BY RAND() LIMIT 1000")
            content = [[int(content[i][0]), int(content[i][1])] for i in range(len(content))]
            content = np.array(content)
            print(content.shape[0])
            plt_draw_2D_s(content, '租金和面积关系-'+name_class+'-'+name_district, '面积', '租金')

def analysis_unitmoney_divbyclass_divbydistrict():
    for name_class in ("出租房", "写字楼出租房", "商铺出租房"):
        list_district = sql_select("`district`, COUNT(*) AS `count_district`", "WHERE `class`='"+name_class+"' AND `money`!='NULL' AND `area`!='NULL' AND `floor`!='NULL' GROUP BY `province`, `district` ORDER BY `count_district` DESC LIMIT 12");
        list_district= np.array(list_district)
        list_district = list_district[:, 0]
        #拼接list字符串
        str_list_district = "("
        for district in list_district:
            str_list_district += "'"+district+"',"
        str_list_district = str_list_district[:-1]+")"
        #print(str_list_district)
        content = sql_select("`district`, (CONVERT(`money`, UNSIGNED)/CONVERT(`area`, UNSIGNED)) AS `num_unitmoney`", "WHERE `money` != 'NULL' AND `area` != 'NULL' AND `class` = '"+name_class+"' AND `district` IN "+str_list_district+" AND CONVERT(`money`, UNSIGNED) < 50000 AND CONVERT(`area`, UNSIGNED) > 5 HAVING `num_unitmoney` < 500 ORDER BY RAND() LIMIT 5000")
        content = np.array(content)
        print(content.shape[0])
        for i in range(len(content)):
            content[i][1] = float(content[i][1])
        #print(content)
        plt_draw_box(content, '租金单价和区域关系-'+name_class, '区域', '单价')    

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
    if False:
        analysis_company_count()
        analysis_class_count()
        analysis_province_count()
        analysis_city_count()
        analysis_district_count()
        analysis_room_count()
        analysis_floor_count()
        analysis_direction_count()
        analysis_decoration_count()
        analysis_old_count()
    if False:
        analysis_month_count()
        analysis_hour_count()
    if False:
        analysis_money_num_divbyclass()
        analysis_area_num_divbyclass()
        analysis_money_num_divbyfloor()
        analysis_unitmoney_num_divbyfloor()
    if False:
        analysis_money_area_num_divbyclass()
        analysis_money_area_num_divbyclass_divbydistrict()
    if True:
        #analysis_money_area_num_divbyclass()
        analysis_unitmoney_divbyclass_divbydistrict()
