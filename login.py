"""
    login.py 登录模块

    check_login(employeeid, password)

        该函数用于检查是否登录成功

        输入用户ID和密码 有5种返回值

        返回'Invalid_Name' 用户ID不存在 登录失败 -> 弹出提醒

        返回'Invalid_Password' 用户密码错误 登录失败 -> 弹出提醒

        返回'PA' 登录成功 权限为PA（管理） -> 进入PA界面

        返回'E' 登录成功 权限为E（普通用户） -> 进入E界面

        返回'check_login_error' 未知错误 理论上不会发生
"""

import pymysql


def check_login(employeeid, password):

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select * from user_info where '+'employee_ID = ' + "'" + employeeid + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()

    if value == ():
        print('employee_ID不存在')
        return '员工不存在！'

    if value[0][1] != password:
        print('password错误')
        return '密码错误！'

    if value[0][2] == 'PA':
        print('PA权限')
        return 'PA'

    if value[0][2] == 'E':
        print('E权限')
        return 'E'

    print('check_login未知错误')
    return 'check_login_error'


# 测试
"""
print(check_login('000001', 'zhangyichuan') + '\n')
print(check_login('000003', 'xiangfuxiong') + '\n')

print(check_login('000000', 'zhangyichuan') + '\n')
print(check_login('000001', '随便写') + '\n')

print(check_login('随便写', '随便写') + '\n')
print(check_login('', '') + '\n')

print(check_login('随便写', '') + '\n')
print(check_login('', '随便写') + '\n')

print(check_login('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', '') + '\n')
print(check_login('❀', '😊') + '\n')
#"""