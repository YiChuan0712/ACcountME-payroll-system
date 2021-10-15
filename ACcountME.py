import sys
import time

from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit, QDialog, QMessageBox, QFileDialog, QComboBox, QScrollArea, QListWidget, QScrollBar
from login import check_login
from select_payment_method import *
from maintain_purchase_order import *
from create_employee_report import *
from maintain_employee_info import *
from maintain_timecard import *
from linktest import *
from show_info import *

# pyinstaller -F -w ACcountME.py

app = QApplication(sys.argv)


class PayrollAdministrator(QDialog):
    def __init__(self, employee_id):
        super().__init__()

        self.employee_id = employee_id
        self.box = QVBoxLayout()
        self.mylayout = QFormLayout()
        self.employee_widget = QWidget(self)
        self.box.addLayout(self.mylayout, 2)
        self.employee_widget.setLayout(self.box)
        res = return_PA_info(self.employee_id)
        self.setWindowTitle(res[1] + " - 管理员操作")

        self.initUi()

    def initUi(self):
        self.mydelete()
        app.processEvents()

        self.set_background()

        btn_create_administrative_report = QPushButton("生成管理报告")
        set_button(btn_create_administrative_report)
        btn_create_administrative_report.clicked.connect(self.click_create_administrative_report)

        btn_maintain_employee_info = QPushButton("维护员工信息")
        set_button(btn_maintain_employee_info)
        btn_maintain_employee_info.clicked.connect(self.click_maintain_employee_info)

        self.setObjectName("payroll_administrator_Window")
        self.setFixedSize(600, 400)

        self.mylayout.addWidget(btn_create_administrative_report)
        self.mylayout.addWidget(btn_maintain_employee_info)
        self.mylayout.setHorizontalSpacing(20)
        self.mylayout.setVerticalSpacing(12)

    def click_create_administrative_report(self):
        # print(self.mylayout.count())

        self.mydelete()
        app.processEvents()

        btn_total = QPushButton("总工时")
        set_button(btn_total)
        btn_total.clicked.connect(self.click_total)

        btn_ytd = QPushButton("总工资")
        set_button(btn_ytd)
        btn_ytd.clicked.connect(self.click_YTD)

        btn_return = QPushButton("返回")
        set_button(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addWidget(btn_total)
        self.mylayout.addWidget(btn_ytd)
        self.mylayout.addWidget(btn_return)

    def click_total(self):
        self.mydelete()
        app.processEvents()

        self.list_ID = ()
        self.list_name = ()

        lbl_employee_ID = QLabel("员工号")
        lbl_employee_ID.setFont(QFont("Microsoft YaHei"))
        let_employee_ID = QLineEdit()
        let_employee_ID.setFixedWidth(270)
        let_employee_ID.setFixedHeight(38)

        topFiller = QWidget()
        topFiller.setMinimumSize(330, 1300)  #######设置滚动条的尺寸

        scroll = QScrollArea()
        scroll.setWidget(topFiller)

        Hbox = QHBoxLayout()
        Hbox.addWidget(scroll)
        Hbox.addStretch(0)

        btn_add_employee_ID = QPushButton("添加")
        set_button_small(btn_add_employee_ID)
        btn_add_employee_ID.clicked.connect(lambda :self.click_add_employee_ID(let_employee_ID.text()))

        btn_employee_ID_post = QPushButton("确定")
        set_button_small(btn_employee_ID_post)
        btn_employee_ID_post.clicked.connect(lambda :self.click_employee_ID_post())

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        buttonbox = QHBoxLayout()
        buttonbox.addWidget(btn_add_employee_ID)
        buttonbox.addWidget(btn_employee_ID_post)
        buttonbox.addWidget(btn_return)
        buttonbox.addStretch(0)

        self.set_size_l(btn_add_employee_ID, 105, 30)
        self.set_size_l(btn_employee_ID_post, 105, 30)
        self.set_size_l(btn_return, 105, 30)

        self.mylayout.addRow(lbl_employee_ID, let_employee_ID)
        # self.set_size(190, 30)

        # self.mylayout.addRow(btn_add_employee_ID, btn_employee_ID_post)
        # self.mylayout.addRow(btn_return)

        self.mylayout.setHorizontalSpacing(20)
        self.mylayout.setVerticalSpacing(12)
        self.box.addLayout(buttonbox)
        self.box.addLayout(Hbox)

    def click_add_employee_ID(self, employeeID):
        if employeeID not in self.list_ID:
            res = return_total_hours_worked(employeeID, '2020', '1', '1', '2020', '1', '1')
            if isinstance(res, str):
                reply = QMessageBox.information(self, "错误", res, QMessageBox.Ok)
                self.mylayout.itemAt(1).widget().setText("")
            else:
                self.list_ID += (employeeID,)
                ret = return_employee_info(employeeID)
                self.list_name += (ret[1],)

                box_item = self.box.itemAt(2)
                self.mylayout.removeItem(box_item)
                if box_item.widget():
                    box_item.widget().deleteLater()

                layout_list = list(range(box_item.count()))
                layout_list.reverse()  # 倒序删除，避免影响布局顺序

                for j in layout_list:
                    layout_item = box_item.itemAt(j)
                    box_item.removeItem(layout_item)
                    if layout_item.widget():
                        layout_item.widget().deleteLater()

                topFiller = QWidget()
                topFiller.setMinimumSize(330, 1300)  #######设置滚动条的尺寸

                lbl_ID = QLabel(topFiller)
                lbl_ID.setText("员工号")
                lbl_ID.setFixedWidth(60)
                lbl_ID.move(10, 20)

                lbl_name = QLabel(topFiller)
                lbl_name.setText("姓名")
                lbl_name.setFixedWidth(60)
                lbl_name.move(170, 20)

                count = 1
                for id in self.list_ID:

                    lbl_employee_ID = QLabel(topFiller)
                    lbl_employee_ID.setText(str(id))
                    lbl_employee_ID.setFixedWidth(60)
                    lbl_employee_ID.move(10, 20+30*(count))
                    count += 1

                count = 1
                for name in self.list_name:
                    lbl_name = QLabel(topFiller)
                    lbl_name.setText(str(name))
                    lbl_name.setFixedWidth(60)
                    lbl_name.move(170, 20+30*(count))
                    count += 1

                scroll = QScrollArea()
                scroll.setWidget(topFiller)

                Hbox = QHBoxLayout()
                Hbox.addWidget(scroll)
                Hbox.addStretch(0)

                self.box.addLayout(Hbox)

                self.mylayout.itemAt(1).widget().setText("")

        else:
            reply = QMessageBox.information(self, "错误", "重复输入", QMessageBox.Ok)
            self.mylayout.itemAt(1).widget().setText("")

    def click_employee_ID_post(self):
        self.mydelete()
        app.processEvents()

        if check_connection() == "NO":
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("请求信息不可得")

            btn_ok = msgbox.addButton("确认", QMessageBox.AcceptRole)
            btn_no = msgbox.addButton("取消", QMessageBox.RejectRole)
            res = msgbox.exec()
            if res == QMessageBox.RejectRole:
                self.mydelete()
                app.processEvents()

                self.initUi()
                return
            else:
                self.mydelete()
                app.processEvents()
                self.click_total()
                return

        lbl_begin_year = QLabel("开始时间（年）")
        lbl_begin_year.setFont(QFont("Microsoft YaHei"))
        let_begin_year = QLineEdit()
        let_begin_year.setFixedWidth(270)
        let_begin_year.setFixedHeight(38)

        lbl_begin_month = QLabel("开始时间（月）")
        lbl_begin_month.setFont(QFont("Microsoft YaHei"))
        let_begin_month = QLineEdit()
        let_begin_month.setFixedWidth(270)
        let_begin_month.setFixedHeight(38)

        lbl_begin_day = QLabel("开始时间（日）")
        lbl_begin_day.setFont(QFont("Microsoft YaHei"))
        let_begin_day = QLineEdit()
        let_begin_day.setFixedWidth(270)
        let_begin_day.setFixedHeight(38)

        lbl_end_year = QLabel("结束时间（年）")
        lbl_end_year.setFont(QFont("Microsoft YaHei"))
        let_end_year = QLineEdit()
        let_end_year.setFixedWidth(270)
        let_end_year.setFixedHeight(38)

        lbl_end_month = QLabel("结束时间（月）")
        lbl_end_month.setFont(QFont("Microsoft YaHei"))
        let_end_month = QLineEdit()
        let_end_month.setFixedWidth(270)
        let_end_month.setFixedHeight(38)

        lbl_end_day = QLabel("结束时间（日）")
        lbl_end_day.setFont(QFont("Microsoft YaHei"))
        let_end_day = QLineEdit()
        let_end_day.setFixedWidth(270)
        let_end_day.setFixedHeight(38)

        msg1 = let_begin_year
        msg2 = let_begin_month
        msg3 = let_begin_day
        msg4 = let_end_year
        msg5 = let_end_month
        msg6 = let_end_day

        buttonbox = QHBoxLayout()

        btn_report_post = QPushButton("提交")
        set_button_small(btn_report_post)
        btn_report_post.clicked.connect(lambda :self.click_report_post(1, msg1, msg2, msg3, msg4, msg5, msg6))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.set_size_l(btn_report_post, 105, 30)
        self.set_size_l(btn_return, 105, 30)

        buttonbox.addWidget(btn_report_post)
        buttonbox.addStretch(1)
        buttonbox.addWidget(btn_return)
        buttonbox.addStretch(3)
        # buttonbox.addStretch(0)
        # buttonbox.addStretch(0)
        # buttonbox.addStretch(0)


        self.mylayout.addRow(lbl_begin_year, let_begin_year)
        self.mylayout.addRow(lbl_begin_month, let_begin_month)
        self.mylayout.addRow(lbl_begin_day, let_begin_day)
        self.mylayout.addRow(lbl_end_year, let_end_year)
        self.mylayout.addRow(lbl_end_month, let_end_month)
        self.mylayout.addRow(lbl_end_day, let_end_day)
        self.box.addLayout(buttonbox)
        # self.mylayout.addRow(btn_report_post, btn_return)
        self.set_size(type(QLineEdit()),190,30)
        self.set_size(type(QLabel()), 110, 30)

    def click_report_post(self, flag, msg1, msg2, msg3, msg4, msg5, msg6, msg7="yes", msg8="no"):
        showFlag = True
        if flag == 1:
            ret = ()
            for employee_id in self.list_ID:
                if showFlag:
                    total_hour = return_total_hours_worked(employee_id, msg1.text(), msg2.text(), msg3.text(),
                                                           msg4.text(), msg5.text(), msg6.text())
                    if isinstance(total_hour, float):
                        res = create_ONE_report(employee_id, "All", total_hour, msg1.text(), msg2.text(), msg3.text(),
                                                msg4.text(), msg5.text(), msg6.text())
                        if isinstance(res, tuple):
                            ret += res
                        else:
                            QMessageBox.warning(self, "错误", res)
                            showFlag = False
                    else:
                        QMessageBox.warning(self, "错误", total_hour)
                        showFlag = False

            if showFlag:
                self.show_report(ret,flag)
        elif flag == 2:
            ret = ()
            for employee_id in self.list_ID:
                if showFlag:
                    money = return_pay_YTD(employee_id, msg1.text(), msg2.text(), msg3.text(),
                                                           msg4.text(), msg5.text(), msg6.text())
                    if isinstance(money, float):
                        res = create_ONE_report_YTD(employee_id, money, msg1.text(), msg2.text(), msg3.text(),
                                                msg4.text(), msg5.text(), msg6.text())
                        if isinstance(res, tuple):
                            ret += res
                        else:
                            QMessageBox.warning(self, "错误", res)
                            showFlag = False
                    else:
                        QMessageBox.warning(self, "错误", money)
                        showFlag = False
            if showFlag:
                self.show_report(ret, flag)

    def show_report(self, res, flag):
        if flag == 1:
            self.mydelete()
            app.processEvents()

            # lbl_name = QLabel("姓名")
            # lbl_name.setFont(QFont("Microsoft YaHei"))
            # lbl_total_hour = QLabel("工作总时长")
            # lbl_total_hour.setFont(QFont("Microsoft YaHei"))
            # self.mylayout.addRow(lbl_name,lbl_total_hour)

            topFiller = QWidget()
            topFiller.setMinimumSize(430, 1300)

            lbl_id = QLabel(topFiller)
            lbl_id.setText("员工号")
            lbl_id.setFont(QFont("Microsoft YaHei"))
            lbl_id.setFixedWidth(60)
            lbl_id.move(10, 20)

            lbl_name = QLabel(topFiller)
            lbl_name.setText("姓名")
            lbl_name.setFont(QFont("Microsoft YaHei"))
            lbl_name.setFixedWidth(100)
            lbl_name.move(150, 20)

            lbl_total_hour = QLabel(topFiller)
            lbl_total_hour.setText("工作总时长")
            lbl_total_hour.setFont(QFont("Microsoft YaHei"))
            lbl_total_hour.setFixedWidth(100)
            lbl_total_hour.move(250, 20)

            count = 1
            for row in res:

                # let_name = QLabel()
                # let_name.setFont(QFont("Microsoft YaHei"))
                # let_name.setText(row[1]+'\t'+row[0])
                #
                # let_total_hour = QLabel()
                # let_total_hour.setFont(QFont("Microsoft YaHei"))
                # let_total_hour.setText(str(row[5]))
                #
                # self.mylayout.addRow(let_name, let_total_hour)

                lbl_id_res = QLabel(topFiller)
                lbl_id_res.setText(row[1])
                lbl_id_res.setFont(QFont("Microsoft YaHei"))
                lbl_id_res.setFixedWidth(60)
                lbl_id_res.move(10, 20 + 30 * count)

                lbl_name_res = QLabel(topFiller)
                lbl_name_res.setText(row[0])
                lbl_name_res.setFont(QFont("Microsoft YaHei"))
                lbl_name_res.setFixedWidth(60)
                lbl_name_res.move(150, 20 + 30 * count)

                lbl_total_hour_res = QLabel(topFiller)
                lbl_total_hour_res.setText(str(row[5]))
                lbl_total_hour_res.setFont(QFont("Microsoft YaHei"))
                lbl_total_hour_res.setFixedWidth(60)
                lbl_total_hour_res.move(270, 20 + 30 * count)

                count += 1

            scroll = QScrollArea()
            scroll.setWidget(topFiller)

            Hbox = QHBoxLayout()
            Hbox.addWidget(scroll)
            Hbox.addStretch(0)

            btn_save = QPushButton("生成报告")
            set_button_small(btn_save)
            btn_save.clicked.connect(lambda: self.click_save(flag, res))

            btn_return = QPushButton("返回")
            set_button_small(btn_return)
            btn_return.clicked.connect(self.back)

            self.mylayout.addRow(btn_save, btn_return)
            self.box.addLayout(Hbox)

        elif flag == 2:
            self.mydelete()
            app.processEvents()

            # lbl_name = QLabel("姓名")
            # lbl_name.setFont(QFont("Microsoft YaHei"))
            # lbl_money = QLabel("工作总时长")
            # lbl_money.setFont(QFont("Microsoft YaHei"))
            # self.mylayout.addRow(lbl_name, lbl_money)
            #
            # for row in res:
            #     let_name = QLabel()
            #     let_name.setFont(QFont("Microsoft YaHei"))
            #     let_name.setText(row[1]+'\t'+row[0])
            #
            #     let_total_hour = QLabel()
            #     let_total_hour.setFont(QFont("Microsoft YaHei"))
            #     let_total_hour.setText(str(row[4]))
            #
            #     self.mylayout.addRow(let_name, let_total_hour)
            #
            # btn_save = QPushButton("生成报告")
            # set_button_small(btn_save)
            # btn_save.clicked.connect(lambda: self.click_save(flag, res))
            #
            # btn_return = QPushButton("返回")
            # set_button_small(btn_return)
            # btn_return.clicked.connect(self.back)
            #
            # self.mylayout.addRow(btn_save, btn_return)

            topFiller = QWidget()
            topFiller.setMinimumSize(430, 1300)

            lbl_id = QLabel(topFiller)
            lbl_id.setText("员工号")
            lbl_id.setFont(QFont("Microsoft YaHei"))
            lbl_id.setFixedWidth(60)
            lbl_id.move(10, 20)

            lbl_name = QLabel(topFiller)
            lbl_name.setText("姓名")
            lbl_name.setFont(QFont("Microsoft YaHei"))
            lbl_name.setFixedWidth(60)
            lbl_name.move(150, 20)

            lbl_total_hour = QLabel(topFiller)
            lbl_total_hour.setText("工资")
            lbl_total_hour.setFont(QFont("Microsoft YaHei"))
            lbl_total_hour.setFixedWidth(60)
            lbl_total_hour.move(250, 20)

            count = 1
            for row in res:
                # let_name = QLabel()
                # let_name.setFont(QFont("Microsoft YaHei"))
                # let_name.setText(row[1]+'\t'+row[0])
                #
                # let_total_hour = QLabel()
                # let_total_hour.setFont(QFont("Microsoft YaHei"))
                # let_total_hour.setText(str(row[5]))
                #
                # self.mylayout.addRow(let_name, let_total_hour)

                lbl_id_res = QLabel(topFiller)
                lbl_id_res.setText(row[1])
                lbl_id_res.setFont(QFont("Microsoft YaHei"))
                lbl_id_res.setFixedWidth(60)
                lbl_id_res.move(10, 20 + 30 * count)

                lbl_name_res = QLabel(topFiller)
                lbl_name_res.setText(row[0])
                lbl_name_res.setFont(QFont("Microsoft YaHei"))
                lbl_name_res.setFixedWidth(100)
                lbl_name_res.move(150, 20 + 30 * count)

                lbl_total_hour_res = QLabel(topFiller)
                lbl_total_hour_res.setText(str(row[4]))
                lbl_total_hour_res.setFont(QFont("Microsoft YaHei"))
                lbl_total_hour_res.setFixedWidth(100)
                lbl_total_hour_res.move(250, 20 + 30 * count)

                count += 1

            scroll = QScrollArea()
            scroll.setWidget(topFiller)

            Hbox = QHBoxLayout()
            Hbox.addWidget(scroll)
            Hbox.addStretch(0)

            btn_save = QPushButton("生成报告")
            set_button_small(btn_save)
            btn_save.clicked.connect(lambda: self.click_save(flag, res))

            btn_return = QPushButton("返回")
            set_button_small(btn_return)
            btn_return.clicked.connect(self.back)

            self.mylayout.addRow(btn_save, btn_return)
            self.box.addLayout(Hbox)

    def click_save(self, flag, msg):
        fname = QFileDialog.getSaveFileName(self, "保存位置", "./", ".docx")
        if fname[0]:
            if flag == 1:
                res = create_doc(self.employee_id, fname[0] + fname[1], "总工时报告", msg)
                if res == "YES":
                    QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
                else:
                    pass
            elif flag == 2:
                res = create_doc_YTD(self.employee_id, fname[0] + fname[1], "工资报告", msg)
                if res == "YES":
                    QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
                else:
                    pass
        elif fname[0] == '':
            pass
        else:
            QMessageBox.warning(self, "错误", "文件存储错误")

    def click_YTD(self):
        self.mydelete()
        app.processEvents()

        self.list_ID = ()
        self.list_name = ()

        lbl_employee_ID = QLabel("员工号")
        lbl_employee_ID.setFont(QFont("Microsoft YaHei"))
        let_employee_ID = QLineEdit()
        let_employee_ID.setFixedWidth(270)
        let_employee_ID.setFixedHeight(38)

        btn_add_employee_ID = QPushButton("添加")
        set_button_small(btn_add_employee_ID)
        btn_add_employee_ID.clicked.connect(lambda: self.YTD_add_employee_ID(let_employee_ID.text()))

        btn_employee_ID_post = QPushButton("确定")
        set_button_small(btn_employee_ID_post)
        btn_employee_ID_post.clicked.connect(lambda: self.click_YTD_employee_ID_post())

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.set_size_l(btn_add_employee_ID,105, 30)
        self.set_size_l(btn_employee_ID_post, 105, 30)
        self.set_size_l(btn_return, 105, 30)

        buttonbox = QHBoxLayout()
        buttonbox.addWidget(btn_add_employee_ID)
        buttonbox.addWidget(btn_employee_ID_post)
        buttonbox.addWidget(btn_return)
        buttonbox.addStretch(0)

        topFiller = QWidget()
        topFiller.setMinimumSize(330, 1300)  #######设置滚动条的尺寸

        scroll = QScrollArea()
        scroll.setWidget(topFiller)

        Hbox = QHBoxLayout()
        Hbox.addWidget(scroll)
        Hbox.addStretch(0)

        self.mylayout.addRow(lbl_employee_ID, let_employee_ID)
        # self.mylayout.addRow(btn_add_employee_ID, btn_employee_ID_post)
        # self.mylayout.addRow(btn_return)
        self.mylayout.setHorizontalSpacing(20)
        self.mylayout.setVerticalSpacing(12)
        self.box.addLayout(buttonbox)
        self.box.addLayout(Hbox)

    def YTD_add_employee_ID(self, employeeID):
        if employeeID not in self.list_ID:
            res = return_pay_YTD(employeeID,'2020','1','1','2020','1','1')
            if isinstance(res, str):
                reply = QMessageBox.information(self, "错误", res, QMessageBox.Ok)
            else:
                self.list_ID += (employeeID,)
                ret = return_employee_info(employeeID)
                self.list_name += (ret[1],)

                box_item = self.box.itemAt(2)
                self.mylayout.removeItem(box_item)
                if box_item.widget():
                    box_item.widget().deleteLater()

                layout_list = list(range(box_item.count()))
                layout_list.reverse()  # 倒序删除，避免影响布局顺序

                for j in layout_list:
                    layout_item = box_item.itemAt(j)
                    box_item.removeItem(layout_item)
                    if layout_item.widget():
                        layout_item.widget().deleteLater()

                topFiller = QWidget()
                topFiller.setMinimumSize(330, 1300)  #######设置滚动条的尺寸

                lbl_ID = QLabel(topFiller)
                lbl_ID.setText("员工号")
                lbl_ID.setFixedWidth(60)
                lbl_ID.move(10, 20)

                lbl_name = QLabel(topFiller)
                lbl_name.setText("姓名")
                lbl_name.setFixedWidth(60)
                lbl_name.move(170, 20)

                count = 1
                for id in self.list_ID:
                    lbl_employee_ID = QLabel(topFiller)
                    lbl_employee_ID.setText(str(id))
                    lbl_employee_ID.setFixedWidth(60)
                    lbl_employee_ID.move(10, 20 + 30 * (count))
                    count += 1

                count = 1
                for name in self.list_name:
                    lbl_name = QLabel(topFiller)
                    lbl_name.setText(str(name))
                    lbl_name.setFixedWidth(60)
                    lbl_name.move(170, 20 + 30 * (count))
                    count += 1

                scroll = QScrollArea()
                scroll.setWidget(topFiller)

                Hbox = QHBoxLayout()
                Hbox.addWidget(scroll)
                Hbox.addStretch(0)

                self.box.addLayout(Hbox)
        else:
            reply = QMessageBox.information(self, "错误", "重复输入", QMessageBox.Ok)

    def click_YTD_employee_ID_post(self):
        self.mydelete()
        app.processEvents()

        if check_connection() == "NO":
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("请求信息不可得")

            btn_ok = msgbox.addButton("确认", QMessageBox.AcceptRole)
            btn_no = msgbox.addButton("取消", QMessageBox.RejectRole)
            res = msgbox.exec()
            if res == QMessageBox.RejectRole:
                self.mydelete()
                app.processEvents()

                self.initUi()
                return
            else:
                self.mydelete()
                app.processEvents()
                self.click_YTD()
                return

        lbl_begin_year = QLabel("开始时间（年）")
        lbl_begin_year.setFont(QFont("Microsoft YaHei"))
        let_begin_year = QLineEdit()
        let_begin_year.setFixedWidth(270)
        let_begin_year.setFixedHeight(38)

        lbl_begin_month = QLabel("开始时间（月）")
        lbl_begin_month.setFont(QFont("Microsoft YaHei"))
        let_begin_month = QLineEdit()
        let_begin_month.setFixedWidth(270)
        let_begin_month.setFixedHeight(38)

        lbl_begin_day = QLabel("开始时间（日）")
        lbl_begin_day.setFont(QFont("Microsoft YaHei"))
        let_begin_day = QLineEdit()
        let_begin_day.setFixedWidth(270)
        let_begin_day.setFixedHeight(38)

        lbl_end_year = QLabel("结束时间（年）")
        lbl_end_year.setFont(QFont("Microsoft YaHei"))
        let_end_year = QLineEdit()
        let_end_year.setFixedWidth(270)
        let_end_year.setFixedHeight(38)

        lbl_end_month = QLabel("结束时间（月）")
        lbl_end_month.setFont(QFont("Microsoft YaHei"))
        let_end_month = QLineEdit()
        let_end_month.setFixedWidth(270)
        let_end_month.setFixedHeight(38)

        lbl_end_day = QLabel("结束时间（日）")
        lbl_end_day.setFont(QFont("Microsoft YaHei"))
        let_end_day = QLineEdit()
        let_end_day.setFixedWidth(270)
        let_end_day.setFixedHeight(38)

        msg1 = let_begin_year
        msg2 = let_begin_month
        msg3 = let_begin_day
        msg4 = let_end_year
        msg5 = let_end_month
        msg6 = let_end_day

        buttonbox = QHBoxLayout()

        btn_report_post = QPushButton("提交")
        set_button_small(btn_report_post)
        btn_report_post.clicked.connect(lambda: self.click_report_post(2, msg1, msg2, msg3, msg4, msg5, msg6))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.set_size_l(btn_report_post, 105, 30)
        self.set_size_l(btn_return, 105, 30)

        buttonbox.addWidget(btn_report_post)
        buttonbox.addStretch(1)
        buttonbox.addWidget(btn_return)
        buttonbox.addStretch(3)


        self.mylayout.addRow(lbl_begin_year, let_begin_year)
        self.mylayout.addRow(lbl_begin_month, let_begin_month)
        self.mylayout.addRow(lbl_begin_day, let_begin_day)
        self.mylayout.addRow(lbl_end_year, let_end_year)
        self.mylayout.addRow(lbl_end_month, let_end_month)
        self.mylayout.addRow(lbl_end_day, let_end_day)
        # self.mylayout.addRow(btn_report_post, btn_return)
        self.box.addLayout(buttonbox)

        self.set_size(type(QLineEdit()), 190, 30)
        self.set_size(type(QLabel()), 110, 30)

    def click_maintain_employee_info(self):
        # print(self.mylayout.count())

        self.mydelete()
        app.processEvents()

        btn_add_employee_info = QPushButton("添加员工")
        btn_delete_employee_info = QPushButton("删除员工")
        btn_modify_employee_info = QPushButton("修改员工信息")
        btn_return = QPushButton("返回")

        set_button(btn_add_employee_info)
        set_button(btn_delete_employee_info)
        set_button(btn_modify_employee_info)
        set_button(btn_return)

        btn_add_employee_info.clicked.connect(self.click_add_employee_info)
        btn_delete_employee_info.clicked.connect(self.click_delete_employee_info)
        btn_modify_employee_info.clicked.connect(self.click_modify_employee_info)
        btn_return.clicked.connect(self.back)

        self.mylayout.addWidget(btn_add_employee_info)
        self.mylayout.addWidget(btn_delete_employee_info)
        self.mylayout.addWidget(btn_modify_employee_info)
        self.mylayout.addWidget(btn_return)

    def click_add_employee_info(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 0)
        self.employee_widget.setGeometry(100, 0, 750, 400)

        lbl_name = QLabel("姓名")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        let_name = QLineEdit()

        lbl_employee_type = QLabel("员工类型")
        lbl_employee_type.setFont(QFont("Microsoft YaHei"))
        # let_employee_type = QLineEdit()
        let_employee_type = QComboBox()
        let_employee_type.addItem("salaried")
        let_employee_type.addItem("commissioned")
        let_employee_type.addItem("hour")
        let_employee_type.setFixedWidth(270)
        let_employee_type.setFixedHeight(26)

        lbl_mailing_address = QLabel("邮寄地址")
        lbl_mailing_address.setFont(QFont("Microsoft YaHei"))
        let_mailing_address = QLineEdit()

        lbl_social_security_number = QLabel("身份证号")
        lbl_social_security_number.setFont(QFont("Microsoft YaHei"))
        let_social_security_number = QLineEdit()

        lbl_standard_tax_deductions = QLabel("扣税")
        lbl_standard_tax_deductions.setFont(QFont("Microsoft YaHei"))
        let_standard_tax_deductions = QLineEdit()

        lbl_the401k_deduction = QLabel("养老保险")
        lbl_the401k_deduction.setFont(QFont("Microsoft YaHei"))
        let_the401k_deduction = QLineEdit()

        lbl_medical_deduction = QLabel("医保")
        lbl_medical_deduction.setFont(QFont("Microsoft YaHei"))
        let_medical_deduction = QLineEdit()

        lbl_phone_number = QLabel("手机号")
        lbl_phone_number.setFont(QFont("Microsoft YaHei"))
        let_phone_number = QLineEdit()

        lbl_hourly_rate = QLabel("每小时工资")
        lbl_hourly_rate.setFont(QFont("Microsoft YaHei"))
        let_hourly_rate = QLineEdit()

        lbl_salary = QLabel("工资")
        lbl_salary.setFont(QFont("Microsoft YaHei"))
        let_salary = QLineEdit()

        lbl_commission_rate = QLabel("分成")
        lbl_commission_rate.setFont(QFont("Microsoft YaHei"))
        #let_commission_rate = QLineEdit()
        let_commission_rate = QComboBox()
        let_commission_rate.addItem("10%")
        let_commission_rate.addItem("15%")
        let_commission_rate.addItem("25%")
        let_commission_rate.addItem("35%")
        let_commission_rate.setFixedWidth(270)
        let_commission_rate.setFixedHeight(26)

        lbl_hour_limit = QLabel("每天工作上限")
        lbl_hour_limit.setFont(QFont("Microsoft YaHei"))
        let_hour_limit = QLineEdit()

        btn_post = QPushButton("提交")
        set_button_small(btn_post)

        msg1 = let_name
        msg2 = let_employee_type
        msg3 = let_mailing_address
        msg4 = let_social_security_number
        msg5 = let_standard_tax_deductions
        msg6 = let_the401k_deduction
        msg7 = let_medical_deduction
        msg8 = let_phone_number
        msg9 = let_hourly_rate
        msg10 = let_salary
        msg11 = let_commission_rate
        msg12 = let_hour_limit

        btn_post.clicked.connect(
            lambda: self.click_employee_info_post(1, msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10, msg11,
                                                  msg12, ))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.set_size_l(btn_return, 105, 26)
        self.set_size_l(btn_post, 105, 26)

        buttonbox = QHBoxLayout()
        buttonbox.addStretch(3)
        buttonbox.addWidget(btn_post)
        buttonbox.addStretch(1)
        buttonbox.addWidget(btn_return)
        buttonbox.addStretch(8)

        self.mylayout.addRow(lbl_name, let_name)
        self.mylayout.addRow(lbl_employee_type, let_employee_type)
        self.mylayout.addRow(lbl_mailing_address, let_mailing_address)
        self.mylayout.addRow(lbl_social_security_number, let_social_security_number)
        self.mylayout.addRow(lbl_standard_tax_deductions, let_standard_tax_deductions)
        self.mylayout.addRow(lbl_the401k_deduction, let_the401k_deduction)
        self.mylayout.addRow(lbl_medical_deduction, let_medical_deduction)
        self.mylayout.addRow(lbl_phone_number, let_phone_number)
        self.mylayout.addRow(lbl_hourly_rate, let_hourly_rate)
        self.mylayout.addRow(lbl_salary, let_salary)
        self.mylayout.addRow(lbl_commission_rate, let_commission_rate)
        self.mylayout.addRow(lbl_hour_limit, let_hour_limit)

        self.set_size(type(QLineEdit()), 270, 26)
        self.set_size(type(QLabel()), 100, 30)
        # self.mylayout.addRow(btn_return, btn_post)
        self.box.addLayout(buttonbox)

    def click_delete_employee_info(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 50)
        self.employee_widget.setGeometry(100, 50, 650, 300)

        lbl_employee_ID = QLabel("员工号")
        lbl_employee_ID.setFont(QFont("Microsoft YaHei"))
        let_employee_ID = QLineEdit()

        btn_search_id = QPushButton("搜索员工")
        set_button_small(btn_search_id)

        topFiller = QWidget()
        topFiller.setMinimumSize(400, 410)  #######设置滚动条的尺寸

        scroll = QScrollArea()
        scroll.setWidget(topFiller)
        scroll.setVisible(False)

        Hbox = QHBoxLayout()
        Hbox.addWidget(scroll)
        Hbox.addStretch(0)

        lbl_name = QLabel(topFiller)
        lbl_name.setText("姓名")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        lbl_name.move(10, 20)
        let_name = QLineEdit(topFiller)
        let_name.move(200, 20)
        let_name.setEnabled(False)
        # item.setReadOnly(True)#设置只读
        # item.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")#设置无色无边框

        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity()
        # let_name.setGraphicsEffect(op)
        # let_name.setAutoFillBackground(True)

        lbl_employee_type = QLabel(topFiller)
        lbl_employee_type.setText("员工类型")
        lbl_employee_type.setFont(QFont("Microsoft YaHei"))
        lbl_employee_type.move(10, 50)
        let_employee_type = QLineEdit(topFiller)
        let_employee_type.move(200, 50)
        let_employee_type.setEnabled(False)

        lbl_mailing_address = QLabel(topFiller)
        lbl_mailing_address.setText("邮寄地址")
        lbl_mailing_address.setFont(QFont("Microsoft YaHei"))
        lbl_mailing_address.move(10, 80)
        let_mailing_address = QLineEdit(topFiller)
        let_mailing_address.move(200, 80)
        let_mailing_address.setEnabled(False)

        lbl_social_security_number = QLabel(topFiller)
        lbl_social_security_number.setText("身份证号")
        lbl_social_security_number.setFont(QFont("Microsoft YaHei"))
        lbl_social_security_number.move(10, 110)
        let_social_security_number = QLineEdit(topFiller)
        let_social_security_number.move(200, 110)
        let_social_security_number.setEnabled(False)

        lbl_standard_tax_deductions = QLabel(topFiller)
        lbl_standard_tax_deductions.setText("扣税")
        lbl_standard_tax_deductions.setFont(QFont("Microsoft YaHei"))
        lbl_standard_tax_deductions.move(10, 140)
        let_standard_tax_deductions = QLineEdit(topFiller)
        let_standard_tax_deductions.move(200, 140)
        let_standard_tax_deductions.setEnabled(False)

        lbl_the401k_deduction = QLabel(topFiller)
        lbl_the401k_deduction.setText("养老保险")
        lbl_the401k_deduction.setFont(QFont("Microsoft YaHei"))
        lbl_the401k_deduction.move(10, 170)
        let_the401k_deduction = QLineEdit(topFiller)
        let_the401k_deduction.move(200, 170)
        let_the401k_deduction.setEnabled(False)

        lbl_medical_deduction = QLabel(topFiller)
        lbl_medical_deduction.setText("医保")
        lbl_medical_deduction.setFont(QFont("Microsoft YaHei"))
        lbl_medical_deduction.move(10, 200)
        let_medical_deduction = QLineEdit(topFiller)
        let_medical_deduction.move(200, 200)
        let_medical_deduction.setEnabled(False)

        lbl_phone_number = QLabel(topFiller)
        lbl_phone_number.setText("手机号")
        lbl_phone_number.setFont(QFont("Microsoft YaHei"))
        lbl_phone_number.move(10, 230)
        let_phone_number = QLineEdit(topFiller)
        let_phone_number.move(200, 230)
        let_phone_number.setEnabled(False)

        lbl_hourly_rate = QLabel(topFiller)
        lbl_hourly_rate.setText("每小时工资")
        lbl_hourly_rate.setFont(QFont("Microsoft YaHei"))
        lbl_hourly_rate.move(10, 260)
        let_hourly_rate = QLineEdit(topFiller)
        let_hourly_rate.move(200, 260)
        let_hourly_rate.setEnabled(False)

        lbl_salary = QLabel(topFiller)
        lbl_salary.setText("工资")
        lbl_salary.setFont(QFont("Microsoft YaHei"))
        lbl_salary.move(10, 290)
        let_salary = QLineEdit(topFiller)
        let_salary.move(200, 290)
        let_salary.setEnabled(False)

        lbl_commission_rate = QLabel(topFiller)
        lbl_commission_rate.setText("分成")
        lbl_commission_rate.setFont(QFont("Microsoft YaHei"))
        lbl_commission_rate.move(10, 320)
        let_commission_rate = QLineEdit(topFiller)
        let_commission_rate.move(200, 320)
        let_commission_rate.setEnabled(False)

        lbl_hour_limit = QLabel(topFiller)
        lbl_hour_limit.setText("每天工作上限")
        lbl_hour_limit.setFont(QFont("Microsoft YaHei"))
        lbl_hour_limit.move(10, 350)
        let_hour_limit = QLineEdit(topFiller)
        let_hour_limit.move(200, 350)
        let_hour_limit.setEnabled(False)

        btn_post = QPushButton(topFiller)
        btn_post.setText("删除")
        set_button_small(btn_post)
        btn_post.move(10, 380)

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        templayout = QFormLayout()
        templayout.addRow(lbl_name, let_name)
        templayout.addRow(lbl_employee_type, let_employee_type)
        templayout.addRow(lbl_mailing_address, let_mailing_address)
        templayout.addRow(lbl_social_security_number, let_social_security_number)
        templayout.addRow(lbl_standard_tax_deductions, let_standard_tax_deductions)
        templayout.addRow(lbl_the401k_deduction, let_the401k_deduction)
        templayout.addRow(lbl_medical_deduction, let_medical_deduction)
        templayout.addRow(lbl_phone_number, let_phone_number)
        templayout.addRow(lbl_hourly_rate, let_hourly_rate)
        templayout.addRow(lbl_salary, let_salary)
        templayout.addRow(lbl_commission_rate, let_commission_rate)
        templayout.addRow(lbl_hour_limit, let_hour_limit)
        templayout.addWidget(btn_post)

        btn_search_id.clicked.connect(lambda: self.click_search_id(2, templayout, let_employee_ID))

        self.set_size_l(btn_search_id, 180, 30)
        self.set_size_l(btn_return, 180, 30)
        self.set_size_l(let_employee_ID, 180, 30)
        self.set_size_l(lbl_employee_ID, 180, 30)
        self.set_size_l(btn_post, 380, 30)

        self.mylayout.addRow(lbl_employee_ID, let_employee_ID)
        self.mylayout.addRow(btn_search_id, btn_return)
        self.box.addLayout(Hbox)
        # self.box.addLayout(buttonbox)

    def click_modify_employee_info(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 50)
        self.employee_widget.setGeometry(100, 50, 650, 300)

        lbl_employee_ID = QLabel("员工号")
        lbl_employee_ID.setFont(QFont("Microsoft YaHei"))
        let_employee_ID = QLineEdit()

        btn_search_id = QPushButton("搜索员工")
        set_button_small(btn_search_id)

        topFiller = QWidget()
        topFiller.setMinimumSize(400, 410)  #######设置滚动条的尺寸

        scroll = QScrollArea()
        scroll.setWidget(topFiller)
        scroll.setVisible(False)

        Hbox = QHBoxLayout()
        Hbox.addWidget(scroll)
        Hbox.addStretch(0)

        lbl_name = QLabel(topFiller)
        lbl_name.setText("姓名")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        lbl_name.move(10,20)
        let_name = QLineEdit(topFiller)
        let_name.move(200, 20)

        lbl_employee_type = QLabel(topFiller)
        lbl_employee_type.setText("员工类型")
        lbl_employee_type.setFont(QFont("Microsoft YaHei"))
        lbl_employee_type.move(10, 50)
        #let_employee_type = QLineEdit(topFiller)
        let_employee_type = QComboBox(topFiller)
        let_employee_type.addItem("salaried")
        let_employee_type.addItem("commissioned")
        let_employee_type.addItem("hour")
        let_employee_type.setFixedWidth(170)
        let_employee_type.setFixedHeight(26)
        let_employee_type.move(200, 50)

        lbl_mailing_address = QLabel(topFiller)
        lbl_mailing_address.setText("邮寄地址")
        lbl_mailing_address.setFont(QFont("Microsoft YaHei"))
        lbl_mailing_address.move(10, 80)
        let_mailing_address = QLineEdit(topFiller)
        let_mailing_address.move(200, 80)

        lbl_social_security_number = QLabel(topFiller)
        lbl_social_security_number.setText("身份证号")
        lbl_social_security_number.setFont(QFont("Microsoft YaHei"))
        lbl_social_security_number.move(10, 110)
        let_social_security_number = QLineEdit(topFiller)
        let_social_security_number.move(200, 110)

        lbl_standard_tax_deductions = QLabel(topFiller)
        lbl_standard_tax_deductions.setText("扣税")
        lbl_standard_tax_deductions.setFont(QFont("Microsoft YaHei"))
        lbl_standard_tax_deductions.move(10, 140)
        let_standard_tax_deductions = QLineEdit(topFiller)
        let_standard_tax_deductions.move(200, 140)

        lbl_the401k_deduction = QLabel(topFiller)
        lbl_the401k_deduction.setText("养老保险")
        lbl_the401k_deduction.setFont(QFont("Microsoft YaHei"))
        lbl_the401k_deduction.move(10, 170)
        let_the401k_deduction = QLineEdit(topFiller)
        let_the401k_deduction.move(200, 170)

        lbl_medical_deduction = QLabel(topFiller)
        lbl_medical_deduction.setText("医保")
        lbl_medical_deduction.setFont(QFont("Microsoft YaHei"))
        lbl_medical_deduction.move(10, 200)
        let_medical_deduction = QLineEdit(topFiller)
        let_medical_deduction.move(200, 200)

        lbl_phone_number = QLabel(topFiller)
        lbl_phone_number.setText("手机号")
        lbl_phone_number.setFont(QFont("Microsoft YaHei"))
        lbl_phone_number.move(10, 230)
        let_phone_number = QLineEdit(topFiller)
        let_phone_number.move(200, 230)

        lbl_hourly_rate = QLabel(topFiller)
        lbl_hourly_rate.setText("每小时工资")
        lbl_hourly_rate.setFont(QFont("Microsoft YaHei"))
        lbl_hourly_rate.move(10, 260)
        let_hourly_rate = QLineEdit(topFiller)
        let_hourly_rate.move(200, 260)

        lbl_salary = QLabel(topFiller)
        lbl_salary.setText("工资")
        lbl_salary.setFont(QFont("Microsoft YaHei"))
        lbl_salary.move(10, 290)
        let_salary = QLineEdit(topFiller)
        let_salary.move(200, 290)

        lbl_commission_rate = QLabel(topFiller)
        lbl_commission_rate.setText("分成")
        lbl_commission_rate.setFont(QFont("Microsoft YaHei"))
        lbl_commission_rate.move(10, 320)
        #let_commission_rate = QLineEdit(topFiller)
        let_commission_rate = QComboBox(topFiller)
        let_commission_rate.addItem("10%")
        let_commission_rate.addItem("15%")
        let_commission_rate.addItem("25%")
        let_commission_rate.addItem("35%")
        let_commission_rate.setFixedWidth(170)
        let_commission_rate.setFixedHeight(26)
        let_commission_rate.move(200, 320)

        lbl_hour_limit = QLabel(topFiller)
        lbl_hour_limit.setText("每天工作上限")
        lbl_hour_limit.setFont(QFont("Microsoft YaHei"))
        lbl_hour_limit.move(10, 350)
        let_hour_limit = QLineEdit(topFiller)
        let_hour_limit.move(200, 350)

        btn_post = QPushButton(topFiller)
        btn_post.setText("修改")
        set_button_small(btn_post)
        btn_post.move(10, 380)

        # #buttonbox = QHBoxLayout()
        # # buttonbox.addWidget(btn_post)

        # lbl_name = QLabel("姓名")
        # lbl_name.setFont(QFont("Microsoft YaHei"))
        # let_name = QLineEdit()
        #
        # lbl_employee_type = QLabel("员工类型")
        # lbl_employee_type.setFont(QFont("Microsoft YaHei"))
        # let_employee_type = QLineEdit()
        #
        # lbl_mailing_address = QLabel("邮寄地址")
        # lbl_mailing_address.setFont(QFont("Microsoft YaHei"))
        # let_mailing_address = QLineEdit()
        #
        # lbl_social_security_number = QLabel("身份证号")
        # lbl_social_security_number.setFont(QFont("Microsoft YaHei"))
        # let_social_security_number = QLineEdit()
        #
        # lbl_standard_tax_deductions = QLabel("扣税")
        # lbl_standard_tax_deductions.setFont(QFont("Microsoft YaHei"))
        # let_standard_tax_deductions = QLineEdit()
        #
        # lbl_the401k_deduction = QLabel("养老保险")
        # lbl_the401k_deduction.setFont(QFont("Microsoft YaHei"))
        # let_the401k_deduction = QLineEdit()
        #
        # lbl_medical_deduction = QLabel("医保")
        # lbl_medical_deduction.setFont(QFont("Microsoft YaHei"))
        # let_medical_deduction = QLineEdit()
        #
        # lbl_phone_number = QLabel("手机号")
        # lbl_phone_number.setFont(QFont("Microsoft YaHei"))
        # let_phone_number = QLineEdit()
        #
        # lbl_hourly_rate = QLabel("每小时工资")
        # lbl_hourly_rate.setFont(QFont("Microsoft YaHei"))
        # let_hourly_rate = QLineEdit()
        #
        # lbl_salary = QLabel("工资")
        # lbl_salary.setFont(QFont("Microsoft YaHei"))
        # let_salary = QLineEdit()
        #
        # lbl_commission_rate = QLabel("分成")
        # lbl_commission_rate.setFont(QFont("Microsoft YaHei"))
        # let_commission_rate = QLineEdit()
        #
        # lbl_hour_limit = QLabel("每天工作上限")
        # lbl_hour_limit.setFont(QFont("Microsoft YaHei"))
        # let_hour_limit = QLineEdit()
        #
        # btn_post = QPushButton("修改")
        # set_button_small(btn_post)

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        templayout = QFormLayout()
        templayout.addRow(lbl_name, let_name)
        templayout.addRow(lbl_employee_type, let_employee_type)
        templayout.addRow(lbl_mailing_address, let_mailing_address)
        templayout.addRow(lbl_social_security_number, let_social_security_number)
        templayout.addRow(lbl_standard_tax_deductions, let_standard_tax_deductions)
        templayout.addRow(lbl_the401k_deduction, let_the401k_deduction)
        templayout.addRow(lbl_medical_deduction, let_medical_deduction)
        templayout.addRow(lbl_phone_number, let_phone_number)
        templayout.addRow(lbl_hourly_rate, let_hourly_rate)
        templayout.addRow(lbl_salary, let_salary)
        templayout.addRow(lbl_commission_rate, let_commission_rate)
        templayout.addRow(lbl_hour_limit, let_hour_limit)
        templayout.addWidget(btn_post)

        btn_search_id.clicked.connect(lambda: self.click_search_id(1, templayout, let_employee_ID))

        self.set_size_l(btn_search_id, 180, 30)
        self.set_size_l(btn_return, 180, 30)
        self.set_size_l(let_employee_ID, 180, 30)
        self.set_size_l(lbl_employee_ID, 180, 30)
        self.set_size_l(btn_post, 380, 30)

        self.mylayout.addRow(lbl_employee_ID, let_employee_ID)
        self.mylayout.addRow(btn_search_id, btn_return)
        self.box.addLayout(Hbox)
        # self.box.addLayout(buttonbox)

    def click_employee_info_post(self, flag, msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10, msg11, msg12,
                                 msg13="yes"):
        if flag == 1:
            temp = msg11.currentText()
            if temp == "10%":
                temp = "0.1"
            elif temp == "15%":
                temp = "0.2"
            elif temp == "25":
                temp = "0.25"
            elif temp == "35%":
                temp = "0.35"
            res = add_employee(msg1.text(), msg2.currentText(), msg3.text(), msg4.text(),
                               msg5.text(), msg6.text(), msg7.text(), msg8.text(),
                               msg9.text(), msg10.text(), temp, msg12.text())
            if (res.find("SUCCESS_")) == 0:
                reply = QMessageBox.information(self, "成功", "生成的员工号为：" + res[8:], QMessageBox.Ok)
                self.mydelete()
                app.processEvents()
                self.initUi()
            else:
                QMessageBox.warning(self, "错误", res)
        elif flag == 2:
            temp = msg12.currentText()
            if temp == "10%":
                temp = "0.1"
            elif temp == "15%":
                temp = "0.2"
            elif temp == "25":
                temp = "0.25"
            elif temp == "35%":
                temp = "0.35"
            res = update_employee(msg1.text(), msg2.text(), msg3.currentText(), msg4.text(), msg5.text(),
                                  msg6.text(), msg7.text(), msg8.text(), msg9.text(), msg10.text(), msg11.text(),
                                  temp, msg13.text())
            if res == "YES":
                QMessageBox.information(self, "提示", "修改成功", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "错误警告", res)
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setText("你确定要删除吗")
            OK = msgbox.addButton("确认", QMessageBox.AcceptRole)
            NO = msgbox.addButton("取消", QMessageBox.RejectRole)
            OK.clicked.connect(lambda: self.click_delete_ok(msg1))
            NO.clicked.connect(self.click_delete_cancel)
            reply = msgbox.exec()

    def click_delete_ok(self, msg1):
        delete_employee(msg1.text())
        reply = QMessageBox.information(self, "提示", "删除成功", QMessageBox.Ok)
        self.click_delete_employee_info()

    def click_delete_cancel(self):
        self.click_delete_employee_info()

    def click_search_id(self, flag, tmsg1, tmsg2):
        res = return_employee_info(tmsg2.text())
        if isinstance(res, tuple):
            item_list = list(range(tmsg1.count() - 1))
            for i in item_list:
                if i % 2 == 0:
                    if isinstance(tmsg1.itemAt(i + 1).widget(), type(QLineEdit())):
                        tmsg1.itemAt(i + 1).widget().setText(str(res[int(i / 2 + 1)]))
                    else:
                        tmsg1.itemAt(i + 1).widget().setCurrentText(str(res[int(i / 2 + 1)]))
                    # self.mylayout.addRow(tmsg1.itemAt(i).widget(), tmsg1.itemAt(i + 1).widget())

            # msg1 = self.mylayout.itemAt(5).widget()
            # msg2 = self.mylayout.itemAt(7).widget()
            # msg3 = self.mylayout.itemAt(9).widget()
            # msg4 = self.mylayout.itemAt(11).widget()
            # msg5 = self.mylayout.itemAt(13).widget()
            # msg6 = self.mylayout.itemAt(15).widget()
            # msg7 = self.mylayout.itemAt(17).widget()
            # msg8 = self.mylayout.itemAt(19).widget()
            # msg9 = self.mylayout.itemAt(21).widget()
            # msg10 = self.mylayout.itemAt(23).widget()
            # msg11 = self.mylayout.itemAt(25).widget()
            # msg12 = self.mylayout.itemAt(27).widget()

            msg1 = tmsg1.itemAt(1).widget()
            msg2 = tmsg1.itemAt(3).widget()
            msg3 = tmsg1.itemAt(5).widget()
            msg4 = tmsg1.itemAt(7).widget()
            msg5 = tmsg1.itemAt(9).widget()
            msg6 = tmsg1.itemAt(11).widget()
            msg7 = tmsg1.itemAt(13).widget()
            msg8 = tmsg1.itemAt(15).widget()
            msg9 = tmsg1.itemAt(17).widget()
            msg10 = tmsg1.itemAt(19).widget()
            msg11 = tmsg1.itemAt(21).widget()
            msg12 = tmsg1.itemAt(23).widget()

            # self.mylayout.addWidget(tmsg1.itemAt(24).widget())
            if flag == 1:
                tmsg1.itemAt(24).widget().clicked.connect(
                    lambda: self.click_employee_info_post(2, tmsg2, msg1, msg2, msg3, msg4,
                                                          msg5, msg6, msg7, msg8,
                                                          msg9, msg10, msg11, msg12))
            else:
                tmsg1.itemAt(24).widget().clicked.connect(
                    lambda: self.click_employee_info_post(3, tmsg2, msg1, msg2, msg3, msg4,
                                                          msg5, msg6, msg7, msg8,
                                                          msg9, msg10, msg11, msg12))

            self.box.itemAt(1).itemAt(0).widget().setVisible(True)
        else:
            reply = QMessageBox.information(self, "错误", res, QMessageBox.Ok)

    def back(self):
        self.mydelete()
        app.processEvents()
        self.initUi()

    def mydelete(self):
        self.employee_widget.move(120, 100)
        self.employee_widget.setGeometry(120, 100, 650, 260)
        item_list = list(range(self.mylayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.mylayout.itemAt(i)
            self.mylayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        box_item_list = list(range(self.box.count()))
        box_item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in box_item_list:
            if i > 0:
                box_item = self.box.itemAt(i)
                self.box.removeItem(box_item)
                if box_item.widget():
                    box_item.widget().deleteLater()

                layout_list = list(range(box_item.count()))
                layout_list.reverse()  # 倒序删除，避免影响布局顺序

                for j in layout_list:
                    layout_item = box_item.itemAt(j)
                    box_item.removeItem(layout_item)
                    if layout_item.widget():
                        layout_item.widget().deleteLater()

    def set_background(self):
        self.setWindowIcon(QIcon('logo.png'))
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("BACKGROUND.JPG")))
        self.setPalette(window_pale)

    def set_size(self,t, w, h):
        item_list = list(range(self.mylayout.count()))
        for i in item_list:
            if isinstance(self.mylayout.itemAt(i).widget(),t):
                self.mylayout.itemAt(i).widget().setFixedWidth(w)
                self.mylayout.itemAt(i).widget().setFixedHeight(h)

    def set_size_l(self, item, w, h):
            item.setFixedWidth(w)
            item.setFixedHeight(h)


class Employee(QDialog):
    def __init__(self, employee_id):
        super().__init__()

        self.employee_id = employee_id
        self.box = QVBoxLayout()
        self.mylayout = QFormLayout()
        self.employee_widget = QWidget(self)
        self.box.addLayout(self.mylayout, 0)
        self.employee_widget.setLayout(self.box)
        res = return_employee_info(self.employee_id)
        self.flag = res[2]
        self.setWindowTitle(res[1] + " - 员工操作")
        self.initUi()

    def initUi(self):
        self.mydelete()
        app.processEvents()
        self.set_background()

        btn_info = QPushButton("查看个人信息")
        set_button(btn_info)
        btn_info.clicked.connect(self.click_info)

        btn_timecard = QPushButton("打卡")
        set_button(btn_timecard)
        btn_timecard.clicked.connect(self.input_timecard)

        btn_select_payment = QPushButton("选择支付方式")
        set_button(btn_select_payment)
        btn_select_payment.clicked.connect(self.select_payment_method)

        btn_employee_report = QPushButton("员工报告")
        set_button(btn_employee_report)
        btn_employee_report.clicked.connect(self.click_employee_report)



        self.setObjectName("employee_Window")
        self.setFixedSize(600, 400)

        self.mylayout.addWidget(btn_info)
        self.mylayout.addWidget(btn_timecard)
        self.mylayout.addWidget(btn_select_payment)
        self.mylayout.addWidget(btn_employee_report)

        if self.flag == "commissioned":
            btn_maintain_orders = QPushButton("维护订单")
            set_button(btn_maintain_orders)
            btn_maintain_orders.clicked.connect(self.click_maintain_orders)
            self.mylayout.addWidget(btn_maintain_orders)

        self.mylayout.setHorizontalSpacing(20)
        self.mylayout.setVerticalSpacing(12)

    def click_info(self):
        self.mydelete()
        app.processEvents()

        self.box.removeItem(self.box.itemAt(0))
        self.employee_widget.move(10, 10)
        self.employee_widget.setGeometry(10, 10, 600, 380)

        vbox = QVBoxLayout()

        top = QWidget()
        top.setMinimumSize(550, 600)

        res = show_employee_info(self.employee_id)

        h = 10

        lbl_id = QLabel(top)
        lbl_id.setText("员工号：")
        lbl_id.setFont(QFont("Microsoft YaHei"))
        lbl_id.setFixedWidth(150)
        lbl_id.setFixedHeight(28)
        lbl_id.move(150, h)
        h += 30

        lbl_state = QLabel(top)
        lbl_state.setText("员工状态：")
        lbl_state.setFont(QFont("Microsoft YaHei"))
        lbl_state.setFixedWidth(150)
        lbl_state.setFixedHeight(28)
        lbl_state.move(150, h)
        h += 30

        lbl_name = QLabel(top)
        lbl_name.setText("姓名：")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        lbl_name.setFixedWidth(150)
        lbl_name.setFixedHeight(28)
        lbl_name.move(150, h)
        h += 30

        lbl_type = QLabel(top)
        lbl_type.setText("员工类型")
        lbl_type.setFont(QFont("Microsoft YaHei"))
        lbl_type.setFixedWidth(150)
        lbl_type.setFixedHeight(28)
        lbl_type.move(150, h)
        h += 30

        lbl_addr = QLabel(top)
        lbl_addr.setText("邮寄地址")
        lbl_addr.setFont(QFont("Microsoft YaHei"))
        lbl_addr.setFixedWidth(150)
        lbl_addr.setFixedHeight(28)
        lbl_addr.move(150, h)
        h += 30

        lbl_num = QLabel(top)
        lbl_num.setText("身份证号")
        lbl_num.setFont(QFont("Microsoft YaHei"))
        lbl_num.setFixedWidth(150)
        lbl_num.setFixedHeight(28)
        lbl_num.move(150, h)
        h += 30

        lbl_tax = QLabel(top)
        lbl_tax.setText("扣税")
        lbl_tax.setFont(QFont("Microsoft YaHei"))
        lbl_tax.setFixedWidth(150)
        lbl_tax.setFixedHeight(28)
        lbl_tax.move(150, h)
        h += 30

        lbl_ins = QLabel(top)
        lbl_ins.setText("养老保险")
        lbl_ins.setFont(QFont("Microsoft YaHei"))
        lbl_ins.setFixedWidth(150)
        lbl_ins.setFixedHeight(28)
        lbl_ins.move(150, h)
        h += 30

        lbl_ins = QLabel(top)
        lbl_ins.setText("医保")
        lbl_ins.setFont(QFont("Microsoft YaHei"))
        lbl_ins.setFixedWidth(150)
        lbl_ins.setFixedHeight(28)
        lbl_ins.move(150, h)
        h += 30

        lbl_phone = QLabel(top)
        lbl_phone.setText("手机号")
        lbl_phone.setFont(QFont("Microsoft YaHei"))
        lbl_phone.setFixedWidth(150)
        lbl_phone.setFixedHeight(28)
        lbl_phone.move(150, h)
        h += 30

        lbl_hour = QLabel(top)
        lbl_hour.setText("每小时工资")
        lbl_hour.setFont(QFont("Microsoft YaHei"))
        lbl_hour.setFixedWidth(150)
        lbl_hour.setFixedHeight(28)
        lbl_hour.move(150, h)
        h += 30

        lbl_salary = QLabel(top)
        lbl_salary.setText("每月工资")
        lbl_salary.setFont(QFont("Microsoft YaHei"))
        lbl_salary.setFixedWidth(150)
        lbl_salary.setFixedHeight(28)
        lbl_salary.move(150, h)
        h += 30

        lbl_add = QLabel(top)
        lbl_add.setText("分成")
        lbl_add.setFont(QFont("Microsoft YaHei"))
        lbl_add.setFixedWidth(150)
        lbl_add.setFixedHeight(28)
        lbl_add.move(150, h)
        h += 30

        lbl_limit = QLabel(top)
        lbl_limit.setText("每天工作时间上限")
        lbl_limit.setFont(QFont("Microsoft YaHei"))
        lbl_limit.setFixedWidth(150)
        lbl_limit.setFixedHeight(28)
        lbl_limit.move(150, h)
        h += 30

        lbl_pay = QLabel(top)
        lbl_pay.setText("支付方式")
        lbl_pay.setFont(QFont("Microsoft YaHei"))
        lbl_pay.setFixedWidth(150)
        lbl_pay.setFixedHeight(28)
        lbl_pay.move(150, h)
        h += 30

        lbl_payaddr = QLabel(top)
        lbl_payaddr.setText("支付地址")
        lbl_payaddr.setFont(QFont("Microsoft YaHei"))
        lbl_payaddr.setFixedWidth(150)
        lbl_payaddr.setFixedHeight(28)
        lbl_payaddr.move(150, h)
        h += 30

        lbl_bank = QLabel(top)
        lbl_bank.setText("银行名称")
        lbl_bank.setFont(QFont("Microsoft YaHei"))
        lbl_bank.setFixedWidth(150)
        lbl_bank.setFixedHeight(28)
        lbl_bank.move(150, h)
        h += 30

        lbl_accnum = QLabel(top)
        lbl_accnum.setText("银行账号")
        lbl_accnum.setFont(QFont("Microsoft YaHei"))
        lbl_accnum.setFixedWidth(150)
        lbl_accnum.setFixedHeight(28)
        lbl_accnum.move(150, h)
        h += 30

        for i in range(18):
            item = QLineEdit(top)
            item.setFixedHeight(28)
            item.setFixedWidth(100)
            item.setFont(QFont("Microsoft YaHei"))
            item.setText(str(res[i]))
            item.setReadOnly(True)  # 设置只读
            item.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")  # 设置无色无边框
            item.move(320, 10 + i * 30)

        btn_show_order = QPushButton(top)
        set_button(btn_show_order)
        btn_show_order.setText("查看订单")
        btn_show_order.setFixedWidth(100)
        btn_show_order.setFixedHeight(38)
        btn_show_order.move(150, h)
        btn_show_order.clicked.connect(self.click_show_order)

        btn_return = QPushButton(top)
        set_button(btn_return)
        btn_return.setText("返回")
        btn_return.setFixedWidth(100)
        btn_return.setFixedHeight(38)
        btn_return.move(320, h)
        btn_return.clicked.connect(self.click_timecard_back)

        scroll = QScrollArea()
        scroll.setWidget(top)
        vbox.addWidget(scroll)
        self.box.addLayout(vbox)

    def click_show_order(self):
        self.mydelete()
        app.processEvents()

        self.box.removeItem(self.box.itemAt(0))
        self.employee_widget.move(10, 10)
        self.employee_widget.setGeometry(10, 10, 600, 380)

        vbox = QVBoxLayout()

        top = QWidget()
        top.setMinimumSize(900, 2000)

        res = show_orders(self.employee_id)

        h = 10

        for i in res:
            lbl_oid = QLabel(top)
            lbl_oid.setText("订单号：")
            lbl_oid.setFont(QFont("Microsoft YaHei"))
            lbl_oid.setFixedWidth(60)
            lbl_oid.setFixedHeight(28)
            lbl_oid.move(10, h)

            let_oid = QLineEdit(top)
            let_oid.setFixedHeight(28)
            let_oid.setFixedWidth(210)
            let_oid.setFont(QFont("Microsoft YaHei"))
            let_oid.setText(str(i[0]))
            let_oid.setReadOnly(True)  # 设置只读
            let_oid.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")  # 设置无色无边框
            let_oid.move(80, h)

            lbl_item = QLabel(top)
            lbl_item.setText("订单物品：")
            lbl_item.setFont(QFont("Microsoft YaHei"))
            lbl_item.setFixedWidth(80)
            lbl_item.setFixedHeight(28)
            lbl_item.move(300, h)

            let_item = QLineEdit(top)
            let_item.setFixedHeight(28)
            let_item.setFixedWidth(120)
            let_item.setText(str(i[1]))
            let_item.setFont(QFont("Microsoft YaHei"))
            let_item.setReadOnly(True)  # 设置只读
            let_item.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")  # 设置无色无边框
            let_item.move(390, h)

            lbl_sale = QLabel(top)
            lbl_sale.setText("订单金额：")
            lbl_sale.setFont(QFont("Microsoft YaHei"))
            lbl_sale.setFixedWidth(80)
            lbl_sale.setFixedHeight(28)
            lbl_sale.move(520, h)

            let_sale = QLineEdit(top)
            let_sale.setFixedHeight(28)
            let_sale.setFixedWidth(80)
            let_sale.setText(str(i[2]))
            let_sale.setFont(QFont("Microsoft YaHei"))
            let_sale.setReadOnly(True)  # 设置只读
            let_sale.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")  # 设置无色无边框
            let_sale.move(610, h)

            lbl_date = QLabel(top)
            lbl_date.setText("订单日期：")
            lbl_date.setFont(QFont("Microsoft YaHei"))
            lbl_date.setFixedWidth(80)
            lbl_date.setFixedHeight(28)
            lbl_date.move(700, h)

            let_date = QLineEdit(top)
            let_date.setFixedHeight(28)
            let_date.setFixedWidth(100)
            let_date.setFont(QFont("Microsoft YaHei"))
            let_date.setText(str(i[3]))
            let_date.setReadOnly(True)  # 设置只读
            let_date.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")  # 设置无色无边框
            let_date.move(790, h)

            h += 30

        btn_return = QPushButton(top)
        set_button(btn_return)
        btn_return.setText("返回")
        btn_return.setFixedWidth(400)
        btn_return.setFixedHeight(38)
        btn_return.move(320, h)
        btn_return.clicked.connect(self.click_timecard_back)

        scroll = QScrollArea()
        scroll.setWidget(top)
        vbox.addWidget(scroll)
        self.box.addLayout(vbox)

    def click_add_order(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 60)
        self.employee_widget.setGeometry(100, 60, 600, 400)

        lbl_customer_point_of_contact = QLabel("客户联络地点")
        lbl_customer_point_of_contact.setFont(QFont("Microsoft YaHei"))
        let_customer_point_of_contact = QLineEdit()

        lbl_customer_billing_address = QLabel("客户账单地址")
        lbl_customer_billing_address.setFont(QFont("Microsoft YaHei"))
        let_customer_billing_address = QLineEdit()

        lbl_products_purchased = QLabel("购买产品")
        lbl_products_purchased.setFont(QFont("Microsoft YaHei"))
        let_products_purchased = QLineEdit()

        lbl_sale = QLabel("订单金额")
        lbl_sale.setFont(QFont("Microsoft YaHei"))
        let_sale = QLineEdit()

        lbl_date_year = QLabel("日期：(年)")
        lbl_date_year.setFont(QFont("Microsoft YaHei"))
        let_date_year = QLineEdit()

        lbl_date_month = QLabel("日期：(月)")
        lbl_date_month.setFont(QFont("Microsoft YaHei"))
        let_date_month = QLineEdit()


        lbl_date_day = QLabel("日期：(日)")
        lbl_date_day.setFont(QFont("Microsoft YaHei"))
        let_date_day = QLineEdit()

        btn_post = QPushButton("提交")
        set_button_small(btn_post)

        msg1 = let_customer_point_of_contact
        msg2 = let_customer_billing_address
        msg3 = let_products_purchased
        msg4 = let_sale
        msg5 = let_date_year
        msg6 = let_date_month
        msg7 = let_date_day

        btn_post.clicked.connect(lambda: self.click_order_post(1, msg1, msg2, msg3, msg4, msg5, msg6, msg7))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_customer_point_of_contact, let_customer_point_of_contact)
        self.mylayout.addRow(lbl_customer_billing_address, let_customer_billing_address)
        self.mylayout.addRow(lbl_products_purchased, let_products_purchased)
        self.mylayout.addRow(lbl_sale, let_sale)
        self.mylayout.addRow(lbl_date_year, let_date_year)
        self.mylayout.addRow(lbl_date_month, let_date_month)
        self.mylayout.addRow(lbl_date_day, let_date_day)
        self.mylayout.addRow(btn_return, btn_post)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

    def click_delete_order(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 20)
        self.employee_widget.setGeometry(100, 20, 600, 400)

        lbl_order_id = QLabel("订单号")
        lbl_order_id.setFont(QFont("Microsoft YaHei"))
        let_order_id = QLineEdit()

        btn_search_id = QPushButton("搜索订单信息")
        set_button_small(btn_search_id)

        lbl_employee_id = QLabel("员工号")
        lbl_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id = QLineEdit()

        lbl_customer_point_of_contact = QLabel("客户联络地点")
        lbl_customer_point_of_contact.setFont(QFont("Microsoft YaHei"))
        let_customer_point_of_contact = QLineEdit()

        lbl_customer_billing_address = QLabel("客户账单地址")
        lbl_customer_billing_address.setFont(QFont("Microsoft YaHei"))
        let_customer_billing_address = QLineEdit()

        lbl_products_purchased = QLabel("购买产品")
        lbl_products_purchased.setFont(QFont("Microsoft YaHei"))
        let_products_purchased = QLineEdit()

        lbl_sale = QLabel("订单金额")
        lbl_sale.setFont(QFont("Microsoft YaHei"))
        let_sale = QLineEdit()

        lbl_date_year = QLabel("日期：(年)")
        lbl_date_year.setFont(QFont("Microsoft YaHei"))
        let_date_year = QLineEdit()

        lbl_date_month = QLabel("日期：(月)")
        lbl_date_month.setFont(QFont("Microsoft YaHei"))
        let_date_month = QLineEdit()

        lbl_date_day = QLabel("日期：(日)")
        lbl_date_day.setFont(QFont("Microsoft YaHei"))
        let_date_day = QLineEdit()

        btn_post = QPushButton("删除")
        set_button_small(btn_post)

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_order_id, let_order_id)
        self.mylayout.addRow(btn_search_id, btn_return)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

        templayout = QFormLayout()
        templayout.addRow(lbl_employee_id, let_employee_id)
        templayout.addRow(lbl_customer_point_of_contact, let_customer_point_of_contact)
        templayout.addRow(lbl_customer_billing_address, let_customer_billing_address)
        templayout.addRow(lbl_products_purchased, let_products_purchased)
        templayout.addRow(lbl_sale, let_sale)
        templayout.addRow(lbl_date_year, let_date_year)
        templayout.addRow(lbl_date_month, let_date_month)
        templayout.addRow(lbl_date_day, let_date_day)
        templayout.addWidget(btn_post)

        btn_search_id.clicked.connect(lambda: self.click_search_id(2, templayout, let_order_id))

    def click_order_post(self, flag, msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8="yes", msg9="no"):
        if flag == 1:
            res = create_order(self.employee_id, msg1.text(), msg2.text(), msg3.text(), msg4.text(),
                               msg5.text(), msg6.text(), msg7.text())
            if (res.find("SUCCESS_")) == 0:
                reply = QMessageBox.information(self, "成功", "生成的订单号为：" + res[8:], QMessageBox.Ok)
                self.mydelete()
                app.processEvents()
                self.initUi()
            else:
                QMessageBox.warning(self, "错误", res)
        elif flag == 2:
            res = update_order(self.employee_id, msg1.text(), msg2.text(), msg3.text(), msg4.text(), msg5.text(),
                               msg6.text(), msg7.text(), msg8.text(), msg9.text())
            if res == "YES":
                QMessageBox.information(self, "提示", "修改成功", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "错误警告", res)
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setText("你确定要删除吗")
            OK = msgbox.addButton("确认", QMessageBox.AcceptRole)
            NO = msgbox.addButton("取消", QMessageBox.RejectRole)
            OK.clicked.connect(lambda: self.click_delete_ok(msg1))
            NO.clicked.connect(self.click_delete_cancel)
            reply = msgbox.exec()

    def click_delete_ok(self, msg1):
        delete_order(msg1.text(), self.employee_id)
        reply = QMessageBox.information(self, "提示", "删除成功", QMessageBox.Ok)
        self.click_delete_order()

    def click_delete_cancel(self):
        self.click_delete_order()

    def click_modify_order(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 20)
        self.employee_widget.setGeometry(100, 20, 600, 400)

        lbl_order_id = QLabel("订单号")
        lbl_order_id.setFont(QFont("Microsoft YaHei"))
        let_order_id = QLineEdit()

        btn_search_id = QPushButton("搜索订单信息")
        set_button_small(btn_search_id)

        lbl_employee_id = QLabel("员工号")
        lbl_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id = QLineEdit()

        lbl_customer_point_of_contact = QLabel("客户联络地点")
        lbl_customer_point_of_contact.setFont(QFont("Microsoft YaHei"))
        let_customer_point_of_contact = QLineEdit()

        lbl_customer_billing_address = QLabel("客户账单地址")
        lbl_customer_billing_address.setFont(QFont("Microsoft YaHei"))
        let_customer_billing_address = QLineEdit()

        lbl_products_purchased = QLabel("购买产品")
        lbl_products_purchased.setFont(QFont("Microsoft YaHei"))
        let_products_purchased = QLineEdit()

        lbl_sale = QLabel("订单金额")
        lbl_sale.setFont(QFont("Microsoft YaHei"))
        let_sale = QLineEdit()

        lbl_date_year = QLabel("日期：(年)")
        lbl_date_year.setFont(QFont("Microsoft YaHei"))
        let_date_year = QLineEdit()

        lbl_date_month = QLabel("日期：(月)")
        lbl_date_month.setFont(QFont("Microsoft YaHei"))
        let_date_month = QLineEdit()

        lbl_date_day = QLabel("日期：(日)")
        lbl_date_day.setFont(QFont("Microsoft YaHei"))
        let_date_day = QLineEdit()

        btn_post = QPushButton("提交")
        set_button_small(btn_post)

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_order_id, let_order_id)
        self.mylayout.addRow(btn_search_id, btn_return)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

        templayout = QFormLayout()
        templayout.addRow(lbl_employee_id, let_employee_id)
        templayout.addRow(lbl_customer_point_of_contact, let_customer_point_of_contact)
        templayout.addRow(lbl_customer_billing_address, let_customer_billing_address)
        templayout.addRow(lbl_products_purchased, let_products_purchased)
        templayout.addRow(lbl_sale, let_sale)
        templayout.addRow(lbl_date_year, let_date_year)
        templayout.addRow(lbl_date_month, let_date_month)
        templayout.addRow(lbl_date_day, let_date_day)
        templayout.addWidget(btn_post)

        btn_search_id.clicked.connect(lambda: self.click_search_id(1, templayout, let_order_id))

    def click_search_id(self, flag, tmsg1, tmsg2):
        res = return_order_info(tmsg2.text(), self.employee_id)

        if isinstance(res, tuple):
            item_list = list(range(tmsg1.count() - 1))
            print(item_list)
            for i in item_list:
                if i % 2 == 0:
                    print(i)
                    tmsg1.itemAt(i+1).widget().setText(str(res[int(i/2+1)]))
                    self.mylayout.addRow(tmsg1.itemAt(i).widget(), tmsg1.itemAt(i + 1).widget())
            self.mylayout.addWidget(tmsg1.itemAt(16).widget())
            msg1 = self.mylayout.itemAt(5).widget()
            msg2 = self.mylayout.itemAt(7).widget()
            msg3 = self.mylayout.itemAt(9).widget()
            msg4 = self.mylayout.itemAt(11).widget()
            msg5 = self.mylayout.itemAt(13).widget()
            msg6 = self.mylayout.itemAt(15).widget()
            msg7 = self.mylayout.itemAt(17).widget()
            msg8 = self.mylayout.itemAt(19).widget()

            self.set_size(type(QLabel()), 110, 30)
            self.set_size(type(QLineEdit()), 180, 30)

            if flag == 1:
                self.mylayout.itemAt(20).widget().clicked.connect(
                    lambda: self.click_order_post(2, tmsg2, msg1, msg2, msg3, msg4, msg5, msg6, msg7
                                                  , msg8))
            else:
                self.mylayout.itemAt(20).widget().clicked.connect(
                    lambda: self.click_order_post(3, tmsg2, msg1, msg2, msg3, msg4, msg5, msg6, msg7
                                                  , msg8))
        else:
            reply = QMessageBox.information(self, "错误", res, QMessageBox.Ok)

    def mydelete(self):
        self.employee_widget.move(120, 100)
        self.employee_widget.setGeometry(120, 100, 650, 400)
        myitem = self.box.itemAt(0)
        item_list = list(range(myitem.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = myitem.itemAt(i)
            myitem.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        box_item_list = list(range(self.box.count()))
        box_item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in box_item_list:
            if i > 0:
                box_item = self.box.itemAt(i)
                self.box.removeItem(box_item)
                if box_item.widget():
                    box_item.widget().deleteLater()

                layout_list = list(range(box_item.count()))
                layout_list.reverse()  # 倒序删除，避免影响布局顺序

                for j in layout_list:
                    layout_item = box_item.itemAt(j)
                    box_item.removeItem(layout_item)
                    if layout_item.widget():
                        layout_item.widget().deleteLater()

    def input_timecard(self):

        self.mydelete()
        app.processEvents()

        # self.setWindowIcon(QIcon('./logo.png'))
        # window_pale = QtGui.QPalette()
        # window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./background2.png")))
        # self.setPalette(window_pale)

        flag = return_card_submit(self.employee_id)
        res = return_charge_numbers(self.employee_id)
        flag1 = 0
        if flag == "NO":
            if isinstance(res, str):
                msgbox = QMessageBox()
                msgbox.setWindowTitle("提示")
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setText("无法访问项目数据库，是否要继续打卡")

                btn_ok = msgbox.addButton("是", QMessageBox.AcceptRole)
                btn_no = msgbox.addButton("否", QMessageBox.RejectRole)
                res = msgbox.exec()
                if res == QMessageBox.RejectRole:
                    self.mydelete()
                    app.processEvents()

                    self.initUi()
                    return
                else:
                    flag1 = 1

        self.box.removeItem(self.box.itemAt(0))

        self.employee_widget.move(10, 10)
        self.employee_widget.setGeometry(10, 10, 600, 380)
        time_range = return_pay_period(self.employee_id)
        num = len(time_range)
        item_list = list(range(num))

        vbox = QVBoxLayout()

        topFiller = QWidget()
        if num < 28:
            topFiller.setMinimumSize(550, 325)
        else:
            topFiller.setMinimumSize(550, 1300)  #######设置滚动条的尺寸

        save_info = ()
        for i in time_range:
            temp1 = get_ONE_timecard(self.employee_id, i[0:4], i[4:6], i[6:8])
            save_info += (temp1,)
        print("enter11111")
        print(time_range)
        print(save_info)


        msg = QFormLayout()
        for filename in item_list:
            lbl_time = QLabel(topFiller)
            lbl_time.setText("时间:")
            lbl_time.setFixedWidth(40)
            lbl_time.move(10, filename * 40)

            lbl_show_time = QLabel(topFiller)
            lbl_show_time.setText(time_range[filename])
            lbl_show_time.setFixedWidth(70)
            lbl_show_time.move(60, filename * 40)
            msg.addWidget(lbl_show_time)

            lbl_charge = QLabel(topFiller)
            lbl_charge.setText("任务类型:")
            lbl_charge.setFixedWidth(70)
            lbl_charge.move(140, filename * 40)

            if flag == "NO":
                cmobobox = QComboBox(topFiller)
                cmobobox.setFixedWidth(200)

                charge_item = ""
                flag2 = 0
                if save_info[filename][0] != "":
                    # for i in res:
                    #     if i[0] == save_info[filename][0]:
                    #         charge_item = i[1]
                    # cmobobox.addItem(save_info[filename][0] + "-" + charge_item)
                    if save_info[filename][0] != "V0000-旷工" and save_info[filename][0] != "不可修改":
                            cmobobox.addItem(save_info[filename][0])
                    elif flag1 == 1:
                        cmobobox.addItem("不可修改")
                        flag2 = 1
                elif flag1 == 1:
                    cmobobox.addItem("不可修改")
                    flag2 = 1
                if isinstance(res, tuple):
                    for i in res:
                        s = save_info[filename][0].find("-")
                        charge_item = save_info[filename][0][0:s]
                        if charge_item == "V0000" or charge_item != i[0]:
                            cmobobox.addItem(i[0] + "-" + i[1])
                cmobobox.move(220, filename * 40)
                msg.addWidget(cmobobox)

                let_time = QLineEdit(topFiller)
                let_time.setFixedWidth(40)
                if flag1 == 1 and flag2 == 1:
                    let_time.setReadOnly(True)
                    let_time.setStyleSheet("background-color:rgba(0,0,0,0);border:none;")
                    let_time.setText("0")
                else:
                    if save_info[filename][1] == "":
                        let_time.setText("0")
                    else:
                        let_time.setText(save_info[filename][1])
                let_time.move(500, filename * 40)
                msg.addWidget(let_time)
            else:
                cmobobox = QLabel(topFiller)
                cmobobox.setFixedWidth(200)
                charge_item = ""
                for i in res:
                    cmobobox.setText(save_info[filename][0])
                cmobobox.move(220, filename * 40)

                let_time = QLabel(topFiller)
                let_time.setFixedWidth(40)
                let_time.setText(save_info[filename][1])
                let_time.move(500, filename * 40)

            lbl_work_time = QLabel(topFiller)
            lbl_work_time.setText("工作时长：")
            lbl_work_time.setFixedWidth(70)
            lbl_work_time.move(430, filename * 40)

        ##创建一个滚动条
        scroll = QScrollArea()
        scroll.setWidget(topFiller)
        vbox.addWidget(scroll)

        temp_box = QHBoxLayout()
        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.click_timecard_back)
        temp_box.addWidget(btn_return)

        if flag == "NO":
            btn_save = QPushButton("保存")
            set_button_small(btn_save)
            btn_save.clicked.connect(lambda: self.click_timecard_save(msg))
            temp_box.addWidget(btn_save)

            if flag1 == 0:
                btn_submit = QPushButton("提交")
                set_button_small(btn_submit)
                btn_submit.clicked.connect(lambda: self.click_timecard_submit(msg))
                temp_box.addWidget(btn_submit)

        self.box.addLayout(vbox)
        self.box.addLayout(temp_box)

    def click_timecard_save(self, msg):
        item_list = list(range(msg.count()))
        print(item_list)
        res = ""
        for i in item_list:
            if i % 3 == 0:
                my_time = msg.itemAt(i).widget().text()
                my_charge = msg.itemAt(i+1).widget().currentText()
                my_hour = msg.itemAt(i+2).widget().text()
                print(type(my_time))
                res = save_ONE_timecard(self.employee_id, my_charge, my_hour, my_time[0:4], my_time[4:6],
                                        my_time[6:8])
        if res == "YES":
            QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "错误", "保存记录发生错误")

    def click_timecard_submit(self, msg):
        item_list = list(range(msg.count()))
        res = ""
        for i in item_list:
            if i % 3 == 0:
                my_time = msg.itemAt(i).widget().text()
                my_charge = msg.itemAt(i+1).widget().currentText()
                s = my_charge.find("-")
                my_hour = msg.itemAt(i + 2).widget().text()
                res = check_timecard(self.employee_id,  my_charge[0:s], my_hour, my_time[0:4], my_time[4:6],
                                     my_time[6:8])
                if res != "YES":
                    QMessageBox.warning(self, "错误", res)
                    break
        if res == "YES":
            res = ""
            for i in item_list:
                if i % 3 == 0:
                    my_time = msg.itemAt(i).widget().text()
                    my_charge = msg.itemAt(i+1).widget().currentText()
                    my_hour = msg.itemAt(i + 2).widget().text()
                    res = submit_timecard(self.employee_id,  my_charge[0:s], my_hour, my_time[0:4], my_time[4:6],
                                          my_time[6:8])
            if res == "YES":
                QMessageBox.information(self, "提示", "提交成功", QMessageBox.Ok)
                reverse_card_submit(self.employee_id)

    def click_timecard_back(self):
        self.mydelete()
        item = self.box.itemAt(0)
        self.box.removeItem(item)
        if item.widget():
            item.widget().deleteLater()
        self.box.addLayout(self.mylayout, 0)
        app.processEvents()
        self.initUi()

    def back(self):
        self.mydelete()
        app.processEvents()
        self.initUi()

    def select_payment_method(self):
        self.mydelete()
        app.processEvents()

        btn_pick_up = QPushButton("现金")
        set_button(btn_pick_up)
        btn_pick_up.clicked.connect(self.click_pick_up)

        btn_mail = QPushButton("邮寄")
        set_button(btn_mail)
        btn_mail.clicked.connect(self.click_mail)

        btn_bank_account = QPushButton("汇款")
        set_button(btn_bank_account)
        btn_bank_account.clicked.connect(self.click_bank_account)

        btn_return = QPushButton("返回")
        set_button(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addWidget(btn_pick_up)
        self.mylayout.addWidget(btn_mail)
        self.mylayout.addWidget(btn_bank_account)
        self.mylayout.addWidget(btn_return)

    def click_pick_up(self):
        flag = select_pick_up(self.employee_id)
        if flag == "YES":
            self.tip("修改成功")
        else:
            self.tip("修改失败")

    def click_mail(self):
        self.mydelete()
        app.processEvents()

        lbl_mail_addr = QLabel("支付地址")
        lbl_mail_addr.setFont(QFont("Microsoft YaHei"))
        let_mail_addr = QLineEdit()
        let_mail_addr.setFixedWidth(270)
        let_mail_addr.setFixedHeight(38)

        btn_post = QPushButton("提交")
        set_button(btn_post)
        btn_post.clicked.connect(lambda: self.click_post(1, let_mail_addr.text()))

        btn_return = QPushButton("返回")
        set_button(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_mail_addr, let_mail_addr)
        self.mylayout.addWidget(btn_post)
        self.mylayout.addWidget(btn_return)

    def click_bank_account(self):
        self.mydelete()
        app.processEvents()

        lbl_bank_name = QLabel("银行名称")
        lbl_bank_name.setFont(QFont("Microsoft YaHei"))
        let_bank_name = QLineEdit()
        let_bank_name.setFixedWidth(270)
        let_bank_name.setFixedHeight(38)

        lbl_bank_account = QLabel("银行账户")
        lbl_bank_account.setFont(QFont("Microsoft YaHei"))
        let_bank_account = QLineEdit()
        let_bank_account.setFixedWidth(270)
        let_bank_account.setFixedHeight(38)

        btn_post = QPushButton("提交")
        set_button(btn_post)
        btn_post.clicked.connect(lambda: self.click_post(2, let_bank_name.text(), let_bank_account.text()))

        btn_return = QPushButton("返回")
        set_button(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_bank_name, let_bank_name)
        self.mylayout.addRow(lbl_bank_account, let_bank_account)
        self.mylayout.addWidget(btn_post)
        self.mylayout.addWidget(btn_return)

    def click_post(self, flag, msg1, msg2="yes"):
        if flag == 1:
            res = select_mail(self.employee_id, msg1)
            if res == "YES":
                self.tip("success!")
            else:
                QMessageBox.warning(self, "错误", res)
        else:
            res = select_direct_deposit(self.employee_id, msg1, msg2)
            if res == "YES":
                self.tip("success!")
            else:
                QMessageBox.warning(self, "错误", res)

    def tip(self, msg):

        msgbox = QMessageBox()
        msgbox.setWindowTitle("提示")
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(msg)

        btn_ok = msgbox.addButton("完成", QMessageBox.AcceptRole)
        res = msgbox.exec()
        if res == QMessageBox.AcceptRole:
            self.mydelete()
            app.processEvents()

            self.initUi()

    def click_employee_report(self):
        # print(self.mylayout.count())

        self.mydelete()
        app.processEvents()

        btn_total = QPushButton("总工时")
        btn_total_project = QPushButton("项目工时")
        btn_vacation = QPushButton("病/休假")
        btn_pay = QPushButton("总工资")
        btn_return = QPushButton("返回")

        set_button(btn_total)
        set_button(btn_total_project)
        set_button(btn_vacation)
        set_button(btn_pay)
        set_button(btn_return)

        btn_total.clicked.connect(self.click_total)
        btn_total_project.clicked.connect(self.click_total_project)
        btn_vacation.clicked.connect(self.click_vacation)
        btn_pay.clicked.connect(self.click_pay)
        btn_return.clicked.connect(self.back)

        self.mylayout.addWidget(btn_total)
        self.mylayout.addWidget(btn_total_project)
        self.mylayout.addWidget(btn_vacation)
        self.mylayout.addWidget(btn_pay)
        self.mylayout.addWidget(btn_return)

    def click_total(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 60)
        self.employee_widget.setGeometry(100, 60, 650, 400)

        lbl_begin_year = QLabel("开始时间（年）")
        lbl_begin_year.setFont(QFont("Microsoft YaHei"))
        let_begin_year = QLineEdit()

        lbl_begin_month = QLabel("开始时间（月）")
        lbl_begin_month.setFont(QFont("Microsoft YaHei"))
        let_begin_month = QLineEdit()

        lbl_begin_day = QLabel("开始时间（日）")
        lbl_begin_day.setFont(QFont("Microsoft YaHei"))
        let_begin_day = QLineEdit()

        lbl_end_year = QLabel("结束时间（年）")
        lbl_end_year.setFont(QFont("Microsoft YaHei"))
        let_end_year = QLineEdit()

        lbl_end_month = QLabel("结束时间（月）")
        lbl_end_month.setFont(QFont("Microsoft YaHei"))
        let_end_month = QLineEdit()

        lbl_end_day = QLabel("结束时间（日）")
        lbl_end_day.setFont(QFont("Microsoft YaHei"))
        let_end_day = QLineEdit()

        btn_post = QPushButton("查询")
        set_button_small(btn_post)

        msg1 = let_begin_year
        msg2 = let_begin_month
        msg3 = let_begin_day
        msg4 = let_end_year
        msg5 = let_end_month
        msg6 = let_end_day

        btn_post.clicked.connect(lambda: self.click_report_post(1, msg1, msg2, msg3, msg4, msg5, msg6))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_begin_year, let_begin_year)
        self.mylayout.addRow(lbl_begin_month, let_begin_month)
        self.mylayout.addRow(lbl_begin_day, let_begin_day)
        self.mylayout.addRow(lbl_end_year, let_end_year)
        self.mylayout.addRow(lbl_end_month, let_end_month)
        self.mylayout.addRow(lbl_end_day, let_end_day)
        self.mylayout.addRow(btn_post, btn_return)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

    def click_report_post(self, flag, msg1, msg2, msg3, msg4, msg5, msg6, msg7="yes", msg8="no"):
        if check_connection() == "NO":
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("请求信息不可得")

            btn_ok = msgbox.addButton("确认", QMessageBox.AcceptRole)
            btn_no = msgbox.addButton("取消", QMessageBox.RejectRole)
            res = msgbox.exec()
            if res == QMessageBox.RejectRole:
                self.mydelete()
                app.processEvents()

                self.initUi()
                return
            else:
                self.mydelete()
                app.processEvents()
                if flag == 1:
                    self.click_total()
                    return
                elif flag == 2:
                    self.click_total_project()
                    return
                elif flag == 3:
                    self.click_vacation()
                    return

        if flag == 1:
            total_hour = return_total_hours_worked(self.employee_id, msg1.text(), msg2.text(), msg3.text(),
                                                   msg4.text(), msg5.text(), msg6.text())
            if isinstance(total_hour, float):
                res = create_ONE_report(self.employee_id, "All", total_hour, msg1.text(), msg2.text(), msg3.text(),
                                        msg4.text(), msg5.text(), msg6.text())
                if isinstance(res, tuple):
                    self.show_report(res, flag)
                else:
                    QMessageBox.warning(self, "错误", res)
            else:
                QMessageBox.warning(self, "错误", total_hour)
        elif flag == 2 or flag == 3:
            flag = 2
            charge_number = msg8[msg7.currentIndex()][0]
            total_hour = return_total_hours_for_a_project(self.employee_id, charge_number, msg1.text(),
                                                          msg2.text(), msg3.text(), msg4.text(), msg5.text(),
                                                          msg6.text())
            if isinstance(total_hour, float):
                print("enter11111")
                res = create_ONE_report(self.employee_id, charge_number, total_hour, msg1.text(), msg2.text(), msg3.text(),
                                        msg4.text(), msg5.text(), msg6.text())
                print("enter2")
                print(res)
                if isinstance(res, tuple):
                    self.show_report(res, flag)
                else:
                    QMessageBox.warning(self, "错误", res)
            else:
                QMessageBox.warning(self, "错误", str(total_hour))
        elif flag == 3:
            pass

    def show_report(self, res, flag):
        self.mydelete()
        app.processEvents()

        lbl_name = QLabel("姓名")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        let_name = QLabel()
        let_name.setFont(QFont("Microsoft YaHei"))
        let_name.setText(res[0][0])

        lbl_employee_id = QLabel("员工号")
        lbl_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id = QLabel()
        let_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id.setText(res[0][1])

        lbl_charge_num = QLabel("任务号")
        lbl_charge_num.setFont(QFont("Microsoft YaHei"))
        let_charge_num = QLabel()
        let_charge_num.setFont(QFont("Microsoft YaHei"))
        let_charge_num.setText(res[0][2])

        lbl_begin_time = QLabel("开始时间")
        lbl_begin_time.setFont(QFont("Microsoft YaHei"))
        let_begin_time = QLabel()
        let_begin_time.setFont(QFont("Microsoft YaHei"))
        let_begin_time.setText(res[0][3])

        lbl_end_time = QLabel("结束时间")
        lbl_end_time.setFont(QFont("Microsoft YaHei"))
        let_end_time = QLabel()
        let_end_time.setFont(QFont("Microsoft YaHei"))
        let_end_time.setText(res[0][4])

        lbl_total_hour = QLabel("工作总时长")
        lbl_total_hour.setFont(QFont("Microsoft YaHei"))
        let_total_hour = QLabel()
        let_total_hour.setFont(QFont("Microsoft YaHei"))
        let_total_hour.setText(str(res[0][5]))

        btn_save = QPushButton("生成报告")
        set_button_small(btn_save)
        btn_save.clicked.connect(lambda: self.click_save(flag, res))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_name, let_name)
        self.mylayout.addRow(lbl_employee_id, let_employee_id)
        self.mylayout.addRow(lbl_charge_num, let_charge_num)
        self.mylayout.addRow(lbl_begin_time, let_begin_time)
        self.mylayout.addRow(lbl_end_time, let_end_time)
        self.mylayout.addRow(lbl_total_hour, let_total_hour)
        self.mylayout.addRow(btn_save, btn_return)

    def click_save(self, flag, msg):
        fname = QFileDialog.getSaveFileName(self, "保存位置", "./", ".docx")
        if fname[0]:
            if flag == 1:
                res = create_doc(self.employee_id, fname[0] + fname[1], "总工时报告", msg)
                if res == "YES":
                    QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
                else:
                    pass
            elif flag == 2:
                if msg[0][2].find("V") == 0:
                    res = create_doc(self.employee_id, fname[0] + fname[1], "休假报告", msg)
                else:
                    res = create_doc(self.employee_id, fname[0] + fname[1], "项目总工时报告", msg)
                if res == "YES":
                    QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
                else:
                    pass
        elif fname[0] == '':
            pass
        else:
            QMessageBox.warning(self, "错误", "文件存储错误")

    def click_total_project(self):
            self.mydelete()
            app.processEvents()

            self.employee_widget.move(100, 60)
            self.employee_widget.setGeometry(100, 60, 650, 400)

            lbl_charge_num = QLabel("任务类型:")
            lbl_charge_num.setFont(QFont("Microsoft YaHei"))
            cmobobox = QComboBox()
            cmobobox.setFixedWidth(180)
            cmobobox.setFixedHeight(30)
            res = return_charge_numbers_noV(self.employee_id)
            if isinstance(res, tuple):
                for i in res:
                    cmobobox.addItem(i[0] + "-" + i[1])
            else:
                QMessageBox.warning(self, "错误", res)

            lbl_begin_year = QLabel("开始时间（年）")
            lbl_begin_year.setFont(QFont("Microsoft YaHei"))
            let_begin_year = QLineEdit()

            lbl_begin_month = QLabel("开始时间（月）")
            lbl_begin_month.setFont(QFont("Microsoft YaHei"))
            let_begin_month = QLineEdit()

            lbl_begin_day = QLabel("开始时间（日）")
            lbl_begin_day.setFont(QFont("Microsoft YaHei"))
            let_begin_day = QLineEdit()

            lbl_end_year = QLabel("结束时间（年）")
            lbl_end_year.setFont(QFont("Microsoft YaHei"))
            let_end_year = QLineEdit()

            lbl_end_month = QLabel("结束时间（月）")
            lbl_end_month.setFont(QFont("Microsoft YaHei"))
            let_end_month = QLineEdit()

            lbl_end_day = QLabel("结束时间（日）")
            lbl_end_day.setFont(QFont("Microsoft YaHei"))
            let_end_day = QLineEdit()

            btn_post = QPushButton("查询")
            set_button_small(btn_post)

            msg1 = let_begin_year
            msg2 = let_begin_month
            msg3 = let_begin_day
            msg4 = let_end_year
            msg5 = let_end_month
            msg6 = let_end_day
            msg7 = cmobobox

            btn_post.clicked.connect(lambda: self.click_report_post(2, msg1, msg2, msg3, msg4, msg5, msg6, msg7, res))

            btn_return = QPushButton("返回")
            set_button_small(btn_return)
            btn_return.clicked.connect(self.back)

            self.mylayout.addRow(lbl_charge_num, cmobobox)
            self.mylayout.addRow(lbl_begin_year, let_begin_year)
            self.mylayout.addRow(lbl_begin_month, let_begin_month)
            self.mylayout.addRow(lbl_begin_day, let_begin_day)
            self.mylayout.addRow(lbl_end_year, let_end_year)
            self.mylayout.addRow(lbl_end_month, let_end_month)
            self.mylayout.addRow(lbl_end_day, let_end_day)
            self.mylayout.addRow(btn_post, btn_return)

            self.set_size(type(QLabel()), 110, 30)
            self.set_size(type(QLineEdit()), 180, 30)

    def click_vacation(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 60)
        self.employee_widget.setGeometry(100, 60, 650, 400)

        lbl_charge_num = QLabel("任务类型:")
        lbl_charge_num.setFont(QFont("Microsoft YaHei"))
        cmobobox = QComboBox()
        cmobobox.setFixedWidth(180)
        cmobobox.setFixedHeight(30)
        res = (("V0001", "病假"), ("V0002", "事假"))
        if isinstance(res, tuple):
            for i in res:
                cmobobox.addItem(i[0] + "-" + i[1])
        else:
            QMessageBox.warning(self, "错误", res)

        lbl_begin_year = QLabel("开始时间（年）")
        lbl_begin_year.setFont(QFont("Microsoft YaHei"))
        let_begin_year = QLineEdit()

        lbl_begin_month = QLabel("开始时间（月）")
        lbl_begin_month.setFont(QFont("Microsoft YaHei"))
        let_begin_month = QLineEdit()

        lbl_begin_day = QLabel("开始时间（日）")
        lbl_begin_day.setFont(QFont("Microsoft YaHei"))
        let_begin_day = QLineEdit()

        lbl_end_year = QLabel("结束时间（年）")
        lbl_end_year.setFont(QFont("Microsoft YaHei"))
        let_end_year = QLineEdit()

        lbl_end_month = QLabel("结束时间（月）")
        lbl_end_month.setFont(QFont("Microsoft YaHei"))
        let_end_month = QLineEdit()

        lbl_end_day = QLabel("结束时间（日）")
        lbl_end_day.setFont(QFont("Microsoft YaHei"))
        let_end_day = QLineEdit()

        btn_post = QPushButton("查询")
        set_button_small(btn_post)

        msg1 = let_begin_year
        msg2 = let_begin_month
        msg3 = let_begin_day
        msg4 = let_end_year
        msg5 = let_end_month
        msg6 = let_end_day
        msg7 = cmobobox

        btn_post.clicked.connect(lambda: self.click_report_post(3, msg1, msg2, msg3, msg4, msg5, msg6, msg7, res))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_charge_num, cmobobox)
        self.mylayout.addRow(lbl_begin_year, let_begin_year)
        self.mylayout.addRow(lbl_begin_month, let_begin_month)
        self.mylayout.addRow(lbl_begin_day, let_begin_day)
        self.mylayout.addRow(lbl_end_year, let_end_year)
        self.mylayout.addRow(lbl_end_month, let_end_month)
        self.mylayout.addRow(lbl_end_day, let_end_day)
        self.mylayout.addRow(btn_post, btn_return)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

    def click_maintain_orders(self):
        # print(self.mylayout.count())

        self.mydelete()
        app.processEvents()

        btn_add_order = QPushButton("添加订单")
        btn_delete_order = QPushButton("删除订单")
        btn_modify_order = QPushButton("修改订单")
        btn_return = QPushButton("返回")

        set_button(btn_add_order)
        set_button(btn_delete_order)
        set_button(btn_modify_order)
        set_button(btn_return)

        btn_add_order.clicked.connect(self.click_add_order)
        btn_delete_order.clicked.connect(self.click_delete_order)
        btn_modify_order.clicked.connect(self.click_modify_order)
        btn_return.clicked.connect(self.back)

        self.mylayout.addWidget(btn_add_order)
        self.mylayout.addWidget(btn_delete_order)
        self.mylayout.addWidget(btn_modify_order)
        self.mylayout.addWidget(btn_return)

    def set_background(self):
        self.setWindowIcon(QIcon('./logo.png'))
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./BACKGROUND.JPG")))
        self.setPalette(window_pale)

    def click_pay(self):
        self.mydelete()
        app.processEvents()

        self.employee_widget.move(100, 60)
        self.employee_widget.setGeometry(100, 60, 650, 400)

        lbl_begin_year = QLabel("开始时间（年）")
        lbl_begin_year.setFont(QFont("Microsoft YaHei"))
        let_begin_year = QLineEdit()

        lbl_begin_month = QLabel("开始时间（月）")
        lbl_begin_month.setFont(QFont("Microsoft YaHei"))
        let_begin_month = QLineEdit()

        lbl_begin_day = QLabel("开始时间（日）")
        lbl_begin_day.setFont(QFont("Microsoft YaHei"))
        let_begin_day = QLineEdit()

        lbl_end_year = QLabel("结束时间（年）")
        lbl_end_year.setFont(QFont("Microsoft YaHei"))
        let_end_year = QLineEdit()

        lbl_end_month = QLabel("结束时间（月）")
        lbl_end_month.setFont(QFont("Microsoft YaHei"))
        let_end_month = QLineEdit()

        lbl_end_day = QLabel("结束时间（日）")
        lbl_end_day.setFont(QFont("Microsoft YaHei"))
        let_end_day = QLineEdit()

        msg1 = let_begin_year
        msg2 = let_begin_month
        msg3 = let_begin_day
        msg4 = let_end_year
        msg5 = let_end_month
        msg6 = let_end_day

        btn_report_post = QPushButton("提交")
        set_button_small(btn_report_post)
        btn_report_post.clicked.connect(lambda: self.click_pay_post(2, msg1, msg2, msg3, msg4, msg5, msg6))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_begin_year, let_begin_year)
        self.mylayout.addRow(lbl_begin_month, let_begin_month)
        self.mylayout.addRow(lbl_begin_day, let_begin_day)
        self.mylayout.addRow(lbl_end_year, let_end_year)
        self.mylayout.addRow(lbl_end_month, let_end_month)
        self.mylayout.addRow(lbl_end_day, let_end_day)
        self.mylayout.addRow(btn_report_post, btn_return)

        self.set_size(type(QLabel()), 110, 30)
        self.set_size(type(QLineEdit()), 180, 30)

    def click_pay_post(self, flag, msg1, msg2, msg3, msg4, msg5, msg6, msg7="yes", msg8="no"):
        if check_connection() == "NO":
            msgbox = QMessageBox()
            msgbox.setWindowTitle("提示")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("请求信息不可得")

            btn_ok = msgbox.addButton("确认", QMessageBox.AcceptRole)
            btn_no = msgbox.addButton("取消", QMessageBox.RejectRole)
            res = msgbox.exec()
            if res == QMessageBox.RejectRole:
                self.mydelete()
                app.processEvents()

                self.initUi()
                return
            else:
                self.mydelete()
                app.processEvents()
                self.click_pay()
                return

        if flag == 1:
            pass
        elif flag == 2:
            money = return_pay_YTD(self.employee_id, msg1.text(), msg2.text(), msg3.text(),
                                                   msg4.text(), msg5.text(), msg6.text())
            if isinstance(money, float):
                res = create_ONE_report_YTD(self.employee_id, money, msg1.text(), msg2.text(), msg3.text(),
                                        msg4.text(), msg5.text(), msg6.text())
                if isinstance(res, tuple):
                    self.show_pay_report(res, flag)
                else:
                    QMessageBox.warning(self, "错误", res)
            else:
                QMessageBox.warning(self, "错误", money)

    def show_pay_report(self, res, flag):
        self.mydelete()
        app.processEvents()

        lbl_name = QLabel("姓名")
        lbl_name.setFont(QFont("Microsoft YaHei"))
        let_name = QLabel()
        let_name.setFont(QFont("Microsoft YaHei"))
        let_name.setText(res[0][0])

        lbl_employee_id = QLabel("员工号")
        lbl_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id = QLabel()
        let_employee_id.setFont(QFont("Microsoft YaHei"))
        let_employee_id.setText(res[0][1])

        lbl_begin_time = QLabel("开始时间")
        lbl_begin_time.setFont(QFont("Microsoft YaHei"))
        let_begin_time = QLabel()
        let_begin_time.setFont(QFont("Microsoft YaHei"))
        let_begin_time.setText(res[0][2])

        lbl_end_time = QLabel("结束时间")
        lbl_end_time.setFont(QFont("Microsoft YaHei"))
        let_end_time = QLabel()
        let_end_time.setFont(QFont("Microsoft YaHei"))
        let_end_time.setText(res[0][3])

        lbl_payment = QLabel("工资")
        lbl_payment.setFont(QFont("Microsoft YaHei"))
        let_payment = QLabel()
        let_payment.setFont(QFont("Microsoft YaHei"))
        let_payment.setText(str(res[0][4]))

        btn_save = QPushButton("生成报告")
        set_button_small(btn_save)
        btn_save.clicked.connect(lambda: self.click_pay_save(flag, res))

        btn_return = QPushButton("返回")
        set_button_small(btn_return)
        btn_return.clicked.connect(self.back)

        self.mylayout.addRow(lbl_name, let_name)
        self.mylayout.addRow(lbl_employee_id, let_employee_id)
        self.mylayout.addRow(lbl_begin_time, let_begin_time)
        self.mylayout.addRow(lbl_end_time, let_end_time)
        self.mylayout.addRow(lbl_payment, let_payment)
        self.mylayout.addRow(btn_save, btn_return)

    def click_pay_save(self, flag, msg):
        fname = QFileDialog.getSaveFileName(self, "保存位置", "./", ".docx")
        if fname[0]:
            if flag == 1:
                pass
            elif flag == 2:
                res = create_doc_YTD(self.employee_id, fname[0] + fname[1], "工资报告", msg)
                if res == "YES":
                    QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
                else:
                    pass
        elif fname[0] == '':
            pass
        else:
            QMessageBox.warning(self, "错误", "文件存储错误")

    def set_size(self, t, w, h):
        item_list = list(range(self.mylayout.count()))
        for i in item_list:
            if isinstance(self.mylayout.itemAt(i).widget(), t):
                self.mylayout.itemAt(i).widget().setFont(QFont("Microsoft YaHei"))
                self.mylayout.itemAt(i).widget().setFixedWidth(w)
                self.mylayout.itemAt(i).widget().setFixedHeight(h)


