from aircraft import *
from airports import *
import matplotlib.pyplot as plt


#Primerament, creem les classes necessàries


# Aeroport
class BarcelonaAP:
   def __init__(self):
       self.code = ""        # codi ICAO (ex: LEBL)
       self.terminals = []   # llista de terminals


# Terminal
class Terminal:
   def __init__(self):
       self.name = ""        # nom del terminal (T1, T2...)
       self.areas = []       # llista de BoardingArea
       self.airlines = []    # llista de codis ICAO d'aerolínies




# Zona d'embarcament
class BoardingArea:
   def __init__(self):
       self.name = ""        # nom de l’àrea (ex: T1BAA)
       self.area_type = ""   # tipus: Schengen o non-Schengen
       self.gates = []       # llista de portes (Gate)




# Porta d'embarcament
class Gate:
   def __init__(self):
       self.name = ""            # nom de la porta (ex: T1BAAG1)
       self.isOccupied = False  # indica si està ocupada
       self.aircraft_id = ""    # id de l’avió si està ocupada


# Funció per a crear les portes de cada àrea
def SetGates(area, init_gate, end_gate, prefix):
   # Comprovem que els valors siguin correctes
   if end_gate <= init_gate:
       return -1   # error


   # Calculem nombre de portes
   num_gates = end_gate - init_gate + 1


   # Creem la llista de portes
   area.gates = [None] * num_gates


   i = 0
   gate_number = init_gate


   # Fem el recorregut
   while gate_number <= end_gate:
       gate = Gate()   # creem nova porta


       # Assignem nom: prefix + número
       gate.name = prefix + str(gate_number)


       # Totes les portes comencen estant lliures
       gate.isOccupied = False
       gate.aircraft_id = ""


       # Guardem la porta
       area.gates[i] = gate


       # Avancem posició i número
       i = i + 1
       gate_number = gate_number + 1


   return 0


# Carreguem les aerolínies de cada terminal a partir dels fitxers
def LoadAirlines(terminal, t_name):
   # Escriure nom del fitxer
   filename = t_name + "_Airlines.txt"


   # Obrim el fitxer
   try:
       file = open(filename, "r")
   except FileNotFoundError:
       print ("File was not found")
       return -1   # Si el fitxer no existeix, dona error


   # Llegim totes les línies
   lines = file.readlines()
   file.close()


   # Creem la llista d’aerolínies
   terminal.airlines = [None] * len(lines)


   #Iniciem recorregut
   i = 0
   while i < len(lines):
       # Separem per tabulador
       parts = lines[i].split("\t")


       # Guardem només el codi ICAO
       code = parts[1].strip()
       terminal.airlines[i] = code


       i = i + 1


   return 0   # correcte


#Llegim el fitxer i creem tots els objectes necessaris per apoder treballar amb ells
def LoadAirportStructure(filename):
   # Obrim el fitxer
   try:
       file = open(filename, "r")
   except FileNotFoundError:
       print ("File was not found")
       return -1


   # Llegim primera línia
   line = file.readline()
   parts = line.split()


   # Creem objecte aeroport i assignem parts
   bcn = BarcelonaAP()
   bcn.code = parts[0]


   num_terminals = int(parts[1])
   bcn.terminals = [None] * num_terminals


   # Iniciem recorregut
   i = 0
   while i < num_terminals:


       # Llegim línia del terminal
       line = file.readline()
       parts = line.split()


       terminal = Terminal()
       terminal.name = parts[1]


       # Num d’àrees d’embarcament
       num_areas = int(parts[2])
       terminal.areas = [None] * num_areas


       # Carreguem aerolínies
       result = LoadAirlines(terminal, terminal.name)
       if result == -1:
           file.close()
           return -1


       # Iniciem recorregut
       j = 0
       while j < num_areas:


           # Llegim línia d’una àrea
           line = file.readline()
           parts = line.split()


           area = BoardingArea()


           # Construïm de l’àrea
           area_letter = parts[1]
           area.name = terminal.name + "BA" + area_letter


           # Assignem tipus
           area.area_type = parts[2]


           # Llegim rang de portes
           init_gate = int(parts[4])
           end_gate = int(parts[6])


           # Prefix per crear noms de portes
           prefix = area.name + "G"


           # Creem les portes de l’àrea
           result = SetGates(area, init_gate, end_gate, prefix)
           if result == -1:
               file.close()
               return -1


           # Guardem l’àrea dins el terminal
           terminal.areas[j] = area


           j = j + 1


       # Guardem el terminal dins l’aeroport
       bcn.terminals[i] = terminal


       i = i + 1


   file.close()
   return bcn


