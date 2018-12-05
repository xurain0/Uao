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
    host = read_ini.getConfValue(config_File, 'remote', 'host')
    cmd = xmlUtils()
    ssh = sshUtils()
    x2j = xml2jsonUtils()
    o2j = oracle2jsonUtils()
    compf = compareFilesUtils()
    orcl = orclUtils()
    accountRecord = seleniumAccountRecordUtils()
    analysis = analysisResult.AnalysisResult()
    getResult = getResult.GetResult()

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
        log.logger.info('Get Initial Date : IN_MAX_NO = %s, GEN_MAX_NO = %s ' % (inseqno, respseqno))
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
            killUaoThread = self.ssh.connSsh(remoteServiceIp, killUaoThreadCmd)
            print(killUaoThread[2])
            exceIneUaoCmd = self.cmd.readXml('exceIneUao', self.backInfo_File)
            s = exceIneUaoCmd + " " + date + " " + group
            exceIneUao = self.ssh.connSsh(remoteServiceIp, s)
            if exceIneUao[0] != 0:
                ret1 = "errcode=" + str(exceIneUao[0]) + ";" + "errmsg=" + str(exceIneUao[1])
                log.logger.debug(ret1)
            else:
                ret1 = exceIneUao[2]
                log.logger.info(ret1)
        print(ret, ret1)

    #重启uao job
    def xtest_reStartUaoJob(self):
        restartUaoCmd = self.cmd.readXml('restartUao', self.backInfo_File)
        restart = self.ssh.connSsh(self.host, restartUaoCmd)
        if restart[0] != 0:
            ret = "errcode=" + str(restart[0]) + ";" + "errmsg=" + str(restart[1])
            log.logger.exception(ret)
        else:
            ret = restart[2]
            log.logger.info('Uao restart success!', ret)
        print(ret)

    #个人
    def xtest_Ine_Person_OpenAccount(self):
        group = 'ine'
        type = 'ine_person'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_person_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData()[0]
        respseqno = test_Uao().initialData()[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysis.analysisTestResult(local_dir, inseqno, group)
        #获取开户结果
        test_Uao().getResult.getResult(inseqno, respseqno, type, group)

    def xtest_Ine_Organ_OpenAccount(self):
        group = 'ine'
        type = 'ine_organ'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_organ_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData(group)[0]
        respseqno = test_Uao().initialData(group)[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysis.analysisTestResult(local_dir, inseqno, group)
        #获取开户结果
        test_Uao().getResult.getResult(inseqno, respseqno, type)

    def xtest_Ine_Specialorgan_OpenAccount(self):
        group = 'ine'
        type = 'ine_specialorgan'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_specialorgan_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData()[0]
        respseqno = test_Uao().initialData()[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysis.analysisTestResult(local_dir, inseqno, group)
        #获取开户结果
        test_Uao().getResult.getResult(inseqno, respseqno, type)

    def xtest_Ine_Asset_OpenAccount(self):
        group = 'ine'
        type = 'ine_asset'
        local_dir = DoConfIni().getConfValue(self.config_File, 'accountType', 'ine_asset_dir')
        #获取当前的seqno
        inseqno = test_Uao().initialData()[0]
        respseqno = test_Uao().initialData()[1]
        #执行uao job
        test_Uao().executeUao(local_dir, self.ine_remote_dir, group)
        #结果对比
        test_Uao().analysis.analysisTestResult(local_dir, inseqno, group)
        #获取开户结果
        test_Uao().getResult.getResult(inseqno, respseqno, type)

if __name__ == '__main__':

    u = test_Uao()
    u.ine_remote_dir()
    #u.xtest_Ine_Person_OpenAccount()
