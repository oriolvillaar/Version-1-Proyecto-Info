# Importem les llibreries
import matplotlib.pyplot as plt
import math
import tkinter as tk

# Importem funcions i classes dels altres fitxers
from airports import *
from aircraft import *

# Creem dues llistes, una pels aeroports i l'altre pels vols
airports = []
aircrafts = []


#Actualitzem la llista d'aeroports de la interfície
def UpdateAirportList():
    # Esborrem tot el que hi havia abans al llistat
    listbox_airports.delete(0, tk.END)

    # Recorrem la llista
    i = 0
    while i < len(airports):
        # text que volem mostrar de cada aeroport
        text = airports[i].ICAO + " | " + str(airports[i].latitude) + " | " + str(airports[i].longitude) + " | " + str(airports[i].isSchengen)

        # Afegim text
        listbox_airports.insert(tk.END, text)
        i = i + 1


# Actualitzem la llista de vols de la interfície
def UpdateAircraftList():
    # Esborrem el que hi havia abans
    listbox_aircrafts.delete(0, tk.END)

    # Recorrem la llista
    i = 0
    while i < len(aircrafts):
        # Preparem el text
        text = aircrafts[i].id + " | " + aircrafts[i].origin + " | " + aircrafts[i].landing_time + " | " + aircrafts[i].airline

        # Afegim text al llistat
        listbox_aircrafts.insert(tk.END, text)
        i = i + 1


# Carreguem els aeroports des del fitxer
def LoadButton():
    global airports

    # Agafem el nom del fitxer escrit
    filename = entry_file.get().strip()

    # Carreguem els aeroports del fitxer
    airports = LoadAirports(filename)

    # Actualitzem el valor Schengen de tots els aeroports
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    # Actualitzem llista que es veu a la finestra
    UpdateAirportList()

    # Mostrem quants aeroports s'han carregat
    label_result.config(text="Airports loaded: " + str(len(airports)))


# Afegim un aeroport nou
def AddButton():
    try:
        # Llegim dades escrites pels camps
        code = entry_code.get().strip().upper()
        lat = float(entry_lat.get())
        lng = float(entry_lng.get())

        # Creem aeroport nou
        airport = Airport(code, lat, lng)

        # Mirem si és Schengen o no
        SetSchengen(airport)

        # Afegim l'aeroport a la llista
        AddAirport(airports, airport)

        # Actualitzem la llista
        UpdateAirportList()

        # confirmació
        label_result.config(text="Airport processed")
    except:
        # Si hi ha algun error en les dades, mostrem missatge
        label_result.config(text="Error in airport data")


# Eliminem un aeroport a partir del seu codi
def RemoveButton():
    # Llegim el codi escrit per l'usuari
    code = entry_code.get().strip().upper()

    # Intentem eliminar l'aeroport
    result = RemoveAirport(airports, code)

    # Si s'ha trobat i eliminat, actualitzem la llista
    if result:
        UpdateAirportList()
        label_result.config(text="Airport removed")
    else:
        # Si no existeix, ho indiquem
        label_result.config(text="Airport not found")


# Tornem a calcular si cada aeroport és Schengen o no
def SetSchengenButton():
    # Recorrem tots els aeroports
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    # Actualitzem la llista
    UpdateAirportList()

    # Missatge de confirmació
    label_result.config(text="Schengen updated")


# Guardem en un fitxer els aeroports Schengen
def SaveButton():
    # Agafem el nom del fitxer on volem guardar
    filename = entry_save.get().strip()

    # Guardem els aeroports Schengen
    result = SaveSchengenAirports(airports, filename)

    # Comprovem si s'ha pogut guardar bé
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
    # Mirem quin element del llistat està seleccionat
    selected = listbox_airports.curselection()

    # Si hi ha algun element seleccionat
    if len(selected) > 0:
        index = selected[0]
        airport = airports[index]

        # Esborrem el text anterior
        text_output.delete("1.0", tk.END)

        # Escrivim la informació de l'aeroport
        text_output.insert(tk.END, "ICAO: " + airport.ICAO + "\n")
        text_output.insert(tk.END, "Latitude: " + str(airport.latitude) + "\n")
        text_output.insert(tk.END, "Longitude: " + str(airport.longitude) + "\n")
        text_output.insert(tk.END, "Schengen: " + str(airport.isSchengen) + "\n")


