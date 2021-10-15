"""
    linktest.py 连通检测模块

    check_connection()

        该函数用于检查与服务器的连接状态

        有2种返回值

        返回'YES' 正常连接

        返回'NO' 连接失败
"""

import pymysql


def check_connection():

    try:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = 'select * from properties'
        print(sql)
        cur.execute(sql)
        value = cur.fetchall()
        cur.close()
        con.close()
        if value[0][0] == 1:
            return 'YES'

    except Exception:
        return 'NO'


# 测试
# print(check_connection())
