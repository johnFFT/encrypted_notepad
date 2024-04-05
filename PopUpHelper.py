import tkinter as tk
from config import DEFAULT_UNTITLED



def newPasswordPopUp(parent):
    class PassHandle:
        def __init__(self,parent):
            self.arr = ["",None]
            self.parent = parent
            self.quit = False
        def set(self,_):
            self.arr[self.idx] = self.pText.get()
            self.pText.delete(0,"end")
            self.savePopUp.destroy()
        def quitWindow(self):
            self.quit = True
            self.savePopUp.destroy()
        def popUp(self,pVerb):
            self.savePopUp = tk.Toplevel(self.parent)
            self.savePopUp.iconbitmap('notepadIcon.ico')
            self.savePopUp.protocol("WM_DELETE_WINDOW", self.quitWindow)
            self.savePopUp.geometry("300x120")
            self.savePopUp.geometry("+%d+%d" %(self.parent.winfo_x()+(self.parent.bbox()[2]-306)//2,self.parent.winfo_y()+min(300,(self.parent.bbox()[3]-117)//2)))
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
    p = PassHandle(parent)
    return p.run() # quitBool, keyword = p.run()











def saveChangesPopUp(parent, textBox, thisFileName, saveFileFun, c):
    def pushButton(eventType):
        textBox['bg'] = 'white'
        textBox['fg'] = 'black'
        popUp.destroy()
        if eventType == "s":
            saveFileFun()
        elif eventType == "c":
            c.keepGoing = False
    popUp = tk.Toplevel(parent)
    popUp.iconbitmap('notepadIcon.ico')
    popUp.title("")
    #popUp.geometry("450x200")
    popUp['bg'] = '#ffffff'
    popUp.focus_set()
    popUp.grab_set()
    popUp.protocol("WM_DELETE_WINDOW", lambda : pushButton("c"))
    #popUp.wm_attributes('-fullscreen','True')
    #popUp.overrideredirect(True)
    #popUp.attributes('-disabled', True)
    popUp.bind("<Return>",lambda _ : pushButton("s"))
    popUp.bind("<Escape>",lambda _ : pushButton("c"))
    textBox['bg'] = '#888888'
    textBox['fg'] = '#686868'
    fileName = thisFileName.split('/')[-1] if thisFileName else DEFAULT_UNTITLED
    saveText = tk.Label(popUp, text=f'Would you like to save changes to "{fileName}"?', bg=popUp['bg'])
    saveText.grid(row=0,columnspan=3,pady=15,padx=20)
    saveButton = tk.Button(popUp,text="Save",height = 1, width=10, bg='#0969ff', fg='#ffffff', command = lambda : pushButton("s"))
    saveButton.grid(row=1,column=0,pady=20)
    discardButton = tk.Button(popUp,text="Don't save",height=1, width=10,command = lambda : pushButton("d"))
    discardButton.grid(row=1,column=1,pady=20)
    cancelButton = tk.Button(popUp,text="Cancel",height=1,width=10,command = lambda : pushButton("c"))
    cancelButton.grid(row=1,column=2,pady=20)
    popUp.geometry("+%d+%d" %(parent.winfo_x()+(parent.bbox()[2]-306)//2,parent.winfo_y()+min(300,(parent.bbox()[3]-117)//2))) # (307,117) is the size of popUp when "Untitled.txt" is the fileName
    parent.wait_window(popUp)
    return c