# Carreguem els vols des d'un fitxer
def LoadArrivalsButton():
    global aircrafts

    # Agafem el nom del fitxer
    filename = entry_arrivals_file.get().strip()

    # Carreguem els vols
    aircrafts = LoadArrivals(filename)

    # Actualitzem la llista de vols a la finestra
    UpdateAircraftList()

    # Mostrem quants vols s'han carregat
    label_result.config(text="Flights loaded: " + str(len(aircrafts)))


# Guardem els vols en un fitxer
def SaveFlightsButton():
    # Agafem el nom del fitxer de sortida
    filename = entry_arrivals_save.get().strip()

    # Guardem els vols
    result = SaveFlights(aircrafts, filename)

    # Comprovem s'ha executat bé
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
    # Si no hi ha aeroports carregats, no es pot
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return

    # Fem el gràfic
    PlotFlightsType(aircrafts, airports)
    label_result.config(text="Flights type plot shown")


# Creem el fitxer KML dels vols
def MapFlightsButton():
    # Si no hi ha aeroports carregats, no es pot
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return

    # Creem el fitxer per a Google Earth
    MapFlights(aircrafts, airports)
    label_result.config(text="Flights KML file created")


# Filtrem només els vols de llarga distància
def ShowLongDistanceButton():
    global aircrafts

    # Si no hi ha aeroports carregats, no es pot calcular
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return

    # Ens quedem només amb els vols de llarga distància
    aircrafts = LongDistanceArrivals(aircrafts, airports)

    # Actualitzem la llista de vols
    UpdateAircraftList()

    # Mostrem quants vols han quedat
    label_result.config(text="Long distance flights shown: " + str(len(aircrafts)))


# Mostrem la informació del vol seleccionat
def ShowSelectedAircraftButton():
    # Mirem quin vol està seleccionat
    selected = listbox_aircrafts.curselection()

    # Si hi ha algun seleccionat
    if len(selected) > 0:
        index = selected[0]
        aircraft = aircrafts[index]

        # Esborrem el text anterior
        text_output.delete("1.0", tk.END)

        # Escrivim la informació del vol
        text_output.insert(tk.END, "ID: " + aircraft.id + "\n")
        text_output.insert(tk.END, "Origin: " + aircraft.origin + "\n")
        text_output.insert(tk.END, "Landing time: " + aircraft.landing_time + "\n")
        text_output.insert(tk.END, "Airline: " + aircraft.airline + "\n")


# Creem la finestra principal del programa
root = tk.Tk()

# Posem el títol de la finestra
root.title("Airport and Aircraft Interface")

# Posem la mida de la finestra
root.geometry("1200x700")


# Etiqueta fitxer d'aeroports
label1 = tk.Label(root, text="Load airports file:")
label1.grid(row=0, column=0)

# Casella per escriure el nom del fitxer d'aeroports
entry_file = tk.Entry(root, width=20)
entry_file.grid(row=0, column=1)
entry_file.insert(0, "Airports.txt")

# Botó per carregar aeroports
button_load = tk.Button(root, text="Load Airports", command=LoadButton)
button_load.grid(row=0, column=2)

# Etiqueta camp ICAO
label2 = tk.Label(root, text="ICAO:")
label2.grid(row=1, column=0)

# Casella codi ICAO
entry_code = tk.Entry(root, width=10)
entry_code.grid(row=1, column=1)

# Etiqueta latitud
label3 = tk.Label(root, text="Latitude:")
label3.grid(row=2, column=0)

# Casella latitud
entry_lat = tk.Entry(root, width=10)
entry_lat.grid(row=2, column=1)

# Etiqueta longitud
label4 = tk.Label(root, text="Longitude:")
label4.grid(row=3, column=0)

# Casella longitud
entry_lng = tk.Entry(root, width=10)
entry_lng.grid(row=3, column=1)

# Botó afegir aeroport
button_add = tk.Button(root, text="Add Airport", command=AddButton)
button_add.grid(row=4, column=0)

