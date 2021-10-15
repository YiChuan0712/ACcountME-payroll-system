"""
    maintain_purchase_order.py 维护订单信息

    ① return_order_info(order_ID, employee_ID)
        该函数返回对应订单号的信息

        返回具体信息成功
        返回值格式：元组
                order_ID,
                employee_ID,
                customer_point_of_contact,
                customer_billing_address,
                products_purchased,
                sale,
                date_year,
                date_month,
                date_day

        也可能返回"订单不存在！"等信息


    ② return_employee_type(employee_ID)
        返回员工类型


    ③ create_order(...)

                输入employee_ID,
                customer_point_of_contact,
                customer_billing_address,
                products_purchased,
                sale,
                date_year, 如 2000
                date_month, 如 2 或 10
                date_day, 如 1 或 31

        成功创建 就返回 "SUCCESS_二十位订单号"


    ④ update_order(order_ID, employee_ID...)

        该函数用于修改订单信息
        new_employee_ID 是更新后的ID employee_ID是当前登录的ID
        返回YES成功
        也可能有其他返回值


    ④ delete_order(order_ID, employee_ID)

        该函数用于删除订单信息

        返回YES成功
        也可能有其他返回值


"""

import pymysql
from datetime import datetime


def isTrueDate(a):
    # 查询输入日期是否有效
    # 把年月日剥离出来
    year = int(a[0:4])
    month = int(a[4:6])
    day = int(a[6:])

    print(year)
    print(month)
    print(day)

    if year <= 0 or year > 9999:
        return False
    elif month <= 0 or month > 12:
        return False

    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31 or day < 1:
            return False
        else:
            return True

        # 四六九冬
    elif month == 4 or month == 6 or month == 9 or month == 11:
        if day > 30 or day < 1:
            return False
        else:
            return True
        # 平年二月二十八
    else:
        if year % 4 == 0 and year % 400 == 0:
            print('leap')
            if day > 29 or day < 1:
                return False
            else:
                return True

        elif year % 4 == 0 and year % 100 != 0:
            print('leap')
            if day > 29 or day < 1:
                return False
            else:
                return True
        else:
            print('common')
            if day > 28 or day < 1:
                return False
            else:
                return True


def check_money_interface(money):
    # 支付时，输入的金额可能是小数，也可能是整数
    s = str(money)
    if s == '0':
        return True
    if s.count('.') == 1:  # 判断小数点个数
        sl = s.split('.')  # 按照小数点进行分割
        left = sl[0]  # 小数点前面的
        right = sl[1]  # 小数点后面的
        print("in check_money_interface, right = '"+right+"'")
        count_right = 0
        for num in right:
            count_right += 1
        if count_right == 0:
            return True
        if 2 >= count_right > 0:  # 判断小数位数是否小于等于2
            if left.startswith('-') and left.count('-') == 1 and right.isdigit():
                lleft = left.split('-')[1]  # 按照-分割，然后取负号后面的数字
                if lleft.isdigit():
                    return False
            elif left.isdigit() and right.isdigit():
                # 判断是否为正小数
                return True
        else:
            return False
    elif s.isdigit():
        s = int(s)
        if s != 0:
            return True
    return False


