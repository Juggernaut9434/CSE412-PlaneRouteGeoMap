from tkinter import *
window=Tk()
# add widgets here

window.title('Hello Python')
window.geometry("750x280")
canvas = Canvas(window, width = 850, height = 750, bg = "cyan")
canvas.create_text(375,50, text = "Hello World!", fill = "black", font = ('Helvetica 15 bold'))
canvas.pack()
window.mainloop()
