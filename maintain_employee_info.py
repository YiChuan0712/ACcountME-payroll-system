"""
    maintain_employee_info.py 维护员工信息

    ① add_employee(...)

        该函数用于增加新员工

        有多种返回值

        新建成功 返回'SUCCESS_123456' 后面六位是新员工编号

        其余返回值属于报错



    ② return_employee_info(employee_ID)
        该函数返回对应员工号的信息

        返回具体信息成功
        返回值格式：元组
                 employee_ID
                 name,  # 姓名
                 employee_type,  # 员工类型 仅支持hour, salaried, commissioned
                 mailing_address,  # 邮寄地址
                 social_security_number,  # 身份证号 我用的学号代替
                 standard_tax_deductions,  # 扣税
                 the401k_deduction,  # 养老保险
                 medical_deduction,  # 医保
                 phone_number,  # 手机号
                 hourly_rate,  # 每小时工资
                 salary,  # 工资
                 commission_rate,  # 分成
                 hour_limit  # 每天工作上限 单位小时
        也可能返回Employee_Not_Found



    ③ update_employee(employee_ID...)

        该函数用于修改员工信息

        返回YES成功
        也可能返回Employee_Not_Found



    ④ delete_employee(employee_ID)

        该函数用于删除员工信息

        employee_ID 是要删除的员工的编号

        返回YES成功
        也可能返回Employee_Not_Found






        standard_tax_deductions,  # 扣税
        the401k_deduction,  # 养老保险
        medical_deduction,  # 医保

        hourly_rate,  # 每小时工资
        salary,  # 工资
        commission_rate,  # 分成
        hour_limit  # 每天工作上限 单位小时
"""

import pymysql


def isNum(str):
    try:
        # 因为使用float有一个例外是'NaN'
        if str=='NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False



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