def return_employee_type(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select * from employee_info where '+'employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()

    if value == ():
        print('employee_ID不存在')
        return '员工不存在！'

    if value[0][3] == 'commissioned':
        print('commissioned')
        return 'commissioned'
    elif value[0][3] == 'hour':
        print('hour')
        return 'hour'
    elif value[0][3] == 'salaried':
        print('salaried')
        return 'salaried'
    elif value[0][3] == 'PA':
        print('PA')
        return 'PA'

    print('return_employee_type未知错误')
    return 'return_employee_type_error'


def return_order_info(order_ID, employee_ID):
    if order_ID.isspace() or employee_ID.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(order_ID) == 0 or len(employee_ID) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif len(order_ID) > 50:
        print('order_ID太长')
        return '订单号过长！'

    elif len(employee_ID) > 50:
        print('employee_ID太长')
        return '员工号过长！'

        # Purchase Order Not Found
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select * from purchase_orders where ' + 'order_ID = ' + "'" + order_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()
    if value == ():
        print("订单不存在！")
        return "订单不存在！"

    # Invalid Access to a Purchase Order
    if value[0][1] != employee_ID:
        print("Invalid Access to a Purchase Order")
        return "您无权访问该订单！"


    returnvalue = (value[0][0],)
    returnvalue += (value[0][1],)
    returnvalue += (value[0][2],)
    returnvalue += (value[0][3],)
    returnvalue += (value[0][4],)
    returnvalue += (value[0][5],)
    temp = value[0][6]
    returnyear = int(temp[0:4])
    returnvalue += (returnyear,)
    returnmonth = int(temp[4:6])
    returnvalue += (returnmonth,)
    returnday = int(temp[6:8])
    returnvalue += (returnday,)

    return returnvalue


def create_order(
                     employee_ID,
                     customer_point_of_contact,
                     customer_billing_address,
                     products_purchased,
                     sale,
                     date_year,
                     date_month,
                     date_day
                 ):

    if employee_ID.isspace() or customer_point_of_contact.isspace() \
            or customer_billing_address.isspace() or products_purchased.isspace() \
            or sale.isspace() or date_year.isspace() or date_month.isspace() or date_day.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(employee_ID) == 0 or len(customer_point_of_contact) == 0 \
            or len(customer_billing_address) == 0 or len(products_purchased) == 0\
            or len(sale) == 0 or len(date_year) == 0\
            or len(date_month) == 0 or len(date_day) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif len(employee_ID) > 50:
        print('employee_ID太长')
        return '员工号过长！'
    elif len(customer_point_of_contact) > 50:
        print('customer_point_of_contact太长')
        return '客户联络地点过长！'
    elif len(customer_billing_address) > 50:
        print('customer_billing_address太长')
        return '客户账单地址过长！'
    elif len(products_purchased) > 50:
        print('products_purchased太长')
        return '购买产品过长！'

    elif len(sale) > 50:
        print('sale太长')
        return '订单金额过长！'
    elif len(date_year) > 50:
        print('date_year太长')
        return '年过长！'
    elif len(date_month) > 50:
        print('date_month太长')
        return '月过长！'
    elif len(date_day) > 50:
        print('date_day太长')
        return '日过长！'

    elif (date_year.isdigit() and date_month.isdigit() and date_day.isdigit()) == False:
        print("date is not digit!")
        return "无效的日期！"

    elif '.' in date_year or '.' in date_month or '.' in date_day == True:
        print("no dot!")
        return "无效的日期！"

    elif check_money_interface(sale) == False:
        print("sale format incorrect")
        return "无效的金额！"

    elif float(sale) < 0:
        print("sale < 0")
        return "无效的金额！"
    elif int(date_year) <= 0 or int(date_year) > 9999:
        print("date_year <= 0 or > 9999")
        return "无效的年！"
    elif int(date_month) <= 0 or int(date_month) > 12:
        print("date_month <= 0 or > 12")
        return "无效的月！"
    elif int(date_day) <= 0 or int(date_day) > 31:
        print("date_day <= 0 or > 31")
        return "无效的日！"

    elif isTrueDate((str(date_year).zfill(4) + str(date_month).zfill(2) + str(date_day).zfill(2))) == False:
        print((str(date_year).zfill(4) + str(date_month).zfill(2) + str(date_day).zfill(2)))
        print("invalid date")
        return "无效的日期！"

    # 生成 order ID
    today = datetime.today()
    order_ID = employee_ID + str(today.year).zfill(4) + \
               str(today.month).zfill(2) + \
               str(today.day).zfill(2) + \
               str(today.hour).zfill(2) + \
               str(today.minute).zfill(2) + \
               str(today.second).zfill(2)
    print(order_ID)

    # 生成 date
    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)
    print(date)
    # 算今天的日期
    datetoday = str(today.year).zfill(4) + \
               str(today.month).zfill(2) + \
               str(today.day).zfill(2)

    if (datetoday >= date):
        print("date必须晚于当前日期")
        return "新订单的结束日期必须晚于当前时间！"

    con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
    cur = con.cursor()
    sql = "INSERT INTO `purchase_orders`(`order_ID`, `employee_ID`, `customer_point_of_contact`, " +\
          "`customer_billing_address`, `products_purchased`, `sale`, `date`) VALUES " +\
          "('" + order_ID + "','" + employee_ID + "','" + customer_point_of_contact + "'," +\
          "'" + customer_billing_address + "','" + products_purchased + "'," + str(sale) + ",'" + date + "')"

    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    return "SUCCESS_" + order_ID


