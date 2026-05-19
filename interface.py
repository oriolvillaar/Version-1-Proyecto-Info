import tkinter as tk


from airports import *
from aircraft import *
from LEBL import *


airports = []
aircrafts = []
bcn = None


# Actualitzem la llista d'aeroports de la interfície
def UpdateAirportList():
   listbox_airports.delete(0, tk.END)

   i = 0
   while i < len(airports):
       text = airports[i].ICAO + " | " + str(airports[i].latitude) + " | " + str(airports[i].longitude) + " | " + str(airports[i].isSchengen)
       listbox_airports.insert(tk.END, text)
       i = i + 1

# Actualitzem la llista de vols de la interfície
def UpdateAircraftList():
   listbox_aircrafts.delete(0, tk.END)

   i = 0
   while i < len(aircrafts):
       text = aircrafts[i].id + " | " + aircrafts[i].origin + " | " + aircrafts[i].landing_time + " | " + aircrafts[i].airline
       listbox_aircrafts.insert(tk.END, text)
       i = i + 1

# Carreguem els aeroports des del fitxer
def LoadButton():
   global airports

   filename = entry_file.get().strip()
   airports = LoadAirports(filename)

   i = 0
   while i < len(airports):
       SetSchengen(airports[i])
       i = i + 1

   UpdateAirportList()
   label_result.config(text="Airports loaded: " + str(len(airports)))

# Afegim un aeroport nou
def AddButton():
   try:
       code = entry_code.get().strip().upper()
       lat = float(entry_lat.get())
       lng = float(entry_lng.get())


       airport = Airport(code, lat, lng)
       SetSchengen(airport)


       AddAirport(airports, airport)
       UpdateAirportList()


       label_result.config(text="Airport processed")
   except:
       label_result.config(text="Error in airport data")

# Eliminem un aeroport a partir del seu codi
def RemoveButton():
   code = entry_code.get().strip().upper()

   result = RemoveAirport(airports, code)

   if result:
       UpdateAirportList()
       label_result.config(text="Airport removed")
   else:
       label_result.config(text="Airport not found")

# Tornem a calcular si cada aeroport és Schengen o no
def SetSchengenButton():
   i = 0
   while i < len(airports):
       SetSchengen(airports[i])
       i = i + 1

   UpdateAirportList()
   label_result.config(text="Schengen updated")

# Guardem en un fitxer els aeroports Schengen
def SaveButton():
   filename = entry_save.get().strip()


   result = SaveSchengenAirports(airports, filename)

   if result:
       label_result.config(text="Schengen airports saved")
   else:
       label_result.config(text="Error saving file")

# Mostrem el gràfic dels aeroports
def PlotButton():
   PlotAirports(airports)
   label_result.config(text="Airport plot shown")

# Creem fitxer KML per al Google Earth
def MapButton():
   MapAirports(airports)
   label_result.config(text="Airport KML file created")

# Mostrem la informació de l'aeroport seleccionat
def ShowSelectedAirportButton():
   selected = listbox_airports.curselection()


   if len(selected) > 0:
       index = selected[0]
       airport = airports[index]


       text_output.delete("1.0", tk.END)


       text_output.insert(tk.END, "ICAO: " + airport.ICAO + "\n")
       text_output.insert(tk.END, "Latitude: " + str(airport.latitude) + "\n")
       text_output.insert(tk.END, "Longitude: " + str(airport.longitude) + "\n")
       text_output.insert(tk.END, "Schengen: " + str(airport.isSchengen) + "\n")

# Carreguem els vols des d'un fitxer
def LoadArrivalsButton():
   global aircrafts


   filename = entry_arrivals_file.get().strip()
   aircrafts = LoadArrivals(filename)


   UpdateAircraftList()
   label_result.config(text="Flights loaded: " + str(len(aircrafts)))

# Guardem els vols en un fitxer
def SaveFlightsButton():
   filename = entry_arrivals_save.get().strip()


   result = SaveFlights(aircrafts, filename)


   if result:
       label_result.config(text="Flights saved")
   else:
       label_result.config(text="Error saving flights")

# Mostrem el gràfic d'arribades per hora
def PlotArrivalsButton():
   PlotArrivals(aircrafts)
   label_result.config(text="Arrivals plot shown")

# Mostrem el gràfic de vols per aerolínia
def PlotAirlinesButton():
   PlotAirlines(aircrafts)
   label_result.config(text="Airlines plot shown")

# Mostrem el gràfic de vols Schengen i no Schengen
def PlotFlightsTypeButton():
   if len(airports) == 0:
       label_result.config(text="Load airports first")
       return


   PlotFlightsType(aircrafts, airports)
   label_result.config(text="Flights type plot shown")

