#coding = utf-8
'''
Code description：analysis result
Create time：20181030
Developer：xurain
'''
from AutoUao.utils import *
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class GetResult(object):
    accountRecord = seleniumAccountRecordUtils()

    def getResult(self, inseqno, respseqno, type, group):
        # clientregionsql=1,4境内客户不需要页面审核，境外需要页面审核
        # time.sleep(60)
        print('ananlysis table SeqProcess response')
        start = time.clock()
        flag = False
        if group == 'ine':
            clientregionsql = 'select t.clientregion,t.processingno from t_ineSeqProcess t  where t.sender = \'cfmmc\'  and t.seqno > ' + inseqno
        elif group == 'shfe':
            clientregionsql = 'select t.clientregion,t.processingno from t_SeqProcess t  where t.sender = \'cfmmc\'  and t.seqno > ' + inseqno
        clientregion = self.orcl.connOrcl(clientregionsql)[2]
        print(clientregion)
        processingnolist = []
        count = 0
        length = len(clientregion)
        for c in clientregion:
            clientregionNo = int(c[0])
            processingno = str(c[1])
            # clientregionNo = 2,3 境外客户,找出境外客户的processingno，利用processingno在业务进行备案审核
            if clientregionNo == 2 or clientregionNo == 3:
                count = count + 1
                while True:
                    # 查询t_operationlog，直到processingno这条记录处理完，去页面处理
                    operationsql = 'select * from party.t_operationlog t where t.logdesc like \'%ProcessingNo: ' + processingno + '%\''
                    print(operationsql)
                    operationHasValue = self.orcl.connOrcl(operationsql)[2]
                    if operationHasValue != []:
                        processingnolist.append(str(processingno))
                        flag = True
                    print(processingnolist)
                    if flag:
                        break
            # clientregionNo = 1,4 境内客户
            elif clientregionNo == 1 or clientregionNo == 4:
                # length查出共有几条请求数据要处理，count查出几天数据是境外请求的。num为剩下的几条境内要处理的数据
                num = length - count
                if num > 0:
                    for n in range(1, num + 1):
                        while True:
                            # 查询t_ineSeqProcess返回给监控中心的数据是否处理。如果exreturncode=0表示处理成功。
                            end = time.clock()
                            if int(end - start) == 600:
                                print('waiting for 10 min ,cant get result .Timeout!')
                                break
                            # 初始的seqno加上递增的num
                            rSeqno = int(respseqno) + n
                            if group == 'ine':
                                analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_ineSeqProcess t  where t.sender = \'N\' and t.seqno =' + str(
                                    rSeqno) + ' order by t.seqno desc'
                                maxSeqnosql = 'select max(t.seqno) from t_ineSeqProcess t  where t.sender = \'N\' '
                            elif group == 'shfe':
                                analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_SeqProcess t  where t.sender = \'N\' and t.seqno =' + str(
                                    rSeqno) + ' order by t.seqno desc'
                                maxSeqnosql = 'select max(t.seqno) from t_SeqProcess t  where t.sender = \'N\' '
                            maxRseqno = self.getValue(maxSeqnosql)[0]
                            if int(maxRseqno) >= int(rSeqno):
                                flag = True
                                analysisRes = self.orcl.connOrcl(analysisRessql)[2]
                                for i in analysisRes:
                                    if i[1] != 0:
                                        print('seqno = ' + str(i[0]) + ' operate filed and errmsg: ' + str(i[2]))
                                    else:
                                        print('seqno = ' + str(i[0]) + ' operate success and sucmsg: ' + str(i[2]))
                                print('ananlysis result end')
                            if flag:
                                break
        # 存在境外客户的数据需要页面进行备案审核
        if count > 0:
            maxRsqnoplus = int(maxRseqno) + count + 1
            print('selenium Account Record begin')
            print(processingnolist)
            self.accountRecord.review(type, processingnolist)
            print('selenium Account Record end')
            for r in range(maxRseqno + 1, maxRsqnoplus):
                if group == 'ine':
                    analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_ineSeqProcess t  where t.sender = \'N\' and t.seqno =' + str(
                        r) + ' order by t.seqno desc'
                elif group == 'shfe':
                    analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_SeqProcess t  where t.sender = \'N\' and t.seqno =' + str(
                        r) + ' order by t.seqno desc'
                analysisRes = self.orcl.connOrcl(analysisRessql)[2]
                for i in analysisRes:
                    if i[1] != 0:
                        print('seqno = ' + str(i[0]) + ' operate filed and errmsg: ' + str(i[2]))
                    else:
                        print('seqno = ' + str(i[0]) + ' operate success and sucmsg: ' + str(i[2]))
                print('ananlysis result end')