def add_employee(
                     name,  # 姓名
                     employee_type,  # 员工类型 仅支持hour, salaried, commissioned
                     mailing_address,  # 邮寄地址
                     social_security_number,  # 身份证号 我用的学号代替
                     standard_tax_deductions,  # 扣税
                     the401k_deduction,  # 养老保险
                     medical_deduction,  # 医保
                     phone_number,  # 手机号
                     hourly_rate,  # 每小时工资
                     salary,  # 工资
                     commission_rate,  # 分成
                     hour_limit  # 每天工作上限 单位小时
                 ):
    if name.isspace() or employee_type.isspace() or mailing_address.isspace() \
            or social_security_number.isspace() or phone_number.isspace() \
            or standard_tax_deductions.isspace() or the401k_deduction.isspace() or medical_deduction.isspace() \
            or salary.isspace() or hourly_rate.isspace() \
            or commission_rate.isspace() or hour_limit.isspace() == True:

        print('无效输入(1)空格')
        return '输入内容不能全为空格！'
    elif len(name) == 0 or len(employee_type) == 0 or len(mailing_address) == 0 \
            or len(social_security_number) == 0 or len(phone_number) == 0\
            or len(standard_tax_deductions) == 0 or len(the401k_deduction) == 0 or len(medical_deduction) == 0 \
            or len(salary) == 0 or len(hourly_rate) == 0 \
            or len(commission_rate) == 0 or len(hour_limit) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif (isNum(standard_tax_deductions) and isNum(the401k_deduction) and isNum(medical_deduction) \
        and isNum(hourly_rate) and isNum(salary) \
        and isNum(commission_rate) and isNum(hour_limit)) == False:
        print("not digit!")
        return "无效的数字！"

    elif len(standard_tax_deductions) > 50:
        print('standard_tax_deductions太长')
        return '扣税过长！'
    elif len(the401k_deduction) > 50:
        print('the401k_deduction太长')
        return '养老保险过长！'
    elif len(medical_deduction) > 50:
        print('medical_deduction太长')
        return '医保过长！'
    elif len(hourly_rate) > 50:
        print('hourly_rate太长')
        return '每小时工资过长！'
    elif len(salary) > 50:
        print('salary太长')
        return '工资过长！'
    elif len(commission_rate) > 50:
        print('commission_rate太长')
        return '分成过长！'
    elif len(hour_limit) > 50:
        print('hour_limit太长')
        return '工作时间上限过长！'

    elif len(name) > 50:
        print('name太长')
        return '姓名过长！'
    elif len(employee_type) > 50:
        print('employee_type太长')
        return '员工类型过长！'
    elif employee_type not in('salaried', 'hour', 'commissioned'):
        print('employee_type不是规定值')
        return '无效的员工类型！'

    elif len(mailing_address) > 50:
        print('mailing_address太长')
        return '邮寄地址过长！'
    elif len(social_security_number) > 50:
        print('social_security_number太长')
        return '身份证号过长！'
    elif len(phone_number) > 50:
        print('phone_number太长')
        return '手机号过长！'
    elif float(standard_tax_deductions) > 1 or float(standard_tax_deductions) < 0:
        print('standard_tax_deductions必须在0到1之间')
        return '税率必须在0到1之间！'
    elif float(the401k_deduction) > 1 or float(the401k_deduction) < 0:
        print('the401k_deduction必须在0到1之间')
        return '养老保险扣除比例必须在0到1之间！'
    elif float(medical_deduction) > 1 or float(medical_deduction) < 0:
        print('medical_deduction必须在0到1之间')
        return '医保扣除比例必须在0到1之间！'
    elif float(standard_tax_deductions) + float(the401k_deduction) + float(medical_deduction) > 1:
        print('总扣除必须在0到1之间')
        return '总扣除比例不得大于1！'

    elif float(hourly_rate) < 0:
        print('hourly_rate必须大于0')
        return '时薪必须大于0！！'

    elif float(salary) < 0:
        print('salary必须大于0')
        return '工资必须大于0！'

    elif float(commission_rate) not in(0.1, 0.15, 0.25, 0.35):
        print('commission_rate不是规定值')
        return '分成不是规定值！'

    elif float(hour_limit) > 24 or float(hour_limit) < 0:
        print('hour_limit超过24小时或小于0')
        return '工作时长应限制在0到24小时！'

    elif check_money_interface(salary) == False:
        print("salary format incorrect")
        return "金额小数点后最多两位！"

    elif check_money_interface(hourly_rate) == False:
        print("hourly_rate format incorrect")
        return "金额小数点后最多两位！"

    """
        生成新用户ID
    """

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
    print()
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()
    current_num = value[0][1]
    current_num = current_num + 1
    employee_ID = str(current_num).zfill(6)
    # print(employee_ID)

    """
        insert 新用户信息
    """

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "INSERT INTO `employee_info`(" +\
          "`employee_ID`, `state`, `name`, " +\
          "`employee_type`, `mailing_address`, " +\
          "`social_security_number`, `standard_tax_deductions`, " +\
          "`401k_deduction`, `medical_deduction`, `phone_number`, " +\
          "`hourly_rate`, `salary`, `commission_rate`, `hour_limit`, " +\
          "`payment_method`,`paying_address`, `bank_name`, `account_number`, `card_submit`) " +\
          "VALUES('" + employee_ID + "', 'active', '" + name + "', " +\
          "'" + employee_type + "', '" + mailing_address + "', " +\
          "'" + social_security_number + "', " + str(standard_tax_deductions) + ", " +\
          str(the401k_deduction) + "," + str(medical_deduction) + ", '" + phone_number + "', " +\
          str(hourly_rate) + ", " + str(salary) + ", " + str(commission_rate) + ", " + str(hour_limit) + ", " +\
          "'pick_up','" + mailing_address + "', 'unknown_bank','unknown_account','no')"
    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    """
            insert 新账号
    """

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "INSERT INTO `user_info`(`employee_ID`, `password`, `authority`) " +\
          "VALUES ('" + employee_ID + "','" + employee_ID + "','E')"

    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    """
            UPDATE properties 记录最新用户编号
    """

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "UPDATE `properties` SET `employee_counter`=" + str(current_num) + " WHERE 1"
    print(sql)
    print()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    return "SUCCESS_" + employee_ID


