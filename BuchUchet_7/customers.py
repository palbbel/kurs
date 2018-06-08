#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import codecs

from addFirm import Add
from dataBase import Base
from addDataToCustomer import AddDataCustomer
from checkFormatData import Format
#from logging_app import LoggerFactory


class Customer():

    def __init__(self,root):

        #self.loggerFactory = LoggerFactory()
        #self.logger = self.loggerFactory.getLoggers("customer")
        name = 'customer'
        self.root = root
        self.addFirm = Add(name)
        self.db = Base(name)
        self.format = Format()
        self.var=IntVar()
        self.var.set(1)
        self.sortType = 1

    def pageCustomer(self):
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        self.customer = Toplevel(self.root,bg='#20BAB5')
        self.customer.title('Покупатели')
        self.customer.geometry('1160x550+50+50')
        #self.customer.grab_set()

        Grid.rowconfigure(self.customer, 1, weight=1)
        Grid.columnconfigure(self.customer, 1, weight=1)
        fram1 = Frame(self.customer,width=230,height=550,bg='#20CCB5')

        self.fram2()
        fram1.grid(row=1,column=1, rowspan=1, columnspan=1, sticky=N + S + E + W)

        fram1ButtonAdd = Button(fram1,font="Arial 12 bold",width=20,height=1,text="Добавить покупателя",bg='#E1E9E8',command=self.addCustomer)
        fram1ButtonAdd.place(x = 10, y = 45)
        #fram1ButtonAdd.bind('<Button-1>', lambda _: self.addFirm.formAdd(self.customer))
        fram1ButtonEdit = Button(fram1,font="Arial 12 bold",width=20,height=1,text="Редактировать",bg='#E1E9E8',command=self.editCustomer)
        fram1ButtonEdit.place(x = 10, y = 90)
        fram1ButtonDelete = Button(fram1,font="Arial 12 bold",width=20,height=1,text="Удалить",bg='#E1E9E8',command=self.deleteCustomer)
        fram1ButtonDelete.place(x = 10, y = 135)
        fram1ButtonReload = Button(fram1,font="Arial 12 bold",width=20,height=1,text="Обновить",bg='#E1E9E8',command=self.update)
        fram1ButtonReload.place(x = 10, y = 180)
        #Label(fram1, text="Сортировать:",font="Arial 12 bold",bg='#E1E9E8').place(x=10,y=240)
        #self.radioButton(fram1)
        fram1ButtonExit = Button(fram1,font="Arial 12 bold",width=8,height=1,text="Выход",bg='#E1E9E8',command=self.cancel)
        fram1ButtonExit.place(x = 70, y = 470)

        Label(fram1, text="Сортировать:",font="Arial 12 bold",bg='#20BAB5').place(x=10,y=240)
        #var=IntVar()
        #var.set(1)
        rbutton1=Radiobutton(fram1,text='по организации',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=1,command=self.radio_change)
        rbutton2=Radiobutton(fram1,text='по менеджеру',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=2,command=self.radio_change)
        rbutton3=Radiobutton(fram1,text='по дате',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=3,command=self.radio_change)
        rbutton1.place(x = 12, y = 270)
        rbutton2.place(x = 12, y = 300)
        rbutton3.place(x = 12, y = 330)

        #self.radioButton(fram1)

    def radio_change(self):
        if self.var.get() == 1:
            self.sortType = 1
        elif self.var.get() == 2:
            self.sortType = 2
        elif self.var.get() == 3:
            self.sortType = 3

    def fram2(self):
        self.lists = []
        Grid.rowconfigure(self.customer, 1, weight=100)
        Grid.columnconfigure(self.customer, 2, weight=100)
        framSel2 = Frame(self.customer,width=930,height=550)
        framSel2.grid(row=1,column=2, rowspan=1, columnspan=1, sticky=N + S + E + W)
        Label(framSel2, text='Покупатели',font="Arial 15 bold",bg="#20BAB5",bd=10).pack(fill=BOTH)

        frameb1 = Frame(framSel2); frameb1.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb1, text='№\n',borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        lb1 = Listbox(frameb1, width=5, height=23, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        lb1.pack(expand=YES, fill=BOTH)
        lb1.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        lb1.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        lb1.bind('<Leave>', lambda e: 'break')
        lb1.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        lb1.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))

        frameb2 = Frame(framSel2); frameb2.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb2, text='Организация\n', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        self.lb2 = Listbox(frameb2, width=40, height=23, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold",bg='#D3E9E6')
        self.lb2.pack(expand=YES, fill=BOTH)
        self.lb2.bind('<Double-Button-1>', self.curSelect)
        self.lb2.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        self.lb2.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        self.lb2.bind('<Leave>', lambda e: 'break')
        self.lb2.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        self.lb2.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        self.menu = Menu(self.lb2, font="Arial 12 bold", bg = 'lightblue', bd=10, tearoff=0)
        self.menu.add_command(label="Редактировать", command=self.editCustomer)
        self.menu.add_command(label="Удалить", command=self.deleteCustomer)
        self.lb2.bind("<Button-3>", lambda e, s=self: s.showMenu(e))

        frameb3 = Frame(framSel2); frameb3.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb3, text='ИНН\n', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        lb3 = Listbox(frameb3, width=15, height=23, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb3.pack(expand=YES, fill=BOTH)
        lb3.bind('<Double-Button-1>', self.curSelect)
        lb3.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        lb3.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        lb3.bind('<Leave>', lambda e: 'break')
        lb3.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        lb3.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        #lb3.bind('<Button-3>', lambda e, s=self: s._select(e.y))
        self.menu = Menu(lb3, font="Arial 12 bold", bg = 'lightblue', bd=10, tearoff=0)
        self.menu.add_command(label="Редактировать", command=self.editCustomer)
        self.menu.add_command(label="Удалить", command=self.deleteCustomer)
        lb3.bind("<Button-3>", lambda e, s=self: s.showMenu(e))

        frameb4 = Frame(framSel2); frameb4.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb4, text='Дата\nактуальлности', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        lb4 = Listbox(frameb4, width=15, height=23, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb4.pack(expand=YES, fill=BOTH)
        lb4.bind('<Double-Button-1>', self.curSelect)
        lb4.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        lb4.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        lb4.bind('<Leave>', lambda e: 'break')
        lb4.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        lb4.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        #lb4.bind('<Button-3>', lambda e, s=self: s._select(e.y))
        self.menu = Menu(lb4, font="Arial 12 bold", bg = 'lightblue', bd=10, tearoff=0)
        self.menu.add_command(label="Редактировать", command=self.editCustomer)
        self.menu.add_command(label="Удалить", command=self.deleteCustomer)
        lb4.bind("<Button-3>", lambda e, s=self: s.showMenu(e))


        frameb5 = Frame(framSel2); frameb5.pack(side=LEFT, expand=YES, fill=BOTH)
        Label(frameb5, text='Менеджер\n', borderwidth=1, relief=RAISED, font="Arial 12 bold", bg = '#20BAB5').pack(fill=X)
        lb5 = Listbox(frameb5, width=25, height=23, borderwidth=0, selectborderwidth=0,
                      relief=FLAT, exportselection=FALSE,font="Arial 13 bold", bg = '#D3E9E6')
        lb5.pack(expand=YES, fill=BOTH)
        lb5.bind('<Double-Button-1>', self.curSelect)
        lb5.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
        lb5.bind('<Button-1>', lambda e, s=self: s._select(e.y))
        lb5.bind('<Leave>', lambda e: 'break')
        lb5.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
        lb5.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        #lb5.bind('<Button-3>', lambda e, s=self: s._select(e.y))
        self.menu = Menu(lb5, font="Arial 12 bold", bg = 'lightblue', bd=10, tearoff=0)
        self.menu.add_command(label="Редактировать", command=self.editCustomer)
        self.menu.add_command(label="Удалить", command=self.deleteCustomer)
        lb5.bind("<Button-3>", lambda e, s=self: s.showMenu(e))

        self.lists.append(lb1)
        self.lists.append(self.lb2)
        self.lists.append(lb3)
        self.lists.append(lb4)
        self.lists.append(lb5)
        sb = Scrollbar(framSel2, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

        resault = self.db.selectData(self.sortType)

        iter = 1
        for name,inn,date_act,comment in resault:
            name = self.format.formatCode(name)
            comment = self.format.formatCode(comment)
            if str(name) == '' or str(name) == '-':
                break
            else:
                lb1.insert(END, ' %s' % str(iter))
                self.lb2.insert(END, '%s' % str(name))
                lb3.insert(END, '%s' % str(inn))
                lb4.insert(END, '%s' % str(date_act))
                lb5.insert(END, '%s' % str(comment))
                iter = iter + 1


    def showMenu(self,e):
        self._select2(e.y)
        self.curSelectAll(e)
        self.menu.post(e.x_root, e.y_root)

    def curSelect(self,evt):
        try:
            self.lb2.get(self.lb2.curselection())
            values = [self.lb2.get(idx) for idx in self.lb2.curselection()]
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
                self.listParameter.append(str(self.format.formatCode(', '.join(values))))    #(str((', '.join(values)).encode('utf-8')))
                #print '%s' % ', '.join(values)
        except Exception:
            pass


    def addCustomer(self):
        self.addFirm.formAdd(self.customer)


    def editCustomer(self):
        try:
            self.addFirm.formEdit(self.customer, self.listParameter)
        except Exception:
            pass


    def deleteCustomer(self):
        self.delWindow = Toplevel(self.customer,bg = '#20BAB5')
        self.delWindow.title('Удаление покупателя')
        self.delWindow.geometry('280x150+450+180')
        self.delWindow.grab_set()
        Label(self.delWindow, text="",font="Arial 12 bold",bg = '#20BAB5').pack(side=TOP)
        Label(self.delWindow, text="Удалить все данные",font="Arial 12 bold",bg = '#20BAB5').pack(side=TOP)
        Label(self.delWindow, text="по выбранной организации?",font="Arial 12 bold",bg = '#20BAB5').pack(side=TOP)

        Button1 = Button(self.delWindow,font="Arial 12 bold",width=8,height=1,bg ='#E1E9E8',text="Нет",command=self.quitDel).pack(side=LEFT,padx=33)
        Button2 = Button(self.delWindow,font="Arial 12 bold",width=8,height=1,bg ='#E1E9E8',text="Да",command=self.deleteFirm).pack(side=LEFT)


    def deleteFirm(self):
        try:
            self.db.deleteFirm(self.listParameter)
        except Exception:
            pass
        self.quitDel()
        self.update()


    def quitDel(self):
        self.delWindow.destroy()


    def _select2(self, y):
        try:
            row = self.lists[0].nearest(y)
            self.selection_clear(0, END)
            self.selection_set(row)
            return 'break'
        except Exception:
            pass


    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        self.curSelectAll(y)
        return 'break'

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
        #print str(self.lists[0].curselection())
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

    def update(self):
        self.fram2()

    def cancel(self):
        self.customer.destroy()


    def doubleClick(self,nameFirm):
        nameFirm = str(self.format.formatCode(nameFirm))
        addData = AddDataCustomer(self.customer, nameFirm)
        addData.addForm()

    def radioButton(self,fram):
        #var=IntVar()
        #var.set(1)
        rbutton1=Radiobutton(fram,text='по организации',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=1)
        rbutton2=Radiobutton(fram,text='по менеджеру',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=2)
        rbutton3=Radiobutton(fram,text='по дате',font="Arial 11 bold",bg='#20BAB5',variable=self.var,value=3)
        rbutton1.place(x = 12, y = 270)
        rbutton2.place(x = 12, y = 300)
        rbutton3.place(x = 12, y = 330)
