import matplotlib.pyplot as plt
import math
from airports import *


# Definim la classe i establim les seves característiques
class Aircraft:
   def __init__(self):
       self.id = ""
       self.airline = ""
       self.origin = ""
       self.landing_time = ""




# Funció per comprovar si l'hora és correcta (format hh:mm)
def IsValidTime(time_text):
   parts = time_text.split(":")


   if len(parts) != 2:
       return False


   try:
       hour = int(parts[0])
       minute = int(parts[1])
   except:
       return False


   if hour < 0 or hour > 23:
       return False


   if minute < 0 or minute > 59:
       return False


   return True




# Funció per carregar els vols des del fitxer
def LoadArrivals(filename):
   aircrafts = []


   try:
       file = open(filename, "r")
   except FileNotFoundError:
       return aircrafts


   line = file.readline()   # llegim la capçalera i la ignorem
   line = file.readline()


   while line != "":
       parts = line.split()


       # Comprovem que la línia té l'estructura correcta
       if len(parts) == 4:
           aircraftid = parts[0]
           origin = parts[1]
           landing_time = parts[2]
           airline = parts[3]


           # Comprovem que l'hora és correcta
           if IsValidTime(landing_time):
               aircraft = Aircraft()
               aircraft.id = aircraftid
               aircraft.airline = airline
               aircraft.origin = origin
               aircraft.landing_time = landing_time


               aircrafts.append(aircraft)


       line = file.readline()


   file.close()
   return aircrafts



#Fem gràfic per hores
def PlotArrivals(aircrafts):
   if len(aircrafts) == 0:
       print("Error: empty aircraft list")
       return


   # Llista per comptar vols per hora
   hours = [0] * 24


   i = 0
   while i < len(aircrafts):
       parts = aircrafts[i].landing_time.split(":")
       hour = int(parts[0])


       hours[hour] = hours[hour] + 1


       i = i + 1


   # Crear eix X manualment
   x = [0] * 24
   i = 0
   while i < 24:
       x[i] = i
       i = i + 1


   # Gràfic
   plt.bar(x, hours)
   plt.xlabel("Hour")
   plt.ylabel("Number of arrivals")
   plt.title("Landing frequency during the day")
   plt.grid()
   plt.show()



#Guardem vols a fitxer
def SaveFlights(aircrafts, filename):
   if len(aircrafts) == 0:
       print("Error: empty aircraft list")
       return False


   file = open(filename, "w")


   # Escriure capçalera
   file.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")


   i = 0
   while i < len(aircrafts):
       aircraftid = aircrafts[i].id
       origin = aircrafts[i].origin
       landing_time = aircrafts[i].landing_time
       airline = aircrafts[i].airline


       # Si algun camp està buit, posar "-"
       if aircraftid == "":
           aircraftid = "-"
       if origin == "":
           origin = "-"
       if landing_time == "":
           landing_time = "-"
       if airline == "":
           airline = "-"


       # Escriure línia
       file.write(aircraftid + " " + origin + " " + landing_time + " " + airline + "\n")


       i = i + 1


   file.close()
   return True



#Fem gràfic per aerolínies filtrant el nombre de vols per poder aparèixer com a aerolínia pròpia i no col·lapsar els títols
def PlotAirlines(aircrafts):
   if len(aircrafts) == 0:
       print("Error: empty aircraft list")
       return


   airlines = []
   counts = []


   i = 0
   while i < len(aircrafts):
       company = aircrafts[i].airline


       found = False
       j = 0
       while j < len(airlines) and found == False:
           if airlines[j] == company:
               counts[j] = counts[j] + 1
               found = True
           j = j + 1


       if found == False:
           airlines.append(company)
           counts.append(1)


       i = i + 1


   # Crear noves llistes amb principals + Altres
   airlines2 = []
   counts2 = []
   others = 0


   i = 0
   while i < len(airlines):
       if counts[i] >= 10: #Mínim 10 vols per poder aparèxier com a aerolínia pròpia
           airlines2.append(airlines[i])
           counts2.append(counts[i])
       else:
           others = others + counts[i]
       i = i + 1


   if others > 0:
       airlines2.append("Others")
       counts2.append(others)


   plt.bar(airlines2, counts2)
   plt.xlabel("Airline")
   plt.ylabel("Number of flights")
   plt.title("Flights per airline")
   plt.grid()
   plt.show()



#Fem gràfic segons si el vols és Schengen o no
def PlotFlightsType(aircrafts, airports):
   if len(aircrafts) == 0:
       print("Error: empty aircraft list")
       return


   schengen = 0
   nonschengen = 0


   i = 0
   while i < len(aircrafts):
       origin_code = aircrafts[i].origin


       found = False
       j = 0
       while j < len(airports) and found == False:
           if airports[j].ICAO == origin_code:
               if airports[j].isSchengen == True:
                   schengen = schengen + 1
               else:
                   nonschengen = nonschengen + 1
               found = True
           j = j + 1


       i = i + 1


   x = [0]
   labels = ["Arrivals"]


   plt.bar(x, [schengen], label="Schengen")
   plt.bar(x, [nonschengen], bottom=[schengen], label="Non-Schengen")


   plt.xticks(x, labels)


   plt.ylabel("Number of flights")
   plt.title("Schengen vs Non-Schengen arrivals")
   plt.legend()
   plt.grid()
   plt.show()



