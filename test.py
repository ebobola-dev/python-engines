import pyglet
from tkinter import Tk
from tkinter.ttk import *
pyglet.font.add_file('fonts/helvetica.otf')

from config.ui import UI_CONFIG
from config.ui import UI_COLORS

gui = Tk()
gui.title(UI_CONFIG.PROGRAM_NAME)
gui.geometry("{0}x{1}".format(*UI_CONFIG.WINDOW_SIZE)) #? "500x300"
gui.configure(bg=UI_COLORS.background)

s = Style()
s.configure('Main.TFrame', background=UI_COLORS.background)

frm = Frame(gui, padding=50, style='Main.TFrame')
frm.grid()
Label(frm, text="Hello World!", font='helvetica', background=UI_COLORS.background).grid(column=0, row=0)
# Button(frm, text="Quit", command=gui.destroy).grid(column=1, row=0)
gui.mainloop()