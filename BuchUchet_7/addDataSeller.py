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
        self.dataSel = Toplevel(self.slaves)
        self.dataSel.title('Заведение данных по %s' % (self.nameFirm))
        self.dataSel.geometry('620x225+240+220')
        self.dataSel.grab_set()
        # Label
        Label(self.dataSel, text="Дата операции:",font="Arial 12 bold").grid(row=1,sticky=E,pady=10,padx=8)
        Label(self.dataSel, text="Оплатили на сумму:",font="Arial 12 bold").grid(row=2,sticky=E,pady=10,padx=8)
        Label(self.dataSel, text="Получено товара на сумму:",font="Arial 12 bold").grid(row=3,sticky=E,pady=10,padx=8)
        Label(self.dataSel, text="Примечание:",font="Arial 12 bold").grid(row=4,sticky=E,pady=10,padx=8)
        Label(self.dataSel, text="рублей. (12344,00 или 232.90)",font="Arial 12 bold").grid(row=2,column=1,sticky=W,pady=10,padx=125)
        Label(self.dataSel, text="рублей. (12344,00 или 232.90)",font="Arial 12 bold").grid(row=3,column=1,sticky=W,pady=10,padx=125)
        Label(self.dataSel, text="YYYY-MM-DD",font="Arial 11 bold").grid(row=1,column=1,sticky=W,pady=10,padx=125)
        # Entry
        self.date = Entry(self.dataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.opl = Entry(self.dataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.pol = Entry(self.dataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.comment = Entry(self.dataSel,width=42,background = '#CAE9C8',font="Arial 11 bold")
        self.date.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        self.opl.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        self.pol.grid(row=3,column=1,padx=10,pady=10,sticky=W)
        self.comment.grid(row=4,column=1,padx=10,pady=10,sticky=W)
        # Button
        butSave = Button(self.dataSel,text="Сохранить",width=10,font='Arial 11 bold')
        butSave.grid(row=13,column=1,sticky=W,padx=250)
        butSave.bind("<Button-1>",self.newData)
        butCancel = Button(self.dataSel,text="Выход",width=10,font='Arial 11 bold',command=self.cancelAdd)
        butCancel.grid(row=13,column=1,sticky=W,padx=140)


    def editFormSellerData(self,slavs,listParam):
        self.oldListParam = listParam
        self.editDataSel = Toplevel(slavs)
        self.editDataSel.title('Редактирование данных по %s' % (self.nameFirm))
        self.editDataSel.geometry('620x225+240+220')
        self.editDataSel.grab_set()

        Label(self.editDataSel, text="Дата операции:",font="Arial 12 bold").grid(row=1,sticky=E,pady=10,padx=8)
        Label(self.editDataSel, text="Оплатили на сумму:",font="Arial 12 bold").grid(row=2,sticky=E,pady=10,padx=8)
        Label(self.editDataSel, text="Получено товара на сумму:",font="Arial 12 bold").grid(row=3,sticky=E,pady=10,padx=8)
        Label(self.editDataSel, text="Примечание:",font="Arial 12 bold").grid(row=4,sticky=E,pady=10,padx=8)
        Label(self.editDataSel, text="рублей.",font="Arial 12 bold").grid(row=2,column=1,sticky=W,pady=10,padx=125)
        Label(self.editDataSel, text="рублей.",font="Arial 12 bold").grid(row=3,column=1,sticky=W,pady=10,padx=125)

        self.date = Entry(self.editDataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.date.insert(0, listParam[0][1:])
        self.opl = Entry(self.editDataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.opl.insert(0, listParam[1])
        self.pol = Entry(self.editDataSel,width=13,background = '#CAE9C8',font="Arial 11 bold")
        self.pol.insert(0, listParam[2])
        self.comment = Entry(self.editDataSel,width=42,background = '#CAE9C8',font="Arial 11 bold")
        self.comment.insert(0, listParam[3])
        self.date.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        self.opl.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        self.pol.grid(row=3,column=1,padx=10,pady=10, sticky=W)
        self.comment.grid(row=4,column=1,padx=10,pady=10,sticky=W)

        butSave = Button(self.editDataSel,text="Сохранить",width=10,font='Arial 11 bold')
        butSave.grid(row=13,column=1,sticky=W,padx=250)
        butSave.bind("<Button-1>",self.editData)
        butCancel = Button(self.editDataSel,text="Выход",width=10,font='Arial 11 bold',command=self.cancelEdit)
        butCancel.grid(row=13,column=1,sticky=W,padx=140)


    def newData(self,event):
        dateParam = self.date.get()
        checkDate = self.format.formatDate(dateParam)
        if checkDate != False:
            oplParam = self.opl.get()
            polParam = self.pol.get()
            oplParam = oplParam.replace(',','.')
            polParam = polParam.replace(',','.')
            checkOpl = self.format.formatMany(oplParam)
            checkPol = self.format.formatMany(polParam)
            if checkOpl != False and checkPol != False:
                if polParam == None: polParam = ''
                if oplParam == None: oplParam = ''
                comment = self.comment.get()
                comment = comment.replace('\"','')
                comment = comment.replace('\'','')
                comment = self.format.formatCode(comment)
                dataInsert = Base(self.nameParam)
                dataInsert.insertDataFirm(self.nameFirm,dateParam,oplParam,polParam,comment)
                self.cancelAdd()
            else:
                self.error(self.dataSel,2)
        else:
            self.error(self.dataSel,1)

    def editData(self,event):
        newDateParam = self.date.get()
        checkDate = self.format.formatDate(newDateParam)
        if checkDate != False:
            newoplParam = self.opl.get()
            newpolParam = self.pol.get()
            newoplParam = newoplParam.replace(',','.')
            newpolParam = newpolParam.replace(',','.')
            checkNewoplParam = self.format.formatMany(newoplParam)
            checkNewpolParam = self.format.formatMany(newpolParam)
            if checkNewoplParam != False and checkNewpolParam != False:
                if newpolParam == None: newpolParam = ''
                if newoplParam == None: newoplParam = ''
                newComment = self.comment.get()
                newComment = newComment.replace('\"','')
                newComment = newComment.replace('\'','')
                newComment =self.format.formatCode(newComment)
                dataUpdate = Base(self.nameParam)
                dataUpdate.updateDataFirm(self.nameFirm,self.oldListParam,newDateParam,newoplParam,newpolParam,newComment)
                self.cancelEdit()
            else:
                self.error(self.editDataSel,2)
        else:
            self.error(self.editDataSel,1)

    def cancelAdd(self):
        self.dataSel.destroy()

    def cancelEdit(self):
        self.editDataSel.destroy()

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