def set_button(btn):
    btn.setFixedWidth(270)
    btn.setFixedHeight(40)
    btn.setFont(QFont("Microsoft YaHei"))
    btn.setObjectName("maintain_orders_btn")
    btn.setStyleSheet(
        "#maintain_orders_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")


def set_button_small(btn):
    btn.setFixedWidth(180)
    btn.setFixedHeight(30)
    btn.setFont(QFont("Microsoft YaHei"))
    btn.setObjectName("maintain_orders_btn")
    btn.setStyleSheet(
        "#maintain_orders_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_login = QPushButton("登录")
        self.__led_workerid = QLineEdit()
        self.__led_pwd = QLineEdit()
        self.initUI()
        self.employee = 0
        self.payrollAdministrator = 0

    def get_password(self):
        return self.__led_pwd

    def get_workerid(self):
        return self.__led_workerid

    def initUI(self):
        """
        初始化UI
        :return:
        """

        self.setObjectName("loginWindow")
        #self.setStyleSheet('#loginWindow{background-color:white}')
        #self.setStyleSheet('#loginWindow{background-image:url()}')
        #self.setStyleSheet("#loginWindow{border-image:url(./logo3.png)}")
        self.setFixedSize(410, 380)
        self.setWindowTitle("登录")

        self.setWindowIcon(QIcon('./logo.png'))
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./LOGIN.JPG")))
        self.setPalette(window_pale)

        # 登录表单内容部分
        login_widget = QWidget(self)
        login_widget.move(50, 140)
        login_widget.setGeometry(50, 140, 650, 260)

        hbox = QHBoxLayout()

        # 添加右侧表单
        fmlayout = QFormLayout()
        self.get_workerid().setFixedWidth(270)
        self.get_workerid().setFixedHeight(38)
        self.get_workerid().setPlaceholderText("账号")

        self.get_password().setEchoMode(QLineEdit.Password)
        self.get_password().setFixedWidth(270)
        self.get_password().setFixedHeight(38)
        self.get_password().setPlaceholderText("密码")

        self.btn_login.setFixedWidth(270)
        self.btn_login.setFixedHeight(38)
        self.btn_login.setFont(QFont("Microsoft YaHei"))
        self.btn_login.setObjectName("login_btn")
        self.btn_login.setStyleSheet("#login_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
        self.btn_login.clicked.connect(self.check)

        fmlayout.addRow(self.get_workerid())
        fmlayout.addRow(self.get_password())
        fmlayout.addWidget(self.btn_login)
        hbox.setAlignment(Qt.AlignCenter)
        # 调整间距
        fmlayout.setHorizontalSpacing(0)
        fmlayout.setVerticalSpacing(12)

        hbox.addLayout(fmlayout, 2)

        login_widget.setLayout(hbox)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check(self):
        ans = check_connection()
        if ans == "YES":
            res = check_login(self.get_workerid().text(), self.get_password().text())
            if res == 'PA':
                self.payrollAdministrator = PayrollAdministrator(self.get_workerid().text())
                ex.close()
                self.payrollAdministrator.show()
            elif res == 'E':
                self.employee = Employee(self.get_workerid().text())
                ex.close()
                self.employee.show()
            else:
                QMessageBox.warning(self, "错误", res)
        else:
            QMessageBox.warning(self, "错误", "请检查网络连接")


if __name__ == "__main__":
    ex = LoginForm()
    #temp = Employee('000003')
    #temp.show()
    #temp = PayrollAdministrator("000000")
    #temp.show()
    sys.exit(app.exec_())