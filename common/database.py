#-*- coding:utf-8 -*-
#author:yupeng
'''
python连接数据库，必要时使用数据库取数据作为测试数据，或做断言验证
'''
import pymysql


class MysqlTest():
    def __init__(self):
        '''数据库连接信息'''
        self.connection = pymysql.connect(
            host='172.16.2.153',
            port='3306',
            user='admin',
            password='admin@admin.com',
            database='haohuan_db_dev',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor   #select出的结果是以dict格式输出的，不设置的话默认为tuple格式
        )
        #创建数据库游标
        self.cursor = self.connection.cursor()

    def select_sql(self,sql):
        '''执行sql'''
        try:
            self.cursor.execute(sql)
            #self.connection.commit()#提交到数据库中执行   （select语句貌似不需要提交就可以执行）
            result=self.cursor.fetchone()  #fetchall()取所有值返回的是一个list嵌套字典，fetchone()取一个值，返回一个字典
            return result
        except:
            return "Error: sql execution failure"
        finally:
            #关闭数据库
            self.connection.close()

    def execute_sql(self,sql):
        '''执行sql'''
        try:
            self.cursor.execute(sql)
            self.connection.commit()#提交到数据库中执行
            return 'sql执行成功'
        except:
            self.connection.rollback()  #发生错误是回滚
            return "Error: sql execution failure"
        finally:
            #关闭数据库
            self.connection.close()