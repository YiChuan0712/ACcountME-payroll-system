import pymysql
"""
step 1
    判断是否是 周五
    如果是周五
    list：上周五到本周四
    搜employee info 找到所有 是hour的员工 列个表 加上那几项信息
    
    逐个员工搜索
        搜timecard 时间在上周五到本周四之内
        每天算时间 超过8小时 超过部分乘1.5
        
    存
    
step 2
    判断是否是 某个月的最后一个工作日
    如果是
    list 上个月的最后一个工作日到今天的前一天 
    
    搜employee info 找到所有 是salary的员工 列个表 加上那几项信息
    逐个员工搜索
        搜timecard 时间在之内
    
    搜employee info 找到所有 是salary的员工 列个表 加上那几项信息
    逐个员工搜索
        搜timecard 时间在之内
    
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import pandas as pd

def bank_interface(info, money):
    """
    内有判断：是否需要访问银行接口（是否是汇款员工）
    然后连接银行接口并获取返回值并返回
    """
    return True

def cut(num, c):
    str_num = str(num)
    return float(str_num[:str_num.index('.') + 1 + c])

def Friday():
    # 获取上周一日期
    lastFri = (datetime.today() - timedelta(days=11)).strftime('%Y%m%d')
    print("lastFri = " + lastFri)
    # 获取上周日日期
    thisThu = (datetime.today() - timedelta(days=5)).strftime('%Y%m%d')
    print("thisThu = " + thisThu)

    # 查hour员工
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select employee_ID, hourly_rate, standard_tax_deductions, 401k_deduction, medical_deduction " + \
          "from employee_info where employee_type  = 'hour' "
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    print(value)
    cur.close()
    con.close()
    """
        employee_ID, hourly_rate, standard_tax_deductions, 401k_deduction, medical_deduction
    """
    # 一个员工一个员工看
    for i in range(len(value)):
        employee_ID = value[i][0]
        hourly_rate = value[i][1]
        standard_tax_deductions = value[i][2]
        the401k_deduction = value[i][3]
        medical_deduction = value[i][4]

        begindate = employee_ID + lastFri
        enddate = employee_ID + thisThu

        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select work_hour " + \
              "from timecards where employee_ID_date  >= '" + begindate + "' and " + \
              "employee_ID_date  <= '" + enddate + "' and " + \
              " charge_number not like 'V%' "

        print(sql)
        print()
        cur.execute(sql)
        workhourvalue = cur.fetchall()
        print(workhourvalue)
        cur.close()
        con.close()

        money = 0.000
        # 一个timecard 一个timecard看
        for j in range(len(workhourvalue)):
            hour = workhourvalue[j][0]
            if hour > 8:
                hour = 8 + (hour - 8) * 1.5
            print(hour)
            money += hour * hourly_rate
            print(money)

        salary = cut(money, 2)
        tax = cut(money * standard_tax_deductions, 2)
        the401k = cut(money * the401k_deduction, 2)
        medical = cut(money * medical_deduction, 2)
        getpaid = cut(float(salary) - float(tax) - float(the401k) - float(medical), 2)

        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "INSERT INTO `payroll`" + \
              "(`employee_ID_begin_end`, `enddate`, `salary`, `tax`, `commission`, `the401k`, `medical`, `getpaid`) " + \
              "VALUES ('" + (employee_ID + lastFri + thisThu) + "','" + (datetime.today()).strftime('%Y%m%d') + "" + \
              "'," + str(salary) + "," + str(tax) + "," + "0" + "," + str(the401k) + "," + str(medical) + "," + str(
            getpaid) + ")"
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        # """
        #     银行接口
        # """
        # con = pymysql.Connect(
        #     host='XX.XXX.XXX.XX',
        #     port=XXXX,
        #     user='XXX',
        #     passwd='XXXXXXXXXX',
        #     db='XXX'
        # )
        #
        # cur = con.cursor()
        # sql = "select payment_method, bank_name, account_number " + \
        #       "from employee_info where employee_ID = '" + employee_ID + "' "
        #
        # print(sql)
        # print()
        # cur.execute(sql)
        # tvalue = cur.fetchall()
        # # print("银行接口")
        # # print(tvalue)
        # cur.close()
        # con.close()
        # if bank_interface(tvalue, getpaid):
        #     pass
        # else:
        #     return "Bank System Unavailable"



def Friday_delete():
    # 获取上周一日期
    lastFri = (datetime.today() - timedelta(days=11)).strftime('%Y%m%d')
    print("lastFri = " + lastFri)
    # 获取上周日日期
    thisThu = (datetime.today() - timedelta(days=5)).strftime('%Y%m%d')
    print("thisThu = " + thisThu)

    # 查hour员工
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select employee_ID " + \
          "from employee_info where employee_type  = 'hour' and state = 'quit' "
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    print(value)
    cur.close()
    con.close()
    """
        employee_ID
    """
    # 一个员工一个员工看
    for i in range(len(value)):
        employee_ID = value[i][0]
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "DELETE FROM `employee_info` WHERE employee_ID = '" + employee_ID + "'"
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "DELETE FROM `user_info` WHERE employee_ID = '" + employee_ID + "'"
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

