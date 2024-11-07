from tkinter import *
import os

root = Tk()

root.title("4 in a row")

root.geometry('350x350')

lbl = Label(root, text = "Can you beat the AI?")
lbl.grid()

#def clicked():
#    lbl.configure(text = "I just got clicked")

def openBoard():
    os.system('python Board.py')

# button widget with red color text
# inside
pvp = Button(root, text = "PvP" ,
             fg = "red", command=openBoard)

pvai = Button(root, text = "PvAI" ,
             fg = "red", command=openBoard)

# set Button grid
pvp.grid(column=1, row=0)
pvai.grid(column=1, row=1)

root.mainloop()