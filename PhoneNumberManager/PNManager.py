#coding=gbk
import os, random, struct, string
from Tkinter import *
import tkMessageBox


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """define the sign in module"""
        titlelabel = Label(self, text=u"用 户 登 记", width=8)
        titlelabel.grid(columnspan=2, row=0, padx=2, sticky=W)

        namelabel = Label(self, text=u"姓 名：")
        namelabel.grid(column=0, row=1, pady=1, padx=2, sticky=NSEW)

        nameentry = Entry(self, width=10)
        nameentry.grid(column=1, row=1, columnspan=1, sticky=W)

        idlabel = Label(self, text=u"证件号码：")
        idlabel.grid(column=0, row=2, pady=1, padx=2, sticky=NSEW)

        identry = Entry(self, width=13)
        identry.grid(column=1, row=2, columnspan=1, sticky=W)

        phonenumlabel = Label(self, text=u"电话号码：", width=6)
        phonenumlabel.grid(column=0, row=3, padx=2, pady=1, sticky=NSEW)

        phonenumentry = Entry(self, width=19)
        phonenumentry.grid(column=1, row=3, columnspan=1, sticky=W)

        unitlabel = Label(self, text=u"单 位：")
        unitlabel.grid(column=0, row=4, padx=2, pady=1, sticky=NSEW)

        unitentry = Entry(self, width=19)
        unitentry.grid(column=1, row=4, columnspan=1, sticky=W)

        signinbutton = Button(self, text=u"注 册",
                              width=8, command=self.sign_infos)
        signinbutton.grid(column=4, row=3, rowspan=2, sticky=SE, padx=5, pady=4)

        titlesearchlabel = Label(self, text=u"信 息 查 询")
        titlesearchlabel.grid(column=0, row=5, sticky=W, padx=2)

        numsearchlabel = Label(self, text=u"查 询：", width=6)
        numsearchlabel.grid(column=0, row=6, sticky=NSEW)

        numsearchentry = Entry(self, width=19)
        numsearchentry.grid(column=1, row=6, sticky=W)

        numsearchbutton = Button(self, text=u"查 询",
                                 width=8, command=self.num_search)
        numsearchbutton.grid(column=4, row=6, sticky=E, padx=5, pady=4)

        validnumberlabel = Label(self, text=u"资 源 查 询")
        validnumberlabel.grid(column=0, row=7, padx=2, sticky=W)

        segsearchlabel = Label(self, text=u"号 段：", width=6)
        segsearchlabel.grid(column=0, row=8, sticky=NSEW)

        segsearchentry1 = Entry(self, width=19)
        segsearchentry1.grid(column=1, row=8, sticky=W)

        segsetchlabel2 = Label(self, text="~")
        segsetchlabel2.grid(column=2, row=8, sticky=NSEW)

        segsearchentry2 = Entry(self, width=18)
        segsearchentry2.grid(column=3, row=8, sticky=W)

        segsearchbutton = Button(self, text=u"空号查询",
                                 width=8, command=self.seg_search)
        segsearchbutton.grid(column=4, row=8, sticky=E, padx=5, pady=4)

        infotext = Text(self, width=60, height=28)
        infotext.grid(column=0, columnspan=5, sticky=W, padx=6, pady=6)

    def sign_infos(self):
        """save the sign in info to the file"""
        pass

    def num_search(self):
        """search for the designed number or person"""
        pass

    def seg_search(self):
        """search the unoccupied number among the designed segment"""
        pass

app = Application()
app.master.title(u'手机号码管理系统')
app.mainloop()