# Obtenim llista amb les portes i si estan ocupades o no i per qui
def GateOccupancy(bcn):
   # Comptem el nombre total de portes
   total_gates = 0


   # Iniciem recorregut terminals
   i = 0
   while i < len(bcn.terminals):
       terminal = bcn.terminals[i]


       # Iniciem recorregut àrees terminal
       j = 0
       while j < len(terminal.areas):
           area = terminal.areas[j]


           total_gates = total_gates + len(area.gates)


           j = j + 1


       i = i + 1


   # Creem la llista resultat amb mida fixa
   result = [None] * total_gates


   k = 0


   # Tornem a recórrer per guardar la info
   i = 0
   while i < len(bcn.terminals):
       terminal = bcn.terminals[i]


       j = 0
       while j < len(terminal.areas):
           area = terminal.areas[j]


           # Recrrem gates
           h = 0
           while h < len(area.gates):
               gate = area.gates[h]


               # Guardem la info en una llista
               result[k] = [gate.name, gate.isOccupied, gate.aircraft_id]


               k = k + 1
               h = h + 1


           j = j + 1


       i = i + 1


   return result


# Comprovem si una aerolínia és a la terminal
def IsAirlineInTerminal(terminal, name):


   # Comprovem si el nom és buit
   if name == "":
       return -1


   # Si la llista està buida
   if len(terminal.airlines) == 0:
       return False


   # Iniciem recorregut llista aerolínies
   i = 0
   while i < len(terminal.airlines):
       if terminal.airlines[i] == name:
           return True
       i = i + 1


   return False


# Busca en quin terminal opera una aerolínia
def SearchTerminal(bcn, name):


   # Si el nom és buit
   if name == "":
       return ""


   i = 0
   while i < len(bcn.terminals):
       terminal = bcn.terminals[i]


       # Fem servir la funció anterior
       result = IsAirlineInTerminal(terminal, name)


       if result == True:
           return terminal.name


       i = i + 1


   # Si no es troba en cap terminal
   return ""


def AssignGate(bcn, aircraft):


   # Comprovem dades bàsiques de l’avió
   if aircraft.airline == "" or aircraft.origin == "" or aircraft.id == "":
       return -1


   # Busquem el terminal de l’aerolínia
   terminal_name = SearchTerminal(bcn, aircraft.airline)


   # Si no existeix l’aerolínia
   if terminal_name == "":
       return -1


   # Mirem si l’origen és Schengen
   origin_airport = Airport(aircraft.origin, 0, 0)
   SetSchengen(origin_airport)


   if origin_airport.isSchengen == True:
       flight_type = "Schengen"
   else:
       flight_type = "non-Schengen"


   # Busquem el terminal dins bcn
   i = 0
   found_terminal = False


   while i < len(bcn.terminals) and found_terminal == False:
       if bcn.terminals[i].name == terminal_name:
           found_terminal = True
       else:
           i = i + 1


   if found_terminal == False:
       return -1


   terminal = bcn.terminals[i]


   # Busquem porta lliure del tipus correcte
   j = 0
   while j < len(terminal.areas):
       area = terminal.areas[j]


       if area.area_type == flight_type:
           k = 0
           while k < len(area.gates):
               gate = area.gates[k]


               if gate.isOccupied == False:
                   gate.isOccupied = True
                   gate.aircraft_id = aircraft.id
                   return 0


               k = k + 1


       j = j + 1


   return -1


