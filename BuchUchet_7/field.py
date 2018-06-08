from tkinter import *

class BasicWindows(object):

    def __init__(self):
        pass


    def basicFrame(self):
        root.minsize(width=500,height=500)
        root.title(string='Морской бой')

        fram = Frame(root, width=505, height=500, bg="#1DA7A2")
        fram.grid(row=1, column=1)
        self.buttons(fram)

    def buttons(self,fram):
        i =1
        for b in range(0, 500, 50):
            for a in range (0, 500, 50):
                but = Button(fram,font="Arial 10 bold",width=5,height=3,text=str(i), command=self.button_event)
                but.place(x = a, y = b)
                #but.bind("<Button-1>", lambda e, s=self: s._select(e.y))

                i += 1

   #def check(event, val):
    def button_event(val):
        print(val)






if __name__ == '__main__':

    root = Tk()

    basic = BasicWindows()
    basic.basicFrame()
    root.mainloop()

