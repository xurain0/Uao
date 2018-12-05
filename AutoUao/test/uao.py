# -*- coding: utf-8 -*-
'''
Created on 2018-05-22

@author: xu.ren
'''

from AutoUao.utils import *
from AutoUao.test.models import *

log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class test_Uao(object):

    backInfo_File = os.path.join(currPath, 'backinfo.xml')
    config_File = os.path.join(currPath, 'config.ini')
    #获取uao所在服务器信息
    read_ini = DoConfIni()
    shfe_remote_dir = read_ini.getConfValue(config_File, 'remote', 'shfe_remote_dir')
    ine_remote_dir = read_ini.getConfValue(config_File, 'remote', 'ine_remote_dir')
    json_file = read_ini.getConfValue(config_File, 'result', 'jsonfile')
    host = read_ini.getConfValue(config_File, 'remote', 'host')
    cmd = xmlUtils()
    ssh = sshUtils()
    x2j = xml2jsonUtils()
    o2j = oracle2jsonUtils()
    compf = compareFilesUtils()
    orcl = orclUtils()
    accountRecord = seleniumAccountRecordUtils()
    #analysis = analysisResult.AnalysisResult()
    #getResult = getResult.GetResult()

    #获取初始化已经接收到的最大SEQ_NO和已经产生的最大SEQ_NO
    def initialData(self, group):
        if group == 'ine':
            findinMaxNosql = self.cmd.readXml('find_ine_inMaxNosql', self.backInfo_File)
            genMaxNosql = self.cmd.readXml('gen_ine_MaxNosql', self.backInfo_File)
        elif group == 'shfe':
            findinMaxNosql = self.cmd.readXml('find_shfe_inMaxNosql', self.backInfo_File)
            genMaxNosql = self.cmd.readXml('gen_shfe_MaxNosql', self.backInfo_File)
        inseqno = self.orcl.getMaxSeqNo(findinMaxNosql)
        respseqno = self.orcl.getMaxSeqNo(genMaxNosql)
        print('Get Initial Date : IN_MAX_NO = %s, GEN_MAX_NO = %s ' % (inseqno, respseqno))
        #log.logger.info('Get Initial Date : IN_MAX_NO = %s, GEN_MAX_NO = %s ' % (inseqno, respseqno))
        return inseqno, respseqno

    #上传xml文件，执行uao
    def executeUao(self, local_dir, remote_dir, group):
        #获取当前日期，例如20180622
        date = str(datetime.date.today()).replace('-', '')
        #获取uao远程部署的服务地址
        getRemoteServiceIpCmd = self.cmd.readXml('getServiceIp', self.backInfo_File)
        getRemoteServiceIp = self.ssh.connSsh(self.host, getRemoteServiceIpCmd)
        if getRemoteServiceIp[0] != 0:
            ret = "errcode=" + str(getRemoteServiceIp[0]) + ";" + "errmsg=" + str(getRemoteServiceIp[1])
            log.logger.debug(ret)
        else:
            ret = getRemoteServiceIp[2]
            remoteServiceIp = ret.strip()
            log.logger.info('Get Uao Remote Service Ip : %s' % remoteServiceIp)
            print('Get Uao Remote Service Ip :', remoteServiceIp)
            #上传xml文件到recv
            self.ssh.uploadFiles(remoteServiceIp, local_dir, remote_dir, date)
            #kill uao服务的进程。
            killUaoThreadCmd = self.cmd.readXml('killUaoThread', self.backInfo_File)
            print('killUaoThreadCmd = %s' % killUaoThreadCmd)
            killUaoThread = self.ssh.connSsh(remoteServiceIp, killUaoThreadCmd)
            #killUaoThread = self.ssh.connSsh(remoteServiceIp, 'ls')
            print('killUaoThread = %s' % killUaoThread[2])
            exceUaoCmd = self.cmd.readXml('exceUao', self.backInfo_File)
            s = exceUaoCmd + " " + date + " " + group
            print(s)
            exceIneUao = self.ssh.connSsh(remoteServiceIp, s)
            if exceIneUao[0] != 0:
                ret1 = "errcode=" + str(exceIneUao[0]) + ";" + "errmsg=" + str(exceIneUao[1])
                log.logger.debug(ret1)
                sys.exit()
            else:
                ret1 = exceIneUao[2]
                log.logger.info(ret1)
                if 'excu done' not in ret1 :
                    sys.exit()
        print(ret, ret1)
        print('ret = %s' % ret)

    def analysisTestResult(self, local_dir, inseqno, type, group):
        # xml文件数据转成input.json，oralce中流水表数据转成output.json
        # 统一开户业务流水表中直到seqno=配置文件seqno，对比这条流水与xml配置文件信息是否一致
        if type == 'ine_person':
            f1 = os.path.join(self.json_file, 'inePersonInput.json')
            print(local_dir)
            print(f1)
            print('put xml data into InePersonInput json file')
            self.x2j.personInfo(local_dir, f1, group)
        if type == 'ine_organ':
            f1 = os.path.join(self.json_file, 'ineOrganInput.json')
            print('put xml data into IneOrganInput json file')
            print(local_dir)
            print(f1)
            self.x2j.organInfo(local_dir, f1, group)
        if type == 'ine_specialorgan':
            f1 = os.path.join(self.json_file, 'ineSpecialorganInput.json')
            print('put xml data into IneSpecialorganInput json file')
            self.x2j.specialorganInfo(local_dir, f1, group)
        if type == 'ine_asset':
            f1 = os.path.join(self.json_file, 'ineAssetInput.json')
            print('put xml data into IneAssetInput json file')
            self.x2j.assetInfo(local_dir, f1, group)
        if type == 'shfe_person':
            f1 = os.path.join(self.json_file, 'shfePersonInput.json')
            print('put xml data into shfePersonInput json file')
            self.x2j.personInfo(local_dir, f1, group)
        if type == 'shfe_organ':
            f1 = os.path.join(self.json_file, 'shfeOrganInput.json')
            print('put xml data into shfeOrganInput json file')
            self.x2j.organInfo(local_dir, f1, group)
        if type == 'shfe_specialorgan':
            f1 = os.path.join(self.json_file, 'shfeSpecialorganInput.json')
            print('put xml data into shfeSpecialorganInput json file')
            self.x2j.specialorganInfo(local_dir, f1, group)
        if type == 'shfe_asset':
            f1 = os.path.join(self.json_file, 'shfeAssetInput.json')
            print('put xml data into shfeAssetInput json file')
            self.x2j.assetInfo(local_dir, f1, group)
        # findinMaxNosql = 'select t.settingvalue from t_inesetting t where t.settingkey = \'IN_MAX_NO\''
        # sSeqNosql = 'select max(t.seqno) from t_ineSeqProcess t  where t.sender = \'cfmmc\''
        # 查找执行完uao后，落地t_setting后已经收到到最大seqno，如果t_SeqProcess业务流水表中seqno=刚才接收到的
        # 最大seqno，则流水写入，对比流水中的数据与传入的数据。
        if group == 'ine':
            findinMaxNosql = self.cmd.readXml('find_ine_inMaxNosql', self.backInfo_File)
            sSeqNosql = self.cmd.readXml('ine_SeqNosql', self.backInfo_File)
            analysisSendsql = 'select * from t_ineSeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno
        elif group == 'shfe':
            findinMaxNosql = self.cmd.readXml('find_shfe_inMaxNosql', self.backInfo_File)
            sSeqNosql = self.cmd.readXml('shfe_SeqNosql', self.backInfo_File)
            analysisSendsql = 'select * from t_SeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno

        flag = False
        while True:
            inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
            sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
            print('%s, %s' % (inseqno, sSeqNo))
            if int(sSeqNo) == int(inMaxNo):
                flag = True
                print('put Process data into json file')
                if type == 'ine_person':
                    f2 = os.path.join(self.json_file, 'inePersonOutput.json')
                    print(f2)
                    self.o2j.personData(analysisSendsql, f2)
                if type == 'ine_organ':
                    f2 = os.path.join(self.json_file, 'ineOrganOutput.json')
                    print('333333333333333333333333333333', analysisSendsql)
                    self.o2j.organData(analysisSendsql, f2)
                if type == 'ine_specialorgan':
                    f2 = os.path.join(self.json_file, 'ineSpecialorganOutput.json')
                    self.o2j.specialorganData(analysisSendsql, f2)
                if type == 'ine_asset':
                    f2 = os.path.join(self.json_file, 'ineAssetOutput.json')
                    self.o2j.assetData(analysisSendsql, f2)
                if type == 'shfe_person':
                    f2 = os.path.join(self.json_file, 'shfePersonOutput.json')
                    self.o2j.personData(analysisSendsql, f2)
                if type == 'shfe_organ':
                    f2 = os.path.join(self.json_file, 'shfeOrganOutput.json')
                    self.o2j.organData(analysisSendsql, f2)
                if type == 'shfe_specialorgan':
                    f2 = os.path.join(self.json_file, 'shfeSpecialorganOutput.json')
                    self.o2j.specialorganData(analysisSendsql, f2)
                if type == 'shfe_asset':
                    f2 = os.path.join(self.json_file, 'shfeAssetOutput.json')
                    self.o2j.assetData(analysisSendsql, f2)
                print('compare outputfile with inputfile')
                compare_file = os.path.join(self.json_file, 'IOdiff.html')
                self.compf.compareFile(f1, f2, compare_file)
            if flag:
                break
        # elif group == 'shfe':
        #     findinMaxNosql = self.cmd.readXml('find_shfe_inMaxNosql', self.backInfo_File)
        #     sSeqNosql = self.cmd.readXml('shfe_SeqNosql', self.backInfo_File)
        #     analysisSendsql = 'select * from t_SeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno
        #     flag = False
        #     while True:
        #         inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
        #         sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
        #         if int(sSeqNo) == int(inMaxNo):
        #             flag = True
        #             print('put t_SeqProcess data into json file')
        #             if type == 'shfe_person':
        #                 f2 = os.path.join(self.json_file, 'shfePersonOutput.json')
        #                 self.o2j.personData(analysisSendsql, f2)
        #             if type == 'shfe_organ':
        #                 f2 = os.path.join(self.json_file, 'shfeOrganOutput.json')
        #                 self.o2j.organData(analysisSendsql, f2)
        #             if type == 'shfe_specialorgan':
        #                 f2 = os.path.join(self.json_file, 'shfeSpecialorganOutput.json')
        #                 self.o2j.specialorganData(analysisSendsql, f2)
        #             if type == 'shfe_asset':
        #                 f2 = os.path.join(self.json_file, 'shfeAssetOutput.json')
        #                 self.o2j.assetData(analysisSendsql, f2)
        #             print('compare outputfile with inputfile')
        #             self.compf.compareFile(f1, f2, self.compare_file)
        #         if flag:
        #             break

    def getResult(self, inseqno, respseqno, type, group):
        # clientregionsql=1,4境内客户不需要页面审核，境外需要页面审核
        # time.sleep(60)
        print('ananlysis table SeqProcess response')
        start = time.perf_counter()
        flag = False
        maxRseqno = 0
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
                            end = time.perf_counter()
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
                                analysisRessql = 'select  t.seqno,t.exreturncode,t.exreturnmsg  from t_SeqProcess t  where t.sender = \'S\' and t.seqno =' + str(
                                    rSeqno) + ' order by t.seqno desc'
                                maxSeqnosql = 'select max(t.seqno) from t_SeqProcess t  where t.sender = \'S\' '
                            maxRseqno = self.orcl.getMaxSeqNo(maxSeqnosql)
                            #print("maxRseqno = %s" % maxRseqno )
                            #print(rSeqno)
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
        print('count = %s' % count)
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

    #重启uao job
    def test_reStartUaoJob(self):
        restartUaoCmd = self.cmd.readXml('restartUao', self.backInfo_File)
        restart = self.ssh.connSsh(self.host, restartUaoCmd)
        if restart[0] != 0:
            ret = "errcode=" + str(restart[0]) + ";" + "errmsg=" + str(restart[1])
            #log.logger.exception(ret)
        else:
            ret = restart[2]
            #log.logger.info('Uao restart success!', ret)
        print(ret)

    #个人
    def test_Ine_Person_OpenAccount(self):
        group = 'ine'
        type = 'ine_person'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_person_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData(group)[0]
        respseqno = test_Uao().initialData(group)[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysisTestResult(local_dir, inseqno, type, group)
        #获取开户结果
        test_Uao().getResult(inseqno, respseqno, type, group)

    def test_Ine_Organ_OpenAccount(self):
        group = 'ine'
        type = 'ine_organ'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_organ_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData(group)[0]
        respseqno = test_Uao().initialData(group)[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysisTestResult(local_dir, inseqno, type, group)
        #获取开户结果
        test_Uao().getResult(inseqno, respseqno, type, group)

    def test_Ine_Specialorgan_OpenAccount(self):
        group = 'ine'
        type = 'ine_specialorgan'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_specialorgan_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData(group)[0]
        respseqno = test_Uao().initialData(group)[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysisTestResult(local_dir, inseqno, type, group)
        #获取开户结果
        test_Uao().getResult(inseqno, respseqno, type, group)

    def test_Ine_Asset_OpenAccount(self):
        group = 'ine'
        type = 'ine_asset'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_asset_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData(group)[0]
        respseqno = test_Uao().initialData(group)[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysisTestResult(local_dir, inseqno, type, group)
        #获取开户结果
        test_Uao().getResult(inseqno, respseqno, type, group)

if __name__ == '__main__':

    u = test_Uao()
    #analysisTestResult(self, local_dir, inseqno, type, group):
    #getResult(self, inseqno, respseqno, type, group):
    u.getResult('33', '33', 'ine_organ', 'ine')
    # config_File = os.path.join(currPath, 'config.ini')
    # local_dir = DoConfIni().getConfValue(config_File, 'accountType', 'ine_person_dir')
    # print(local_dir)
    # u.analysisTestResult(local_dir, '26', 'ine_person', 'ine')
    #u.test_Ine_Person_OpenAccount()
    #u.test_Ine_Organ_OpenAccount()