#Fem fitxer KML per a les rutes de Barcelona
def MapFlights(aircrafts, airports):
   if len(aircrafts) == 0:
       print("Error: empty aircraft list")
       return


   # Buscar l'aeroport LEBL
   foundLEBL = False
   i = 0
   while i < len(airports) and foundLEBL == False:
       if airports[i].ICAO == "LEBL":
           lebl_longitude = airports[i].longitude
           lebl_latitude = airports[i].latitude
           foundLEBL = True
       i = i + 1


   if foundLEBL == False:
       print("Error: LEBL airport not found")
       return


   file = open("flights.kml", "w")


   file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
   file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
   file.write("<Document>\n")
   file.write("<name>Flights to LEBL</name>\n")


   file.write("<Style id=\"schengenStyle\">\n")
   file.write("<LineStyle>\n")
   file.write("<color>ff00ff00</color>\n")
   file.write("<width>2</width>\n")
   file.write("</LineStyle>\n")
   file.write("</Style>\n")


   file.write("<Style id=\"nonSchengenStyle\">\n")
   file.write("<LineStyle>\n")
   file.write("<color>ff0000ff</color>\n")
   file.write("<width>2</width>\n")
   file.write("</LineStyle>\n")
   file.write("</Style>\n")


   i = 0
   while i < len(aircrafts):
       origin_code = aircrafts[i].origin


       foundAirport = False
       j = 0
       while j < len(airports) and foundAirport == False:
           if airports[j].ICAO == origin_code:
               origin_longitude = airports[j].longitude
               origin_latitude = airports[j].latitude
               origin_schengen = airports[j].isSchengen
               foundAirport = True
           j = j + 1


       if foundAirport == True:
           file.write("<Placemark>\n")
           file.write("<name>" + aircrafts[i].id + "</name>\n")


           if origin_schengen == True:
               file.write("<styleUrl>#schengenStyle</styleUrl>\n")
           else:
               file.write("<styleUrl>#nonSchengenStyle</styleUrl>\n")


           file.write("<LineString>\n")
           file.write("<tessellate>1</tessellate>\n")
           file.write("<coordinates>\n")
           file.write(str(origin_longitude) + "," + str(origin_latitude) + ",0 ")
           file.write(str(lebl_longitude) + "," + str(lebl_latitude) + ",0\n")
           file.write("</coordinates>\n")
           file.write("</LineString>\n")
           file.write("</Placemark>\n")


       i = i + 1


   file.write("</Document>\n")
   file.write("</kml>\n")
   file.close()


   print("KML file created: flights.kml")



#Funció per calcular distància de ruta tenint en compte curvatura terra
def HaversineDistance(lat1, lon1, lat2, lon2):
   R = 6371.0   # radi de la Terra en km


   lat1 = math.radians(lat1)
   lon1 = math.radians(lon1)
   lat2 = math.radians(lat2)
   lon2 = math.radians(lon2)


   dlat = lat2 - lat1
   dlon = lon2 - lon1


   a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2)
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


   distance = R * c
   return distance



#Filtrar vols segons si són llarga distància amb criteri mínim 2000km de distància de ruta
def LongDistanceArrivals(aircrafts, airports):
   longdistance = []


   # Buscar LEBL
   foundLEBL = False
   i = 0
   while i < len(airports) and foundLEBL == False:
       if airports[i].ICAO == "LEBL":
           lebl_latitude = airports[i].latitude
           lebl_longitude = airports[i].longitude
           foundLEBL = True
       i = i + 1


   if foundLEBL == False:
       return longdistance


   i = 0
   while i < len(aircrafts):
       origin_code = aircrafts[i].origin


       foundAirport = False
       j = 0
       while j < len(airports) and foundAirport == False:
           if airports[j].ICAO == origin_code:
               origin_latitude = airports[j].latitude
               origin_longitude = airports[j].longitude
               foundAirport = True
           j = j + 1


       if foundAirport == True:
           distance = HaversineDistance(origin_latitude, origin_longitude, lebl_latitude, lebl_longitude)


           if distance > 2000:
               longdistance.append(aircrafts[i])


       i = i + 1


   return longdistance




# TEST
if __name__ == "__main__":
   airports = LoadAirports("Airports.txt")


   i = 0
   while i < len(airports):
       SetSchengen(airports[i])
       i = i + 1


   aircrafts = LoadArrivals("Arrivals.txt")


   print("Flights loaded:", len(aircrafts))


   PlotArrivals(aircrafts)
   SaveFlights(aircrafts, "output_arrivals.txt")
   PlotAirlines(aircrafts)
   PlotFlightsType(aircrafts, airports)
   MapFlights(aircrafts, airports)


   longdistance = LongDistanceArrivals(aircrafts, airports)


   print("Long distance flights:", len(longdistance))


