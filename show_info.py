import pymysql

"""
(
    (order_ID订单号, products_purchased订单物品, sale金额, date订单关闭日期),
    (),
    ()
)
"""
def show_orders(employee_ID):
    con = pymysql.Connect(
        host='XX.XXX.XXX.XX',
        port=XXXX,
        user='XXX',
        passwd='XXXXXXXXXX',
        db='XXX'
    )
    cur = con.cursor()
    sql = 'select order_ID, products_purchased, sale, date from purchase_orders where ' + ' employee_ID = ' + "'" + employee_ID + "'"
    print(sql)
    cur.execute(sql)
    value = cur.fetchall()
    cur.close()
    con.close()
    print(value)
    return value


"""
18个
# ID 0 
# 员工状态（在职active、离职quit）1
# 姓名 2
# 员工类型 3 
# 邮寄地址 4 
# 身份证号 5
# 扣税 6 
# 养老保险 7 
# 医保 8 
# 手机号 9
# 每小时工资 10 
# 工资 11
# 分成 12 
# 每天工作时间上限 13 
# 支付方式 14 
# 支付地址 默认和邮寄地址一样 15 
# 银行名称 默认unknown 看到unknown不是bug 是用户没填 16 
# 银行账号 unknown 不是bug 是用户没填 17 
"""

def show_employee_info(employee_ID):
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
        returnvalue += (str(value[0][0]),)  # ID
        returnvalue += (str(value[0][1]),)   # 员工状态（在职active、离职quit）
        returnvalue += (str(value[0][2]),)  # 姓名
        returnvalue += (str(value[0][3]),)  # 员工类型
        returnvalue += (str(value[0][4]),)  # 邮寄地址
        returnvalue += (str(value[0][5]),)  # 身份证号
        returnvalue += (str(value[0][6]),)  # 扣税
        returnvalue += (str(value[0][7]),)  # 养老保险
        returnvalue += (str(value[0][8]),)  # 医保
        returnvalue += (str(value[0][9]),)  # 手机号
        returnvalue += (str(value[0][10]),)  # 每小时工资
        returnvalue += (str(value[0][11]),)  # 工资
        returnvalue += (str(value[0][12]),)  # 分成
        returnvalue += (str(value[0][13]),)  # 每天工作时间上限
        returnvalue += (str(value[0][14]),)  # 支付方式
        returnvalue += (str(value[0][15]),)  # 支付地址 unknown 不是bug 是用户没填
        returnvalue += (str(value[0][16]),)  # 银行名称 unknown 不是bug 是用户没填
        returnvalue += (str(value[0][17]),)  # 银行账号 unknown 不是bug 是用户没填
        return returnvalue
    else:
        return "员工不存在！"

# print(show_orders("000001"))
# print(show_employee_info("005613"))
