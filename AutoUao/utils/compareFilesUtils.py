# -*- coding: utf-8 -*-
'''
Created on 2018-06-05

@author: xu.ren
'''

import difflib
import sys
from AutoUao.utils import *
# from AutoUao.test.models import *
# log = Logger(__name__, CmdLevel=logging.INFO, FileLevel=logging.INFO)

class compareFilesUtils(object):

    def compareFile(self, f1, f2, compareFile):
        inputFile = open(f1)
        outputFile = open(f2)

        count = 0
        dif = []
        for a in inputFile:
            b = outputFile.readline()
            count += 1
            if a != b:
                dif.append(count)
        if dif == []:
            print('%s and %s , Two files are same !' % (f1, f2))
            #log.logger.info('%s and %s , Two files are same !' % (f1, f2))
        else:
            print('%s and %s , Two files has %d differents'% (f1, f2, len(dif)))
            for each in dif:
                print('%d line different ' % each)
            # log.logger.info('%s and %s ,\n Two files has %d differents .\n '
            #                 '%s line are different '% (f1, f2, len(dif), dif))

        #create diff html
        text1_lines = open(f1, 'r').readlines()
        text2_lines = open(f2, 'r').readlines()
        d = difflib.HtmlDiff()
        dm = d.make_file(text1_lines, text2_lines)
        with open(compareFile, 'w') as resultfile:
                resultfile.write(dm)
        inputFile.close()
        outputFile.close()

        return dif

if __name__ == '__main__':
    t = compareFilesUtils()
    f1 = 'E:\TestPlatform\\Uao\AutoUao\\results\ineOrganInput.json'
    f2 = 'E:\TestPlatform\\Uao\AutoUao\\results\ineOrganOutput.json'
    f3 = 'E:\TestPlatform\\Uao\AutoUao\\results\IOdiff.html'
    a = t.compareFile(f1, f2, f3)
    if a != []:
        sys.exit()
    print(a)