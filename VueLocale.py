from tkinter import Frame
from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sin, cos, atan2
import math
import numpy as np
import numpy.ma as ma


class Courbes(Frame):
    def __init__(self, root, tmin, tmax, precip, posx, posy, year):
        self.main = Frame(root)
        self.tmin = tmin
        self.tmax = tmax
        self.precip = precip
        self.year = year
        
        #Configration de la courbe des Temp�rature
        self.fig = Figure(frameon=True)
        self.gs = self.fig.add_gridspec(2,1)
        self.plot1 = self.fig.add_subplot(self.gs[0,0])
        self.plot1.set_xlabel('Temps (Jour)')
        self.plot1.set_ylabel('Temperature(C)')
        tailletmin = np.shape(self.tmin.vals)
        tailletmax = np.shape(self.tmax.vals)
        tailleprecip = np.shape(self.precip.vals)
        print(self.tmin.lats[posx])
        print(self.tmin.lons[posy])
        
        
        y1 = [self.tmin.vals[y][posx][posy] for y in range(tailletmin[0])]
        y2 = [self.tmax.vals[y][posx][posy] for y in range(tailletmax[0])]
        y3 = [self.precip.vals[y][posx][posy] for y in range(tailleprecip[0])]
        self.plot1.plot([x+1 for x in range(tailletmin[0])], y1, 'b-', label='Min')
        self.plot1.plot([x+1 for x in range(tailletmax[0])], y2, 'r-', label='Max')

        #Configuration de la courbe des precipitations
        self.plot2 = self.fig.add_subplot(self.gs[1, 0])
        self.plot2.set_xlabel('Temps(jour)')
        self.plot2.set_ylabel('Precipiations(mm)')
        self.plot2.plot([x+1 for x in range(tailleprecip[0])], y3, 'b-')

        self.canvas = FigureCanvasTkAgg(self.fig, self.main)
        self.canvas = self.canvas.get_tk_widget()
        self.main.pack(fill=BOTH)
        self.canvas.pack(padx=5, pady=5, fill=BOTH, expand=1)


class VueLocale(Frame):
    def __init__(self, root, tmin, tmax, precip, year):
        self.tmin = tmin
        self.tmax = tmax
        self.precip = precip
        self.year = year
        self.posx = None
        self.posy = None
        
        self.main = Frame(root)
        self.parametres = Frame(self.main)
        self.courbeTemperature = Frame(self.main)
        self.courbePrecipitation = Frame(self.main)
        self.courbes = None
        self.latText = Label(self.parametres, text="Latitude") 
        self.lonText = Label(self.parametres, text="Longitude") 
        self.Latitude = Entry(self.parametres, width=10)
        self.Longitude = Entry(self.parametres)
        self.afficher = Button(self.parametres, text="Afficher", command=lambda:self.afficher_courbes(self.Longitude.get(), self.Latitude.get()))

        self.main.pack()
        self.parametres.grid()
        self.courbeTemperature.grid()
        self.courbePrecipitation.grid()
        self.latText.grid(row=0, column=0)
        self.lonText.grid(row=0, column=2)
        self.Latitude.grid(row=0, column=1)
        self.Longitude.grid(row=0, column=3)
        self.afficher.grid(row=0, column=4)

    def afficher_courbes(self, longitude, latitude):
        if self.tester_saisie(longitude, latitude):
            latitude = float(latitude)
            longitude = float(longitude)
            if latitude > 90:
                while(latitude > 90):
                    latitude = latitude - 180
            if latitude < -90:
                while(latitude < -90):
                    latitude = latitude + 180
            if longitude > 180:
                while(longitude > 180):
                    longitude = longitude - 360
            if longitude < -180:
                while(longitude < -180):
                    longitude = longitude + 360
            if self.courbes == None:
                self.equivalence_cordonnees(longitude, latitude)
                self.courbes = Courbes(self.courbeTemperature, self.tmin, self.tmax, self.precip, self.posx, self.posy, self.year)
            else:
                self.courbes.main.destroy()
                self.equivalence_cordonnees(longitude, latitude)
                self.courbes = Courbes(self.courbeTemperature, self.tmin, self.tmax, self.precip, int(self.posx), int(self.posy), self.year)     

    def equivalence_cordonnees(self, longitude, latitude):
        rayonTerre = 6373
        nbre_masquer = np.ma.count_masked(self.tmin.vals[0])
        tai = np.shape(self.tmin.vals)
        t = (tai[1]*tai[2]) - nbre_masquer
        distances = np.zeros((t, 3))
        
        taille = np.shape(distances)
        dist = np.zeros(taille[0])
        k = 0
        print(t)
        for i, lat in enumerate(self.tmin.lats):
            for j, lon in enumerate(self.tmin.lons):
                if ma.is_masked(self.tmin.vals[0][i][j]):
                    continue
                else:
                    a = ((sin(math.radians((latitude - lat) / 2))**2)) + cos(math.radians(latitude)) * cos(math.radians(lat)) * ((sin(math.radians((longitude - lon) / 2))**2))
                    c = 2 * atan2(math.radians(((a)**0.5)), math.radians(((1 - a)**0.5)))
                    d = rayonTerre * c
                    distances[k][0] = i
                    distances[k][1] = j
                    distances[k][2] = d
                    k+=1
        print(k)           
        for i in range(t):
            dist[i] = distances[i][2]
        print(distances)
        courte_dist = np.amin(dist)
        print(courte_dist)
        for j in range(k):
            if distances[j][2] == courte_dist:
                self.posx = int(distances[j][0])
                self.posy = int(distances[j][1])
                print(distances[j][0], distances[j][1], distances[j][2])
                break
        
        print(self.posx, self.posy)

    def tester_saisie(self, longitude, latitude):
        consomne = ["abcdefghijklmnopqrstuvwxyz"]
        if longitude == "" and latitude == "":
            messagebox.showerror('Erreur','Saisir les coordonnees')
            return False
        elif longitude == "" and latitude != "":
            messagebox.showerror('Erreur','Saisir la longitude')
            return False
        elif longitude != "" and latitude == "":
            messagebox.showerror('Erreur','Saisir la latitude')
            return False
        elif longitude != "" and latitude != "":
            if self.tester_char(longitude, latitude):
                return True
            else:
                return False
        """
        elif longitude != "" and latitude != "":
            if len(longitude.ascii_letters)==0 and len(latitude.ascii_letters)==0:
                return True
            elif len(longitude.ascii_letters)==0 and len(latitude.ascii_letters) != 0:
                messagebox.showerror('Erreur','Le format de saisie de la latitude est incorrect')
                return False
            elif len(longitude.ascii_letters)!=0 and len(latitude.ascii_letters)==0:
                messagebox.showerror('Erreur','Le format de saisie de la longitude est incorrect')
                return False
        """

    def tester_char(self, longitude, latitude):
        consomne = ["abcdefghijklmnopqrstuvwxyz"]
        for i in range(len(longitude)):
            for j in range(len(consomne)):
                if longitude[i] == consomne[j]:
                    return False
                else:
                    continue
        for i in range(len(latitude)):
            for j in range(len(consomne)):
                if latitude[i] == consomne[j]:
                    return False
                else:
                    continue
        return True




        



