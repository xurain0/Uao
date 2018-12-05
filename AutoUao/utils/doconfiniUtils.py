#coding:utf-8
'''
Code description : read config.ini get path
Create time : 20181022
Developer : xurain
'''
import logging
import configparser
from AutoUao.utils.log import Logger
from AutoUao.config.conf import *

log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class DoConfIni(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

    #从ini文件读取数据
    def getConfValue(self, filename, section, name):
        """

        :param filename:
        :param section:
        :param name:
        :return:
        """
        try:
            self.cf.read(filename)
            value = self.cf.get(section, name)
        except Exception as e:
            log.logger.exception('read file [%s] for [%s] failed , did not get the value' %(filename, section))
            raise e
        else:
            log.logger.info('read config.ini value [%s] successed! ' %value)
            return value
    #从ini文件中写数据
    def writerConfValue(self, filename, section, name, value):
        """

        :param filename:
        :param section:
        :param name:
        :param value:
        :return:
        """
        try:
            self.cf.add_section(section)
            self.cf.set(section, name, value)
            self.cf.write(open(filename, 'w'))
        except Exception:
            log.logger.exception('section %s has been exist!' %section)
            raise configparser.DuplicateSectionError(section)
        else:
            log.logger.info('write section'+section+'with value '+value+' successed!')

if __name__ == '__main__':
    filepath = currPath
    print(filepath)
    read_config = DoConfIni()
    value = read_config.getConfValue(os.path.join(currPath, 'config.ini'), 'accountType', 'ine_person_dir')
    print(value)