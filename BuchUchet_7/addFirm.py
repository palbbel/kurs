#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from tkinter import *
from dataBase import Base
import sellers
from checkFormatData import Format
#import customers

class Add():

    def __init__(self,name):
        self.name = name
        self.format = Format()

    def formAdd(self,nameParam):
        #print  nameParam
        self.firm = Toplevel(nameParam,bg = '#E3EED8')
        if self.name == 'seller':
            self.firm.title('Добавить поставщика')
        elif self.name == 'customer':
            self.firm.title('Добавить покупателя')
        self.firm.geometry('650x250+290+195')
        self.firm.grab_set()

        Label(self.firm, text="Наименование:",font="Arial 12 bold",bg = '#E3EED8').grid(row=1,sticky=E,pady=10)
        Label(self.firm, text="ИНН:",font="Arial 12 bold",bg = '#E3EED8').grid(row=2,sticky=E,pady=10)
        Label(self.firm, text="Менеджер:",font="Arial 12 bold",bg = '#E3EED8').grid(row=3,sticky=E,pady=10)

        self.entName = Entry(self.firm,width=60,background = '#CCEBEE',font="Arial 11 bold")
        self.entInn = Entry(self.firm,width=20,background = '#CCEBEE',font="Arial 11 bold")
        self.entComment = Entry(self.firm,width=60,background = '#CCEBEE',font="Arial 11 bold")
        self.entName.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        self.entInn.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        self.entComment.grid(row=3,column=1,padx=10,pady=10,sticky=W)

        butSave = Button(self.firm,text="Сохранить",width=10,font='Arial 11 bold',bg = '#E3EED8')
        butSave.grid(row=10,column=1,sticky=E,pady=50,padx=150)
        butSave.bind("<Button-1>",self.newData)

        butCancel = Button(self.firm,text="Отмена",width=10,font='Arial 11 bold',bg = '#E3EED8',command=self.cancelAdd)
        butCancel.grid(row=10,column=1,sticky=W,pady=50,padx=260)


    def formEdit(self, nameParam, listParam):
        self.listParam = listParam
        self.edit = Toplevel(nameParam,bg = '#E3EED8')
        if self.name == 'seller':
            self.edit.title('Редактирование поставщика')
        elif self.name == 'customer':
            #print '2'
            self.edit.title('Редактирование покупателя')
        self.edit.geometry('650x250+290+195')
        self.edit.grab_set()

        Label(self.edit, text="Наименование:",font="Arial 12 bold",bg = '#E3EED8').grid(row=1,sticky=E,pady=10)
        Label(self.edit, text="ИНН:",font="Arial 12 bold",bg = '#E3EED8').grid(row=2,sticky=E,pady=10)
        #Label(self.edit, text="Дата актуальности:",font="Arial 12 bold",bg = '#E3EED8').grid(row=3,sticky=E,pady=10)
        Label(self.edit, text="Менеджер:",font="Arial 12 bold",bg = '#E3EED8').grid(row=4,sticky=E,pady=10)
        #print '3'
        self.entName = Entry(self.edit,width=60,background = '#CCEBEE',font="Arial 11 bold")
        self.entName.insert(0, listParam[1])
        self.entInn = Entry(self.edit,width=20,background = '#CCEBEE',font="Arial 11 bold")
        self.entInn.insert(0, listParam[2])
        #self.entDate = Entry(self.edit,width=20,background = '#CCEBEE',font="Arial 11 bold")
        #self.entDate.insert(0, listParam[3])
        self.entComment = Entry(self.edit,width=60,background = '#CCEBEE',font="Arial 11 bold")
        self.entComment.insert(0, listParam[4])

        self.entName.grid(row=1,column=1,padx=10,pady=10,sticky=W)
        self.entInn.grid(row=2,column=1,padx=10,pady=10, sticky=W)
        #self.entDate.grid(row=3,column=1,padx=10,pady=10, sticky=W)
        self.entComment.grid(row=4,column=1,padx=10,pady=10,sticky=W)


        butSave = Button(self.edit,text="Сохранить",width=10,font='Arial 11 bold',bg = '#E3EED8')
        butSave.grid(row=10,column=1,sticky=E,pady=50,padx=150)
        butSave.bind("<Button-1>",self.editData)
        butCancel = Button(self.edit,text="Отмена",width=10,font='Arial 11 bold',bg = '#E3EED8',command=self.cancelEdit)
        butCancel.grid(row=10,column=1,sticky=W,pady=50,padx=260)

    def newData(self,event):
        nameFirm = self.entName.get()
        nameFirm = nameFirm.replace('\"','').replace('\'','')
        nameFirm = nameFirm.strip()
        nameFirm = self.format.formatCode(nameFirm)
        inn = self.entInn.get()
        dateAct = ''
        comment = self.entComment.get()
        comment = comment.replace('\"','').replace('\'','')
        comment = self.format.formatCode(comment)
        if nameFirm == '' or nameFirm == None:
            self.cancelAdd()
        else:
            dataInsert = Base(self.name)
            check = dataInsert.insertData(nameFirm.strip(),inn,dateAct,comment)
            if check == False:
                self.error(self.firm)
            else:
                self.cancelAdd()



    def editData(self,event):
        #print '1'
        newNameFirm = self.entName.get()
        newNameFirm = newNameFirm.replace('\"','').replace('\'','')
        newNameFirm = self.format.formatCode(newNameFirm)
        newInn = self.entInn.get()
        #newDateAct = self.entDate.get()
        newComment = self.entComment.get()
        newComment = newComment.replace('\"','').replace('\'','')
        newComment = self.format.formatCode(newComment)
        dataUpdate = Base(self.name)
        check = dataUpdate.updateData(self.listParam, newNameFirm.strip(),newInn,newComment)
        if check == False:
            self.error(self.edit)
        else:
            self.cancelEdit()

    def error(self,slave):
        self.err = Toplevel(slave)
        self.err.title('Ошибка заведения поставщика')
        self.err.geometry('400x110+400+260')
        self.err.grab_set()
        Label(self.err, text='Поставщик уже существует',font="Arial 12 bold").pack(side=TOP,pady=15)
        buttonExit = Button(self.err,font="Arial 12 bold",width=8,height=1,text="Ok",bd=10,command=self.quitOk).pack(side=BOTTOM,pady=5)

    def quitOk(self):
        self.err.destroy()

    def cancelAdd(self):
        self.firm.destroy()


    def cancelEdit(self):
        self.edit.destroy()