# Creem el fitxer KML dels vols
def MapFlightsButton():
   if len(airports) == 0:
       label_result.config(text="Load airports first")
       return


   MapFlights(aircrafts, airports)
   label_result.config(text="Flights KML file created")

# Filtrem només els vols de llarga distància
def ShowLongDistanceButton():
   global aircrafts


   if len(airports) == 0:
       label_result.config(text="Load airports first")
       return


   aircrafts = LongDistanceArrivals(aircrafts, airports)


   UpdateAircraftList()
   label_result.config(text="Long distance flights shown: " + str(len(aircrafts)))

# Mostrem la informació del vol seleccionat
def ShowSelectedAircraftButton():
   selected = listbox_aircrafts.curselection()


   if len(selected) > 0:
       index = selected[0]
       aircraft = aircrafts[index]


       text_output.delete("1.0", tk.END)


       text_output.insert(tk.END, "ID: " + aircraft.id + "\n")
       text_output.insert(tk.END, "Origin: " + aircraft.origin + "\n")
       text_output.insert(tk.END, "Landing time: " + aircraft.landing_time + "\n")
       text_output.insert(tk.END, "Airline: " + aircraft.airline + "\n")

# Actualitzem la llista de portes de la interfície
def UpdateGateList():
   listbox_gates.delete(0, tk.END)


   if bcn == None:
       return


   gates = GateOccupancy(bcn)


   i = 0
   while i < len(gates):
       if gates[i][1] == True:
           status = "Occupied"
       else:
           status = "Free"


       text = gates[i][0] + "  " + status + "  " + gates[i][2]
       listbox_gates.insert(tk.END, text)
       i = i + 1

# Carreguem l’estructura de l’aeroport
def LoadLEBLButton():
   global bcn


   filename = entry_lebl_file.get().strip()
   bcn = LoadAirportStructure(filename)


   if bcn == -1:
       bcn = None
       label_result.config(text="Error loading LEBL structure")
   else:
       UpdateGateList()
       label_result.config(text="LEBL structure loaded")


# Assignem portes als vols
def AssignGatesButton():
   if bcn == None:
       label_result.config(text="Load LEBL structure first")
       return


   if len(aircrafts) == 0:
       label_result.config(text="Load arrivals first")
       return


   assigned = 0
   errors = 0


   i = 0
   while i < len(aircrafts):
       result = AssignGate(bcn, aircrafts[i])


       if result == 0:
           assigned = assigned + 1
       else:
           errors = errors + 1


       i = i + 1


   UpdateGateList()


   label_result.config(
       text="Assigned: " + str(assigned) +
            " | Errors: " + str(errors) +
            " (some flights may have no free gate)"
   )

# Mostrem informació de la porta seleccionada
def ShowSelectedGateButton():
   if bcn == None:
       label_result.config(text="Load LEBL structure first")
       return


   selected = listbox_gates.curselection()


   if len(selected) > 0:
       index = selected[0]


       gates = GateOccupancy(bcn)
       gate = gates[index]


       if gate[1] == True:
           status = "Occupied"
       else:
           status = "Free"


       text_output.delete("1.0", tk.END)


       text_output.insert(tk.END, "Gate: " + gate[0] + "\n")
       text_output.insert(tk.END, "Status: " + status + "\n")
       text_output.insert(tk.END, "Aircraft ID: " + gate[2] + "\n")


# Mostrem gràfic d’ocupació de portes
def PlotGateOccupancyButton():
   if bcn == None:
       label_result.config(text="Load LEBL structure first")
       return


   PlotGateOccupancy(bcn)
   label_result.config(text="Gate occupancy plot shown")




# Creem la finestra principal
root = tk.Tk()
root.title("Airport Management Interface")
root.geometry("1300x800")


# Blocs principals
frame_airports = tk.LabelFrame(root, text="Airports", padx=10, pady=10)
frame_airports.grid(row=0, column=0, padx=10, pady=10)


frame_flights = tk.LabelFrame(root, text="Flights", padx=10, pady=10)
frame_flights.grid(row=0, column=1, padx=10, pady=10)


frame_gates = tk.LabelFrame(root, text="LEBL Gates", padx=10, pady=10)
frame_gates.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


frame_details = tk.LabelFrame(root, text="Details", padx=10, pady=10)
frame_details.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# Airports
tk.Label(frame_airports, text="Load airports file:").grid(row=0, column=0)


entry_file = tk.Entry(frame_airports, width=20)
entry_file.grid(row=0, column=1)
entry_file.insert(0, "Airports.txt")


