#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import traceback
import traceback
from tkinter import *
from dataBase import Base
from checkFormatData import Format
from addDataToSeller import AddDataSeller
from addDataToCustomer import AddDataCustomer



class Info():

    def __init__(self, slave, name):

        self.name = name
        self.slave = slave
        self.db = Base(name)
        self.format = Format()
        self.var=IntVar()
        self.var.set(1)
        self.sortType = 1

    def tableInfo(self):

        Grid.rowconfigure(self.slave, 0, weight=1)
        Grid.columnconfigure(self.slave, 0, weight=1)
        self.text,self.oneColumn,self.twoColumn = self.param()
        self.slave.title(self.text)
        self.slave.geometry('1300x555+100+100')



        self.info = Toplevel(self.slave)
        ###self.info.title(self.text)
        ###self.info.geometry('1300x555+100+100')
        self.info.grab_set()


        self.frameDialog()
        self.frameBox()


    def frameDialog(self):
        Grid.rowconfigure(self.info, 1, weight=1)
        Grid.columnconfigure(self.info, 0, weight=1)
        frame2 = Frame(self.info,width=1300,height=95,bg='#20BAB5')
        frame2.grid(row=1,column=0, rowspan=1, columnspan=1, sticky=N + S + E + W)
        # Label
        Label(frame2, text="Начало периода:",font="Arial 12 bold",bg='#20BAB5').place(x=10,y=20)
        Label(frame2, text="Окончание периода:",font="Arial 12 bold",bg='#20BAB5').place(x=270,y=20)
        # Entry
        self.startDate = Entry(frame2,width=9,background = '#CCEBEE',font="Arial 11 bold")
        self.startDate.insert(0, '2016-01-01')
        self.startDate.place(x=160,y=20)
        self.endDate = Entry(frame2,width=9,background = '#CCEBEE',font="Arial 11 bold")
        self.endDate.insert(0, self.currentDate())
        self.endDate.place(x=450,y=20)
        # Button
        buttonAdd = Button(frame2,font="Arial 12 bold",width=15,height=1,text="Сохранить в файл",bg='#E1E9E8',command=self.printToFile).place(x = 11, y = 55)
        buttonEdit = Button(frame2,font="Arial 12 bold",width=15,height=1,text="Обновить",bg='#E1E9E8',command=self.replace).place(x = 180, y = 55)
        buttonDel = Button(frame2,font="Arial 12 bold",width=15,height=1,text="Выход",bg='#E1E9E8',command=self.quit).place(x = 350, y = 55)

        Label(frame2, text="Сортировать:",font="Arial 12 bold",bg='#20BAB5').place(x=850,y=66)
        rbutton1=Radiobutton(frame2,text='по организации',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=1,command=self.radio_change)
        rbutton2=Radiobutton(frame2,text='по менеджеру',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=2,command=self.radio_change)
        rbutton1.place(x = 980, y = 66)
        rbutton2.place(x = 1130, y = 66)


    def frameBox(self):
        self.lists = []
        Grid.rowconfigure(self.info, 2, weight=100)
        Grid.columnconfigure(self.info, 0, weight=100)
        frame1 = Frame(self.info,width=1300,height=450)
        frame1.grid(row=2,column=0,rowspan=1, columnspan=1, sticky=N + S + E + W)
        Label(frame1, text=self.text,font="Arial 14 bold",bd=15,bg='#20BAB5').pack(side=TOP, fill=X)


        frameb = Frame(frame1); frameb.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb, text='ID\n',borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        lb = Listbox(frameb, width=5, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb.pack(expand=YES, fill=BOTH)
        self.serv(lb)

        frameb1 = Frame(frame1); frameb1.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb1, text='Наименование\n',borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        self.lb1 = Listbox(frameb1, width=58, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        self.lb1.pack(expand=YES, fill=BOTH)
        self.serv(self.lb1)

        frameb2 = Frame(frame1); frameb2.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb2, text=self.oneColumn, borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        lb2 = Listbox(frameb2, width=14, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb2.pack(expand=YES, fill=BOTH)
        self.serv(lb2)

        frameb3 = Frame(frame1); frameb3.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb3, text=self.twoColumn, borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        lb3 = Listbox(frameb3, width=14, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb3.pack(expand=YES, fill=BOTH)
        self.serv(lb3)

        frameb5 = Frame(frame1); frameb5.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb5, text='Остаток на\nначало периода', borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        lb5 = Listbox(frameb5, width=16, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb5.pack(expand=YES, fill=BOTH)
        self.serv(lb5)

        frameb4 = Frame(frame1); frameb4.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb4, text='Остаток на\nконец периода', borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        lb4 = Listbox(frameb4, width=16, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb4.pack(expand=YES, fill=BOTH)
        self.serv(lb4)


        frameb6 = Frame(frame1); frameb6.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb6, text='Менеджер\n', borderwidth=1, relief=RAISED, font="Arial 12 bold",bg='#20BAB5').pack(fill=X)
        lb6 = Listbox(frameb6, width=18, height=18, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb6.pack(expand=YES, fill=BOTH)
        self.serv(lb6)

        self.lists.append(lb)
        self.lists.append(self.lb1)
        self.lists.append(lb2)
        self.lists.append(lb3)
        self.lists.append(lb5)
        self.lists.append(lb4)
        self.lists.append(lb6)
        sb = Scrollbar(frame1, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

        valueStartDate, valueEndDate = self.getDates()
        self.resault = self.db.infoStat(valueStartDate,valueEndDate,self.sortType)
        iter = 1
        for param in self.resault:
            if str(param) == '' or str(param) == '-':
                break
            else:
                #iter = 1
                #for rec xrange (0,len(param)): #name, plus, minus, balans in param:
                lb.insert(END, ' %s' % str(iter))
                self.lb1.insert(END, ' %s' % param[0])
                lb2.insert(END, '%s' % str(param[1]))
                lb3.insert(END, '%s' % str(param[2]))
                lb5.insert(END, '%s' % str(param[3]))
                lb4.insert(END, '%s' % str(param[4]))
                lb6.insert(END, '%s' % str(param[5]))
                iter = iter + 1

    def param(self):

        if self.name == 'seller':
            text = 'Сводная таблица по поставщикам'
            oneColumn = 'Оплатили\nна сумму'
            twoColumn = 'Получили\nна сумму'
        elif self.name == 'customer':
            text = 'Сводная таблица по покупателям'
            oneColumn = 'Отгрузили\nна сумму'
            twoColumn = 'Оплата\n на сумму'
        return  text,oneColumn,twoColumn

    def radio_change(self):
        if self.var.get() == 1:
            self.sortType = 1
        elif self.var.get() == 2:
            self.sortType = 2

    def quit(self):
        self.info.destroy()


    def replace(self):
        self.frameBox()


    def serv(self,slave):
        #slave.bind('<Button-3>', self.curseleсt())
        slave.bind('<Double-Button-1>', self.curSelect)
        slave.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        slave.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        slave.bind('<Leave>', lambda e: 'break')
        slave.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        slave.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))

        return

    def curSelect(self,evt):
        try:
            self.lb1.get(self.lb1.curselection())
            values = [self.lb1.get(idx) for idx in self.lb1.curselection()]
            #print (', '.join(values))
            self.doubleClick(', '.join(values))
            #print '%s' % ', '.join(values)
        except Exception:
            pass


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


    '''
    def editCustomerData(self):
        try:
            self.data.editFormCustomerData(self.cus, self.listParameter)
        except Exception:
            pass


    def deleteCustomerData(self):
        try:
            self.db.deleteDataFirm(self.nameFirm,self.listParameter)
        except Exception:
            pass
    '''

    def currentDate(self):
        curDate = datetime.date.today()
        return str(curDate)

    def currentTime(self):
        curTime = datetime.datetime.now()
        strCurTime = str(curTime).replace(' ','_').replace(':','')[:17]
        return strCurTime


    def currentDate(self):
        curDate = datetime.date.today()
        return str(curDate)


    def getDates(self):
        sDate = self.startDate.get()
        eDate = self.endDate.get()
        return sDate, eDate

    def doubleClick(self,nameFirm):
        nameFirm = nameFirm.strip()
        nameFirm = str(self.format.formatCode(nameFirm))
        if self.name == 'seller':
            addData = AddDataSeller(self.info, nameFirm)
        elif  self.name == 'customer':
            addData = AddDataCustomer(self.info, nameFirm)
        addData.addForm()


    def printToFile(self):
        res = self.resault
        name = self.name
        if name == 'seller':
            nameRus = 'ПОСТАВЩИКИ'
            columnOne = ' Оплачено  '
            columnTwo = '  Получено  '
        elif name == 'customer':
            nameRus = 'ПОКУПАТЕЛИ'
            columnOne = '  Отгружено'
            columnTwo = '   Оплата   '
        sDate = self.startDate.get()
        eDate = self.endDate.get()
        try:
            dirApp = (os.getcwd()).decode('cp1251')
            self.pathDir = '%s/savefile' % (dirApp)
            nameDecode = name.decode('UTF-8')
            self.nameFile = '%s.txt' % (nameRus.decode('UTF-8'))
            #self.nameFile = '%s_%s.txt' % (self.currentTime(),nameDecode)
            self.pathFile = os.path.join(self.pathDir,self.nameFile)
            with open(self.pathFile, 'w') as file:
                file.write(nameRus + '\n')
                file.write('Период с %s по %s%s' % (str(sDate),str(eDate),'\n'))
                file.write('\n')
                file.write('%s%s' % ('************************************************************************************************************************','\n'))
                file.write('%s %-2s %s %-48s %s %11s %s %11s%s %11s %s%s' % ('|','N','|','НАИМЕНОВАНИЕ','|',columnOne,'|',columnTwo,'|',' Остаток на |  Остаток на |     Менеджер    ','|','\n'))
                file.write('%s%s' % ('|    |                                      |             |             | нач.периода |оконч.периода|                  |','\n'))
                file.write('%s%s' % ('************************************************************************************************************************','\n'))
                iter = 1
                for param in res:
                    if iter > 1:
                        file.write('%s%s' % ('|----|--------------------------------------|-------------|-------------|-------------|-------------|------------------|','\n'))
                    #line = '%s %-10s %s %-15s %s %-15s %s %-40s %s%s' % ('|',a,'|',b,'|',c,'|',d,'|','\n')
                    #line = '%s %-2s %s %-30s %s %13s %s %13s %s %13s %s%s' % ('|',str(iter),'|',self.formating(param[0]),'|',param[1],'|',param[2],'|',param[3],'|','\n')
                    names = self.formating(param[0],1)
                    manag = self.formating(param[5],2)
                    line = '%s %-2s %s %-19s %s %11s %s %11s %s %11s %s %11s %s %8s %s%s' % ('|',str(iter),'|',names,'|',param[1],'|',param[2],'|',param[3],'|',param[4],'|',manag,'|','\n')
                    #print line
                    file.write(line)
                    iter = iter + 1
                file.write('%s%s' % ('************************************************************************************************************************','\n'))
                file.write('%s%s' % ('','\n'))
                #file.write('Баланс : %s%s' % (balans,'\n'))
            file.close()
            self.ok()

        #except Exception:
        except Exception as error:
            traceback.print_exc()
            self.error()

    def ok(self):
        self.saveWind = Toplevel(self.info)
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
        self.saveWind = Toplevel(self.info)
        self.saveWind.title('Ошибка сохранения файла')
        self.saveWind.geometry('400x110+300+200')
        self.saveWind.grab_set()

        Label(self.saveWind, text='Возникла ошибка при выгрузке данных в файл',font="Arial 12 bold").pack(side=TOP,pady=15)
        buttonExit = Button(self.saveWind,font="Arial 12 bold",width=8,height=1,text="Ok",bd=10,command=self.quitOk).pack(side=BOTTOM,pady=5)


    def quitOk(self):
        self.saveWind.destroy()


    def formating(self,valueString,flag):
        space = ' '
        if flag == 1:
            if len(valueString.decode('utf-8')) > 36:
                splitValue = list(valueString.decode('utf-8'))
                newSplitValue = splitValue[0:36]
                valueString = ''
                for symb in newSplitValue:
                    valueString = valueString + symb
                valueString = valueString.encode('utf-8')
            elif len(valueString.decode('utf-8')) < 36:
                while len(valueString.decode('utf-8')) < 36:
                    valueString = '%s%s' % (valueString,space)

        elif flag == 2:
            if len(valueString.decode('utf-8')) > 16:
                splitValue = list(valueString.decode('utf-8'))
                newSplitValue = splitValue[0:16]
                valueString = ''
                for symb in newSplitValue:
                    valueString = valueString + symb
                valueString = valueString.encode('utf-8')
            elif len(valueString.decode('utf-8')) < 16:
                while len(valueString.decode('utf-8')) < 16:
                    valueString = '%s%s' % (valueString,space)

        return valueString
