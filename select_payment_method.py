"""
    select_payment_method.py 选择支付方式

    ① select_pick_up(employee_ID)

        返回YES则修改成功
        也可能返回Employee_Not_Found


    ② select_mail(employee_ID, paying_address)

    ③ select_direct_deposit(employee_ID, bank_name, account_number)


"""

import pymysql


def select_pick_up(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_ID=" + "'" + employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    #print(value)
    cur.close()
    con.close()

    if value:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `payment_method`= 'pick_up' WHERE `employee_ID`= " + "'" + employee_ID + "'"
        print(sql)
        print()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        return "YES"

    else:
        print("员工不存在")
        return "员工不存在！"


def select_mail(employee_ID, paying_address):

    if paying_address.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(paying_address) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'
    elif len(paying_address) > 50:
        print('address太长')
        return '地址过长！'


    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_ID=" + "'" + employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    #print(value)
    cur.close()
    con.close()

    if value:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `payment_method`= 'mail',`paying_address`= '" + paying_address +\
              "' WHERE `employee_ID`= " + "'" + employee_ID + "'"
        print(sql)
        print()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        return "YES"

    else:
        print("员工不存在")
        return "员工不存在！"

def select_direct_deposit(employee_ID, bank_name, account_number):

    if bank_name.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(bank_name) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'
    elif len(bank_name) > 50:
        print('bank_name太长')
        return '银行名称过长！'

    if account_number.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(account_number) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'
    elif len(account_number) > 50:
        print('account_number太长')
        return '银行账户过长！'

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_ID=" + "'" + employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    #print(value)
    cur.close()
    con.close()

    if value:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `payment_method`= 'direct_deposit',`bank_name`= '" + bank_name +\
              "',`account_number`= '" + account_number +\
              "' WHERE `employee_ID`= " + "'" + employee_ID + "'"
        print(sql)
        print()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        return "YES"

    else:
        print("员工不存在")
        return "员工不存在！"



# 测试
#print(select_mail('p', 'asdf'))
#print(select_pick_up(''))
# print(select_direct_deposit('000000999', 'a', 'a'))

