#coding:utf-8
from AutoUao.config.conf import *
import time
import datetime
from AutoUao.config.conf import *
from AutoUao.utils import *

#
# def analysisTestResult(self, local_dir, inseqno, group):
#     # xml文件数据转成input.json，oralce中流水表数据转成output.json
#     # 统一开户业务流水表中直到seqno=配置文件seqno，对比这条流水与xml配置文件信息是否一致
#     if type == 'ine_person':
#         f1 = '../results/inePersonInput.json'
#         print('put xml data into InePersonInput json file')
#         self.x2j.personInfo(local_dir, f1, group)
#     if type == 'ine_organ':
#         f1 = '../results/ineOrganInput.json'
#         print('put xml data into IneOrganInput json file')
#         self.x2j.organInfo(local_dir, f1, group)
#     if type == 'ine_specialorgan':
#         f1 = '../results/ineSpecialorganInput.json'
#         print('put xml data into IneSpecialorganInput json file')
#         self.x2j.specialorganInfo(local_dir, f1, group)
#     if type == 'ine_asset':
#         f1 = '../results/ineAssetInput.json'
#         print('put xml data into IneAssetInput json file')
#         self.x2j.assetInfo(local_dir, f1, group)
#     if type == 'shfe_person':
#         f1 = '../results/shfePersonInput.json'
#         print('put xml data into InePersonInput json file')
#         self.x2j.personInfo(local_dir, f1, group)
#     if type == 'shfe_organ':
#         f1 = '../results/shfeOrganInput.json'
#         print('put xml data into IneOrganInput json file')
#         self.x2j.organInfo(local_dir, f1, group)
#     if type == 'shfe_specialorgan':
#         f1 = '../results/shfeSpecialorganInput.json'
#         print('put xml data into IneSpecialorganInput json file')
#         self.x2j.specialorganInfo(local_dir, f1, group)
#     if type == 'shfe_asset':
#         f1 = '../results/shfeAssetInput.json'
#         print('put xml data into IneAssetInput json file')
#         self.x2j.assetInfo(local_dir, f1, group)
#     # findinMaxNosql = 'select t.settingvalue from t_inesetting t where t.settingkey = \'IN_MAX_NO\''
#     # sSeqNosql = 'select max(t.seqno) from t_ineSeqProcess t  where t.sender = \'cfmmc\''
#     # 查找执行完uao后，落地t_setting后已经收到到最大seqno，如果t_SeqProcess业务流水表中seqno=刚才接收到的
#     # 最大seqno，则流水写入，对比流水中的数据与传入的数据。
#     if group == 'ine':
#         findinMaxNosql = self.cmd.readXml('find_ine_inMaxNosql', self.backInfo_File)
#         sSeqNosql = self.cmd.readXml('ine_SeqNosql', self.backInfo_File)
#         analysisSendsql = 'select * from t_ineSeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno
#         flag = False
#         while True:
#             inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
#             sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
#             if int(sSeqNo) == int(inMaxNo):
#                 flag = True
#                 print('put t_SeqProcess data into json file')
#                 if type == 'ine_person':
#                     f2 = '../results/personOutput.json'
#                     self.o2j.personData(analysisSendsql, f2)
#                 if type == 'ine_organ':
#                     f2 = '../results/organOutput.json'
#                     self.o2j.organData(analysisSendsql, f2)
#                 if type == 'ine_specialorgan':
#                     f2 = '../results/specialorganOutput.json'
#                     self.o2j.specialorganData(analysisSendsql, f2)
#                 if type == 'ine_asset':
#                     f2 = '../results/assetOutput.json'
#                     self.o2j.assetData(analysisSendsql, f2)
#                 print('compare outputfile with inputfile')
#                 self.compf.compareFile(f1, f2)
#             if flag:
#                 break
#     elif group == 'shfe':
#         findinMaxNosql = self.cmd.readXml('find_shfe_inMaxNosql', self.backInfo_File)
#         sSeqNosql = self.cmd.readXml('shfe_SeqNosql', self.backInfo_File)
#         analysisSendsql = 'select * from t_SeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno
#         flag = False
#         while True:
#             inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
#             sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
#             if int(sSeqNo) == int(inMaxNo):
#                 flag = True
#                 print('put t_SeqProcess data into json file')
#                 if type == 'shfe_person':
#                     f2 = '../results/personOutput.json'
#                     self.o2j.personData(analysisSendsql, f2)
#                 if type == 'shfe_organ':
#                     f2 = '../results/organOutput.json'
#                     self.o2j.organData(analysisSendsql, f2)
#                 if type == 'shfe_specialorgan':
#                     f2 = '../results/specialorganOutput.json'
#                     self.o2j.specialorganData(analysisSendsql, f2)
#                 if type == 'shfe_asset':
#                     f2 = '../results/assetOutput.json'
#                     self.o2j.assetData(analysisSendsql, f2)
#                 print('compare outputfile with inputfile')
#                 self.compf.compareFile(f1, f2)
#             if flag:
#                 break
#
#     def getResult(self, inseqno, respseqno, type):
#         #clientregionsql=1,4境内客户不需要页面审核，境外需要页面审核
#         #time.sleep(60)
#         print('ananlysis table SeqProcess response')
#         start = time.clock()
#         flag = False
#         clientregionsql = 'select t.clientregion,t.processingno from t_ineSeqProcess t  where t.sender = \'cfmmc\'  and t.seqno > '+inseqno
#         clientregion = self.orcl.connOrcl(clientregionsql)[2]
#         print(clientregion)
#         processingnolist = []
#         count = 0
#         length = len(clientregion)
#         for c in clientregion:
#             clientregionNo = int(c[0])
#             processingno = str(c[1])
#             #clientregionNo = 2,3 境外客户,找出境外客户的processingno，利用processingno在业务进行备案审核
#             if clientregionNo == 2 or clientregionNo == 3:
#                 count = count + 1
#                 while True:
#                     #查询t_operationlog，直到processingno这条记录处理完，去页面处理
#                     operationsql = 'select * from party.t_operationlog t where t.logdesc like \'%ProcessingNo: '+processingno+'%\''
#                     print(operationsql)
#                     operationHasValue = self.orcl.connOrcl(operationsql)[2]
#                     if operationHasValue != []:
#                         processingnolist.append(str(processingno))
#                         flag = True
#                     print(processingnolist)
#                     if flag:
#                         break
#             #clientregionNo = 1,4 境内客户
#             elif clientregionNo == 1 or clientregionNo == 4:
#                 #length查出共有几条请求数据要处理，count查出几天数据是境外请求的。num为剩下的几条境内要处理的数据
#                 num = length - count
#                 if num > 0:
#                     for n in range(1, num+1):
#                         while True:
#                             #查询t_ineSeqProcess返回给监控中心的数据是否处理。如果exreturncode=0表示处理成功。
#                             end = time.clock()
#                             if int(end - start) == 600:
#                                 print('waiting for 10 min ,cant get result .Timeout!')
#                                 break
#                             #初始的seqno加上递增的num
#                             rSeqno = int(respseqno) + n
#                             analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_ineSeqProcess t  where t.sender = \'N\' and t.seqno ='+str(rSeqno)+' order by t.seqno desc'
#                             maxSeqnosql = 'select max(t.seqno) from t_ineSeqProcess t  where t.sender = \'N\' '
#                             maxRseqno = self.getValue(maxSeqnosql)[0]
#                             if int(maxRseqno) >= int(rSeqno):
#                                 flag = True
#                                 analysisRes = self.orcl.connOrcl(analysisRessql)[2]
#                                 for i in analysisRes:
#                                     if i[1] != 0:
#                                         print('seqno = '+str(i[0])+' operate filed and errmsg: ' + str(i[2]))
#                                     else:
#                                         print('seqno = '+str(i[0])+' operate success and sucmsg: ' + str(i[2]))
#                                 print('ananlysis result end')
#                             if flag:
#                                 break
#         #存在境外客户的数据需要页面进行备案审核
#         if count > 0:
#             maxRsqnoplus = int(maxRseqno) + count + 1
#             print('selenium Account Record begin')
#             print(processingnolist)
#             test_Uao.accountRecord.review(type, processingnolist)
#             print('selenium Account Record end')
#             for r in range(maxRseqno+1, maxRsqnoplus):
#                 analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_ineSeqProcess t  where t.sender = \'N\' and t.seqno ='+str(r)+' order by t.seqno desc'
#                 analysisRes = self.orcl.connOrcl(analysisRessql)[2]
#                 for i in analysisRes:
#                     if i[1] != 0:
#                         print('seqno = '+str(i[0])+' operate filed and errmsg: ' + str(i[2]))
#                     else:
#                         print('seqno = '+str(i[0])+' operate success and sucmsg: ' + str(i[2]))
#                 print('ananlysis result end')


