import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename


TIMEOUT_PASSWORD = "p4ssw0rd*"


def getKey(pword):
    password = pword.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b's\xa3E\x8a\x18\xb9\x8b\xc0">R[\x1b\xbdQ|', iterations=4000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)



class App:
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("Untitled.txt")
        self.parent.rowconfigure(0, minsize=800, weight=1)
        self.parent.columnconfigure(1, minsize=800, weight=1)
        #self.parent.iconbitmap(ICON_DIR)
        self.fileName = None
        self.decryptedText = ""
        self.Key = None

        self.textBox = self.textBoxInit(parent)

        self.parent.bind('<Control-o>',lambda event : self.openFile())
        self.parent.bind('<Control-s>',lambda event : self.saveFile())
        self.parent.bind('<Control-Shift-s>',lambda event : self.saveAsHelper())
        self.parent.bind('<Control-r>',lambda event : self.rewritePassword())
        self.parent.bind('<Control-n>',lambda event : self.createNewFile())
        self.parent.bind('<Control-q>',lambda event : self.quitProgram())

        self.parent.protocol("WM_DELETE_WINDOW", self.quitProgram) # if app window closes via clicking the [X] button

        # timeout stuff
        self.timeoutLength = 5*60*1000 # 5 minutes
        self.timeoutId = self.parent.after(self.timeoutLength,self.timeout)

        # Menu Bar 
        # File      
        self.menuBar = tk.Menu(self.parent, background='#ffcc99', foreground='black',
                               activebackground='white', activeforeground='black')
        self.menuFile = tk.Menu(self.menuBar, tearoff=False, background='#eeeeee',
                                foreground='black')
        self.menuBar.add_cascade(label="File",menu=self.menuFile)
        self.menuFile.add_command(label="New File",command=lambda : self.createNewFile())
        self.menuFile.add_command(label="Open",command=lambda : self.openFile())
        self.menuFile.add_command(label="Save",command=lambda : self.saveFile())
        self.menuFile.add_command(label="Save As",command=lambda : self.saveAsHelper())
        self.menuFile.add_command(label="Rewrite Password",command=lambda : self.rewritePassword())
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Exit",command=lambda : self.quitProgram())
        # Edit
        self.menuEdit = tk.Menu(self.menuBar, tearoff=False, background='#eeeeee',
                                foreground='black')
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
        def verifyPassword():
            pWord = pText.get()
            pText.delete(0,"end")
            if pWord == TIMEOUT_PASSWORD:
                popUp.destroy()
        def doNothing():
            pass
        self.parent.withdraw()
        popUp = tk.Toplevel(self.parent)
        popUp.title("Timeout")
        popUp.geometry("400x200")
        popUp.bind('<Return>', lambda e : verifyPassword())
        #popUp.overrideredirect(True)
        popUp.protocol("WM_DELETE_WINDOW", doNothing)
        pLabel = tk.Label(popUp, text="Session timed out; please enter password", font=('Segoe UI',13))
        pLabel.pack()
        pText = tk.Entry(popUp, show="*", width=30)
        pText.pack()
        self.parent.wait_window(popUp)
        try:
            self.parent.deiconify()
        except:
            sys.exit(0)
        self.timeoutId = self.parent.after(self.timeoutLength,self.timeout)


    def textBoxInit(self,parent):
        textBox = tk.Text(parent, wrap=tk.WORD, undo=True)
        textBox.insert(1.0,self.decryptedText)
        textBox.bind('<KeyRelease>',self.setTitle)
        textBox.bind('<Button-1>',self.setTitle)
        textBox.grid(row=0,column=1,stick="nsew") # column=1
        scrollbar = tk.Scrollbar(textBox, command=textBox.yview)
        scrollbar.pack( side = tk.RIGHT, fill=tk.Y )
        textBox['yscrollcommand'] = scrollbar.set
        return textBox


    def textChanged(self):
        text = self.textBox.get(1.0,"end").rstrip('\n')
        return text!=self.decryptedText


    def setTitle(self,event):
        self.resetTimer()
        hasChanged = self.textChanged()
        fileName = self.fileName if self.fileName else "Untitled.txt"
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
        class PassHandle:
            def __init__(self,parent):
                self.arr = ["",None]
                self.parent = parent
                self.quit = False
            def set(self,event):
                self.arr[self.idx] = self.pText.get()
                self.pText.delete(0,"end")
                self.savePopUp.destroy()
            def quitWindow(self):
                self.quit = True
                self.savePopUp.destroy()
            def popUp(self,pVerb):
                self.savePopUp = tk.Toplevel(self.parent)
                self.savePopUp.protocol("WM_DELETE_WINDOW", self.quitWindow)
                self.savePopUp.geometry("300x120")
                self.savePopUp.focus_set()
                self.savePopUp.grab_set()
                label = tk.Label(self.savePopUp, text="Please "+pVerb+" password")
                label.pack()
                self.pText = tk.Entry(self.savePopUp, show="*", width=30)
                self.pText.pack()
                self.savePopUp.bind('<Return>',self.set)
                self.parent.wait_window(self.savePopUp)
            def run(self):
                pVerb = ["set","confirm"]
                self.idx = 0
                while not self.quit and self.arr[0]!=self.arr[1]:
                    if self.idx == 0:
                        self.arr = ["",None]
                    self.popUp(pVerb[self.idx])
                    self.idx = 1-self.idx
                return self.quit, self.arr[0]
        p = PassHandle(self.parent)
        quitBool, key = p.run()
        if not quitBool:
            self.Key = getKey(key)
        return quitBool
        

    def saveAsHelper(self):
        initFileName = self.fileName if self.fileName else "Untitled"
        quitBool = self.setNewFilePassword()
        if quitBool:
            return
        fileName = asksaveasfilename(initialfile = initFileName,
                                defaultextension=".txt",
                                filetypes=[('All Text Files',['.txt','.json']),
                                           ('.txt','.txt'), ('.json','.json')])
        if fileName:
            self.fileName = fileName
            self.writeToFile()

    def rewritePassword(self):
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
        self.parent.title("Untitled.txt")
        self.decryptedText = ""
        self.textBox.delete(1.0,"end")
        self.Key = None
        

    def guessPassword(self,encryptedText):
        # called by openFile and rewritePassword (and timeOut)
        # basically the authentication function, and is based on the last saved encrypted text
        self.COUNT = 3
        def verifyPassword(event):
            self.COUNT -= 1
            if self.COUNT==0:
                popUp.destroy()
                self.parent.destroy()
                return
            pWord = pText.get()
            pText.delete(0,"end")
            try:
                K = getKey(pWord)
                decryptedText = K.decrypt(encryptedText.encode()).decode()
                popUp.destroy()
                self.Key = K
                self.decryptedText = decryptedText
            except InvalidToken as e:
                print(f"Incorrect password - {self.COUNT} tries remain")
        self.parent.withdraw()
        popUp = tk.Toplevel(self.parent)
        popUp.title("")
        popUp.geometry("300x200")
        popUp.bind('<Return>',verifyPassword)
        pText = tk.Entry(popUp, show="*", width=30)
        pText.pack()
        self.parent.wait_window(popUp)
        try:
            self.parent.deiconify()
        except:
            sys.exit(0)

    def handleChanges(self):
        class ChangesClass:
            def __init__(self):
                self.keepGoing = True
        c = ChangesClass()
        hasChanged = self.textChanged()
        def pushButton(eventType):
            self.textBox['bg'] = 'white'
            self.textBox['fg'] = 'black'
            popUp.destroy()
            if eventType == "s":
                self.saveFile()
            elif eventType == "c":
                c.keepGoing = False
        if hasChanged:
            popUp = tk.Toplevel(self.parent)
            popUp.title("")
            #popUp.geometry("450x200")
            popUp['bg'] = '#ffffff'
            popUp.focus_set()
            popUp.grab_set()
            popUp.protocol("WM_DELETE_WINDOW", lambda : pushButton("c"))
            #popUp.wm_attributes('-fullscreen','True')
            #popUp.overrideredirect(True)
            #popUp.attributes('-disabled', True)
            popUp.bind("<Return>",lambda event : pushButton("s"))
            popUp.bind("<Escape>",lambda event : pushButton("c"))
            self.textBox['bg'] = '#888888'
            self.textBox['fg'] = '#686868'
            fileName = self.fileName.split('/')[-1] if self.fileName else "Untitiled.txt"
            saveText = tk.Label(popUp, text=f'Would you like to save changes to "{fileName}"?', bg=popUp['bg'])
            saveText.grid(row=0,columnspan=3,pady=15,padx=20)
            saveButton = tk.Button(popUp,text="Save",height = 1, width=10, bg='#0969ff', fg='#ffffff', command = lambda : pushButton("s"))
            saveButton.grid(row=1,column=0,pady=20)
            discardButton = tk.Button(popUp,text="Don't save",height=1, width=10,command = lambda : pushButton("d"))
            discardButton.grid(row=1,column=1,pady=20)
            cancelButton = tk.Button(popUp,text="Cancel",height=1,width=10,command = lambda : pushButton("c"))
            cancelButton.grid(row=1,column=2,pady=20)
            popUp.geometry("+%d+%d" %(self.parent.winfo_x()+(self.parent.bbox()[2]-306)//2,self.parent.winfo_y()+min(300,(self.parent.bbox()[3]-117)//2))) # (307,117) is the size of popUp when "Untitled.txt" is the fileName
            self.parent.wait_window(popUp)
        return c.keepGoing


    def openFile(self):
        keepGoing = self.handleChanges()
        if not keepGoing:
            return
        # Open file
        fileObj = askopenfile(title="Please select a file",
                              filetypes=[('All Text Files',['.txt','.json']),
                                         ('.txt','.txt'), ('.json','.json')])
        if fileObj:
            self.fileName = fileObj.name
            self.parent.title(self.fileName)
            self.textBox.delete(1.0,"end")
            with open(self.fileName,"r") as file:
                encryptedText = file.read()
            self.guessPassword(encryptedText) # setting Key and descryptedText here
            self.textBox.insert(1.0,self.decryptedText)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
