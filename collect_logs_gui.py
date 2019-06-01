#!/usr/bin/env python
# -*- coding: utf-8 -*-

from My_Study.asdff import collect_logs
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("收集联调测试环境日志")
root.geometry("300x200+10+20")

# 创建下拉菜单
Label(root, text="集群名:").grid(row=1,column=0)
cmb = ttk.Combobox(root)
# cmb.pack()
cmb.grid(row=1, column=1, padx=10, pady=5)
cmb['value'] = ("web-crm-yyt", "wf-gsm", "busi-ocrm-yyt", "busi-rule-yyt", "busi-ord-yyt")  # 设置下拉菜单中的值
cmb.current(0)  #设置默认值，即默认下拉框中的内容

#搜索框
ttk.Label(root, text="操作员:").grid(row=3,column=0)  #row 行
Label(root, text="操作员(可不填):").grid(row=3,column=0)

ttk.Label(root, text="本地保存路径").grid(row=5,column=0)
Label(root, text="保存路径(默认D盘):").grid(row=5,column=0)
e1 = Entry(root)
e2 = Entry(root)
e1.grid(row=3, column=1, padx=10, pady=5)
e2.grid(row=5, column=1, padx=10, pady=5)

# 默认值中的内容为索引，从0开始
def show():
    cluster_name = cmb.get()
    user = e1.get()
    local_path = e2.get()
    cl = collect_logs(cluster_name,user,local_path)
    nodeIp, port = cl.get_hostip_port()
    cl.get_logs(nodeIp, port)
    cl.close()
    # e1.delete(0, END)
    # e2.delete(0, END)

# 如果表格大于组件，那么可以使用sticky选项来设置组件的位置
# 同样你需要使用N，E，S,W以及他们的组合NE，SE，SW，NW来表示方位
Button(root, text="获取日志", width=10, command=show).grid(row=9, column=0, sticky=W, padx=10, pady=5)
Button(root, text="退出", width=10, command=root.quit()).grid(row=9, column=1, sticky=E, padx=10, pady=5)

mainloop()
