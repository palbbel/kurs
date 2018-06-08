#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import time
import os
import traceback
import colorsys
import datetime
from tkinter import *
from dataBase import Base
from addDataSeller import Data
from checkFormatData import Format


class AddDataSeller():

    def __init__(self,slave,nameFirm):
        self.slave = slave
        self.nameFirm = nameFirm
        self.data = Data(self.slave,'seller',self.nameFirm)
        self.balans = '----'
        self.db = Base('seller')
        self.format = Format()

    def addForm(self):
        Grid.rowconfigure(self.slave, 0, weight=1)
        Grid.columnconfigure(self.slave, 0, weight=1)
        self.sel = Toplevel(self.slave,bg='#59CCE9')
        self.sel.title('Данные по %s' % (self.nameFirm))
        self.sel.geometry('1000x650+120+100')
        self.sel.grab_set()

        #self.frameBox()
        self.frameDialog()
        self.frameBox()
        self.frameBal()


    def frameDialog(self):
        Grid.rowconfigure(self.sel, 1, weight=1)
        Grid.columnconfigure(self.sel, 0, weight=1)
        frame2 = Frame(self.sel,width=1000,height=95,bg='#59CCE9')
        frame2.grid(row=1,column=0, rowspan=1, columnspan=1, sticky=N + S + E + W)
        # Label
        Label(frame2, text="Начало периода:",font="Arial 12 bold",bg='#59CCE9').place(x=10,y=20)
        Label(frame2, text="Окончание периода:",font="Arial 12 bold",bg='#59CCE9').place(x=270,y=20)
        # Entry
        self.startDate = Entry(frame2,width=9,background = '#CCEBEE',font="Arial 11 bold")
        self.startDate.insert(0, '2016-01-01')
        self.startDate.place(x=160,y=20)
        self.endDate = Entry(frame2,width=9,background = '#CCEBEE',font="Arial 11 bold")
        self.endDate.insert(0, self.currentDate())
        self.endDate.place(x=450,y=20)
        # Button
        buttonAdd = Button(frame2,font="Arial 12 bold",width=15,height=1,text="Завести данные", bg = '#EAEEEE')
        buttonAdd.place(x = 11, y = 55)
        buttonAdd.bind('<Button-1>', lambda _: self.data.formAddData())
        buttonEdit = Button(frame2,font="Arial 12 bold",width=15,height=1,text="Редактировать", bg = '#EAEEEE',command=self.editSellerData).place(x = 180, y = 55)
        buttonDel = Button(frame2,font="Arial 12 bold",width=12,height=1,text="Удалить", bg = '#EAEEEE',command=self.deleteSellerData).place(x = 350, y = 55)
        buttonPrint = Button(frame2,font="Arial 12 bold",width=16,height=1,text="Сохранить в файл", bg = '#EAEEEE',command=self.printToFile).place(x = 490, y = 55)
        buttonExit = Button(frame2,font="Arial 12 bold",width=12,height=1,text="Выход", bg = '#EAEEEE',command=self.quit).place(x = 670, y = 55)
        buttonReload = Button(frame2,font="Arial 12 bold",width=12,height=1,text="Обновить", bg = '#EAEEEE',command=self.replace).place(x = 810, y = 55)

    def frameBox(self):
        self.lists = []
        Grid.rowconfigure(self.sel, 2, weight=100)
        Grid.columnconfigure(self.sel, 0, weight=100)
        frame1 = Frame(self.sel,width=1000,height=450)
        frame1.grid(row=2,column=0, rowspan=1, columnspan=1, sticky=N + S + E + W)
        Label(frame1, text=self.nameFirm,font="Arial 13 bold",bd=15, bg = '#59CCE9').pack(side=TOP, fill=X)


        frameb1 = Frame(frame1); frameb1.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb1, text='Дата\nоперации',borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#59CCE9').pack(fill=X)
        lb1 = Listbox(frameb1, width=18, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb1.pack(expand=YES, fill=BOTH)
        self.serv(lb1)

        frameb2 = Frame(frame1); frameb2.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb2, text='Оплатили\n(в рублях)', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#59CCE9').pack(fill=X)
        lb2 = Listbox(frameb2, width=25, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb2.pack(expand=YES, fill=BOTH)
        self.serv(lb2)

        frameb3 = Frame(frame1); frameb3.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb3, text='Получили товара\nна сумму (в рублях)', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#59CCE9').pack(fill=X)
        lb3 = Listbox(frameb3, width=25, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb3.pack(expand=YES, fill=BOTH)
        self.serv(lb3)

        frameb4 = Frame(frame1); frameb4.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb4, text='Примечание\n', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#59CCE9').pack(fill=X)
        lb4 = Listbox(frameb4, width=40, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb4.pack(expand=YES, fill=BOTH)
        self.serv(lb4)

        self.lists.append(lb1)
        self.lists.append(lb2)
        self.lists.append(lb3)
        self.lists.append(lb4)
        sb = Scrollbar(frame1, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

        valueStartDate, valueEndDate = self.getDates()
        self.resault,self.balansStart,self.balansSum,self.balansEnd,self.payCurr,self.depayCurr = self.db.statFirm(self.nameFirm,valueStartDate,valueEndDate)

        for datePaym, oplata, prichod, comment in self.resault:
            #if str(datePaym.encode('utf-8')) == '' or str(datePaym.encode('utf-8')) == '-':
            if str(datePaym) == '' or str(datePaym) == '-':
                break
            else:
                lb1.insert(END, ' %s' % datePaym)
                lb2.insert(END, '%s' % str(oplata))
                lb3.insert(END, '%s' % str(prichod))
                comment = comment.encode('utf-8')
                lb4.insert(END, '%s' % str(comment))

    def frameBal(self):
        Grid.rowconfigure(self.sel, 3, weight=1)
        Grid.columnconfigure(self.sel, 0, weight=1)
        frameB = Frame(self.sel,width=1000,height=105,bg = '#59CCE9')
        frameB.grid(row=3,column=0, rowspan=1, columnspan=1, sticky=N + S + E + W)
        #Label(frameB, text='Остаток на начало периода : ' + str(self.balansStart), width=47, bd=14, font="Arial 12 bold",bg='#59CCE9').pack(fill=X,side=LEFT)#grid(row = 1, column = 1)
        #Label(frameB, text='Остаток на окончание периода : ' + str(self.balansEnd), width=47, bd=14, font="Arial 12 bold",bg='#59CCE9').pack(fill=X,side=RIGHT)#grid(row = 1, column = 1)
        Label(frameB, text="",font="Arial 3 bold",bg = '#59CCE9').grid(row=0,column=0,padx=15,sticky=W)
        Label(frameB, text="Остаток на начало периода:   ",font="Arial 12 bold",bg = '#59CCE9').grid(row=1,column=0,padx=15,sticky=W)
        Label(frameB, text="Остаток на окончание периода:   ",font="Arial 12 bold",bg = '#59CCE9').grid(row=2,column=0,padx=15,sticky=W)
        Label(frameB,text=str(self.balansStart),font="Arial 12 bold",bg = '#59CCE9').grid(row=1,column=1,sticky=E)
        Label(frameB,text=str(self.balansEnd),font="Arial 12 bold",bg = '#59CCE9').grid(row=2,column=1,sticky=E)
        Label(frameB, text="Оплатили товара за период на сумму:  ",font="Arial 12 bold",bg = '#59CCE9').grid(row=1,column=2,padx=50,sticky=W)
        Label(frameB, text="Получили товара за период на сумму:  ",font="Arial 12 bold",bg = '#59CCE9').grid(row=2,column=2,padx=50,sticky=W)
        Label(frameB,text=str(self.payCurr),font="Arial 12 bold",bg = '#59CCE9').grid(row=1,column=3,sticky=E)
        Label(frameB,text=str(self.depayCurr),font="Arial 12 bold",bg = '#59CCE9').grid(row=2,column=3,sticky=E)
        Label(frameB, text="",font="Arial 12 bold",bg = '#59CCE9').grid(row=1,column=4,padx=40,sticky=W)


    def quit(self):
        self.sel.destroy()

    def replace(self):
        self.frameBox()
        self.frameBal()

    def serv(self,slave):
        #slave.bind('<Button-3>', self.curseleсt())
        slave.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        slave.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        slave.bind('<Leave>', lambda e: 'break')
        slave.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        slave.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        self.menu = Menu(slave, font="Arial 12 bold", bg = 'lightblue', bd=10, tearoff=0)
        self.menu.add_command(label="Редактировать", command=self.editSellerData)
        self.menu.add_command(label="Удалить", command=self.deleteSellerData)
        slave.bind("<Button-3>", lambda e, s=self: s.showMenu(e))
        return


    def showMenu(self,e):
        self._select2(e.y)
        self.curSelectAll(e)
        self.menu.post(e.x_root, e.y_root)

    def curSelectAll(self,evt):
        try:
            self.listParameter = []
            for lb in self.lists:
                lb.get(lb.curselection())
                values = [lb.get(idx) for idx in lb.curselection()]
                self.listParameter.append(str(self.format.formatCode(', '.join(values))))
        except Exception:
            pass

    def _select2(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _select(self, y):
        try:
            row = self.lists[0].nearest(y)
            self.selection_clear(0, END)
            self.selection_set(row)
            self.curSelectAll(y)
            return 'break'
        except Exception:
            pass
    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)



    def editSellerData(self):
        try:
            self.data.editFormSellerData(self.sel, self.listParameter)
        except Exception:
            pass


    def deleteSellerData(self):
        try:
            self.db.deleteDataFirm(self.nameFirm,self.listParameter)
        except Exception:
            pass

    def currentDate(self):
        curDate = datetime.date.today()
        return str(curDate)

    def currentTime(self):
        curTime = datetime.datetime.now()
        strCurTime = str(curTime).replace(' ','_').replace(':','')[:17]
        return strCurTime


    def getDates(self):
        sDate = self.startDate.get()
        eDate = self.endDate.get()
        return sDate, eDate

    def printToFile(self):
        res = self.resault
        name = self.nameFirm
        balansStart = self.balansStart
        balansEnd = self.balansEnd
        sDate = self.startDate.get()
        eDate = self.endDate.get()
        try:
            dirApp = (os.getcwd()).decode('cp1251')
            self.pathDir = '%s/savefile' % (dirApp)
            nameDecode = name.decode('UTF-8')
            self.nameFile = '%s.txt' % (nameDecode)
            #self.nameFile = '%s_%s.txt' % (self.currentTime(),nameDecode)
            self.pathFile = os.path.join(self.pathDir,self.nameFile)
            iter = 1
            with open(self.pathFile, 'w') as file:
                file.write('Поставщик: ' + name + '\n')
                file.write('Период с %s по %s%s' % (str(sDate),str(eDate),'\n'))
                file.write('\n')
                file.write('Остаток на начало периода : %s%s' % (balansStart,'\n'))
                file.write('\n')
                file.write('%s%s' % ('***********************************************************************************************************************','\n'))
                file.write('%s %10s %s %18s %s %18s %s %25s %s%s' % ('|','   Дата   ','|','     Оплачено     ','|','     Получено     ','|','                         Примечание                         ','|','\n'))
                file.write('%s%s' % ('***********************************************************************************************************************','\n'))

                for a,b,c,d in res:
                    if len(d) > 60:
                        d = d[0:60]
                    elif len(d) < 60:
                        d = d.ljust(60)
                    if iter > 1:
                        file.write('%s%s' % ('|------------|--------------------|--------------------|--------------------------------------------------------------|','\n'))
                    #line = '%s %-10s %s %-15s %s %-15s %s %-40s %s%s' % ('|',a,'|',b,'|',c,'|',d,'|','\n')
                    line = '%s %-10s %s %18s %s %18s %s %s %s%s' % ('|',a,'|',b,'|',c,'|',d,'|','\n')
                    file.write(self.format.formatCode(line))
                    iter = iter + 1
                file.write('%s%s' % ('***********************************************************************************************************************','\n'))
                file.write('%s%s' % ('','\n'))
                #file.write('Остаток на начало периода : %s%s' % (balansStart,'\n'))
                file.write('Остаток на окончание периода : %s%s' % (balansEnd,'\n'))
                file.write('Оплатили товара за период на сумму : %s%s' % (self.payCurr,'\n'))
                file.write('Получили товара за период на сумму : %s%s' % (self.depayCurr,'\n'))
            file.close()
            self.ok()

        #except Exception:
        except Exception as error:
            traceback.print_exc()
            self.error()



    def ok(self):
        self.saveWind = Toplevel(self.sel)
        self.saveWind.title('Выгразка данных в файл')
        #self.saveWind["bg"] = "green"
        self.saveWind.geometry('600x200+300+220')
        #self.saveWind.state("zoomed")
        self.saveWind.grab_set()

        Label(self.saveWind, text="Файл:",font="Arial 12 bold").pack(side=TOP,pady=10)
        Label(self.saveWind, text=self.nameFile,font="Arial 12 bold").pack(side=TOP)
        Label(self.saveWind, text="успешно сохранен по пути:",font="Arial 12 bold").pack(side=TOP)
        Label(self.saveWind, text=self.pathDir,font="Arial 12 bold").pack()
        buttonExit = Button(self.saveWind,font="Arial 12 bold",width=8,height=1,text="Ok",bd=10,command=self.quitOk).pack(side=BOTTOM,pady=10)


    def error(self):
        self.saveWind = Toplevel(self.sel)
        self.saveWind.title('Ошибка сохранения файла')
        self.saveWind.geometry('400x110+300+200')
        self.saveWind.grab_set()

        Label(self.saveWind, text='Возникла ошибка при выгрузке данных в файл',font="Arial 12 bold").pack(side=TOP,pady=15)
        buttonExit = Button(self.saveWind,font="Arial 12 bold",width=8,height=1,text="Ok",bd=10,command=self.quitOk).pack(side=BOTTOM,pady=5)


    def quitOk(self):
        self.saveWind.destroy()