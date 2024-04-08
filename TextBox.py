import tkinter as tk
#from tkinter.font import Font
#from tkinter import font
import tkinter.scrolledtext as scrolledtext



class TextBox(scrolledtext.ScrolledText):
    def __init__(self, master: tk.Misc | None = None, **kwargs) -> None:
          super().__init__(master, **kwargs)
          self.grid(row=0,column=1,stick="nsew", pady=(0,20))
          #self.defaultFont = tkFont(self,self.cget("font"))
          #
          # Experiment
          self.insert(1.0,"This is a test\nasdfsafsd\n\n\naaaaaaaaaaaaaaaaaa\n\nlllllsdfsd")
          self.tag_config('bold', font=('Courier', '11', 'bold'))
          self.tag_config('highlightline', background='yellow', foreground='blue', relief='raised')
          self.bind('<Control-b>',lambda _ : self.addFontTags("bold"))
          self.bind('<Control-p>',lambda _ : self.addFontTags("highlightline"))


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
         

    def spellCheck(self):
          pass



'''

     self.bind('<Control-m>', lambda _ : self.printForDebug())

    def printForDebug(self):
         #print(font.nametofont(self['font']).configure()["family"])
         print(font.nametofont(self.cget('font')))
         print("--------------")
         if self.tag_ranges("sel"):
              current_tags = self.tag_names("sel.first")
              print(current_tags)
         else:
              print(self.index(tk.INSERT))
         for x in self.tag_names():
              print(x, self.tag_ranges(x))



def make_bold():
    aText.tag_add("bt", "sel.first", "sel.last")

lord = tk.Tk()

aText = tk.Text(lord, font=("Georgia", "12"))
aText.grid()

aButton = tk.Button(lord, text="bold", command=make_bold)
aButton.grid()

aText.tag_config("bt", font=("Georgia", "12", "bold"))


my_font = Font(
    family = 'Times',
    size = 30,
    weight = 'bold',
    slant = 'roman',
    underline = 1,
    overstrike = 0
)

self.tag_config('highlightline', background='yellow', font=('TkFixedFont'), relief='raised')


'''