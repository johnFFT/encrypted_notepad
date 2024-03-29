import tkinter as tk
from TextBox import TextBox
from tkinter.filedialog import askopenfile, asksaveasfilename
from config import TIMEOUT_TIME, DEFAULT_UNTITLED
from KeyPass import getKey, guessPasswordHelper, timeoutGuesser
from PopUpHelper import newPasswordPopUp, saveChangesPopUp



class App:
    def __init__(self,parent):
        self.parent = parent
        self.parent.title(DEFAULT_UNTITLED)
        self.parent.rowconfigure(0, minsize=800, weight=1)
        self.parent.columnconfigure(1, minsize=800, weight=1)
        self.parent.iconbitmap('notepadIcon.ico')
        self.fileName = None
        self.decryptedText = ""
        self.Key = None

        self.textBox = TextBox(parent, wrap=tk.WORD, undo=True, font=('Courier',11))
        self.textBox.bind('<KeyRelease>',self.setTitle)
        self.textBox.bind('<Button-1>',self.setTitle)

        self.parent.bind('<Control-o>',lambda _ : self.openFile())
        self.parent.bind('<Control-s>',lambda _ : self.saveFile())
        self.parent.bind('<Control-Shift-s>',lambda _ : self.saveAsHelper())
        self.parent.bind('<Control-r>',lambda _ : self.rewritePassword())
        self.parent.bind('<Control-n>',lambda _ : self.createNewFile())
        self.parent.bind('<Control-q>',lambda _ : self.quitProgram())
        self.parent.bind('<Control-l>',lambda _ : self.timeout()) # might be worth making a new function rather than using timeout

        self.parent.protocol("WM_DELETE_WINDOW", self.quitProgram) # if app window closes via clicking the [X] button

        # timeout stuff
        self.timeoutLength = TIMEOUT_TIME*1000
        self.timeoutId = self.parent.after(self.timeoutLength,self.timeout)

        # Menu Bar 
        # File      
        self.menuBar = tk.Menu(self.parent, background='#ffcc99', foreground='black',
                               activebackground='white', activeforeground='black',font=('Segoe UI',10))
        self.menuFile = tk.Menu(self.menuBar, tearoff=False, background='#eeeeee',
                                foreground='black',font=('Segoe UI',10))
        self.menuBar.add_cascade(label="File",menu=self.menuFile)
        self.menuFile.add_command(label="New File",command=lambda : self.createNewFile())
        self.menuFile.add_command(label="Open",command=lambda : self.openFile())
        self.menuFile.add_command(label="Save",command=lambda : self.saveFile())
        self.menuFile.add_command(label="Save As",command=lambda : self.saveAsHelper())
        self.menuFile.add_command(label="Rewrite Password",command=lambda : self.rewritePassword())
        self.menuFile.add_command(label="Lock App",command=lambda : self.timeout())
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit",command=lambda : self.quitProgram())
        # Edit
        self.menuEdit = tk.Menu(self.menuBar, tearoff=False, background='#eeeeee',
                                foreground='black',font=('Segoe UI',10))
        self.menuEdit.add_command(label="Undo",command=lambda : self.textBox.event_generate("<<Undo>>"))
        self.menuEdit.add_command(label="Cut",command=lambda : self.textBox.event_generate("<<Cut>>"))
        self.menuEdit.add_command(label="Copy",command=lambda : self.textBox.event_generate("<<Copy>>"))
        self.menuEdit.add_command(label="Paste",command=lambda : self.textBox.event_generate("<<Paste>>"))
        self.menuBar.add_cascade(label="Edit",menu=self.menuEdit)
        
        self.parent.config(menu=self.menuBar)
        
        
    def resetTimer(self):
        if self.timeoutId is not None:
            self.parent.after_cancel(self.timeoutId)
            self.timeoutId = self.parent.after(self.timeoutLength,self.timeout)


    def timeout(self):
        timeoutGuesser(self.parent)
        self.timeoutId = self.parent.after(self.timeoutLength,self.timeout)


    def textChanged(self):
        text = self.textBox.get(1.0,"end").rstrip('\n')
        return text!=self.decryptedText


    def setTitle(self,_):
        self.resetTimer()
        hasChanged = self.textChanged()
        fileName = self.fileName if self.fileName else DEFAULT_UNTITLED
        if hasChanged:
            self.parent.title("*"+fileName)
        else:
            self.parent.title(fileName)
    

    def quitProgram(self):
        keepGoing = self.handleChanges()
        if not keepGoing:
            return
        self.parent.destroy()
        

    def writeToFile(self):
        self.decryptedText = self.textBox.get(1.0,"end").rstrip('\n')
        with open(self.fileName,"w") as file:
            file.write(self.Key.encrypt(self.decryptedText.encode()).decode())
        self.parent.title(self.fileName)
        
    
    def saveFile(self):
        if not self.fileName: # New doc
            self.saveAsHelper()
        else:
            self.writeToFile()
            

    def setNewFilePassword(self):
        quitBool, keyword = newPasswordPopUp(self.parent)
        if not quitBool:
            self.Key = getKey(keyword)
        return quitBool
        

    def saveAsHelper(self):
        initFileName = self.fileName if self.fileName else DEFAULT_UNTITLED.split('.')[0]
        quitBool = self.setNewFilePassword()
        if quitBool:
            return
        fileTypes = [('All Text Files',['.txt','.json', '.autosave']), ('.txt','.txt'), ('.json','.json')]
        fileName = asksaveasfilename(initialfile = initFileName, defaultextension=".txt", filetypes = fileTypes)
        if fileName:
            self.fileName = fileName
            self.writeToFile()


    def rewritePassword(self):
        if not self.fileName: # New doc
            self.saveAsHelper()
            return
        with open(self.fileName,"r") as file:
            encryptedText = file.read()
        self.guessPassword(encryptedText)
        quitBool = self.setNewFilePassword()
        if quitBool:
            return
        self.writeToFile()


    def createNewFile(self):
        keepGoing = self.handleChanges()
        if not keepGoing:
            return
        self.fileName = None
        self.parent.title(DEFAULT_UNTITLED)
        self.decryptedText = ""
        self.textBox.delete(1.0,"end")
        self.Key = None
        

    def guessPassword(self,encryptedText):
        key, decryptedText = guessPasswordHelper(self.parent, encryptedText)
        self.Key = key
        self.decryptedText = decryptedText


    def handleChanges(self):
        class ChangesClass:
            def __init__(self):
                self.keepGoing = True
        c = ChangesClass()
        hasChanged = self.textChanged()
        if hasChanged:
            c = saveChangesPopUp(self.parent,self.textBox, self.fileName, self.saveFile, c)
        return c.keepGoing


    def openFile(self):
        keepGoing = self.handleChanges()
        if not keepGoing:
            return
        # Open file
        fileTypes = [('All Text Files',['.txt','.json', '.autosave']), ('.txt','.txt'), ('.json','.json')]
        fileObj = askopenfile(title="Please select a file", filetypes=fileTypes)
        if fileObj:
            self.fileName = fileObj.name
            self.parent.title(self.fileName)
            self.textBox.delete(1.0,"end")
            with open(self.fileName,"r") as file:
                encryptedText = file.read()
            self.guessPassword(encryptedText) # setting Key and decryptedText here
            self.textBox.insert(1.0,self.decryptedText)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
