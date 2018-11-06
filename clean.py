#coding: utf-8

import os
import shutil

PATH_SOURCE = "E:\BigData\Source"
PATH_WORK = "E:\BigData\Work"
FOLDER_ORIGINAL = "ORG"
FOLDER_CLEAN = "CLN"
listCompany = []

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
                for line in fS.readlines():
                    items = line.split('\t')
                    if len(items)>=2:
                        if items[1] not in listCompany:
                            listCompany.append(items[1])
                        with open(PATH_WORK+os.sep+folder+os.sep+FOLDER_ORIGINAL+os.sep+items[1]+".csv", "a+", encoding='UTF-8') as fW:
                            fW.write(line)
    print(listCompany)

# --MAIN--    
if __name__ == "__main__":
    classifyByCompany()    