# log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)
# config_File = os.path.join(currPath, 'config.ini')
# jsonfile = DoConfIni().getConfValue(config_File, 'result', 'jsonfile')
# print(os.path.join(jsonfile, 'js1.json'))
#
# json_file = DoConfIni().getConfValue(config_File, 'result', 'jsonfile')
# f1 = os.path.join(json_file, 'inePersonInput.json')
# print(f1)
# import sys
# class dd(object):
#     def nihao(self):
#         start = time.perf_counter()
#         end = time.perf_counter()
#         print(end)
#         print(end - start)
#         sys.exit()
#     def hf(self):
#         print('jjjj')
# a = dd()
# a.nihao()
# a.hf()


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-19 09:47:17
# @Author  : He Liang (helianghit@foxmail.com)
# @Link    : https:#github.com/HeLiangHIT

import random, datetime

'''
排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位校验码:
1、地址码 
表示编码对象常住户口所在县(市、旗、区)的行政区域划分代码，按GB/T2260的规定执行。
2、出生日期码 
表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。 
3、顺序码 
表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。 
4、校验码计算步骤
    (1)十七位数字本体码加权求和公式 
    S = Sum(Ai * Wi), i = 0, ... , 16 ，先对前17位数字的权求和 
    Ai:表示第i位置上的身份证号码数字值(0~9) 
    Wi:7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 （表示第i位置上的加权因子）
    (2)计算模 
    Y = mod(S, 11)
    (3)根据模，查找得到对应的校验码 
    Y: 0 1 2 3 4 5 6 7 8 9 10 
    校验码: 1 0 X 9 8 7 6 5 4 3 2
'''