def update_order(
                     employee_ID,

                     order_ID,
                     new_employee_ID,
                     customer_point_of_contact,
                     customer_billing_address,
                     products_purchased,
                     sale,
                     date_year,
                     date_month,
                     date_day
                 ):
    if order_ID.isspace() or new_employee_ID.isspace() or customer_point_of_contact.isspace() \
            or customer_billing_address.isspace() or products_purchased.isspace() \
            or sale.isspace() or date_year.isspace() or date_month.isspace() or date_day.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(order_ID) == 0 or len(new_employee_ID) == 0 or len(customer_point_of_contact) == 0 \
            or len(customer_billing_address) == 0 or len(products_purchased) == 0\
            or len(sale) == 0 or len(date_year) == 0\
            or len(date_month) == 0 or len(date_day) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif len(order_ID) > 50:
        print('order_ID太长')
        return '订单号过长！'

    elif len(new_employee_ID) > 50:
        print('employee_ID太长')
        return '员工号过长！'
    elif len(customer_point_of_contact) > 50:
        print('customer_point_of_contact太长')
        return '客户联络地点过长！'
    elif len(customer_billing_address) > 50:
        print('customer_billing_address太长')
        return '客户账单地址过长！'
    elif len(products_purchased) > 50:
        print('products_purchased太长')
        return '购买产品过长！'


    elif len(sale) > 50:
        print('sale太长')
        return '订单金额过长！'
    elif len(date_year) > 50:
        print('date_year太长')
        return '年过长！'
    elif len(date_month) > 50:
        print('date_month太长')
        return '月过长！'
    elif len(date_day) > 50:
        print('date_day太长')
        return '日过长！'


    elif (date_year.isdigit() and date_month.isdigit() and date_day.isdigit()) == False:
        print("date is not digit!")
        return "无效的日期！"

    elif '.' in date_year or '.' in date_month or '.' in date_day == True:
        print("no dot!")
        return "无效的日期！"

    elif check_money_interface(sale) == False:
        print("sale format incorrect")
        return "无效的金额！"

    elif float(sale) < 0:
        print("sale < 0")
        return "无效的金额！"
    elif int(date_year) <= 0 or int(date_year) > 9999:
        print("date_year <= 0 or > 9999")
        return "无效的年！"
    elif int(date_month) <= 0 or int(date_month) > 12:
        print("date_month <= 0 or > 12")
        return "无效的月！"
    elif int(date_day) <= 0 or int(date_day) > 31:
        print("date_day <= 0 or > 31")
        return "无效的日！"
    elif isTrueDate((str(date_year).zfill(4) + str(date_month).zfill(2) + str(date_day).zfill(2))) == False:
        print("invalid date")
        return "无效的日期！"


    # employee exist check
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_type = 'commissioned' and employee_ID=" + "'" + new_employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    # print(value)
    cur.close()
    con.close()
    if value:
        pass
    else:
        return "员工不存在或员工权限不足！"


    # Purchase Order Not Found
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select * from purchase_orders where '+'order_ID = ' + "'" + order_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()
    if value == ():
        print("订单不存在！")
        return "订单不存在！"

    # Invalid Access to a Purchase Order
    if value[0][1] != employee_ID:
        print("Invalid Access to a Purchase Order")
        return "您无权访问该订单！"

    # Purchase Order is Closed
    today = datetime.today()
    # 算今天的日期
    datetoday = str(today.year).zfill(4) + \
               str(today.month).zfill(2) + \
               str(today.day).zfill(2)
    print(value[0][6])
    if datetoday >= value[0][6]:
        print("Purchase Order is Closed")
        return "订单已关闭！"

    # update
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)
    sql = "UPDATE `purchase_orders` " +\
          "SET `employee_ID`='" + new_employee_ID + "',`" +\
          "customer_point_of_contact`='" + customer_point_of_contact + "'," +\
          "`customer_billing_address`='" + customer_billing_address + "'," +\
          "`products_purchased`='" + products_purchased + "'," +\
          "`sale`=" + str(sale) + "," +\
          "`date`='" + date + "' " +\
          "WHERE `order_ID` = " + "'" + order_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    return "YES"


def delete_order(
                     order_ID,
                     employee_ID
                 ):

    if order_ID.isspace() or employee_ID.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(order_ID) == 0 or len(employee_ID) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif len(order_ID) > 50:
        print('order_ID太长')
        return '订单号过长！'

    elif len(employee_ID) > 50:
        print('employee_ID太长')
        return '员工号过长！'

    # Purchase Order Not Found
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select * from purchase_orders where '+'order_ID = ' + "'" + order_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()
    if value == ():
        print("订单不存在！")
        return "订单不存在！"

    # Invalid Access to a Purchase Order
    #eid = order_ID[0:6]
    if value[0][1] != employee_ID:
        print("Invalid Access to a Purchase Order")
        return "您无权访问该订单！"

    # Purchase Order is Closed
    today = datetime.today()
    # 算今天的日期
    datetoday = str(today.year).zfill(4) + \
               str(today.month).zfill(2) + \
               str(today.day).zfill(2)
    print(value[0][6])
    if datetoday >= value[0][6]:
        print("Purchase Order is Closed")
        return "订单已关闭！"

    # delete
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "DELETE FROM `purchase_orders` WHERE order_ID = " + "'" + order_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    return "YES"

# 测试
# print(check_commissioned('000003'))
# create_order('000002', '计算机楼', '日新楼', '日用品', '1000', '2022', '3', '29')
# print(update_order('000001', '00000120211002171134','000001', '计算机楼', '北苑一公寓', '普通键盘', '10.01', '2024', '2', '1'))
# print(return_order_info('00000120211002160502','000001'))
# print(delete_order('00000120211002160502','000001'))

