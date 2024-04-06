import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tkinter as tk
import sys
from config import TIMEOUT_PASSWORD, PASSWORD_GUESS_LIMIT


def getKey(pword):
    password = pword.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b's\xa3E\x8a\x18\xb9\x8b\xc0">R[\x1b\xbdQ|', iterations=4000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)




def guessPasswordHelper(parent, encryptedText):
        # called by openFile and rewritePassword (and timeOut)
        # basically the authentication function, and is based on the last saved encrypted text
        class Vars:
             def __init__(self) -> None:
                  self.COUNT = PASSWORD_GUESS_LIMIT
                  self.Key = None
                  self.decryptedText = ""
        V = Vars()
        def verifyPassword(_):
            V.COUNT -= 1
            if V.COUNT==0:
                popUp.destroy()
                parent.destroy()
                return
            pWord = pText.get()
            pText.delete(0,"end")
            try:
                K = getKey(pWord)
                decryptedText = K.decrypt(encryptedText.encode()).decode()
                popUp.destroy()
                V.Key = K
                V.decryptedText = decryptedText
            except InvalidToken as e:
                print(f"Incorrect password - {V.COUNT} tries remain")
        parent.withdraw()
        popUp = tk.Toplevel(parent)
        popUp.iconbitmap('notepadIcon.ico')
        popUp.title("")
        popUp.geometry("300x200")
        popUp.bind('<Return>',verifyPassword)
        popUp.protocol("WM_DELETE_WINDOW", doNothing)
        pText = tk.Entry(popUp, show="*", width=30)
        pText.pack()
        parent.wait_window(popUp)
        try:
            parent.deiconify()
            return V.Key, V.decryptedText
        except:
            sys.exit(0)



# If the key is defined, I would like 'verifyPassword' to work in a similar way to how it works in 'guessPasswordHelper'
def timeoutGuesser(parent, popUpLabel="Session timed out; please enter password"):
    def verifyPassword():
        pWord = pText.get()
        pText.delete(0,"end")
        if pWord == TIMEOUT_PASSWORD:
            popUp.destroy()
    parent.withdraw()
    popUp = tk.Toplevel(parent)
    popUp.iconbitmap('notepadIcon.ico')
    popUp.title("Timeout")
    popUp.geometry("400x200")
    popUp.geometry("+%d+%d" %(parent.winfo_x()+(parent.bbox()[2]-306)//2,parent.winfo_y()+min(300,(parent.bbox()[3]-117)//2)))
    popUp.bind('<Return>', lambda _ : verifyPassword())
    popUp.protocol("WM_DELETE_WINDOW", doNothing)
    pLabel = tk.Label(popUp, text=popUpLabel, font=('Segoe UI',12))
    pLabel.pack()
    pText = tk.Entry(popUp, show="*", width=30)
    pText.pack()
    parent.wait_window(popUp)
    try:
        parent.deiconify()
    except:
        sys.exit(0)


# Create a pop-up window to change the value of self.timeoutLength in the app class
# I would like the 'pText' entry to only allow numbers (no letters or spaces) - https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
def configureTimeoutOptions(parent, textBox, timeOutValue):
    timeoutGuesser(parent, popUpLabel="Please enter password to configure timeout options")
    class T:
        def __init__(self, timeOutValue) -> None:
            self.timeOutValue = timeOutValue
    t = T(timeOutValue)
    def exitWindow():
        textBox['bg'] = 'white'
        textBox['fg'] = 'black'
        popUp.destroy()
    def changeTimeoutValue():
        if disableTimeout.get():
            t.timeOutValue = None
        else:
            t.timeOutValue = int(pText.get()) * 1000
        exitWindow()
    def validate(value):
        if str.isdigit(value) or value == "":
            return True
        return False
    popUp = tk.Toplevel(parent)
    vcmd = (popUp.register(validate))
    popUp.geometry("400x200")
    popUp.geometry("+%d+%d" %(parent.winfo_x()+(parent.bbox()[2]-306)//2,parent.winfo_y()+min(300,(parent.bbox()[3]-117)//2))) 
    popUp.iconbitmap('notepadIcon.ico')
    popUp.protocol("WM_DELETE_WINDOW", exitWindow)
    popUp.focus_set()
    popUp.grab_set()
    textBox['bg'] = '#888888'
    textBox['fg'] = '#686868'
    # handle logic here
    pText = tk.Entry(popUp, width=30, validate='all', validatecommand=(vcmd, '%P'))
    pText.insert(0, str(timeOutValue//1000) if timeOutValue else "")
    disableTimeout = tk.BooleanVar(value= False if timeOutValue else True)
    def activateTimeout():
        if disableTimeout.get():
            pText.configure(state = 'disabled')
        else:
            pText.configure(state = 'normal')
    activateTimeout()
    check = tk.Checkbutton(popUp, variable=disableTimeout, text="Disable timeout?", command=activateTimeout)
    check.pack()
    button = tk.Button(popUp, text="Save", command=changeTimeoutValue)
    button.pack()
    pText.bind('<Return>', lambda _ : changeTimeoutValue())
    pText.pack()
    parent.wait_window(popUp)
    return t.timeOutValue


def doNothing():
    pass