def getValidateCheckout(id17):
    '''获得校验码算法'''
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 十七位数字本体码权重
    validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值

    sum = 0
    mode = 0
    for i in range(0, len(id17)):
        sum = sum + int(id17[i]) * weight[i]
    mode = sum % 11
    return validate[mode]


def getRandomIdNumber(sex=1):
    '''产生随机可用身份证号，sex = 1表示男性，sex = 0表示女性'''
    # 地址码产生
    from AutoUao.test.addr import addr  # 地址码
    addrInfo = random.randint(0, len(addr))  # 随机选择一个值
    addrId = addr[addrInfo][0]
    addrName = addr[addrInfo][1]
    idNumber = str(addrId)
    # 出生日期码
    start, end = "1960-01-01", "2000-12-30"  # 生日起止日期
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birthDays = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
    idNumber = idNumber + str(birthDays)
    # 顺序码
    for i in range(2):  # 产生前面的随机值
        n = random.randint(0, 9)  # 最后一个值可以包括
        idNumber = idNumber + str(n)
    # 性别数字码
    sexId = random.randrange(sex, 10, step=2)  # 性别码
    idNumber = idNumber + str(sexId)
    # 校验码
    checkOut = getValidateCheckout(idNumber)
    idNumber = idNumber + str(checkOut)
    return idNumber, addrName, addrId, birthDays, sex, checkOut


# def getInfoFromId(id18):
#     '''从身份证号码中得出个人信息：地址、生日、性别'''
#     addrId = id18[0:6]
#     from AutoUao.test.addr import addr  # 地址码
#     for it in addr:
#         if addrId == str(it[0]):  # 校验码
#             addrName = it[1]
#             break
#     else:  # 未被break终止
#         addrName = 'unknown'
#
#     birthDays = datetime.datetime.strftime(datetime.datetime.strptime(id18[6:14], "%Y%m%d"), "%Y-%m-%d")
#     sex = 'man' if int(id18[-2]) % 2 else 'woman'  # 0为女性，1为男性
#
#     return addrName, birthDays, sex

def getInfoFromId(id18):
    '''从身份证号码中得出个人信息：地址、生日、性别'''

    birthDays = datetime.datetime.strftime(datetime.datetime.strptime(id18[6:14], "%Y%m%d"), "%Y-%m-%d")
    sex = 'man' if int(id18[-2]) % 2 else 'woman'  # 0为女性，1为男性

    return birthDays, sex
if __name__ == '__main__':
    # print getValidateCheckout("11111111111111111")#该身份证校验码：0
    # a = getRandomIdNumber(0)
    # print(a)
    # print(a[0])
    # b = getInfoFromId(a[0])
    # print(b)
    # print(getRandomIdNumber(0))
    print(getInfoFromId('522424199512121010')[0])



