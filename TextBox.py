import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as scrolledtext



class TextBox(scrolledtext.ScrolledText):
    def __init__(self, master: tk.Misc | None = None, **kwargs) -> None:
          super().__init__(master, **kwargs)
          self.grid(row=0,column=1,stick="nsew", pady=(0,20))
          #self.defaultFont = tkFont(self,self.cget("font"))
          #
          # Experiment
          self.insert(1.0,"This is a test\nasdfsafsd\n\n\naaaaaaaaaaaaaaaaaa\n\nlllllsdfsd")
          self.tag_config('highlightline', background='yellow', font='TkFixedFont', relief='raised')
          self.tag_config('highlightline2', foreground='blue', font='TkFixedFont', relief='raised')
          self.bind('<Control-b>',lambda _ : self.addFontTags("highlightline"))
          self.bind('<Control-p>',lambda _ : self.addFontTags("highlightline2"))
          self.bind('<Control-m>', lambda _ : self.printForDebug())


    def addFontTags(self, tagName):
         if self.tag_ranges("sel"): # text section is highlighted
              current_tags = self.tag_names("sel.first")
              if tagName in current_tags:
                   self.tag_remove(tagName, "sel.first", "sel.last")
              else:
                   self.tag_add(tagName, "sel.first", "sel.last")
              #self.tag_add(tagName, "sel.first", "sel.last")
         else:
              pass
              '''
              pos = self.index(tk.INSERT)
              pos2 = pos.split('.')[0] + '.' + str(int(pos.split('.')[1]) + 1)
              self.tag_add(tagName, pos, pos2)
              '''
         

    def printForDebug(self):
         print("--------------")
         if self.tag_ranges("sel"):
              current_tags = self.tag_names("sel.first")
              print(current_tags)
         else:
              print(self.index(tk.INSERT))
         for x in self.tag_names():
              print(x, self.tag_ranges(x))


    def spellCheck(self):
          pass



'''
def make_bold():
    aText.tag_add("bt", "sel.first", "sel.last")

lord = tk.Tk()

aText = tk.Text(lord, font=("Georgia", "12"))
aText.grid()

aButton = tk.Button(lord, text="bold", command=make_bold)
aButton.grid()

aText.tag_config("bt", font=("Georgia", "12", "bold"))
'''