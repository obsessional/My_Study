#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cx_Oracle as oracle

class Oracle_Operation(object):

    def __init__(self):
        pass

    def connect(self):
        sql='select t.*,t.rowid from crmpre.pre_order t where t.pre_order_id=10010000001755 order by t.create_date desc'
        oracle.clientversion()
        username = 'crmpre'
        password = 'pl,12345'
        connect_str = '172.30.243.100:1521/yydb'
        con = oracle.connect(username, password, connect_str)
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        cursor.close()
        con.close()



    def select(self):
        pass

    def insert(self):
        pass

    def update(self):
        pass


if __name__ == "__main__":

    Oracle_Operation = Oracle_Operation()
    Oracle_Operation.connect()