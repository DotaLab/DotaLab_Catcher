#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'
__date__ = '$2018-7-23$'

import psycopg2
from Config import DatabaseConfig


class Database:
    def __init__(self):
        # 初始化配置信息
        self.DBConfig = DatabaseConfig()
        try:
            # 获取连接
            conn = conn = psycopg2.connect( database=self.DBConfig.database(), user=self.DBConfig.user(), password=self.DBConfig.password(), host=self.DBConfig.host(), port=self.DBConfig.port())
            cur = conn.cursor()
            # 读取SQL语句
            with open(self.DBConfig.init_tables_path(), 'r+') as f:
                init_table_sql = f.read()
            # 执行数据库表初始化
            cur.execute(init_table_sql)
        except Exception as e:
            print(e)
        else:
            # 关闭连接
            cur.close()
            conn.commit()
            conn.close()
            print("Init tables success.")
        return
        
        
    def insert(self, sql):
        try:
            # 获取连接
            conn = conn = psycopg2.connect( database=self.DBConfig.database(), user=self.DBConfig.user(), password=self.DBConfig.password(), host=self.DBConfig.host(), port=self.DBConfig.port())
            cur = conn.cursor()
            # 执行数据库插入语句
            cur.execute(sql)
        except Exception as e:
            print(e)
        else:
            # 关闭连接
            cur.close()
            conn.commit()
            conn.close()
            print("Insert data success.")
        return


    def execute(self, sql):
        try:
            # 获取连接
            conn = conn = psycopg2.connect( database=self.DBConfig.database(), user=self.DBConfig.user(), password=self.DBConfig.password(), host=self.DBConfig.host(), port=self.DBConfig.port())
            cur = conn.cursor()
            # 执行数据库插入语句
            cur.execute(sql)
        except Exception as e:
            print(e)
        else:
            # 关闭连接
            cur.close()
            conn.commit()
            conn.close()
            print("Execute SQL success.")
        return


    def select(self, sql):
        try:
            # 获取连接
            conn = conn = psycopg2.connect( database=self.DBConfig.database(), user=self.DBConfig.user(), password=self.DBConfig.password(), host=self.DBConfig.host(), port=self.DBConfig.port())
            cur = conn.cursor()
            # 执行数据库查询语句
            cur.execute(sql)
            # 获取结果
            res = cur.fetchall()
        except Exception as e:
            print(e)
            return None
        else:
            # 关闭连接
            cur.close()
            conn.commit()
            conn.close()
            print("Select data success.")
            return res


    def selectCount(self, sql):
        # res = []
        try:
            # 获取连接
            conn = conn = psycopg2.connect( database=self.DBConfig.database(), user=self.DBConfig.user(), password=self.DBConfig.password(), host=self.DBConfig.host(), port=self.DBConfig.port())
            cur = conn.cursor()
            # 执行数据库查询语句
            cur.execute(sql)
            # 获取结果
            res = cur.fetchone()
        except Exception as e:
            print(e)
            return None
        else:
            # 关闭连接
            cur.close()
            conn.commit()
            conn.close()
            print("Select count success.")
            return res[0]


    def insertJsonData(self, json_data, table_name):
        # 组构SQL语句
        sql = "INSERT INTO "+ table_name +" ("

        key_str = ''
        value_str = ''

        # 依次将key组合进语句
        for i in json_data.keys():
            key_str = key_str + i + ','

        # 依次将value组合进语句
        for i in json_data.values():
            if i is None:
                value = "null"
            else:
                value = i

            if isinstance(value, list):
                # 处理json格式数据
                value = "{ " + str(value).replace("'", "\"") + " }"
            else:
                # 处理文本中包含的单引号问题
                value = str(value).replace("'", "''")

            if i is None:
                value_str = value_str + value + ','
            else:
                value_str = value_str + '\'' + value + '\','
        sql = sql + key_str[:-1] + ') VALUES(' + value_str[:-1] + ');\n'
        self.insert(sql)
        # print(sql)
        return


    def updateJsonData(self, json_data, con_data, table_name):
        # 组构SQL语句
        sql = "UPDATE "+ table_name + " SET "
        con_str = ' '
        for i in json_data:
            if json_data[i] is None:
                value = "null"
                con_str = con_str + str(i) + " = " + value + ", "
            else:
                value = json_data[i]
                if isinstance(i, list):
                    # 处理json格式数据
                    value = "{ " + str(value).replace("'", "\"") + " }"
                else:
                    # 处理文本中包含的单引号问题
                    value = str(value).replace("'", "''")

                con_str = con_str + str(i) + " = '" + value + "', "

        sql = sql + con_str[:-2]

        con_str = ' '
        # 处理条件
        for i in con_data:
            if con_data[i] is None:
                value = "null"
                con_str = con_str + str(i) + " = " + value + "AND "
            else:
                value = con_data[i]
                if isinstance(i, list):
                    # 处理json格式数据
                    value = "{ " + str(value).replace("'", "\"") + " }"
                else:
                    # 处理文本中包含的单引号问题
                    value = str(value).replace("'", "''")
                con_str = con_str + str(i) + " = '" + value + "'AND "
        sql = sql + " WHERE " + con_str[:-4] + ';\n'
        self.execute(sql)
        # print(sql)
        return


    def selectJsonData(self, key_data, table_name):
        # 组构SQL语句
        key = ""
        for i in key_data:
            key = key + i + ","
        sql = "SELECT " + key[:-1] + " FROM " + table_name
        return self.select(sql)


    def selectJsonDataCount(self, json_data, table_name):
        # 组构SQL语句
        sql = "SELECT COUNT(*) FROM "+ table_name + " WHERE "
        con_str = ' '
        for i in json_data:
            if json_data[i] is None:
                value = "null"
            else:
                value = json_data[i]
            
            if isinstance(i, list):
                # 处理json格式数据
                value = "{ " + str(value).replace("'", "\"") + " }"
            else:
                # 处理文本中包含的单引号问题
                value = str(value).replace("'", "''")
            
            if json_data[i] is None:
                con_str = con_str + str(i) + " = " + value + " AND "
            else:
                con_str = con_str + str(i) + " = '" + value + "' AND "
            
        sql = sql + con_str[:-4] + ';\n'
        return self.selectCount(sql)


    def deleteJsonData(self, json_data, table_name):
        # 组构SQL语句
        sql = "DELETE FROM "+ table_name + " WHERE "
        con_str = ' '
        for i in json_data:
            # 处理文本中包含的单引号问题
            value_str = str(json_data[i]).replace("'", "''")
            con_str = con_str + str(i) + " = '" + value_str + "' AND "
        sql = sql + con_str[:-4] + ';\n'
        self.execute(sql)
        return 

    # def checkExist(self, resList):
    #     # 创建一个Cursor:
    #     cursor = self.conn.cursor()

    #     # 组合查询语句，查询符合条件的结果数量
    #     checkExistSQL = "SELECT COUNT(*) FROM " + self.TABLE + " WHERE "
    #     for index, field in enumerate(self.XPATH):
    #         checkExistSQL += field + " = \"" + resList[index] + "\""
    #         if index != len(self.XPATH) - 1:
    #             checkExistSQL += " AND "

    #     # 执行查询，返回满足条件的数量
    #     cursor.execute(checkExistSQL)

    #     # 获取结果
    #     c = cursor.fetchone()[0]

    #     # 当数量为0时表示未被记录，使用flag标记结果
    #     if c == 0:
    #         print("未查询到，开始插入数据。")
    #         flag = False
    #     else:
    #         print("查询到，跳过。")
    #         flag = True

    #     # 关闭cursor
    #     cursor.close()

    #     return flag

    # def insertData(self, resList):
    #     # 创建一个Cursor:
    #     cursor = self.conn.cursor()

    #     # 组合插入语句
    #     insertDataSQL = "INSERT INTO " + self.TABLE + "( "

    #     # 遍历设置中的XPATH，获取field字段
    #     for index, field in enumerate(self.XPATH):
    #         insertDataSQL += field
    #         if index != len(self.XPATH) - 1:
    #             insertDataSQL += " , "
    #     insertDataSQL += " ) VALUES ( "

    #     # 遍历得到的结果，组合进入语句
    #     for index, field in enumerate(resList):
    #         insertDataSQL += "\'" + field + "\'"
    #         if index != len(self.XPATH) - 1:
    #             insertDataSQL += " , "
    #     insertDataSQL += " )"
    #     print(insertDataSQL)

    #     # 执行插入语句，插入信息
    #     cursor.execute(insertDataSQL)

    #     # 提交事务，保存改动
    #     self.conn.commit()

    #     # 关闭cursor
    #     cursor.close()
    #     return

    # def closeConnection(self):
    #     # 关闭连接
    #     self.conn.close()
    #     return


def main():

    return


if __name__ == '__main__':
    main()
