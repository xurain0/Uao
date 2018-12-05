# -*- coding: utf-8 -*-
'''
Created on 2018-05-16
@author : xu.ren
'''

import paramiko
import datetime
import os
import logging
from AutoUao.utils.log import Logger
log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class sshUtils(object):

    username = 'uapp'
    password = 'Sfituser_123'
    def connSsh(self, host, cmd):
        print('host =============== %s' % host)
        print('cmd =============== %s ' % cmd)
        code = 0
        errmsg = ""
        status = ""
        try:
            paramiko.util.log_to_file('paramiko.log')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            status = ""
            errmsg = ""
            for out in stdout:
                status = status + out
            for out in stderr:
                errmsg = errmsg + out
            ssh.close()

        except Exception as e:
            errmsg = e.args[0]
            code = -1
        return code, errmsg, status

    def uploadFiles(self, host, local_dir, remote_dir, date):

        #将xml文件名改为含有当日date的文件名
        for root, dirs, files in os.walk(local_dir):
            oldname = files
            newname = []
            for i in oldname:
                # if 'xml' in i:
                #     with open(os.path.join(local_dir, i), "r", encoding="gbk") as f:
                #         lines = f.readlines()
                #         # 写的方式打开文件
                #     with open(os.path.join(local_dir, i), "w", encoding="utf-8") as f_w:
                #         for line in lines:
                #             if "encoding=" in line:
                #                 # 替换 encoding="gbk" 为 encoding="utf-8"
                #                 line = line.replace("<?xml version=\"1.0\" encoding=\"gbk\"?>", "<?xml version=\"1.0\" encoding=\"utf-8\"?>")
                #             f_w.write(line)
                #     f.close()
                #     f_w.close()

                i = i.replace(i[8:16], date)
                newname.append(i)

            for n in range(len(newname)):
                os.rename(os.path.join(local_dir, oldname[n]), os.path.join(local_dir, newname[n]))


        #删除recv下当日的文件
        rmCmd = 'cd %s ; rm -r *' % remote_dir + date + '*'
        self.connSsh(host, rmCmd)
        log.logger.info('cd %s ; rm -r *' % remote_dir + date + '*')
        print('rm -r *' + date + '*')

        #上传文件至recv下
        try:
            print('upload files to :', host, ' dir :', remote_dir)
            client = paramiko.Transport((host, 22))
            client.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(client)
            files = os.listdir(local_dir)
            for f in files:
                print('Uploading file :', os.path.join(local_dir, f), 'to ', host, remote_dir)
                sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))
                print('Uploading file success')
            client.close()
            log.logger.info('Uploading file :%s, to %s : %s ,Uploading file success'
                            % (os.path.join(local_dir, f), host, remote_dir))
        except Exception:
            log.logger.debug("Uploading file fail, connect error!")
            print("connect error!")

if __name__ == '__main__':
    c = sshUtils()
    print(c.connSsh('172.24.118.3', 'ls')[2])

    local_dir = 'E:\TestPlatform\\Uao\AutoUao\data\InePersonAccount'
    remote_dir = '/home/uapp/zzz/'
    host = '172.24.118.2'
    date = '20180623'
    #remote_dir = '/home/uapp/services/uao_ineuao1/recv/'
    s = sshUtils()
    s.uploadFiles(host, local_dir, remote_dir, date)


