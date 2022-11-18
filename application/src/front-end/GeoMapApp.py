from tkinter import *
import tkintermapview
from tkinter import ttk

root = Tk()
root.title('CSE412 Project')

def lookup():
    map_widget.set_address(my_entry.get())
    my_slider.config(value=9)

def slide(e):
    map_widget.set_zoom(my_slider.get())

def filterShow():
    pass

my_label = LabelFrame(root)
my_label.pack(pady=20)


map_widget = tkintermapview.TkinterMapView(my_label, width=700, height=500, corner_radius=0)
map_widget.set_zoom(50)
map_widget.pack()

my_filter = LabelFrame(root)
my_filter.pack(pady=7)

filter_button = Button(my_filter, text="Filter", font=("Helvetica", 18), command=filterShow)
filter_button.grid(row=0, column=1, padx=10)

my_frame = LabelFrame(root)
my_frame.pack(pady=10)

my_entry = Entry(my_frame, font=("Helvetica",28))
my_entry.grid(row=0, column=0, pady=20, padx=10)

my_button = Button(my_frame, text="Lookup", font=("Helvetica", 18), command=lookup)
my_button.grid(row=0, column=1, padx=10)

my_slider = ttk.Scale(my_frame, from_=4, to=20, orient=HORIZONTAL, command=slide, value=20, length=220)
my_slider.grid(row=0, column=2, padx=10)


mark1 = map_widget.set_address("Phoenix, Arizona",marker=True)
mark2 = map_widget.set_address("Tuscon, Arizona",marker=True)
path1 = map_widget.set_path([mark1.position, mark2.position])
map_widget.set_address("Phoenix, Arizona")

root.geometry("900x700")

root.mainloop()