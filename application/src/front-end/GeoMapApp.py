from tkinter import *
import tkintermapview
from tkinter import ttk
from route import Route


route1 = Route("2B", "ASF", 46.2832984924, 48.0063018799, "KZN", 55.606201171875, 49.278701782227)
route2 = Route("2B", "GYD", 40.467498779296875, 50.04669952392578, "NBC", 55.564701080322266, 52.092498779296875)
route3 = Route("2B", "ASF", 46.2832984924, 48.0063018799, "KZN", 55.606201171875, 49.278701782227)

routess = [route1, route2]


root = Tk()
root.title('CSE412 Project')



# lookup function, takes in the city name and sets the address to that location
def lookup():
    map_widget.set_address(my_entry.get())
    my_slider.config(value=9)

#slide function sets the zoom on the map
def slide(e):
    map_widget.set_zoom(my_slider.get())

#filterShow function displays the filter box
def filterShow():
    filterBox = Tk()
    filterBox.title("Filter Routes")
    labelFilter = ttk.Label(filterBox, text="temp label")
    labelFilter.pack(side="top", fill="x", pady=10)
    B1 = Button(filterBox, text="Okay", command = filterBox.destroy)
    B1.pack()
    filterBox.geometry('400x200')
    filterBox.mainloop()

#setMarker sets the marker
def setMarker(tempLat, tempLong):
    return map_widget.set_marker(tempLat, tempLong)

#setPath sets the path between 2 markers
def setPath(first, second):
    return map_widget.set_path([first.position, second.position])

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





mark1 = setMarker(getattr(routess[0], 'src_lat'), getattr(routess[0], 'src_long'))
mark2 = setMarker(getattr(routess[0], 'dest_lat'), getattr(routess[0], 'dest_long'))

setPath(mark1, mark2)

map_widget.set_address("Russia",marker=False)

root.geometry("900x700")

root.mainloop()