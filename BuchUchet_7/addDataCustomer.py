#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from tkinter import *
from dataBase import Base
import time
import datetime
from checkFormatData import Format

class Data():

    def __init__(self,slave,nameParam,nameFirm):
        self.slaves = slave
        self.nameParam = nameParam
        self.nameFirm = nameFirm
        self.format = Format()


    def formAddData(self):
        self.dataCus = Toplevel(self.slaves)
        self.dataCus.title('Заведение данных по %s' % (self.nameFirm))
        self.dataCus.geometry('620x225+240+220')
        self.dataCus.grab_set()
        # Label
        Label(self.dataCus, text="Дата операции:",font="Arial 12 bold").grid(row=1,sticky=E,pady=10,padx=8)
        Label(self.dataCus, text="Отгрузили на сумму:",font="Arial 12 bold").grid(row=2,sticky=E,pady=10,padx=8)
        Label(self.dataCus, text="Получена сумма:",font="Arial 12 bold").grid(row=3,sticky=E,pady=10,padx=8)
        Label(self.dataCus, text="Примечание:",font="Arial 12 bold").grid(row=4,sticky=E,pady=10,padx=8)
        Label(self.dataCus, text="рублей. (12344,00 или 232.90)",font="Arial 12 bold").grid(row=2,column=1,sticky=W,pady=10,padx=125)
        Label(self.dataCus, text="рублей. (12344,00 или 232.90)",font="Arial 12 bold").grid(row=3,column=1,sticky=W,pady=10,padx=125)

        #Label(self.dataCus, text="-",font="Arial 11 bold").grid(row=1,column=1,sticky=W,pady=10,padx=47)
        #Label(self.dataCus, text="-",font="Arial 11 bold").grid(row=1,column=1,sticky=W,pady=10,padx=80)
        #Label(self.dataCus, text="YYYY-MM-DD",font="Arial 11 bold").grid(row=1,column=1,sticky=W,pady=10,padx=113)
        Label(self.dataCus, text="YYYY-MM-DD",font="Arial 11 bold").grid(row=1,column=1,sticky=W,pady=10,padx=125)
        # Entry
        self.date = Entry(self.dataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        #self.dateYYYY = Entry(self.dataCus,width=4,background = '#CAE9C8',font="Arial 11 bold")
        #self.dateMM = Entry(self.dataCus,width=2,background = '#CAE9C8',font="Arial 11 bold")
        #self.dateDay = Entry(self.dataCus,width=2,background = '#CAE9C8',font="Arial 11 bold")

        self.opl = Entry(self.dataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.pol = Entry(self.dataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.comment = Entry(self.dataCus,width=42,background = '#CAE9C8',font="Arial 11 bold")
        self.date.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        #self.dateYYYY.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        #self.dateMM.grid(row=1,column=1,padx=60,pady=10,sticky=W)
        #self.dateDay.grid(row=1,column=1,padx=93,pady=10,sticky=W)

        self.opl.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        self.pol.grid(row=3,column=1,padx=10,pady=10,sticky=W)
        self.comment.grid(row=4,column=1,padx=10,pady=10,sticky=W)
        # Button
        butSave = Button(self.dataCus,text="Сохранить",width=10,font='Arial 11 bold')
        butSave.grid(row=13,column=1,sticky=W,padx=250)
        butSave.bind("<Button-1>",self.newData)
        butCancel = Button(self.dataCus,text="Выход",width=10,font='Arial 11 bold',command=self.cancelAdd)
        butCancel.grid(row=13,column=1,sticky=W,padx=140)


    def editFormCustomerData(self,slavs,listParam):
        self.oldListParam = listParam
        self.editDataCus = Toplevel(slavs)
        self.editDataCus.title('Редактирование данных по %s' % (self.nameFirm))
        self.editDataCus.geometry('620x225+240+220')
        self.editDataCus.grab_set()

        Label(self.editDataCus, text="Дата операции:",font="Arial 12 bold").grid(row=1,sticky=E,pady=10,padx=8)
        Label(self.editDataCus, text="Отгрузили на сумму:",font="Arial 12 bold").grid(row=2,sticky=E,pady=10,padx=8)
        Label(self.editDataCus, text="Получена сумма:",font="Arial 12 bold").grid(row=3,sticky=E,pady=10,padx=8)
        Label(self.editDataCus, text="Примечание:",font="Arial 12 bold").grid(row=4,sticky=E,pady=10,padx=8)
        Label(self.editDataCus, text="рублей.",font="Arial 12 bold").grid(row=2,column=1,sticky=W,pady=10,padx=125)
        Label(self.editDataCus, text="рублей.",font="Arial 12 bold").grid(row=3,column=1,sticky=W,pady=10,padx=125)

        self.date = Entry(self.editDataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.date.insert(0, listParam[0][1:])
        self.opl = Entry(self.editDataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.opl.insert(0, listParam[1])
        self.pol = Entry(self.editDataCus,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.pol.insert(0, listParam[2])
        self.comment = Entry(self.editDataCus,width=42,background = '#CAE9C8',font="Arial 11 bold")
        self.comment.insert(0, listParam[3])
        self.date.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        self.opl.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        self.pol.grid(row=3,column=1,padx=10,pady=10, sticky=W)
        self.comment.grid(row=4,column=1,padx=10,pady=10,sticky=W)

        butSave = Button(self.editDataCus,text="Сохранить",width=10,font='Arial 11 bold')
        butSave.grid(row=13,column=1,sticky=W,padx=250)
        butSave.bind("<Button-1>",self.editData)
        butCancel = Button(self.editDataCus,text="Выход",width=10,font='Arial 11 bold',command=self.cancelEdit)
        butCancel.grid(row=13,column=1,sticky=W,padx=140)


    def newData(self,event):
        dateParam = self.date.get()
        checkDate = self.format.formatDate(dateParam)
        if checkDate != False:
            otgParam = self.opl.get()
            prhParam = self.pol.get()
            otgParam = otgParam.replace(',','.')
            prhParam = prhParam.replace(',','.')
            checkOpl = self.format.formatMany(otgParam)
            checkPol = self.format.formatMany(prhParam)
            if checkOpl != False and checkPol != False:
                if prhParam == None: prhParam = ''
                if otgParam == None: otgParam = ''
                comment = self.comment.get()
                comment = comment.replace('\"','')
                comment = comment.replace('\'','')
                comment = self.format.formatCode(comment)
                dataInsert = Base(self.nameParam)
                dataInsert.insertDataFirm(self.nameFirm,dateParam,otgParam,prhParam,comment)
                self.cancelAdd()
            else:
                self.error(self.dataCus,2)
        else:
            self.error(self.dataCus,1)

    def editData(self,event):
        newDateParam = self.date.get()
        checkDate = self.format.formatDate(newDateParam)
        if checkDate != False:
            newOtgParam = self.opl.get()
            newPrhParam = self.pol.get()
            newOtgParam = newOtgParam.replace(',','.')
            newPrhParam = newPrhParam.replace(',','.')
            checkNewOtgParam = self.format.formatMany(newOtgParam)
            checkNewPrhParam = self.format.formatMany(newPrhParam)
            if checkNewOtgParam != False and checkNewPrhParam != False:
                if newPrhParam == None: newprhParam = ''
                if newOtgParam == None: newotgParam = ''
                newComment = self.comment.get()
                newComment = newComment.replace('\"','')
                newComment = newComment.replace('\'','')
                newComment =self.format.formatCode(newComment)
                dataUpdate = Base(self.nameParam)
                dataUpdate.updateDataFirm(self.nameFirm,self.oldListParam,newDateParam,newOtgParam,newPrhParam,newComment)
                self.cancelEdit()
            else:
                self.error(self.editDataCus,2)
        else:
            self.error(self.editDataCus,1)

    def cancelAdd(self):
        self.dataCus.destroy()

    def cancelEdit(self):
        self.editDataCus.destroy()

    def error(self,slave,flag):
        self.err = Toplevel(slave)
        self.err.title('Ошибка ввода данных')
        self.err.geometry('400x110+350+290')
        self.err.grab_set()
        if flag == 1:
            Label(self.err, text='Дата введена неверно',font="Arial 12 bold").pack(side=TOP,pady=15)
        elif flag == 2:
            Label(self.err, text='Сумма введена неверно',font="Arial 12 bold").pack(side=TOP,pady=15)
        buttonExit = Button(self.err,font="Arial 12 bold",width=8,height=1,text="Ok",bd=10,command=self.quitOk).pack(side=BOTTOM,pady=5)

    def quitOk(self):
        self.err.destroy()