def last_workday_salaried(nowDate):

    this_month = date.today()
    last_month = date.today() - relativedelta(months=1)
    first_day = (date(last_month.year, last_month.month, 1)).strftime('%Y%m%d')
    last_day = (date(this_month.year, this_month.month, 1) - relativedelta(days=1)).strftime('%Y%m%d')

    print(first_day)
    print(last_day)

    #nowDate = (datetime.today()).strftime('%Y%m%d')
    beginDate = (datetime.today()).strftime('%Y') + "0101"
    endDate = (datetime.today()).strftime('%Y') + "1231"

    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate, freq='BM'))]
    print(date_l)

    if nowDate in date_l:

        # 查salaried员工
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select employee_ID, salary, standard_tax_deductions, 401k_deduction, medical_deduction " + \
              "from employee_info where employee_type  = 'salaried' "
        print(sql)
        print()
        cur.execute(sql)
        value = cur.fetchall()
        print(value)
        cur.close()
        con.close()

        # employee_ID, salary, standard_tax_deductions, 401k_deduction, medical_deduction

        # 一个员工一个员工看
        for i in range(len(value)):
            employee_ID = value[i][0]
            print(employee_ID)
            rawsalary = value[i][1]
            standard_tax_deductions = value[i][2]
            the401k_deduction = value[i][3]
            medical_deduction = value[i][4]

            money = rawsalary

            salary = cut(money, 2)
            tax = cut(money * standard_tax_deductions, 2)
            the401k = cut(money * the401k_deduction, 2)
            medical = cut(money * medical_deduction, 2)
            getpaid = cut(float(salary) - float(tax) - float(the401k) - float(medical), 2)

            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "INSERT INTO `payroll`" + \
                  "(`employee_ID_begin_end`, `enddate`, `salary`, `tax`, `commission`, `the401k`, `medical`, `getpaid`) " + \
                  "VALUES ('" + (employee_ID + first_day + last_day) + "','" + nowDate + "" + \
                  "'," + str(salary) + "," + str(tax) + "," + "0" + "," + str(the401k) + "," + str(medical) + "," + str(
                getpaid) + ")"
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

            # """
            #     银行接口
            # """
            # con = pymysql.Connect(
            #     host='XX.XXX.XXX.XX',
            #     port=XXXX,
            #     user='XXX',
            #     passwd='XXXXXXXXXX',
            #     db='XXX'
            # )
            #
            # cur = con.cursor()
            # sql = "select payment_method, bank_name, account_number " + \
            #       "from employee_info where employee_ID = '" + employee_ID + "' "
            #
            # print(sql)
            # print()
            # cur.execute(sql)
            # tvalue = cur.fetchall()
            # # print("银行接口")
            # # print(tvalue)
            # cur.close()
            # con.close()
            # if bank_interface(tvalue, getpaid):
            #     pass
            # else:
            #     return "Bank System Unavailable"

def last_workday_commissioned(nowDate):

    this_month = datetime.strptime(nowDate,'%Y%m%d')
    last_month = datetime.strptime(nowDate,'%Y%m%d') - relativedelta(months=1)
    first_day = (date(last_month.year, last_month.month, 1)).strftime('%Y%m%d')
    last_day = (date(this_month.year, this_month.month, 1) - relativedelta(days=1)).strftime('%Y%m%d')

    print(first_day)
    print(last_day)

    #nowDate = (datetime.today()).strftime('%Y%m%d')
    beginDate = (datetime.today()).strftime('%Y') + "0101"
    endDate = (datetime.today()).strftime('%Y') + "1231"

    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate, freq='BM'))]
    print(date_l)

    if nowDate in date_l:

        # 查commissioned员工
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select employee_ID, salary, standard_tax_deductions, 401k_deduction, medical_deduction, commission_rate " + \
              "from employee_info where employee_type  = 'commissioned' "
        print(sql)
        print()
        cur.execute(sql)
        value = cur.fetchall()
        print(value)
        cur.close()
        con.close()

        # employee_ID, salary, standard_tax_deductions, 401k_deduction, medical_deduction, commissioned_rate

        # 一个员工一个员工看
        for i in range(len(value)):
            employee_ID = value[i][0]
            print(employee_ID)
            rawsalary = value[i][1]
            standard_tax_deductions = value[i][2]
            the401k_deduction = value[i][3]
            medical_deduction = value[i][4]
            commission_rate = value[i][5]
            print(commission_rate)

            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select sale " + \
                  "from purchase_orders where date  >= '" + first_day + "' and " + \
                  "date  <= '" + last_day + "' and " + \
                  " employee_ID = '" + employee_ID + "'"

            print(sql)
            print()
            cur.execute(sql)
            salevalue = cur.fetchall()
            print(salevalue)
            cur.close()
            con.close()

            commission_money = 0.00
            # 一个order 一个order看
            for j in range(len(salevalue)):
                temp = salevalue[j][0]
                commission_money += temp
                print(commission_money)

            commission_money = cut(commission_money*commission_rate,2)
            print(commission_money)
            money = rawsalary + commission_money
            print(money)


            salary = cut(money, 2)
            tax = cut(money * standard_tax_deductions, 2)
            the401k = cut(money * the401k_deduction, 2)
            medical = cut(money * medical_deduction, 2)
            getpaid = cut(float(salary) - float(tax) - float(the401k) - float(medical), 2)

            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "INSERT INTO `payroll`" + \
                  "(`employee_ID_begin_end`, `enddate`, `salary`, `tax`, `commission`, `the401k`, `medical`, `getpaid`) " + \
                  "VALUES ('" + (employee_ID + first_day + last_day) + "','" + nowDate + "" + \
                  "'," + str(salary) + "," + str(tax) + "," + str(commission_money) + "," + str(the401k) + "," + str(medical) + "," + str(
                getpaid) + ")"
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

            # """
            #     银行接口
            # """
            # con = pymysql.Connect(
            #     host='XX.XXX.XXX.XX',
            #     port=XXXX,
            #     user='XXX',
            #     passwd='XXXXXXXXXX',
            #     db='XXX'
            # )
            #
            # cur = con.cursor()
            # sql = "select payment_method, bank_name, account_number " + \
            #       "from employee_info where employee_ID = '" + employee_ID + "' "
            #
            # print(sql)
            # print()
            # cur.execute(sql)
            # tvalue = cur.fetchall()
            # # print("银行接口")
            # # print(tvalue)
            # cur.close()
            # con.close()
            # if bank_interface(tvalue, getpaid):
            #     pass
            # else:
            #     return "Bank System Unavailable"