# Mostra un dibuix portes
def PlotGateOccupancy(bcn):

   if bcn == None:
       return -1
   plt.figure(figsize=(14, 9))

   # T1
   y_terminal = 95

   # Nom terminal
   plt.text(0, y_terminal + 8, "T1", fontsize=16)

   x_position = 10

   i = 0
   while i < len(bcn.terminals[0].areas):


       area = bcn.terminals[0].areas[i]


       # Longitud barra segons nombre de portes
       height = len(area.gates)


       # Dibuix barra vertical
       plt.plot([x_position, x_position],
                [y_terminal, y_terminal - height],
                linewidth=6)


       # Nom àrea
       plt.text(x_position - 4,
                y_terminal - height - 8,
                area.name)


       # Dibuix portes
       k = 0
       while k < len(area.gates):


           gate = area.gates[k]


           y_gate = y_terminal - k


           # Alternem esquerra / dreta
           if k % 2 == 0:
               x_gate = x_position - 2
           else:
               x_gate = x_position + 2


           # Color segons ocupació
           if gate.isOccupied == True:
               color_gate = "red"
           else:
               color_gate = "green"


           # Línia porta
           plt.plot([x_position, x_gate],
                    [y_gate, y_gate])


           # Quadrat porta
           plt.plot(x_gate,
                    y_gate,
                    marker="s",
                    color=color_gate,
                    markersize=5)


           k = k + 1


       # Més espai per àrees grans
       if len(area.gates) > 30:
           x_position = x_position + 8
       else:
           x_position = x_position + 6


       i = i + 1


   # T2
   y_terminal2 = 10

   plt.text(0, y_terminal2 + 8, "T2", fontsize=16)

   x_position = 10

   j = 0
   while j < len(bcn.terminals[1].areas):


       area = bcn.terminals[1].areas[j]


       height = len(area.gates)


       plt.plot([x_position, x_position],
                [y_terminal2, y_terminal2 - height],
                linewidth=6)


       plt.text(x_position - 4,
                y_terminal2 - height - 8,
                area.name)


       k = 0
       while k < len(area.gates):


           gate = area.gates[k]


           y_gate = y_terminal2 - k


           if k % 2 == 0:
               x_gate = x_position - 2
           else:
               x_gate = x_position + 2


           if gate.isOccupied == True:
               color_gate = "red"
           else:
               color_gate = "green"


           plt.plot([x_position, x_gate],
                    [y_gate, y_gate])


           plt.plot(x_gate,
                    y_gate,
                    marker="s",
                    color=color_gate,
                    markersize=5)


           k = k + 1


       if len(area.gates) > 30:
           x_position = x_position + 8
       else:
           x_position = x_position + 6


       j = j + 1


   # Llegenda
   plt.plot(0, 0,
            marker="s",
            color="green",
            label="Free")


   plt.plot(0, 0,
            marker="s",
            color="red",
            label="Occupied")


   plt.legend()


   # Títol
   plt.title("Gate occupancy")


   # Límit eixos
   plt.axis([0, 50, -60, 110])


   plt.show()


   return 0


# Test


if __name__ == "__main__":


   # Test SetGates
   print("----- TEST SetGates -----")
   area = BoardingArea()
   result = SetGates(area, 1, 3, "T1BAAG")


   print("Result:", result)
   print(area.gates[0].name)
   print(area.gates[1].name)
   print(area.gates[2].name)


   # Test LoadAirlines
   print("----- TEST LoadAirlines -----")
   terminal = Terminal()
   terminal.name = "T1"


   result = LoadAirlines(terminal, terminal.name)
   print("Result:", result)
   print("Airlines loaded:", len(terminal.airlines))
   print("First airline:", terminal.airlines[0])


   # Test LoadAirportStructure
   print("----- TEST LoadAirportStructure -----")
   bcn = LoadAirportStructure("LEBL.txt")


   print("Airport:", bcn.code)
   print("Terminals:", len(bcn.terminals))
   print("First terminal:", bcn.terminals[0].name)
   print("First area:", bcn.terminals[0].areas[0].name)
   print("First gate:", bcn.terminals[0].areas[0].gates[0].name)


   # Test GateOccupancy
   print("----- TEST GateOccupancy -----")
   gates = GateOccupancy(bcn)
   print("Total gates:", len(gates))
   print("First gate info:", gates[0])


   # Test IsAirlineInTerminal
   print("----- TEST IsAirlineInTerminal -----")
   print(IsAirlineInTerminal(bcn.terminals[0], "VLG"))
   print(IsAirlineInTerminal(bcn.terminals[0], "RYR"))
   print(IsAirlineInTerminal(bcn.terminals[0], ""))


   # Test SearchTerminal
   print("----- TEST SearchTerminal -----")
   print(SearchTerminal(bcn, "VLG"))
   print(SearchTerminal(bcn, "RYR"))
   print(SearchTerminal(bcn, "AAA"))


   # Test AssignGate
   print("----- TEST AssignGate -----")
   aircraft = Aircraft()
   aircraft.id = "TEST1"
   aircraft.airline = "VLG"
   aircraft.origin = "LEMD"
   aircraft.landing_time = "10:00"


   result = AssignGate(bcn, aircraft)
   print("Result:", result)


   gates = GateOccupancy(bcn)


   i = 0
   while i < len(gates):
       if gates[i][1] == True:
           print(gates[i])
       i = i + 1
