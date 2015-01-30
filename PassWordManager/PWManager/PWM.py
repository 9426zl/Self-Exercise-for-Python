# coding=gbk
import os, random, struct
from Tkinter import *
import tkMessageBox
from Crypto.Cipher import AES


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        "define the storage module"
        self.StorageLabel = Label(self, text=u"密码保存")
        self.StorageLabel.grid(column=0, row=0, sticky=W)

        self.nameInputLabel = Label(self, text=u"网站名:")
        self.nameInputLabel.grid(column=0, row=1, sticky=W)
        self.nameInput = Entry(self)
        self.nameInput.grid(column=1, row=1, sticky=W)

        self.accountInputLabel = Label(self, text=u"账户名:")
        self.accountInputLabel.grid(column=0, row=2, sticky=W)
        self.accountInput = Entry(self)
        self.accountInput.grid(column=1, row=2, sticky=W)

        self.passwordInputLabel = Label(self, text=u"密码:")
        self.passwordInputLabel.grid(column=0, row=3, sticky=W)
        self.passwordInput = Entry(self)
        self.passwordInput.grid(column=1, row=3, sticky=W)

        self.saveButton = Button(self, text=u'保存 ',
                                 command=self.saveInformation)
        self.saveButton.grid(column=2, row=3, padx=5)

        "define the search module"
        self.SearchLabel = Label(self, text=u"密码查找")
        self.SearchLabel.grid(column=0, row=4, sticky=W)

        self.WebnameLabel = Label(self, text=u"网站名:")
        self.WebnameLabel.grid(column=0, row=5, sticky=W)
        self.senameInput = Entry(self)
        self.senameInput.grid(column=1, row=5, sticky=W)
        self.seButton = Button(self, text=u'搜索',
                               command=self.searchInformation)
        self.seButton.grid(column=2, row=5, padx=5)

    def saveInformation(self):
        "define the search function"
        Webname = self.nameInput.get()
        Aconame = self.accountInput.get()
        PassWord = self.passwordInput.get()
        self.decrypt_file()
        fp = open("InfoSaved.txt", 'a')
        fp.write(Webname)
        fp.write("\\")
        fp.write(Aconame)
        fp.write("\\")
        fp.write(PassWord)
        fp.write("\n")
        fp.close()
        self.encrypt_file()
        tkMessageBox.showinfo("Message", "Information Saved:\n Website: %s\n Account: %s\n PassWord: %s"
                              % (Webname, Aconame, PassWord))
        self.nameInput.delete(0, END)
        self.accountInput.delete(0, END)
        self.passwordInput.delete(0, END)


    def searchInformation(self):
        "define the search function"
        searchname = self.senameInput.get()
        self.decrypt_file()
        fp = open("InfoSaved.txt", 'r')
        found = False
        for line in fp:
            if searchname in line:
                ansline = line
                found = True
                break
        fp.close()
        if found:
            tkMessageBox.showinfo("Message", u"该网站注册的账户名与密码分别是 %s"
                                  % ansline)
        else:
            tkMessageBox.showinfo("Message", u"抱歉，未能查找到相关信息")
        self.senameInput.delete(0, END)

        self.encrypt_file()


    def encrypt_file(self):
        "define the encrypt function"
        key = "12345678asdfghjk"
        in_filename = "InfoSaved.txt"
        out_filename = "InfoSaved.enc.txt"
        chunksize = 64*1024
        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        os.remove('InfoSaved.txt')


    def decrypt_file(self):
        "define the decrypt function"
        key = "12345678asdfghjk"
        in_filename = "InfoSaved.enc.txt"
        out_filename = "InfoSaved.txt"
        chunksize = 64*1024

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)


app = Application()
# Set the title of the GUI
app.master.title('PassWordManager')
# Main information Loop
app.mainloop()