from tkinter import *
import tkintermapview

root = Tk()
root.title('CSE412 Project')

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=500, height=375, corner_radius=0)
map_widget.pack()
root.geometry("800x600")

root.mainloop()