tk.Button(frame_airports, text="Load Airports", command=LoadButton).grid(row=0, column=2)


tk.Label(frame_airports, text="ICAO:").grid(row=1, column=0)


entry_code = tk.Entry(frame_airports, width=10)
entry_code.grid(row=1, column=1)


tk.Label(frame_airports, text="Latitude:").grid(row=2, column=0)


entry_lat = tk.Entry(frame_airports, width=10)
entry_lat.grid(row=2, column=1)


tk.Label(frame_airports, text="Longitude:").grid(row=3, column=0)


entry_lng = tk.Entry(frame_airports, width=10)
entry_lng.grid(row=3, column=1)


tk.Button(frame_airports, text="Add Airport", command=AddButton).grid(row=4, column=0)
tk.Button(frame_airports, text="Remove Airport", command=RemoveButton).grid(row=4, column=1)
tk.Button(frame_airports, text="Set Schengen", command=SetSchengenButton).grid(row=4, column=2)


tk.Label(frame_airports, text="Save airports file:").grid(row=5, column=0)


entry_save = tk.Entry(frame_airports, width=20)
entry_save.grid(row=5, column=1)
entry_save.insert(0, "SchengenAirports.txt")


tk.Button(frame_airports, text="Save Schengen", command=SaveButton).grid(row=5, column=2)


tk.Button(frame_airports, text="Plot Airports", command=PlotButton).grid(row=6, column=0)
tk.Button(frame_airports, text="Map Airports", command=MapButton).grid(row=6, column=1)
tk.Button(frame_airports, text="Show Selected Airport", command=ShowSelectedAirportButton).grid(row=6, column=2)


listbox_airports = tk.Listbox(frame_airports, width=65, height=15)
listbox_airports.grid(row=7, column=0, columnspan=3)

#Flights

tk.Label(frame_flights, text="Load arrivals file:").grid(row=0, column=0)


entry_arrivals_file = tk.Entry(frame_flights, width=20)
entry_arrivals_file.grid(row=0, column=1)
entry_arrivals_file.insert(0, "Arrivals.txt")


tk.Button(frame_flights, text="Load Arrivals", command=LoadArrivalsButton).grid(row=0, column=2)


tk.Label(frame_flights, text="Save flights file:").grid(row=1, column=0)


entry_arrivals_save = tk.Entry(frame_flights, width=20)
entry_arrivals_save.grid(row=1, column=1)
entry_arrivals_save.insert(0, "output_arrivals.txt")


tk.Button(frame_flights, text="Save Flights", command=SaveFlightsButton).grid(row=1, column=2)


tk.Button(frame_flights, text="Plot Arrivals", command=PlotArrivalsButton).grid(row=2, column=0)
tk.Button(frame_flights, text="Plot Airlines", command=PlotAirlinesButton).grid(row=2, column=1)
tk.Button(frame_flights, text="Plot Flights Type", command=PlotFlightsTypeButton).grid(row=2, column=2)


tk.Button(frame_flights, text="Map Flights", command=MapFlightsButton).grid(row=3, column=0)
tk.Button(frame_flights, text="Filter Long Distance", command=ShowLongDistanceButton).grid(row=3, column=1)
tk.Button(frame_flights, text="Show Selected Flight", command=ShowSelectedAircraftButton).grid(row=3, column=2)


listbox_aircrafts = tk.Listbox(frame_flights, width=65, height=15)
listbox_aircrafts.grid(row=7, column=0, columnspan=3)

# Gates

tk.Label(frame_gates, text="LEBL file:").grid(row=0, column=0)


entry_lebl_file = tk.Entry(frame_gates, width=20)
entry_lebl_file.grid(row=0, column=1)
entry_lebl_file.insert(0, "LEBL.txt")


tk.Button(frame_gates, text="Load LEBL", command=LoadLEBLButton).grid(row=0, column=2)
tk.Button(frame_gates, text="Assign Gates", command=AssignGatesButton).grid(row=0, column=3)
tk.Button(frame_gates, text="Show Selected Gate", command=ShowSelectedGateButton).grid(row=0, column=4)
tk.Button(frame_gates, text="Plot Gate Occupancy", command=PlotGateOccupancyButton).grid(row=0, column=5)


listbox_gates = tk.Listbox(frame_gates, width=120, height=12)
listbox_gates.grid(row=1, column=0, columnspan=6)


text_output = tk.Text(frame_details, width=40, height=30)
text_output.grid(row=0, column=0)


label_result = tk.Label(root, text="Ready")
label_result.grid(row=2, column=0, columnspan=3)


# Activem la finestra
root.mainloop()
