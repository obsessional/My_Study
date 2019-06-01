#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cx_Oracle as oracle
import paramiko
from tkinter import *

class connect_linux():

    def __init__(self,ip, username, password, port=22):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, username, password)
        self.chan = self.ssh.invoke_shell()
        self.end_str = ' # \x1b[6n'

    def ssh_commd(self, command, exp_str='', recv_size=1024,timeout=120):
        self.chan.send(command + '\n')
        total_date = []
        if exp_str:
            output = self.chan.recv(recv_size)
            while not output.endswith(exp_str.encode('utf-8')):
                output = self.chan.recv(recv_size)
                total_date.append(output)
        else:
            while True:
                output = self.chan.recv(recv_size)
                if len(output) < recv_size:
                    total_date.append(output)
                    break
                else:
                    total_date.append(output)
        #转换为utf-8字符串并返回
        change_utf8 = lambda x:x.decode('utf-8', 'ignore')
        total_date = map(change_utf8,total_date)
        return ''.join(total_date)

    def ssh_close(self):
        self.ssh.close()

class Oracle_Operation(object):

    def __init__(self,bill_id):
        self.bill_id = bill_id


    def connect_zg(self,username,password,connect_str,sql):
        """
        数据库连接
        :param username:
        :param password:
        :param connect_str:
        :param sql:
        :return:
        """
        oracle.clientversion()
        con = oracle.connect(username, password, connect_str)
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # print('Result:',result)
        cursor.close()
        con.close()
        return result

    def modify_mdb_data(self):
        """
        修改数据
        :return:
        """
        sql = "select acct_id m_llAcctId,sphone_id m_szImsi,phone_id m_szMsisdn,serv_id m_llServId,cust_id m_llCustId," \
              "region_code m_nRegionCode from zg.crm_user where phone_id='"+str(self.bill_id)+"'"
        username = 'zg'
        password = 'ngBOSS4,123'
        connect_str = '10.7.5.164:1521/ngtst02'
        zg_data = self.connect_zg(username,password,connect_str,sql)
        # print(sql)
        # print("====>",zg_data)
        if zg_data and len(zg_data[0])==6:
            delete_sql1 = "delete from CRtUser where m_szMsisdn = '" + zg_data[0][2] + "';"
            delete_sql2 = "delete from crtaccount where m_llAcctId = " + str(zg_data[0][0] )+ ";"
            delete_sql3 = "delete from crtcustomer where m_llCustId= " + str(zg_data[0][4]) + ";"
            # print('delete_sql1-->',delete_sql1)
            # print('delete_sql2-->', delete_sql2)
            # print('delete_sql3-->', delete_sql3)

            insert_sql1="insert into CRtUser(m_llAcctId, m_szImsi, m_szMsisdn, m_llServId, m_llCustId, m_nRegionCode, m_dValidDate, m_dExpireDate) values(" \
                 + str(zg_data[0][0]) +",'" + zg_data[0][1] + "','" + zg_data[0][2] + "'," + str(zg_data[0][3]) + "," + str(zg_data[0][4]) + "," + \
                 str(zg_data[0][5]) +", '20010415000000', '20290101000000');"
            insert_sql2="insert into CRtAccount(m_llAcctId, m_nRegionCode, m_dValidDate, m_dExpireDate) values(" \
                 + str(zg_data[0][0]) +"," + str(zg_data[0][5])+", '20010415000000', '20290101000000');"
            insert_sql3="insert into CRtCustomer(m_llCustId, m_nRegionCode, m_dValidDate, m_dExpireDate) values(" \
                 + str(zg_data[0][4]) +"," +str(zg_data[0][5])+", '20010415000000', '20290101000000');"
            # print('insert_sql-->', insert_sql1)
            # print('insert_sql2-->', insert_sql2)
            # print('insert_sql3-->', insert_sql3)
        else:
            raise FileExistsError("there not are data in zg.crm_user table")
        cl = connect_linux("10.7.5.125", "bjzc", "bjzc")
        try:
            output = cl.ssh_commd("routemdb","mdb>>")
            # print(output)
            output = cl.ssh_commd(delete_sql1, "mdb>>")
            # print(output)
            output = cl.ssh_commd(delete_sql2, "mdb>>")
            # print(output)
            output = cl.ssh_commd(delete_sql3, "mdb>>")
            # print(output)
            output = cl.ssh_commd(insert_sql1, "mdb>>")
            # print(output)
            output = cl.ssh_commd(insert_sql2, "mdb>>")
            # print(output)
            output = cl.ssh_commd(insert_sql3, "mdb>>")
            # print(output)
        finally:
            cl.ssh_close()


if __name__ == "__main__":

#     bill_id="13501246645"
#     Oracle_Operation = Oracle_Operation(bill_id)
#     Oracle_Operation.modify_mdb_data()
    root = Tk()
    root.title("修改准发布MDB数据")
    root.geometry("300x100+10+20")
    # 按扭调用的函数，
    def reg():
        billid = bill_id.get()
        if billid:
            try:
                oo = Oracle_Operation(billid)
                oo.modify_mdb_data()
            except (FileExistsError):
                l_msg['text'] = '账管crm_user表缺少数据，修改失败'
            else:
                l_msg['text'] = '修改成功'
        else:
            l_msg['text'] = '请输入号码'

    # 第一行，用户名标签及输入框
    bill_id = Label(root, text='输入手机号码：')
    bill_id.grid(row=0, sticky=W)
    bill_id =Entry(root)
    bill_id.grid(row=0,column=1,sticky=E)

    # 第三行登陆按扭，command绑定事件
    b_login = Button(root, text='修改', command=reg)
    b_login.grid(row=1, column=1, sticky=E)

    # 登陆是否成功提示
    l_msg = Label(root, text='')
    l_msg.grid(row=3)

    root.mainloop()