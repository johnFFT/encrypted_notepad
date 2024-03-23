import unittest
from app import App, getKey
import tkinter as tk
import os



class TKinterTestCase(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.tk.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass
        

class TestAppFunction(TKinterTestCase):

    def test_encoding_decoding(self):
        # initialize test values
        orig_text, fname, key = "This is a test", "delet1234.txt", getKey("123")
        # initialize app
        a = App(self.root)
        self.pump_events()
        # interact virtually with the UI 
        a.textBox.insert("1.0",orig_text)
        a.Key = key
        a.fileName = fname
        a.writeToFile()
        self.pump_events()
        a.createNewFile()
        self.pump_events()
        # now that interaction with the app is complete, test the encoding/decoding
        with open(fname,"r") as file:
            encryptedText = file.read()
        decryptedText = key.decrypt(encryptedText.encode()).decode()
        os.remove(fname)
        # assertion test
        self.assertEqual(orig_text, decryptedText, "Plaintext instances should be the same")

    def test_password_change(self):
        # initialize test values
        orig_text, fname, key1, key2 = "This is a test", "delet1234.txt", getKey("123"), getKey("456")
        # initialize app
        a = App(self.root)
        self.pump_events()
        # interact virtually with the UI 
        a.textBox.insert("1.0",orig_text)
        a.Key = key1
        a.fileName = fname
        a.writeToFile()
        self.pump_events()
        # encrypt/decrypt with different keys
        with open(fname,"r") as file:
            encryptedText1 = file.read()
        decryptedText = key1.decrypt(encryptedText1.encode()).decode()
        with open(fname,"w") as file:
            file.write(key2.encrypt(decryptedText.encode()).decode())
        with open(fname,"r") as file:
            encryptedText2 = file.read()
        decryptedText = key2.decrypt(encryptedText2.encode()).decode()
        os.remove(fname)
        # assertion test
        self.assertEqual(orig_text, decryptedText, "Plaintext instances should be the same")
        self.assertNotEqual(encryptedText1,encryptedText2, "Encrypted with two different keys - they should not match")


if __name__ == '__main__':
    unittest.main()







