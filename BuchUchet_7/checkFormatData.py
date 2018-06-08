#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime

class Format():

    def __init__(self):

        pass

    def formatDate(self, valueDate):
        try:
            datetime.datetime.strptime(valueDate, '%Y-%m-%d')
            return True
        except:
            return False

    def formatMany(self,param):
        if param == None or param == '':
            return True
        else:
            #param = param.replace(',','.')
            checkParam = re.search('(\d+\.\d{2})',param)
            try:
                if str(checkParam.group(0)) == str(param):
                    return True
                else:
                    return False
            except:
                return False


    def formatCode(self,valueString):
        valueString = valueString.encode('utf-8')
        return valueString

