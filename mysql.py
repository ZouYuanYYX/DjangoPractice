# -*- coding:utf-8 -*-
# author 邹元
import pymysql

def connectMySql():
    #打开数据库连接
    return pymysql.connect(host="192.168.173.150",
                           user="dbadmin",
                           passwd="tms@db123",
                           db ="tms_test",
                           port=3306,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor
                           )

'''从数据库里查到用户userid'''
def getUserId(mobile):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    cursor.execute("select id,username from tms_test.`sys_user` where mobile = " + mobile)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result)
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result

def getStationId(name):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "SELECT id FROM tms_test.`base_organization` WHERE name = " +"\'"+name+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']

def getTydbId(tydId):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "SELECT id FROM tms_test.`consign_base` WHERE consign_no = " +"\'"+tydId+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']

def getThdbId(thdId):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "SELECT id FROM tms_test.`take_goods` WHERE take_goods_no = " +"\'"+thdId+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']

#获取分拨单记录的id
def getFbdbId(fbdId):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "SELECT id FROM tms_test.`separate_list` WHERE separate_number =" +"\'"+fbdId+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']

#获取配载单记录的id
def getPzdbId(pzdId):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "SELECT id FROM tms_test.`stowage` WHERE stowage_no = " +"\'"+pzdId+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']

#获取配送单记录的id
def getPsdbId(psdId):
    db = connectMySql()
    # 使用cursor（）方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行sql语句
    sql = "select id from tms_test.`deliver` where deliver_no = " +"\'"+psdId+"\'"
    print ("sql:"+sql)
    cursor.execute(sql)
    # 使用fetcgone()方法获取一条数据，cursor.fetchone()默认返回类型是tuple，连接数据库的时候，加上那句，就会返回dict类型
    result = cursor.fetchone()
    print (result['id'])
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result['id']
