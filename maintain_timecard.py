"""
    maintain_purchase_order.py 维护 timecard
    流程
    ① 判断员工类型 H, S, C
    ② 系统根据员工类型 把要填的时间段 拉出来
    ③ 每一天的timecard 都可以选charge number
    ④ timecard本地存储记录


    return_pay_period(employee_ID) 以元组格式返回 pay period

    return_charge_numbers(employee_ID) 以元组格式返回 charge number
    此函数还有两个版本
    一个只返回V return_Vonly
    另一个返回值去除了V return_charge_numbers_noV

    submit_timecard(...) 提交 time card
    return_card_submit(employee_ID) 返回 time_card (YES or NO)
    reverse_card_submit(employee_ID) 反转 time_card

    check_timecard 检测输入格式是否正确

    save_ONE_timecard 输入 员工ID 时间 charge number，工作时长
        将信息保存到本地 可以覆盖

    get_ONE_timecard 输入员工ID 时间 返回 （charge number，工作时长）




"""
import pymysql
import datetime
import calendar
import pandas as pd


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


def isNum(str):
    try:
        # 因为使用float有一个例外是'NaN'
        if str=='NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False


def return_pay_period(employee_ID):
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

    elif value[0][3] == 'hour':
        monday = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        while monday.weekday() != 0:
            monday -= one_day
        aweek = (str(monday).replace('-', ''),)
        for i in range(6):
            monday += one_day
            aweek += (str(monday).replace('-', ''),)
        return aweek

    elif value[0][3] == 'commissioned' or value[0][3] == 'salaried':
        today = datetime.datetime.today()
        monthRange = calendar.monthrange(today.year, today.month)[1]
        firstday = str(today.year).zfill(4) + \
               str(today.month).zfill(2) + \
               '01'
        amonth = (firstday,)
        for i in range(monthRange - 1):
            amonth += (firstday[0:6] + str(2+i).zfill(2),)
        return amonth




    print('return_pay_period未知错误')
    return 'return_pay_period'


def return_charge_numbers(employee_ID):
    try:
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

        elif value[0][3] == 'hour':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'V%' or charge_number like 'H%' or charge_number like 'A%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

        elif value[0][3] == 'commissioned':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'V%' or charge_number like 'C%' or charge_number like 'A%' " +\
                  "or charge_number like 'S%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

        elif value[0][3] == 'salaried':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'V%' or charge_number like 'A%' or charge_number like 'S%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

    except Exception:
        return "Project_Management_Database_Not_Available"


def return_charge_numbers_noV(employee_ID):
    try:
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

        elif value[0][3] == 'hour':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'H%' or charge_number like 'A%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

        elif value[0][3] == 'commissioned':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'C%' or charge_number like 'A%' " +\
                  "or charge_number like 'S%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

        elif value[0][3] == 'salaried':
            con = pymysql.Connect(
                host='XX.XXX.XXX.XX',
                port=XXXX,
                user='XXX',
                passwd='XXXXXXXXXX',
                db='XXX'
            )
            cur = con.cursor()
            sql = "select * from project_management_database " +\
                  "where charge_number like 'A%' or charge_number like 'S%'"
            print(sql)
            cur.execute(sql)
            value = cur.fetchall()
            cur.close()
            con.close()
            return value

        print('return_charge_numbers未知错误')
        return 'return_charge_numbers'


    except Exception:
        return "Project_Management_Database_Not_Available"


def return_Vonly():
    try:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "select * from project_management_database " +\
              "where charge_number like 'V%'"
        print(sql)
        cur.execute(sql)
        value = cur.fetchall()
        cur.close()
        con.close()
        return value
    except Exception:
        return "Project_Management_Database_Not_Available"


def check_timecard(employee_ID, charge_number, work_hour, date_year, date_month, date_day):


    if employee_ID.isspace() or charge_number.isspace() or work_hour.isspace() or\
        date_year.isspace() or date_month.isspace() \
            or date_day.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(employee_ID) == 0 or len(charge_number) == 0 or len(work_hour) == 0 \
            or len(date_year) == 0 or len(date_month) == 0 \
            or len(date_day) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'
    elif len(date_year) > 50:
        print('date_year太长')
        return '年过长！'
    elif len(date_month) > 50:
        print('date_month太长')
        return '月过长！'
    elif len(date_day) > 50:
        print('date_day太长')
        return '日过长！'

    if (date_year.isdigit() and date_month.isdigit() and date_day.isdigit()) == False:
        print("date date is not digit!")
        return "无效的日期！"

    elif '.' in date_year or '.' in date_month or '.' in date_day == True:
        print("no dot!")
        return "无效的日期！"


    elif int(date_year) <= 0 or int(date_year) > 9999:
        print("date_year <= 0 or > 9999")
        return "无效的年！"
    elif int(date_month) <= 0 or int(date_month) > 12:
        print("date_month <= 0 or > 12")
        return "无效的月！"
    elif int(date_day) <= 0 or int(date_day) > 31:
        print("date_day <= 0 or > 31")
        return "无效的日！"

    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)

    if isTrueDate(date) == False:
        print("invalid date date")
        return "无效的日期！"

    if isNum(work_hour) == False:
        return "无效的工时！"

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select hour_limit from employee_info where ' + 'employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    print(value[0][0])
    cur.close()
    con.close()

    if float(work_hour) > value[0][0]:
        return "您的工作时间不能超过" + str(int(value[0][0])) + "小时！"

    return "YES"