def last_workday_delete(nowDate):

    this_month = datetime.strptime(nowDate, '%Y%m%d')
    last_month = datetime.strptime(nowDate, '%Y%m%d') - relativedelta(months=1)
    first_day = (date(last_month.year, last_month.month, 1)).strftime('%Y%m%d')
    last_day = (date(this_month.year, this_month.month, 1) - relativedelta(days=1)).strftime('%Y%m%d')

    print(first_day)
    print(last_day)

    # nowDate = (datetime.today()).strftime('%Y%m%d')
    beginDate = (datetime.today()).strftime('%Y') + "0101"
    endDate = (datetime.today()).strftime('%Y') + "1231"

    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate, freq='BM'))]
    print(date_l)

    if nowDate in date_l:
        # 查 commissioned 或 salaried 员工
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select employee_ID " + \
              "from employee_info where employee_type != 'hour' and employee_type != 'PA' and state = 'quit' "
        print(sql)
        print()
        cur.execute(sql)
        value = cur.fetchall()
        print(value)
        cur.close()
        con.close()

        # employee_ID
        # 一个员工一个员工看
        for i in range(len(value)):
            employee_ID = value[i][0]
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "DELETE FROM `employee_info` WHERE employee_ID = '" + employee_ID + "'"
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "DELETE FROM `user_info` WHERE employee_ID = '" + employee_ID + "'"
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

def Monday_card():
    # 查hour员工
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select employee_ID " + \
          "from employee_info where employee_type  = 'hour'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    print(value)
    cur.close()
    con.close()
    """
        employee_ID
    """
    # 一个员工一个员工看
    for i in range(len(value)):
        employee_ID = value[i][0]
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `card_submit`='no' WHERE employee_ID = '" + employee_ID + "'"
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

def first_workday_card(nowDate):

    print(nowDate[6:])
    if nowDate[6:] == '01':
        # 查 commissioned 或 salaried 员工
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select employee_ID " + \
              "from employee_info where employee_type != 'hour' and employee_type != 'PA'"
        print(sql)
        print()
        cur.execute(sql)
        value = cur.fetchall()
        print(value)
        cur.close()
        con.close()

        # 一个员工一个员工看
        for i in range(len(value)):
            employee_ID = value[i][0]
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "UPDATE `employee_info` SET `card_submit`='no' WHERE employee_ID = '" + employee_ID + "'"
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

def runpayroll():
    #"""
    # 获取今天是星期几
    dayOfWeek = datetime.today().weekday() + 1

    # 获取今天的日期
    datetoday = datetime.today().strftime('%Y%m%d')

    # part 1 结算
    # 如果今天是星期五
    if dayOfWeek == 5:
        Friday()

    last_workday_salaried(datetoday)
    last_workday_commissioned(datetoday)

    # part 2 删除员工
    # 如果今天是星期五
    if dayOfWeek == 5:
        Friday_delete()

    last_workday_delete(datetoday)

    # part 3 time card flag
    if dayOfWeek == 1:
        Monday_card()
    first_workday_card(datetoday)
    #"""


# last_workday_salaried('20210930')
# last_workday_commissioned('20210930')

# runpayroll()

# last_workday_salaried("20210129")
#"""
Friday_delete()
# tlast_workday_delete('20210129')
#"""









