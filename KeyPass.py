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
        def doNothing():
            pass
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




def timeoutGuesser(parent):
    def verifyPassword():
        pWord = pText.get()
        pText.delete(0,"end")
        if pWord == TIMEOUT_PASSWORD:
            popUp.destroy()
    parent.withdraw()
    popUp = tk.Toplevel(parent)
    popUp.title("Timeout")
    popUp.geometry("400x200")
    popUp.geometry("+%d+%d" %(parent.winfo_x()+(parent.bbox()[2]-306)//2,parent.winfo_y()+min(300,(parent.bbox()[3]-117)//2)))
    popUp.bind('<Return>', lambda e : verifyPassword())
    popUp.protocol("WM_DELETE_WINDOW", doNothing)
    pLabel = tk.Label(popUp, text="Session timed out; please enter password", font=('Segoe UI',12))
    pLabel.pack()
    pText = tk.Entry(popUp, show="*", width=30)
    pText.pack()
    parent.wait_window(popUp)
    try:
        parent.deiconify()
    except:
        sys.exit(0)


def doNothing():
    pass