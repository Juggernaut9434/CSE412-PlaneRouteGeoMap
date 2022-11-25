from tkinter import *
import tkintermapview
from tkinter import ttk
from src.back_end.route import Route
from src.back_end.database import Database

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

def createPath(route: Route) -> tkintermapview.map_widget.CanvasPath:
    """Creates a path on the map_widget of the given Route"""
    return map_widget.set_path([route.getSource(), route.getDestination()], width=2)

my_label = LabelFrame(root)
my_label.pack(pady=20)


map_widget = tkintermapview.TkinterMapView(my_label, width=700, height=500, corner_radius=0)
map_widget.set_address("New York")
map_widget.set_zoom(1)
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


# Add routes to map
oldPaths: list[tkintermapview.map_widget.CanvasPath] = []

def mapRoutes(routesList: list[Route], debug=False):
    for path in oldPaths:
        # Clear old routes from map
        path.delete()
    
    oldPaths.clear()   

    for i in range(len(routesList)):
        if debug:
            print(f"Mapping route #{i+1} / {len(routesList)}: {str(routesList[i])}")
        oldPaths.append(createPath(routesList[i]))
        print(oldPaths[i])




# Sample Filter Functions

def mapRoutesALL():
    mapRoutes(db.getRoutesAll())

# New York City routes (includes both LGA and JFK airports)
def mapRoutesFromNYC():
    mapRoutes(db.getRoutesFromCity("New York"))
    
def mapRoutesFromLGA():
    mapRoutes(db.getRoutesFromIata("LGA"))

def mapRoutesFromJFK():
    mapRoutes(db.getRoutesFromIata("JFK"))

def mapRoutesAA():
    mapRoutes(db.getAirlineRoutes("AA"))

# Map all 1000 US routes 1 ms after mainloop is called
db = Database(maxRoutes = 1000)
root.after(1, mapRoutesALL)
root.after(3000, mapRoutesFromJFK)

# Close database connection when root window is closed
def onWindowClose():
    db.closeConnection()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", onWindowClose)
root.geometry("900x700")
root.mainloop()

