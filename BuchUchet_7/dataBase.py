#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import codecs
from decimal import Decimal
from checkFormatData import Format

class Base():

    def __init__(self,nameParam):
        self.pathdb = os.getcwd()
        self.nameParam = nameParam
        #self.checkDB = self.checkBase()
        self.format = Format()

    def selectData(self,sortType):
        checkDB = self.checkBase()
        if checkDB == False:
            db = Database(self.nameParam)
            conn,curs = db.connect()
            db.createBase(conn,curs)
            resault = db.selectBase(conn,curs,sortType)
            return resault
        if checkDB == True:
            db = Database(self.nameParam)
            conn,curs = db.connect()
            resault = db.selectBase(conn,curs,sortType)
            return resault

    def insertData(self,nameFirm,inn,dateAct,comment):
        dbInsert = Database(self.nameParam)
        conn,curs = dbInsert.connect()
        checkFirm = dbInsert.selectBase(conn,curs,1)
        listFirm = []
        for a,b,c,d in checkFirm:
            listFirm.append(self.format.formatCode(a))
        if nameFirm not in listFirm:
            conn,curs = dbInsert.connect()
            dbInsert.insert(conn,curs,nameFirm,inn,dateAct,comment)
            return True
        else:
            return False

    def updateData(self,listOldParam,newNmeFirm,newInn,newComment):
        dbUpdate = Database(self.nameParam)
        conn,curs = dbUpdate.connect()
        checkFirm = dbUpdate.selectBase(conn,curs,1)
        listFirm = []
        if newNmeFirm != listOldParam[1]:
            #print listOldParam[1]
            for a,b,c,d in checkFirm:
                listFirm.append(self.format.formatCode(a))
        if newNmeFirm not in listFirm:
            conn,curs = dbUpdate.connect()
            dbUpdate.update(conn,curs,listOldParam,newNmeFirm,newInn,newComment)
            return True
        else:
            return False

    def statFirm(self,nameFirm,startDate,endDate):
        dbStat = Database(self.nameParam)
        #print self.nameParam
        conn,curs = dbStat.connect()
        resault,balansStart,balansSum,balansEnd,payCurr,depayCurr = dbStat.selectStat(conn,curs,nameFirm,startDate,endDate)
        return resault,balansStart,balansSum,balansEnd,payCurr,depayCurr

    def deleteFirm(self,listParam):
        dbdelete = Database(self.nameParam)
        conn,curs = dbdelete.connect()
        dbdelete.delete(conn,curs,listParam)
        return

    def checkBase(self):
        checkPath = os.path.exists(self.pathdb + '/datafiles/' + self.nameParam + '.db')
        return checkPath

    def insertDataFirm(self,nameFirm,valueDate,valueOpl,valuePol,comment):
        dbInsertDataFirm = Database(self.nameParam)
        conn,curs = dbInsertDataFirm.connect()
        dbInsertDataFirm.insertDataSel(conn,curs,nameFirm,valueDate,valueOpl,valuePol,comment)

    def updateDataFirm(self,nameFirm,oldListParam,newDateParam,newoplParam,newpolParam,newComment):
        dbUpdateDataFirm = Database(self.nameParam)
        conn,curs = dbUpdateDataFirm.connect()
        dbUpdateDataFirm.updateDataSel(conn,curs,nameFirm,oldListParam,newDateParam,newoplParam,newpolParam,newComment)

    def deleteDataFirm(self,nameFirm,listParam):
        dbDeleteDataFirm = Database(self.nameParam)
        conn,curs = dbDeleteDataFirm.connect()
        dbDeleteDataFirm.deleteDataSel(conn,curs,nameFirm,listParam)


    def infoStat(self,startDate,endDate,sortType):
        infoStat = Database(self.nameParam)
        conn,curs = infoStat.connect()
        resaultInfo = infoStat.info(conn,curs,startDate,endDate,sortType)
        return resaultInfo

