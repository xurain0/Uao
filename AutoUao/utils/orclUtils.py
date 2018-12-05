# -*- coding: utf-8 -*-
'''
Created on 2018-5-21

@author: xu.ren
'''
import cx_Oracle
from AutoUao.config.conf import *
from AutoUao.utils.doconfiniUtils import DoConfIni
import os
import datetime

class orclUtils(object):

    def __init__(self):
        config_File = os.path.join(currPath, 'config.ini')
        read_ini = DoConfIni()
        self.username = read_ini.getConfValue(config_File, 'dbinfo', 'username')
        self.password = read_ini.getConfValue(config_File, 'dbinfo', 'password')
        self.hostname = read_ini.getConfValue(config_File, 'dbinfo', 'hostname')
        #config_File = 'E:/TestPlatform/Uao/AutoUao/config/'
        # self.username = 'party'
        # self.password = 'oracle'
        # self.hostname = '172.24.118.8:1521/tbdb'

    def connOrcl(self, sql):
        code = 0
        errmsg = ""
        res = ""
        try:
            conn = cx_Oracle.connect(self.username, self.password, self.hostname)
            cr = conn.cursor()
            cr.execute(sql)
            res = cr.fetchall()
            cr.close()
            conn.commit()
            conn.close()

        except Exception as e:
            errmsg = e.args[0]
            code = -1

        return code, errmsg, res

    def getMaxSeqNo(self, sql):
        result = []
        v = self.connOrcl(sql)
        for row in v[2]:
            for i in row:
                value = i
                result.append(str(value))
        return result[0]


if __name__ == "__main__":

    a = orclUtils()
    # processingno = '1775900'
    processingnosql = 'select t.settingvalue from t_inesetting t where t.settingkey = \'IN_MAX_NO\''
    # #operationsql = 'select * from party.t_operationlog t where t.logdesc like \'%ProcessingNo: '+processingno+'%\''
    # b = a.getValue(processingnosql)
    #c = a.getMaxSeqNo(processingnosql)
    #sql = 'select * from t_SeqProcess t  where t.seqno > 8000000166 '
    sql = 'select * from t_ineSeqProcess t  where t.seqno = 14'
    c = a.connOrcl(sql)
    print(c)
    # print str(c[2][0][0])
    # id = ['1775890']
    #
    # d = datetime.datetime.now()
    # date = d.year, d.month, d.day
    # print '%s%s%s'%date
    # f = str(datetime.date.today()).replace('-', '')
    # print f