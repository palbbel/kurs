from tkinter import *
#import tkMessageBox
from sellers import Seller
from customers import Customer
from allInfo import Info
##import logging
#from logging_app import LoggerFactory

class BasicWindows():

    def __init__(self,seller,customer):
        #self.dial = dial
        #self.logger = logger
        self.seller = seller
        self.customer = customer

    def basicFrame(self):
        #self.logger.debug('Создаем основное окно.')
        #root = Tk()
        #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        # for row_index in range(1, 12):
        #     Grid.rowconfigure(root, row_index, weight=1)
        #     for col_index in range(1, 6):
        #         Grid.columnconfigure(root, col_index, weight=1)
        #         fram = Frame(root)
        #         fram.grid(row=row_index, column=col_index, sticky=N + S + E + W)


        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        #root.minsize(width=700,height=400)
        root.geometry('800x500+50+50')
        root.title(string='Данные по контрагентам')

        fram = Frame(root, bg="#1DA7A2",bd=40)
        fram.grid(row=0, column=0, sticky=N + S + E + W)

        # Создание фреймов
        #self.logger.debug('Создем фреймы.')




        # fra1 = Frame(root,width=400,height=300,bg="#1DA7A2",bd=32)
        # fra2 = Frame(root,width=400,height=300,bg="#1DA7A2",bd=32)
        # fra3 = Frame(root,width=400,height=200,bg="#1DA7A2",bd=32)
        # fra4 = Frame(root,width=400,height=200,bg="#1DA7A2",bd=32)
        # fra1.grid(row=1,column=1)
        # fra2.grid(row=1,column=2)
        # fra3.grid(row=2,column=1)
        # fra4.grid(row=2,column=2)


        # Кнопки на первом фрейме
        #self.logger.debug('Создем кнопки на первом фрейме.')
        Grid.rowconfigure(fram, 2, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        Grid.rowconfigure(fram, 4, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        Grid.rowconfigure(fram, 6, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        Grid.rowconfigure(fram, 8, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        Grid.rowconfigure(fram, 10, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        fra1But1 = Button(fram,font="Arial 13 bold",width=32,height=1,text="Сводная таблица по поставщика")
        fra1But1.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra1But1.place(x = 13, y = 10)
        fra1But1.bind('<Button-1>', lambda _: self.make(1))
        fra1But2 = Button(fram,font="Arial 13 bold",width=32,height=1, text="Сводная таблица по покупателям")
        fra1But2.grid(row=4, column=1, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra1But2.place(x = 13, y = 50)
        fra1But2.bind('<Button-1>', lambda _: self.make(2))
        fra1But3 = Button(fram,font="Arial 13 bold",width=32,height=1, text="Выгрузка из 1С")
        fra1But3.grid(row=6, column=1, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra1But3.place(x = 13, y = 90)
        fra1But3.bind('<Button-1>', lambda _: self.make(13))
        fra1But4 = Button(fram,font="Arial 13 bold",width=32,height=1, text="Резерв")
        fra1But4.grid(row=8, column=1, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra1But4.place(x = 13, y = 130)
        fra1But4.bind('<Button-1>', lambda _: self.make(14))
        fra1But5 = Button(fram,font="Arial 13 bold",width=32,height=1, text="Резерв")
        fra1But5.grid(row=10, column=1, rowspan=1, columnspan=1,  sticky=N + S + E + W, pady =20, padx =20)
        # fra1But5.place(x = 13, y = 170)
        fra1But5.bind('<Button-1>', lambda _: self.make(15))

        # Кнопки на втором фрейме
        #self.logger.debug('Создем кнопки на втором фрейме.')
        Grid.rowconfigure(fram, 2, weight=1)
        Grid.columnconfigure(fram, 2, weight=1)
        Grid.rowconfigure(fram, 4, weight=1)
        Grid.columnconfigure(fram, 2, weight=1)
        fra2But1 = Button(fram,font="Arial 13 bold",width=32,height=1,text="ПОСТАВЩИКИ")
        fra2But1.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra2But1.place(x = 10, y = 10)
        fra2But1.bind('<Button-1>', lambda _: self.seller.pageSeller())
        fra2But2 = Button(fram,font="Arial 13 bold",width=32,height=1,text="ПОКУПАТЕЛИ")
        fra2But2.grid(row=4, column=2, rowspan=1, columnspan=1, sticky=N + S + E + W, pady =20, padx =20)
        # fra2But2.place(x = 10, y = 54)
        fra2But2.bind('<Button-1>', lambda _: self.customer.pageCustomer())

        # Кнопки на третьем фрейме
        Grid.rowconfigure(fram, 14, weight=1)
        Grid.columnconfigure(fram, 1, weight=1)
        Grid.rowconfigure(fram, 14, weight=1)
        Grid.columnconfigure(fram, 2, weight=1)
        #self.logger.debug('Создем кнопки на третьем фрейме.')
        # fra3But1 = Button(fra3,font="Arial 12 bold",width=12,height=1,text="О программе",command=self.info).place(x = 218, y = 110)
        fra3But1 = Button(fram,font="Arial 13 bold",width=32,height=1,text="О программе",command=self.info)
        fra3But1.grid(row=14, column=1, rowspan=1, columnspan=1, sticky=N + S + E + W, pady=20, padx=20)

        # # Кнопки на четвертом фрейме
        # #self.logger.debug('Создем кнопки на четвертом фрейме.')
        # fra4But1 = Button(fra4,font="Arial 12 bold",width=12,height=1,text="Выход",command=self.quit).place(x = 0, y = 110)
        fra4But1 = Button(fram,font="Arial 13 bold",width=20,height=1,text="Выход", command=self.quit)
        fra4But1.grid(row=14, column=2, rowspan=1, columnspan=1, sticky=N + S + E + W, pady=20, padx=20)

    def quit(event):
        global root
        root.destroy()

    def info(event):
        win = Toplevel(root,relief=SUNKEN,bd=10)
        win.title("О программе")
        win.minsize(width=450,height=300)
        win.grab_set()
        lab1 = Label(win, text = "Created: Pavel Belyakov", font="Arial 12 bold").place(x = 0, y = 0)

    def make(self, flag):
        if flag == 1:
            name = 'seller'
        elif flag == 2:
            name = 'customer'
        else:
            return
        info = Info(root,name)
        info.tableInfo()



if __name__ == '__main__':

    #loggerFactory = LoggerFactory()
    #logger = loggerFactory.getLoggers("MAIN")

    root = Tk()
    #dial = Dialog(root)
    seller = Seller(root)
    customer = Customer(root)
    basic = BasicWindows(seller,customer)
    basic.basicFrame()
    root.mainloop()