def return_employee_info(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_type <> 'PA' and employee_ID=" + "'" + employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    # print(value)
    cur.close()
    con.close()
    returnvalue = ()
    if value:
        returnvalue += (value[0][0],)  # ID
        returnvalue += (value[0][2],)  # 姓名
        returnvalue += (value[0][3],)  # 员工类型
        returnvalue += (value[0][4],)  # 邮寄地址
        returnvalue += (value[0][5],)  # 身份证号
        returnvalue += (value[0][6],)  # 扣税
        returnvalue += (value[0][7],)  # 养老保险
        returnvalue += (value[0][8],)  # 医保
        returnvalue += (value[0][9],)  # 手机号
        returnvalue += (value[0][10],)  # 每小时工资
        returnvalue += (value[0][11],)  # 工资
        returnvalue += (value[0][12],)  # 分成
        returnvalue += (value[0][13],)  # 每天工作时间上线
        return returnvalue
    else:
        return "员工不存在！"

def return_PA_info(employee_ID):
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
    # print(value)
    cur.close()
    con.close()
    returnvalue = ()
    if value:
        returnvalue += (value[0][0],)  # ID
        returnvalue += (value[0][2],)  # 姓名
        returnvalue += (value[0][3],)  # 员工类型
        returnvalue += (value[0][4],)  # 邮寄地址
        returnvalue += (value[0][5],)  # 身份证号
        returnvalue += (value[0][6],)  # 扣税
        returnvalue += (value[0][7],)  # 养老保险
        returnvalue += (value[0][8],)  # 医保
        returnvalue += (value[0][9],)  # 手机号
        returnvalue += (value[0][10],)  # 每小时工资
        returnvalue += (value[0][11],)  # 工资
        returnvalue += (value[0][12],)  # 分成
        returnvalue += (value[0][13],)  # 每天工作时间上线
        return returnvalue
    else:
        return "员工不存在！"

def update_employee(
                        employee_ID,
                        name,  # 姓名
                        employee_type,  # 员工类型 仅支持hour, salaried, commissioned
                        mailing_address,  # 邮寄地址
                        social_security_number,  # 身份证号 我用的学号代替
                        standard_tax_deductions,  # 扣税
                        the401k_deduction,  # 养老保险
                        medical_deduction,  # 医保
                        phone_number,  # 手机号
                        hourly_rate,  # 每小时工资
                        salary,  # 工资
                        commission_rate,  # 分成
                        hour_limit  # 每天工作上限 单位小时
                    ):

    if name.isspace() or employee_type.isspace() or mailing_address.isspace() \
            or social_security_number.isspace() or phone_number.isspace() \
            or standard_tax_deductions.isspace() or the401k_deduction.isspace() or medical_deduction.isspace() \
            or salary.isspace() or hourly_rate.isspace() \
            or commission_rate.isspace() or hour_limit.isspace() == True:

        print('无效输入(1)空格')
        return '输入内容不能全为空格！'

    elif len(name) == 0 or len(employee_type) == 0 or len(mailing_address) == 0 \
            or len(social_security_number) == 0 or len(phone_number) == 0\
            or len(standard_tax_deductions) == 0 or len(the401k_deduction) == 0 or len(medical_deduction) == 0 \
            or len(salary) == 0 or len(hourly_rate) == 0 \
            or len(commission_rate) == 0 or len(hour_limit) == 0:
        print('无效输入(2)空值')
        return '输入内容不能为空！'

    elif (isNum(standard_tax_deductions) and isNum(the401k_deduction) and isNum(medical_deduction) \
            and isNum(hourly_rate) and isNum(salary) \
            and isNum(commission_rate) and isNum(hour_limit)) == False:
        print(standard_tax_deductions.isdigit())
        print("not digit!")
        return "无效的数字！"

    elif len(standard_tax_deductions) > 50:
        print('standard_tax_deductions太长')
        return '扣税过长！'
    elif len(the401k_deduction) > 50:
        print('the401k_deduction太长')
        return '养老保险过长！'
    elif len(medical_deduction) > 50:
        print('medical_deduction太长')
        return '医保过长！'
    elif len(hourly_rate) > 50:
        print('hourly_rate太长')
        return '每小时工资过长！'
    elif len(salary) > 50:
        print('salary太长')
        return '工资过长！'
    elif len(commission_rate) > 50:
        print('commission_rate太长')
        return '分成过长！'
    elif len(hour_limit) > 50:
        print('hour_limit太长')
        return '工作时间上限过长！'

    elif len(name) > 50:
        print('name太长')
        return '姓名过长！'
    elif len(employee_type) > 50:
        print('employee_type太长')
        return '员工类型过长！'
    elif employee_type not in('salaried', 'hour', 'commissioned'):
        print('employee_type不是规定值')
        return '无效的员工类型！'

    elif len(mailing_address) > 50:
        print('mailing_address太长')
        return '邮寄地址过长！'
    elif len(social_security_number) > 50:
        print('social_security_number太长')
        return '身份证号过长！'
    elif len(phone_number) > 50:
        print('phone_number太长')
        return '手机号过长！'
    elif float(standard_tax_deductions) > 1 or float(standard_tax_deductions) < 0:
        print('standard_tax_deductions必须在0到1之间')
        return '税率必须在0到1之间！'
    elif float(the401k_deduction) > 1 or float(the401k_deduction) < 0:
        print('the401k_deduction必须在0到1之间')
        return '养老保险扣除比例必须在0到1之间！'
    elif float(medical_deduction) > 1 or float(medical_deduction) < 0:
        print('medical_deduction必须在0到1之间')
        return '医保扣除比例必须在0到1之间！'
    elif float(standard_tax_deductions) + float(the401k_deduction) + float(medical_deduction) > 1:
        print('总扣除必须在0到1之间')
        return '总扣除比例不得大于1！'

    elif float(hourly_rate) < 0:
        print('hourly_rate必须大于0')
        return '时薪必须大于0！！'

    elif float(salary) < 0:
        print('salary必须大于0')
        return '工资必须大于0！'

    elif float(commission_rate) not in (0.1, 0.15, 0.25, 0.35):
        print('commission_rate不是规定值')
        return '分成不是规定值！'

    elif float(hour_limit) > 24 or float(hour_limit) < 0:
        print('hour_limit超过24小时或小于0')
        return '工作时长应限制在0到24小时！'

    elif check_money_interface(salary) == False:
        print("salary format incorrect")
        return "金额小数点后最多两位！"
    elif check_money_interface(hourly_rate) == False:
        print("hourly_rate format incorrect")
        return "金额小数点后最多两位！"

    """
        查employee ID
    """
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_type <> 'PA' and state = 'active' and employee_ID=" + "'" + employee_ID + "'"
    print(sql)
    print()
    cur.execute(sql)
    value = cur.fetchall()
    #print(value)
    cur.close()
    con.close()

    if value:
        """
            update 用户信息
        """

        con = pymysql.Connect(
            host='XX.XXX.XXX.XX',
            port=XXXX,
            user='XXX',
            passwd='XXXXXXXXXX',
            db='XXX'
        )
        cur = con.cursor()
        sql = "UPDATE `employee_info` SET `employee_ID`='" + employee_ID + "',`state`='active',`name`='" + name + "'," + \
            "`employee_type`='" + employee_type + "',`mailing_address`='" + mailing_address + "'," + \
            "`social_security_number`='" + social_security_number + "'," + \
            "`standard_tax_deductions`=" + str(standard_tax_deductions) + "," +\
            "`401k_deduction`="+str(the401k_deduction)+"," +\
            "`medical_deduction`=" + str(medical_deduction) + ",`phone_number`='" + phone_number + "'," +\
            "`hourly_rate`="+str(hourly_rate)+",`salary`=" + str(salary) + ",`commission_rate`=" + str(commission_rate) + "," + \
            "`hour_limit`=" + str(hour_limit) + " WHERE `employee_ID`= " + "'" + employee_ID + "'"
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

    return


def delete_employee(employee_ID):

    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = "select * from employee_info where employee_type <> 'PA' and state = 'active'  and employee_ID=" + "'" + employee_ID + "'"
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
        sql = "UPDATE `employee_info` SET `state`= 'quit' WHERE `employee_ID`= " + "'" + employee_ID + "'"
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
#"""
#for i in range(20):
# #print(add_employee('童健',
#                      'salaried',  # 员工类型 仅支持hour, salaried, commissioned
#                      '北苑一公寓',  # 邮寄地址
#                      '21180732',  # 身份证号 我用的学号代替
#                      '0.05',  # 扣税
#                      '0.05',  # 养老保险
#                      '0.03',  # 医保
#                      '12345678',  # 手机号
#                      '100',  # 每小时工资
#                      '10000',  # 工资
#                      '0.15',  # 分成
#                      '12'   # 每天工作上限 单位小时
#                      )
#       )
#"""

# print(update_employee('000003', '', ''))
# print(delete_employee(''))

"""
print(update_employee(
                '000010',
                '翠花',
                'salaried',  # 员工类型 仅支持hour, salaried, commissioned
                 '汉堡王',  # 邮寄地址
                 '21181000',  # 身份证号 我用的学号代替
                 '0.1',  # 扣税
                 '0.1',  # 养老保险
                 '0.2',  # 医保
                 '16600000000',  # 手机号
                 '663.66',  # 每小时工资
                 '8.88',  # 工资
                 '0.25',  # 分成
                 '0.5'   # 每天工作上限 单位小时
                 ))
#"""
#print(return_employee_info("000002"))
#print(delete_employee('test1'))
#print(check_money_interface(0))