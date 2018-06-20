# -*- coding:utf-8 -*-
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

