#coding = utf-8
'''
Code description：analysis result
Create time：20181030
Developer：xurain
'''
from AutoUao.utils import *
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class AnalysisResult(object):

    config_File = os.path.join(currPath, 'config.ini')
    json_file = DoConfIni().getConfValue(config_File, 'result', 'jsonfile')
    compare_file = os.path.join(json_file, 'IOdiff.html')
    cmd = xmlUtils()

    def analysisTestResult(self, local_dir, inseqno, group):
        # xml文件数据转成input.json，oralce中流水表数据转成output.json
        # 统一开户业务流水表中直到seqno=配置文件seqno，对比这条流水与xml配置文件信息是否一致
        if type == 'ine_person':
            f1 = os.path.join(self.json_file, 'inePersonInput.json')
            print('put xml data into InePersonInput json file')
            self.x2j.personInfo(local_dir, f1, group)
        if type == 'ine_organ':
            f1 = os.path.join(self.json_file, 'ineOrganInput.json')
            print('put xml data into IneOrganInput json file')
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
            flag = False
            while True:
                inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
                sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
                if int(sSeqNo) == int(inMaxNo):
                    flag = True
                    print('put t_SeqProcess data into json file')
                    if type == 'ine_person':
                        f2 = os.path.join(self.json_file, 'inePersonOutput.json')
                        self.o2j.personData(analysisSendsql, f2)
                    if type == 'ine_organ':
                        f2 = os.path.join(self.json_file, 'ineOrganOutput.json')
                        self.o2j.organData(analysisSendsql, f2)
                    if type == 'ine_specialorgan':
                        f2 = os.path.join(self.json_file, 'ineSpecialorganOutput.json')
                        self.o2j.specialorganData(analysisSendsql, f2)
                    if type == 'ine_asset':
                        f2 = os.path.join(self.json_file, 'ineAssetOutput.json')
                        self.o2j.assetData(analysisSendsql, f2)
                    print('compare outputfile with inputfile')
                    self.compf.compareFile(f1, f2, self.compare_file)
                if flag:
                    break
        elif group == 'shfe':
            findinMaxNosql = self.cmd.readXml('find_shfe_inMaxNosql', self.backInfo_File)
            sSeqNosql = self.cmd.readXml('shfe_SeqNosql', self.backInfo_File)
            analysisSendsql = 'select * from t_SeqProcess t  where t.sender = \'cfmmc\' and t.seqno >' + inseqno
            flag = False
            while True:
                inMaxNo = self.orcl.getMaxSeqNo(findinMaxNosql)
                sSeqNo = self.orcl.getMaxSeqNo(sSeqNosql)
                if int(sSeqNo) == int(inMaxNo):
                    flag = True
                    print('put t_SeqProcess data into json file')
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
                    self.compf.compareFile(f1, f2, self.compare_file)
                if flag:
                    break
