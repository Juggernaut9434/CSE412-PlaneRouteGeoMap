from tkinter import *
import tkintermapview
from tkinter import ttk
from src.back_end.route import Route
from src.back_end.database import Database

root = Tk()
root.title('CSE412 Project')

# lookup function, takes in the city name and sets the address to that location
def lookup():
    map_widget.set_address(city_entry.get())

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
    
def mapRoutesCity():
    mapRoutes(db.getRoutesFromCity(city_entry.get()))
    
def mapRoutesIata():
    mapRoutes(db.getRoutesFromIata(iata_entry.get()))


my_label = LabelFrame(root)
my_label.pack(pady=10)


map_widget = tkintermapview.TkinterMapView(my_label, width=700, height=500, corner_radius=0)
map_widget.set_address("New York")
map_widget.set_zoom(1)
map_widget.pack()

my_filter = LabelFrame(root)
my_filter.pack(pady=5)

filter_button1 = Button(my_filter, text="All Routes", font=("Helvetica", 18), command=mapRoutesALL)
filter_button1.grid(row=0, column=0, padx=5)

filter_button2 = Button(my_filter, text="From NY", font=("Helvetica", 18), command=mapRoutesFromNYC)
filter_button2.grid(row=0, column=1, padx=5)

filter_button3 = Button(my_filter, text="From LGA", font=("Helvetica", 18), command=mapRoutesFromLGA)
filter_button3.grid(row=0, column=2, padx=5)

filter_button4 = Button(my_filter, text="From JFK", font=("Helvetica", 18), command=mapRoutesFromJFK)
filter_button4.grid(row=0, column=3, padx=5)

filter_button5 = Button(my_filter, text="Operated by AA", font=("Helvetica", 18), command=mapRoutesAA)
filter_button5.grid(row=0, column=4, padx=5)


filter_frame = LabelFrame(root)
filter_frame.pack(pady=10)

city_entry = Entry(filter_frame, font=("Helvetica",28))
city_entry.insert(0, "Boston")
city_entry.grid(row=0, column=1, pady=5)

city_routes_button = Button(filter_frame, text="Filter Routes from City:", font=("Helvetica", 18), command=mapRoutesCity)
city_routes_button.grid(row=0, column=0, pady=5)

iata_entry = Entry(filter_frame, font=("Helvetica",28))
iata_entry.insert(0, "LHR")
iata_entry.grid(row=1, column=1, pady=5)

iata_routes_button = Button(filter_frame, text="Filter Routes from Airport:", font=("Helvetica", 18), command=mapRoutesIata)
iata_routes_button.grid(row=1, column=0, pady=5)


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
            print(oldPaths[i])
        oldPaths.append(createPath(routesList[i]))

# Map all 1000 US routes 1 ms after mainloop is called
db = Database(maxRoutes = 1000)
root.after(1, mapRoutesALL)

# Close database connection when root window is closed
def onWindowClose():
    db.closeConnection()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", onWindowClose)
root.geometry("900x720")
root.mainloop()