# Botó eliminar aeroport
button_remove = tk.Button(root, text="Remove Airport", command=RemoveButton)
button_remove.grid(row=4, column=1)

# Botó recalcular Schengen
button_set = tk.Button(root, text="Set Schengen", command=SetSchengenButton)
button_set.grid(row=4, column=2)

# Etiqueta fitxer on guardar aeroports
label5 = tk.Label(root, text="Save airports file:")
label5.grid(row=5, column=0)

# Casella nom del fitxer de sortida
entry_save = tk.Entry(root, width=20)
entry_save.grid(row=5, column=1)
entry_save.insert(0, "SchengenAirports.txt")

# Botó guardar aeroports Schengen
button_save = tk.Button(root, text="Save Schengen", command=SaveButton)
button_save.grid(row=5, column=2)

# Botó fer el gràfic d'aeroports
button_plot = tk.Button(root, text="Plot Airports", command=PlotButton)
button_plot.grid(row=6, column=0)

# Botó crear el mapa KML d'aeroports
button_map = tk.Button(root, text="Map Airports", command=MapButton)
button_map.grid(row=6, column=1)

# Botó mostrar l'aeroport seleccionat
button_show_airport = tk.Button(root, text="Show Selected Airport", command=ShowSelectedAirportButton)
button_show_airport.grid(row=6, column=2)

# Llistat aeroports
listbox_airports = tk.Listbox(root, width=70, height=15)
listbox_airports.grid(row=7, column=0, columnspan=3)


# Etiqueta fitxer de vols
label6 = tk.Label(root, text="Load arrivals file:")
label6.grid(row=0, column=4)

# Casella nom del fitxer de vols
entry_arrivals_file = tk.Entry(root, width=20)
entry_arrivals_file.grid(row=0, column=5)
entry_arrivals_file.insert(0, "Arrivals.txt")

# Botó carregar els vols
button_load_arrivals = tk.Button(root, text="Load Arrivals", command=LoadArrivalsButton)
button_load_arrivals.grid(row=0, column=6)

# Etiqueta fitxer on guardar vols
label7 = tk.Label(root, text="Save flights file:")
label7.grid(row=1, column=4)

# Casella fitxer de sortida dels vols
entry_arrivals_save = tk.Entry(root, width=20)
entry_arrivals_save.grid(row=1, column=5)
entry_arrivals_save.insert(0, "output_arrivals.txt")

# Botó guardar els vols
button_save_flights = tk.Button(root, text="Save Flights", command=SaveFlightsButton)
button_save_flights.grid(row=1, column=6)

# Botó mostrar el gràfic d'arribades
button_plot_arrivals = tk.Button(root, text="Plot Arrivals", command=PlotArrivalsButton)
button_plot_arrivals.grid(row=2, column=4)

# Botó mostrar el gràfic per aerolínies
button_plot_airlines = tk.Button(root, text="Plot Airlines", command=PlotAirlinesButton)
button_plot_airlines.grid(row=2, column=5)

# Botó mostrar el gràfic de tipus de vol
button_plot_type = tk.Button(root, text="Plot Flights Type", command=PlotFlightsTypeButton)
button_plot_type.grid(row=2, column=6)

# Botó crear el mapa KML dels vols
button_map_flights = tk.Button(root, text="Map Flights", command=MapFlightsButton)
button_map_flights.grid(row=3, column=4)

# Botó filtrar els vols de llarga distància
button_longdistance = tk.Button(root, text="Filter Long Distance", command=ShowLongDistanceButton)
button_longdistance.grid(row=3, column=5)

# Botó mostrar el vol seleccionat
button_show_aircraft = tk.Button(root, text="Show Selected Flight", command=ShowSelectedAircraftButton)
button_show_aircraft.grid(row=3, column=6)

# Llistat on es veuen els vols
listbox_aircrafts = tk.Listbox(root, width=70, height=15)
listbox_aircrafts.grid(row=7, column=4, columnspan=3)

# Zona de text informació detallada
text_output = tk.Text(root, width=40, height=12)
text_output.grid(row=7, column=7)

# Etiqueta de sota per missatges
label_result = tk.Label(root, text="Ready")
label_result.grid(row=8, column=0, columnspan=7)

# Activar finestra
root.mainloop()