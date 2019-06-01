#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import paramiko
import datetime
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

class collect_logs(object):
    def __init__(self, cluster_name,user='',local_path='',start_time='',end_time=''):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect("10.7.5.48", 22, 'haproxy', 'HaCrm-123')
        self.chan = self.ssh.invoke_shell()
        self.cn = cluster_name
        self.end_str = ' # \x1b[6n'
        if local_path:
            self.filepath = local_path.replace('\\', '\\\\')
        else:
            self.filepath = 'D:'
        if cluster_name == 'web-crm-yyt':
            self.kluster_id = "483"
            self.cmd1 = "docker ps |grep "
            self.log_file = "/opt/tomcat/logs/web-crm-yyt-"
        if cluster_name == 'wf-gsm':
            self.kluster_id = "489"
            self.cmd1 = "docker ps |grep wf-gsm |awk '{ print $1 }'"
            self.log_file = "/opt/wf-gsm/logs/wf-gsm-WFGSM*.log"
        if cluster_name == 'busi-ocrm-yyt':
            self.kluster_id = "481"
            self.cmd1 = "docker ps |grep "
            self.log_file = "topt/busi-ocrm/logs/busi-ocrm-yyt-"
        if cluster_name == 'busi-rule-yyt':
            self.kluster_id = "482"
            self.cmd1 = "docker ps |grep "
            self.log_file = "/opt/busi-rule/logs/busi-rule-yyt-"
        if cluster_name == 'busi-ord-yyt':
            self.kluster_id = "478"
            self.cmd1 = "docker ps |grep "
            self.log_file = "/opt/busi-ord/logs/busi-ord-yyt-"
        if cluster_name == 'busi-pre-yyt':
            self.kluster_id = "535"
            self.cmd1 = "docker ps |grep "
            self.log_file = "/opt/busi-pre/logs/busi-pre-yyt-"
        if user:
            self.grep_user = ' |grep '+ user
        else:self.grep_user = ''
        if start_time or end_time:
            pass

    def get_hostip_port(self):
        """
        :param kluster_id: "web-crm-yyt": "483", "wf-gsm": "513", "busi-ocrm-yyt": "481"
        :return: 
        """""
        loginUrl = 'http://bjenv:9020/acc/page/aG9tZQ==/pc/service?action=LOCAL_BUSI_OPERATOR_LOGIN&isconvert=true'
        postData = {"parameter0":"10admin","parameter1":"123456"}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
        "Connection": "keep-alive"}
        #登陆应用托管平台
        session = requests.session()
        rs = session.post(loginUrl, data=postData,verify=False)
        #查询IP和端口
        url2 = 'http://bjenv:9020/acc/page/aG9tZQ==/pc/service?action=IKlusterAdvanceSV.queryRunningInstance&isconvert=true'
        body = {"start": 1, "end": 12, "kluster": {"id": "478"}}
        body["kluster"]["id"]=self.kluster_id
        body = json.dumps(body)
        response = session.post(url2, data=body, headers=headers)
        aa = response.content.decode('utf-8')
        aa = json.loads(aa)
        nodeIp = aa["instances"][0]["nodeIp"]
        ports = aa["instances"][0]["ports"]
        port = ports.split(",")[0]
        session.close()
        return nodeIp, port

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

    def get_logs(self,nodeIp, port):
        command = "ssh crmddzx@" + nodeIp
        output = self.ssh_commd(command, 'password: ')
        output = self.ssh_commd('dcos@01', '$ ')
        if self.cmd1 == "docker ps |grep ":
            cmd1=self.cmd1 + str(port) + " |awk '{ print $1 }'"
        else:
            cmd1=self.cmd1
        self.ssh_commd(cmd1, '$ ')
        docker_id = output.split('\r\n')[0]
        cmd2 = "docker exec -ti " + str(docker_id) + " sh"
        self.ssh_commd(cmd2, self.end_str)
        tmp_file = "\logs_"+self.cn+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".log"
        if self.cn == "wf-gsm":
            cmd3="tail -n 2000 " + self.log_file
        else:
            cmd3="tail -n 2000 " + self.log_file + docker_id + ".log" + self.grep_user
        self.ssh_commd(cmd3, self.end_str)
        with open(self.filepath+tmp_file, 'w+') as f:
            f.writelines(output)
    def close(self):
        self.ssh.close()

if __name__ == "__main__":
    # 支持的集群：{"web-crm-yyt", "wf-gsm", "busi-ocrm-yyt", "busi-rule-yyt", "busi-ord-yyt"}
    # a = input('please input cluster name: ')
    a='busi-pre-yyt'
    name=''
    local_path=''
    collect_logs = collect_logs(a,name,local_path)
    nodeIp, port = collect_logs.get_hostip_port()
    collect_logs.get_logs(nodeIp, port)
    collect_logs.close()

# root = Tk()
# root.title("收集联调测试环境日志")
# root.geometry("350x150+10+20")
#
# def selectPath():
#     path_ = askdirectory()
#     path.set(path_)
#
# # 集群选择下拉菜单
# Label(root, text="集群名:").grid(row=1,column=0)
# cmb = ttk.Combobox(root)
# # cmb.pack()
# cmb.grid(row=1, column=1, padx=10, pady=5)
# cmb['value'] = ("busi-pre-yyt","web-crm-yyt", "wf-gsm", "busi-ocrm-yyt", "busi-rule-yyt", "busi-ord-yyt")  # 设置下拉菜单中的值
# cmb.current(0)  #下拉框中默认值
#
# #筛选框
# # ttk.Label(root, text="操作员:").grid(row=3,column=0)  #row 行
# Label(root, text="筛选(可不填):").grid(row=3,column=0)  #row 行
#
# path = StringVar()
# Label(root, text="路径(默认D盘):").grid(row=5,column=0)
# e1 = Entry(root)
# e1.grid(row=3, column=1, padx=10, pady=5)
# e2 = Entry(root, textvariable = path).grid(row = 5, column = 1)
# Button(root, text = "路径选择", command = selectPath).grid(row = 5, column = 2)
#
# # 默认值中的内容为索引，从0开始
# def show():
#     cluster_name = cmb.get()
#     user = e1.get()
#     local_path = path.get()
#     cl = collect_logs(cluster_name,user,local_path)
#     nodeIp, port = cl.get_hostip_port()
#     cl.get_logs(nodeIp, port)
#     cl.close()
#
# Button(root, text="获取日志", width=10, command=show).grid(row=9, column=0, sticky=W, padx=10, pady=5)
# Button(root, text="退出", width=10, command=root.destroy).grid(row=9, column=1, sticky=E, padx=10, pady=5)
#
# mainloop()





