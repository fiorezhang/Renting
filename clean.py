#coding: utf-8

import os
import shutil

PATH_SOURCE = "E:\BigData\Source"
PATH_WORK = "E:\BigData\Work"
FOLDER_ORIGINAL = "ORG"
FOLDER_CLEAN = "CLN"
listCompany = ['58同城', '爱上租', '赶集网', '365淘房', '嗨住租房', '安居客', '青客公寓', '链家', '房天下', '蛋壳公寓', '优客', '107间', '依依短租', '魔方生活', '诸葛找房', '平安好房', '透明家', '楼盘网', '爱屋吉屋', '城市房产', '房产超市', '透明房产网']

#TODO： log重定向
#TODO: 该提取的还是提取出来，不合理的部分到时候可以列出来。

#创建新目录
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    #print(isExists)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False     

#删除目录
def rmdir(path):
    shutil.rmtree(path)

#按公司名把原始数据拆分，因为不同公司的数据格式略有不同
def classifyByCompany():
    for fileSource in os.listdir(PATH_SOURCE):
        print(fileSource)
        folder = os.path.splitext(fileSource)[0]
        if mkdir(PATH_WORK+os.sep+folder): #工作目录下为每一个原始数据建立一个同名目录
            #TODO: 应加入出错监测机制，如果出错则删掉当前目录
            mkdir(PATH_WORK+os.sep+folder+os.sep+FOLDER_ORIGINAL) #该同名目录下，建立一个子目录，存放按公司名分类的原始数据
            mkdir(PATH_WORK+os.sep+folder+os.sep+FOLDER_CLEAN) #该同名目录下，建立一个子目录，存放按公司名分类的清洗后数据（只建立目录，不在本函数内清洗）
            with open(PATH_SOURCE+os.sep+fileSource, "r", encoding='UTF-8') as fS:
                lines = ""
                companyLast = None
                for line in fS.readlines():
                    items = line.split('\t', 2)
                    if len(items)>=2:
                        #公司名在第二列
                        company = items[1]
                        #如果公司名没有在名单里，更新名单（主要是方便统计）
                        if company not in listCompany:
                            listCompany.append(company)
                        #如果当前行和上一行是一个公司，把当前行的内容加入缓存（lines）；如果换了一个公司，把前一个公司的缓存内容一次性写入，然后开始缓存当前公司内容
                        if company == companyLast:
                            lines += line
                        else:
                            if companyLast != None: #针对第一行，不写缓存，其它时候都要先写缓存
                                with open(PATH_WORK+os.sep+folder+os.sep+FOLDER_ORIGINAL+os.sep+companyLast+".txt", "a+", encoding='UTF-8') as fW:
                                    fW.write(lines)
                            #再从当前行内容开始更新缓存，更新记录的上一个公司名
                            lines = line
                            companyLast = company
                #退出行的遍历后，最后一次的缓存也要写入            
                with open(PATH_WORK+os.sep+folder+os.sep+FOLDER_ORIGINAL+os.sep+companyLast+".txt", "a+", encoding='UTF-8') as fW:
                    fW.write(lines)
    print(listCompany)

# --MAIN--    
if __name__ == "__main__":
    classifyByCompany()    