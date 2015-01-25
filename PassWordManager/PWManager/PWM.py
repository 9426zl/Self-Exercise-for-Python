#coding=gbk
from Tkinter import *
import tkMessageBox

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		"define the storage module"
		self.StorageLabel = Label(self, text = u"密码保存")
		self.StorageLabel.grid(column = 0, row = 0, sticky = W)
		
		self.nameInputLabel = Label(self, text = u"网站名:")
		self.nameInputLabel.grid(column = 0, row = 1, sticky = W)
		self.nameInput = Entry(self)
		self.nameInput.grid(column = 1, row = 1, sticky = W)
		
		self.accountInputLabel = Label(self, text = u"账户名:")
		self.accountInputLabel.grid(column = 0, row = 2, sticky = W)
		self.accountInput = Entry(self)
		self.accountInput.grid(column = 1, row = 2, sticky = W)
		
		self.passwordInputLabel = Label(self, text = u"密码:")
		self.passwordInputLabel.grid(column = 0, row = 3, sticky = W)
		self.passwordInput = Entry(self)
		self.passwordInput.grid(column = 1, row = 3, sticky = W)
		
		self.saveButton = Button(self, text = u'保存 ', command = self.saveInformation)
		self.saveButton.grid(column = 2, row = 3, padx =5)
		
		"define the search module"
		self.SearchLabel = Label(self, text = u"密码查找")
		self.SearchLabel.grid(column = 0, row = 4, sticky = W)
		
		self.WebnameLabel = Label(self, text = u"网站名:")
		self.WebnameLabel.grid(column = 0, row = 5, sticky = W)
		self.senameInput = Entry(self)
		self.senameInput.grid(column = 1, row = 5, sticky = W)
		self.seButton = Button(self, text = u'搜索', command = self.searchInformation)
		self.seButton.grid(column = 2, row = 5, padx =5)


	def saveInformation(self):
		"define the search function"
		Webname = self.nameInput.get()
		Aconame = self.accountInput.get()
		PassWord = self.passwordInput.get()
		fp = open("InfoSaved.txt", 'a')
		fp.write(Webname)
		fp.write("\\")
		fp.write(Aconame)
		fp.write("\\")
		fp.write(PassWord)
		fp.write("\n")
		fp.close()
		
		tkMessageBox.showinfo("Message", "Information Saved:\n Website: %s\n Account: %s\n PassWord: %s"
							% (Webname, Aconame, PassWord))


	def searchInformation(self):
		"define the search function"
		searchname = self.senameInput.get()
		fp = open("InfoSaved.txt", 'r')
		found = False
		for line in fp:
			if searchname in line:
				ansline = line
				found = True
				break
		
		if found:
			tkMessageBox.showinfo("Message",u"该网站注册的账户名与密码分别是 %s"
								% ansline)
		else:
			tkMessageBox.showinfo("Message",u"抱歉，未能查找到相关信息")

app = Application()
# Set the title of the GUI
app.master.title('PassWordManager')
# Main information Loop
app.mainloop()