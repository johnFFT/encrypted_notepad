import tkinter as tk
import tkinter.scrolledtext as scrolledtext



class TextBox(scrolledtext.ScrolledText):
    def __init__(self, master: tk.Misc | None = None, **kwargs) -> None:
          super().__init__(master, **kwargs)
          self.grid(row=0,column=1,stick="nsew", pady=(0,20))

    def spellCheck(self):
          pass