def submit_timecard(employee_ID, charge_number, work_hour, date_year, date_month, date_day):



    if employee_ID.isspace() or charge_number.isspace() or work_hour.isspace() or\
        date_year.isspace() or date_month.isspace() \
            or date_day.isspace() == True:
        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(employee_ID) == 0 or len(charge_number) == 0 or len(work_hour) == 0 \
            or len(date_year) == 0 or len(date_month) == 0 \
            or len(date_day) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'
    elif len(date_year) > 50:
        print('date_year太长')
        return '年过长！'
    elif len(date_month) > 50:
        print('date_month太长')
        return '月过长！'
    elif len(date_day) > 50:
        print('date_day太长')
        return '日过长！'

    if (date_year.isdigit() and date_month.isdigit() and date_day.isdigit()) == False:
        print("date date is not digit!")
        return "无效的日期！"

    elif '.' in date_year or '.' in date_month or '.' in date_day == True:
        print("no dot!")
        return "无效的日期！"


    elif int(date_year) <= 0 or int(date_year) > 9999:
        print("date_year <= 0 or > 9999")
        return "无效的年！"
    elif int(date_month) <= 0 or int(date_month) > 12:
        print("date_month <= 0 or > 12")
        return "无效的月！"
    elif int(date_day) <= 0 or int(date_day) > 31:
        print("date_day <= 0 or > 31")
        return "无效的日！"

    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)

    if isTrueDate(date) == False:
        print("invalid date date")
        return "无效的日期！"

    if isNum(work_hour) == False:
        return "无效的工时！"


    employee_ID_date = employee_ID + str(date_year).zfill(4) + str(date_month).zfill(2) + str(date_day).zfill(2)
    print(employee_ID_date)

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select hour_limit from employee_info where ' + 'employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    print(value[0][0])
    cur.close()
    con.close()

    if float(work_hour) > value[0][0]:
        return "您的工作时间不能超过" + str(int(value[0][0])) + "小时！"

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "INSERT INTO `timecards`(`employee_ID_date`, `charge_number`, `work_hour`) " +\
          "VALUES ('" + employee_ID_date + "','" + charge_number + "'," + str(work_hour) + ")"
    print(sql)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    return "YES"


def return_card_submit(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select card_submit from employee_info where ' + 'employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    print(value[0][0])
    cur.close()
    con.close()

    if value[0][0] == 'no':
        return 'NO'

    else:
        return 'YES'


def reverse_card_submit(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select card_submit from employee_info where ' + 'employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    print(value[0][0])
    cur.close()
    con.close()

    if value[0][0] == 'no':
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `card_submit`= 'yes' WHERE `employee_ID`= " + "'" + employee_ID + "'"
        print(sql)
        print()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        return "YES"
    else:
        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `card_submit`= 'no' WHERE `employee_ID`= " + "'" + employee_ID + "'"
        print(sql)
        print()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        return "YES"

    return "NO"


def save_ONE_timecard(employee_ID, charge_number, work_hour, date_year, date_month, date_day):

    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)

    try:
        timecards = pd.read_csv('./'+employee_ID+'.csv', index_col=0)
        print("read csv")

    except Exception:
        print("new csv just created")
        timecard = pd.DataFrame({'date': [date, ], 'charge_number': [charge_number, ], 'work_hour': [float(work_hour), ]})
        print(timecard)
        timecard.to_csv('./' + employee_ID + '.csv')
        return 'YES'

    list = timecards.values.tolist()
    containflag = False
    for i in range(len(list)):
        # print(list[i][0])
        if str(list[i][0]).zfill(8) == date:
            list[i][0] = str(list[i][0]).zfill(8)
            list[i][1] = charge_number
            list[i][2] = work_hour
            containflag = True

    if containflag == False:
        list.append([date, charge_number, float(work_hour)])

    newtimecards = pd.DataFrame(list, columns=['date', 'charge_number', 'work_hour'])
    newtimecards.to_csv('./' + employee_ID + '.csv')

    return 'YES'


def get_ONE_timecard(employee_ID, date_year, date_month, date_day):

    date = str(int(date_year)).zfill(4) + str(int(date_month)).zfill(2) + str(int(date_day)).zfill(2)

    try:
        timecards = pd.read_csv('./'+employee_ID+'.csv', index_col=0)
        print("read csv")

    except Exception:
        print("new csv just created")
        timecard = pd.DataFrame({'date': [], 'charge_number': [], 'work_hour': []})
        print(timecard)
        timecard.to_csv('./' + employee_ID + '.csv')
        return ('', '')

    timecards = pd.read_csv('./' + employee_ID + '.csv', index_col=0)
    list = timecards.values.tolist()

    for i in range(len(list)):
        if str(list[i][0]).zfill(8) == date:
            return (str(list[i][1]), str(list[i][2]))

    return ('', '')




# print(return_pay_period('000001'))
# print(return_pay_period('000003'))
# print(return_charge_numbers('000001'))
# print(check_timecard('000002', 'A0001', '19', '2021', '10', '08'))
# print(return_card_submit('000003'))
#print(save_ONE_timecard('000002', 'A0001', '1', '2021', '10', '13'))
#print(get_ONE_timecard('000002', '2021', '10', '13'))

# print(return_charge_numbers("000100"))