class Database():
    def __init__(self,paramName):

        self.paramName = paramName
        self.format = Format()

    def connect(self):
        self.con = sqlite3.connect('datafiles/' + self.paramName + '.db')
        self.cur = self.con.cursor()
        return self.con,self.cur

    def createBase(self,conn,curs):
        curs.execute('CREATE TABLE ' + self.paramName + ' (firstName text(100) PRIMARY KEY, inn VARCHAR(10), date_actual VARCHAR(8), comment text(100))')
        conn.commit()

    def selectBase(self,conn,curs,sortType):
        if sortType == 1:
            column = 'firstName'
        elif sortType == 2:
            column = 'comment'
        elif sortType == 3:
            column = 'date_actual'
        scriptSelect = 'SELECT firstName, inn, date_actual, comment from %s order by %s' % (self.paramName,column)
        #print scriptSelect
        curs.execute(scriptSelect)
        resault = curs.fetchall()
        if len(resault) == 0:
            resault = [('','','','')]
        conn.close()
        return  resault

    def insert(self,conn,curs,nameFirm,inn,dateAct,comment):
        scriptInsert = 'INSERT INTO ' + self.paramName + ' (firstName, inn, date_actual, comment) VALUES \
(\'' + str(nameFirm) + '\', \'' + str(inn) + '\', \'' + str(dateAct) + '\', \'' + str(comment) + '\')'
        #print scriptInsert
        curs.execute(scriptInsert)
        conn.commit()
        if self.paramName == 'seller':
            scriptCreate = 'CREATE TABLE \'%s\' (datePaym VARCHAR(10), oplata VARCHAR(20), prichod VARCHAR(20), comment text(100))' % (nameFirm)
        elif self.paramName == 'customer':
            scriptCreate = 'CREATE TABLE \'%s\' (datePaym VARCHAR(10), otgruz VARCHAR(20), oplata VARCHAR(20), comment text(100))' % (nameFirm)
        curs.execute(scriptCreate)
        conn.commit()
        conn.close()

    def update(self,conn,curs,listOldParam,newNmeFirm,newInn,newComment):
        scriptUpdate = 'UPDATE \'%s\' SET firstName = \'%s\', inn = \'%s\', comment = \'%s\' where firstName = \'%s\' and inn = \'%s\'' \
                       % (self.paramName,newNmeFirm,newInn,newComment,listOldParam[1],listOldParam[2])
        #print scriptUpdate
        curs.execute(scriptUpdate)
        conn.commit()
        if newNmeFirm != listOldParam[1]:
            scriptRename = 'ALTER TABLE  \'%s\' RENAME TO \'%s\' ' % (listOldParam[1],newNmeFirm)
            #print scriptRename
            curs.execute(scriptRename)
        conn.commit()
        conn.close()

    def selectStat(self,conn,curs,nameFirm,startDate,endDate):
        payCurr = '0.00'  # оплата за выбранный период
        depayCurr = '0.00'  # отгрузили за выбранный период
        if startDate == None or startDate == '':
            startDate = '1970-01-01'
        if endDate == None or endDate == '':
            endDate = '2099-12-31'

        balansStart = self.getBalansStart(conn,curs,nameFirm,startDate)

        if self.paramName == 'seller':
            scriptStat = 'SELECT datePaym, oplata, prichod, comment from \'%s\' where datePaym >= \'%s\' and  datePaym <= \'%s\' order by datePaym' % (nameFirm,startDate,endDate)
        elif self.paramName == 'customer':
            scriptStat = 'SELECT datePaym,  otgruz, oplata, comment from \'%s\' where datePaym >= \'%s\' and  datePaym <= \'%s\' order by datePaym' % (nameFirm,startDate,endDate)

        curs.execute(scriptStat)
        resault = curs.fetchall()
        conn.close()
        balans = Decimal('0.00')
        if len(resault) == 0:
            resault = [('','','','')]
            balansEnd = balansStart
        else:
            balansEnd = balansStart

            for datePaym, oplata, prichod, comment in resault:
                if str(oplata) == '': oplata = '0.00'
                if str(prichod) == '': prichod = '0.00'
                if self.paramName == 'seller':
                    balansEnd = Decimal(balansEnd) + Decimal(str(oplata)) - Decimal(str(prichod))
                    depayCurr = Decimal(depayCurr) + Decimal(str(prichod))
                    payCurr = Decimal(payCurr) + Decimal(str(oplata))
                elif self.paramName == 'customer':
                    depayCurr = Decimal(depayCurr) + Decimal(str(prichod))
                    payCurr = Decimal(payCurr) + Decimal(str(oplata))
                    balansEnd = Decimal(balansEnd) - Decimal(str(oplata)) + Decimal(str(prichod))

        balansSum = Decimal(balansEnd) - Decimal(balansStart)

        return  resault,balansStart,balansSum,balansEnd,payCurr,depayCurr


    def getBalansStart(self,conn,curs,nameFirm,startDate):
        if self.paramName == 'seller':
            scriptBalStart = 'SELECT oplata, prichod from \'%s\' where datePaym < \'%s\' order by datePaym' % (nameFirm,startDate)
        elif self.paramName == 'customer':
            scriptBalStart = 'SELECT otgruz, oplata from \'%s\' where datePaym < \'%s\' order by datePaym' % (nameFirm,startDate)

        curs.execute(scriptBalStart)
        resault = curs.fetchall()
        balansStart = '0.00'
        if len(resault) == 0:
             balansStart ='0.00'
        else:
            for oplata, prichod in resault:
                if str(oplata) == '': oplata = '0.00'
                if str(prichod) == '': prichod = '0.00'
                if self.paramName == 'seller':
                    balansStart = Decimal(str(balansStart)) + Decimal(str(oplata)) - Decimal(str(prichod))
                elif self.paramName == 'customer':
                    balansStart = Decimal(str(balansStart)) - Decimal(str(oplata)) + Decimal(str(prichod))

        return balansStart




    def delete(self,conn,curs,listParam):
        scriptDel = 'Delete from %s where firstName = \'%s\' and inn = \'%s\' and comment = \'%s\'' % (self.paramName, listParam[1], listParam[2], listParam[4])
        curs.execute(scriptDel)
        conn.commit()
        scriptDrop = 'DROP TABLE IF EXISTS \'%s\'' % (listParam[1])
        curs.execute(scriptDrop)
        conn.commit()
        conn.close()

    def insertDataSel(self,conn,curs,nameFirm,valueDate,valueOpl,valuePol,comment):
        if self.paramName == 'seller':
            scriptInsert = 'INSERT INTO \'%s\' (datePaym, oplata, prichod, comment) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' % (nameFirm,valueDate,str(valueOpl),str(valuePol),comment)

        elif self.paramName == 'customer':
            scriptInsert = 'INSERT INTO \'%s\' (datePaym, otgruz, oplata, comment) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' % (nameFirm,valueDate,str(valueOpl),str(valuePol),comment)

        curs.execute(scriptInsert)
        conn.commit()
        self.updateDate(conn,curs,nameFirm)
        conn.close()

    def updateDate(self,conn,curs,nameFirm):
        scriptSelectMaxDate = 'SELECT max(datePaym) from \'%s\'' % (nameFirm)
        curs.execute(scriptSelectMaxDate)
        resault = curs.fetchall()
        for dateData in resault:
            maxDate = str(dateData[0])

        scriptUpdareMaxDate = 'UPDATE \'%s\' SET date_actual = \'%s\' where firstName = \'%s\'' % (self.paramName,maxDate,nameFirm)
        curs.execute(scriptUpdareMaxDate)
        conn.commit()



    def updateDataSel(self,conn,curs,nameFirm,oldListParam,newDateParam,newoplParam,newpolParam,newComment):
        if self.paramName == 'seller':
            #print 'seller----1'
            scriptUpdate = 'UPDATE \'%s\' SET datePaym = \'%s\', oplata = \'%s\', prichod = \'%s\', comment = \'%s\' where datePaym = \'%s\' and oplata = \'%s\' and prichod = \'%s\' and comment = \'%s\' AND rowid in \
(SELECT rowid from \'%s\' where datePaym = \'%s\' and oplata = \'%s\' and prichod = \'%s\' and comment = \'%s\' LIMIT 1)'\
        % (nameFirm,newDateParam,newoplParam,newpolParam,newComment,oldListParam[0][1:],oldListParam[1],oldListParam[2],oldListParam[3], nameFirm,oldListParam[0][1:],oldListParam[1],oldListParam[2],oldListParam[3])
        elif self.paramName == 'customer':
            #print 'customer----2'
            scriptUpdate = 'UPDATE \'%s\' SET datePaym = \'%s\', otgruz = \'%s\', oplata = \'%s\', comment = \'%s\' where datePaym = \'%s\' and otgruz = \'%s\' and oplata = \'%s\' and comment = \'%s\' AND rowid in \
(SELECT rowid from \'%s\' where datePaym = \'%s\' and otgruz = \'%s\' and oplata = \'%s\' and comment = \'%s\' LIMIT 1)'\
        % (nameFirm,newDateParam,newoplParam,newpolParam,newComment,oldListParam[0][1:],oldListParam[1],oldListParam[2],oldListParam[3], nameFirm,oldListParam[0][1:],oldListParam[1],oldListParam[2],oldListParam[3])

        curs.execute(scriptUpdate)
        conn.commit()
        self.updateDate(conn,curs,nameFirm)
        conn.close()

    def deleteDataSel(self,conn,curs,nameFirm,listParam):
        if self.paramName == 'seller':
            #print 'seller----3'
            scriptDelData = 'Delete from \'%s\' where datePaym = \'%s\' and oplata = \'%s\' and prichod = \'%s\' and comment = \'%s\'  AND rowid in \
(SELECT rowid from \'%s\' where datePaym = \'%s\' and oplata = \'%s\' and prichod = \'%s\' and comment = \'%s\' LIMIT 1)'\
        % (nameFirm, listParam[0][1:], listParam[1], listParam[2], listParam[3], nameFirm, listParam[0][1:], listParam[1], listParam[2], listParam[3])
        elif self.paramName == 'customer':
            #print 'customer----4'
            scriptDelData = 'Delete from \'%s\' where datePaym = \'%s\' and otgruz = \'%s\' and oplata = \'%s\' and comment = \'%s\'  AND rowid in \
(SELECT rowid from \'%s\' where datePaym = \'%s\' and otgruz = \'%s\' and oplata = \'%s\' and comment = \'%s\' LIMIT 1)'\
        % (nameFirm, listParam[0][1:], listParam[1], listParam[2], listParam[3], nameFirm, listParam[0][1:], listParam[1], listParam[2], listParam[3])

        curs.execute(scriptDelData)
        conn.commit()
        self.updateDate(conn,curs,nameFirm)
        conn.close()


    def info(self,conn,curs,startDate,endDate,sortType):
        if sortType == 1:
            sortColumn = 'firstName'
        elif sortType == 2:
            sortColumn = 'comment'

        paramFirm = []
        balans = Decimal('0.00')
        scriptSelect = 'SELECT firstName, comment from %s order by %s' % (self.paramName, sortColumn)
        #print scriptSelect
        curs.execute(scriptSelect)
        resault = curs.fetchall()
        if len(resault) == 0:
            resault = [('','','','')]
        else:
            for nameFirm, manager in resault:
                statFirm = []
                manager = manager.encode('UTF-8')
                nameFirm = nameFirm.encode('UTF-8')
                if self.paramName == 'seller':
                    scriptStat = 'SELECT oplata, prichod from \'%s\' where datePaym >= \'%s\' and  datePaym <= \'%s\'' % (nameFirm,startDate,endDate)
                elif self.paramName == 'customer':
                    scriptStat = 'SELECT otgruz, oplata from \'%s\' where datePaym >= \'%s\' and  datePaym <= \'%s\'' % (nameFirm,startDate,endDate)
                curs.execute(scriptStat)
                resaults = curs.fetchall()
                #conn.close()

                rest = self.restInfo(conn,curs,nameFirm,startDate)

                if len(resaults) == 0:

                    if self.paramName == 'seller':
                        balans = Decimal('0.00') + Decimal(str(rest))
                    elif self.paramName == 'customer':
                        balans = Decimal('0.00') + Decimal(str(rest))

                    resaults = [('','')]
                    statFirm.append(nameFirm)
                    statFirm.append('0.00')
                    statFirm.append('0.00')
                    statFirm.append(rest)
                    statFirm.append(balans)
                    statFirm.append(manager)
                    #print str(balans),str(rest)
                    if str(balans) != '0.00' or str(rest) != '0.00':
                        paramFirm.append(statFirm)

                else:

                    allPlus = '0.00'
                    allMinus = '0.00'
                    for plus, minus in resaults:
                        if str(plus) == '' or plus == None: plus = '0.00'
                        if str(minus) == '' or minus == None: minus = '0.00'
                        allPlus = Decimal(allPlus) + Decimal(plus)
                        allMinus = Decimal(allMinus) + Decimal(minus)

                    if self.paramName == 'seller':
                        balans = Decimal(str(rest)) + Decimal(str(allPlus)) - Decimal(str(allMinus))
                    elif self.paramName == 'customer':
                        balans = Decimal(str(rest)) + Decimal(str(allMinus)) - Decimal(str(allPlus))

                    #rest = self.restInfo(conn,curs,nameFirm,startDate)

                    statFirm.append(nameFirm)
                    statFirm.append(allPlus)
                    statFirm.append(allMinus)
                    statFirm.append(rest)
                    statFirm.append(balans)
                    statFirm.append(manager)
                    paramFirm.append(statFirm)


            conn.close()
        return  paramFirm


    def restInfo(self,conn,curs,nameFirm,startDate):
        if self.paramName == 'seller':
            scriptStat = 'SELECT oplata, prichod from \'%s\' where datePaym < \'%s\'' % (nameFirm,startDate)
        elif self.paramName == 'customer':
            scriptStat = 'SELECT otgruz, oplata from \'%s\' where datePaym < \'%s\'' % (nameFirm,startDate)
        curs.execute(scriptStat)
        resaults = curs.fetchall()

        if len(resaults) == 0:
            rest = '0.00'

        else:
            allPlus = '0.00'
            allMinus = '0.00'
            for plus, minus in resaults:
                if str(plus) == '' or plus == None: plus = '0.00'
                if str(minus) == '' or minus == None: minus = '0.00'
                allPlus = Decimal(allPlus) + Decimal(plus)
                allMinus = Decimal(allMinus) + Decimal(minus)

                if self.paramName == 'seller':
                    rest = Decimal(str(allPlus)) - Decimal(str(allMinus))
                elif self.paramName == 'customer':
                    rest = Decimal(str(allMinus)) - Decimal(str(allPlus))

        return str(rest)