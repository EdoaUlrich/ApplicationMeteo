from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk
import matplotlib.pylab as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import numpy as np
import numpy.ma as ma
# -*- coding: utf-8 -*-


class VueGlobale(Frame):
    def __init__(self, root, tmin, tmax, precip, year): 
        self.tmin = tmin
        self.tmax = tmax
        self.precip = precip
        self.year = year

        #Creations des Frames de l'onglet VueGlobale
        self.main = Frame(root)
        self.parametres = tk.Notebook(self.main)
        self.carteFrame = Frame(self.main)
        self.canvas = None
        self.parJour = tk.Frame(self.parametres)
        self.parMois = tk.Frame(self.parametres)
        self.parametres.add(self.parJour, text="Par jour")
        self.parametres.add(self.parMois, text="Par mois")
        
        donnee = ["Temperatures min", "Temperatures max", "Precipitations"]
        autres = ["Valeurs minimales", "Valeurs maximales"]
        mois = ["Janvier","Fevrier","Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]

        #Widgets de l'onglet Par jour
        self.donneesTextParJour = tk.Label(self.parJour, text="Donnees :")
        slash = tk.Label(self.parJour, text="/")
        self.choixParJour = StringVar()
        self.donneesComboboxParJour = tk.Combobox(self.parJour, values=donnee)
        self.datesRadioParJour = tk.Radiobutton(self.parJour, text="Date precise :", variable=self.choixParJour, value="Dates")
        self.moisComboboxParJour = tk.Combobox(self.parJour, values=mois)
        self.day = None
        self.jourCombobox = tk.Combobox(self.parJour)
        self.autresRadioParJour = tk.Radiobutton(self.parJour, text="Autre :", variable=self.choixParJour, value="Autres")
        self.autresComboboxParJour = tk.Combobox(self.parJour, values=autres)
        self.validerParJour = tk.Button(self.parJour, text="Lancer les calculs", command=lambda:self.afficher_carte_par_jour())

        #Widgets de l'onglet par Mois
        self.donneesTextParMois = Label(self.parMois, text="Donnees:")
        self.donneesComboboxParMois = tk.Combobox(self.parMois, values=donnee)
        self.choixParMois = StringVar()
        self.moisRadio = tk.Radiobutton(self.parMois, text="Mois precis:", variable=self.choixParMois, value="Mois")
        self.moisComboboxParMois = tk.Combobox(self.parMois, values=mois)
        self.autresRadioParMois = tk.Radiobutton(self.parMois, text="Autre:", variable=self.choixParMois, value="Autres")
        self.autresComboboxParMois = tk.Combobox(self.parMois, values=autres)
        self.validerParMois = Button(self.parMois, text="Lancer les calculs", command=lambda:self.afficher_carte_par_mois())
        

        #-------------------PACK et GRID-----------------------
        #Pack et Grid
        self.main.pack()
        self.parametres.pack()
        self.carteFrame.pack()
        #self.carte.pack()

        #Pack de Widgets de l'onglet Par Jour
        self.donneesTextParJour.grid(row=0, column=0, pady=5)
        self.donneesComboboxParJour.grid(row=0, column=1, pady=5)
        self.datesRadioParJour.grid(row=1, column=0, sticky="w", pady=5)
        self.jourCombobox.grid(row=1, column=1, pady=5)
        slash.grid(row=1, column=2, padx=5, sticky="ns", pady=5)
        self.moisComboboxParJour.grid(row=1, column=3, pady=5)
        self.moisComboboxParJour.current()
        self.moisComboboxParJour.bind("<<ComboboxSelected>>", self.comboboxJour)
        self.autresRadioParJour.grid(row=2, column=0, sticky="w", pady=5)
        self.autresComboboxParJour.grid(row=2, column=1, pady=5)
        self.validerParJour.grid(row=3, column=1, pady=5)

        #Pack des widgets de l'onglet Par Mois
        self.donneesTextParMois.grid(row=0 , column=0, pady=5)
        self.donneesComboboxParMois.grid(row=0 , column=1, pady=5)
        self.moisRadio.grid(row=1 , column=0, sticky="w", pady=5)
        self.moisComboboxParMois.grid(row=1 , column=1, pady=5)
        self.autresRadioParMois.grid(row=2 , column=0, sticky="w", pady=5)
        self.autresComboboxParMois.grid(row=2 , column=1, pady=5)
        self.validerParMois.grid(row=3 , column=1, pady=5)

    #------------------------ LES METHODES ------------------------
    def comboboxJour(self, event): #Cette methode permet d'afficher le nombre de jour en fonction du mois selectionné
        mois = event.widget.get()
        if mois=="Janvier" or mois=="Mars" or mois=="Mai" or mois=="Juillet" or mois=="Aout" or mois=="Octobre" or mois=="Decembre":
            self.day = [str(i) for i in range(1,32)]
        if mois=="Avril" or mois=="Juin" or mois=="Septembre" or mois=="Novembre":
            self.day = [str(i) for i in range(1,31)]
        if mois=="Fevrier":
            if self.tester_annee_bisextille():
                self.day = [str(i) for i in range(1, 30)]
            else:
                self.day = [str(i) for i in range(1, 29)]
        self.jourCombobox.config(value=self.day)

    def tester_annee_bisextille(self): #Cette Methode permet de tester si l'année est bisextille
        if int(self.year)%4==0 or int(self.year)%400==0:
            return True
        else:
            return False

    def indices_par_Mois(self, dictionnaire): #Cette methode retourne les deux indices i et j representant les indices du premier et dernier jour du mois
        i = 0
        for key, value in dictionnaire.items():
            if key == self.moisComboboxParMois.get():
                break
            else:
                i += value-1
        j = i + dictionnaire[self.moisComboboxParMois.get()]
        return [i, j]

    def indices_par_Jour(self, dictionnaire): # Cette methode retourne l'indice i qui represente l'indice du jour du mois selectionné
        i = 0
        for key, value in dictionnaire.items():
            if key == self.moisComboboxParJour.get():
                break
            else:
                i += value
        i = i + int(self.jourCombobox.get()) - 1
        return i 

    def tester_widget_par_jour(self): # Fonction permetant de tester si l'utilisateur a rempli correctement les parametres de l'onglet "Par Jour"
        if self.donneesComboboxParJour.get() == "":
            messagebox.showerror('Erreur','Selectionner une valeur Donnees')
            return False
        else:
            if self.choixParJour.get() == "":
                messagebox.showerror('Erreur',"Vous devez faire un choix entre 'Mois precis' et 'Autres' ! ")
                return False
            else:
                if self.choixParJour.get() == "Autres":
                    if self.autresComboboxParJour.get() == "":
                        messagebox.showerror('Erreur','Selectionner une valeur Autres')
                        return False
                    elif self.autresComboboxParJour.get() == "Valeurs minimales":
                        return True
                    elif self.autresComboboxParJour.get() == "Valeurs maximales":
                        return True
                if self.choixParJour.get() == "Dates":
                    if self.moisComboboxParJour.get() == "" and self.jourCombobox.get()=="":
                        messagebox.showerror('Erreur','Selectionner une date')
                        return False
                    elif self.moisComboboxParJour.get() != "" and self.jourCombobox.get()=="":
                        messagebox.showerror('Erreur','Selectionner une Journee')
                        return False
                    elif self.moisComboboxParJour.get() == "" and self.jourCombobox.get()!="":
                        messagebox.showerror('Erreur','Selectionner un mois')
                        return False
                    elif self.moisComboboxParJour.get() != "" and self.jourCombobox.get()!="":
                        return True

    def tester_widget_par_mois(self):  #Fonction permetant de tester si l'utilisateur a rempli correctement les parametres de l'onglet "Par Jour"
        if self.donneesComboboxParMois.get() == "": 
            messagebox.showerror('Erreur','Selectionner une valeur Donnees')
            return False
        else:
            if self.choixParMois.get() == "":
                messagebox.showerror('Erreur',"Vous devez faire un choix entre 'Mois precis' et 'Autres' ! ")
                return False
            else:
                if self.choixParMois.get() == "Autres":
                    if self.autresComboboxParMois.get() == "":
                        messagebox.showerror('Erreur','Selectionner une valeur Autres')
                        return False
                    elif self.autresComboboxParMois.get() == "Valeurs minimales":
                        return True
                    elif self.autresComboboxParMois.get() == "Valeurs maximales":
                        return True
                if self.choixParMois.get() == "Mois":
                    if self.moisComboboxParMois.get() == "":
                        messagebox.showerror('Erreur','Selectionner une valeur Dates')
                        return False
                    else:
                        return True

    def afficher_carte_par_jour(self):
        if self.tester_widget_par_jour(): # On teste si l'utilisateur à fait correctement tous les choix sur les parametres
            if self.canvas == None: # On teste si on avait auparavant déja affiché une carte, on detruit l'ancienne affichage si c'est le cas
                pass
            else:
                self.canvas.destroy()
            
            # On cree un dictionnaire qui permet de gérer le nombre de jour par mois
            mois_dict = {
                'Janvier' : 31,    
                'Fevrier' : 28,   
                'Mars' : 31,    
                'Avril' : 30,    
                'Mai' : 31,    
                'Juin' : 30,    
                'Juillet' : 31,   
                'Aout' : 31,  
                'Septembre' : 30 ,  
                'Octobre' : 31,  
                'Novembre' : 30,  
                'Decembre' : 31    
            }
            if self.tester_annee_bisextille():
                mois_dict["Fevrier"] = 29
            
            #On crée la figure qui contiendra notre carte
            fig = plt.figure(figsize=(7,7))
            ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
            
            if self.choixParJour.get() == "Autres":
                if self.autresComboboxParJour.get() == "Valeurs minimales":
                    indices = self.jour_Min()
                elif self.autresComboboxParJour.get() == "Valeurs maximales":
                    indices = self.jour_Min()
            elif self.choixParJour.get() == "Dates": 
                indices = self.indices_par_Jour(mois_dict) #On recupere l'indices correspondant au jour précis
            if self.donneesComboboxParJour.get() == "Temperatures max":
                cm = ax.pcolormesh(self.tmax.lons, self.tmax.lats, self.tmax.vals[indices], cmap="jet")
            elif self.donneesComboboxParJour.get() == "Temperatures min":
                cm = ax.pcolormesh(self.tmin.lons, self.tmin.lats, self.tmin.vals[indices], cmap="jet")
            elif self.donneesComboboxParJour.get() == "Precipitations":
                cm = ax.pcolormesh(self.precip.lons, self.precip.lats, self.precip.vals[indices], cmap="jet")
            
            ax.coastlines(resolution='110m')
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            plt.colorbar(cm, ax=ax, fraction=0.046, pad=0.04)
            self.canvas = FigureCanvasTkAgg(fig, self.carteFrame)
            self.canvas = self.canvas.get_tk_widget()
            self.canvas.pack()

    def afficher_carte_par_mois(self): 
        if self.tester_widget_par_mois():
            if self.canvas == None:
                pass
            else:
                self.canvas.destroy()
            fig = plt.figure(figsize=(7,7))
            ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

            mois_dict = {
                'Janvier' : 31,    
                'Fevrier' : 28,   
                'Mars' : 31,    
                'Avril' : 30,    
                'Mai' : 31,    
                'Juin' : 30,    
                'Juillet' : 31,   
                'Aout' : 31,  
                'Septembre' : 30 ,  
                'Octobre' : 31,  
                'Novembre' : 30,  
                'Decembre' : 31    
            }
            if self.tester_annee_bisextille():
                mois_dict["Fevrier"] = 29

            if self.donneesComboboxParMois.get() == "Temperatures max":
                if self.choixParMois.get() == "Autres":
                    indices = self.mois_min(mois_dict)
                    avg = np.average(self.tmax.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.tmax.lons, self.precip.lats, avg, cmap="jet")
                if self.choixParMois.get() == "Mois":
                    indices = self.indices_par_Mois(mois_dict)
                    avg = np.mean(self.tmax.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.tmax.lons, self.tmax.lats, avg, cmap="jet")
            elif self.donneesComboboxParMois.get() == "Temperatures min":
                if self.choixParMois.get() == "Autres":
                    indices = self.mois_min(mois_dict)
                    avg = np.average(self.tmin.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.tmin.lons, self.precip.lats, avg, cmap="jet")
                if self.choixParMois.get() == "Mois":
                    indices = self.indices_par_Mois(mois_dict)
                    avg = np.mean(self.tmin.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.tmin.lons, self.tmin.lats, avg, cmap="jet")
            elif self.donneesComboboxParMois.get() == "Precipitations":
                if self.choixParMois.get() == "Autres":
                    indices = self.mois_min(mois_dict)
                    avg = np.average(self.precip.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.precip.lons, self.precip.lats, avg, cmap="jet")
                if self.choixParMois.get() == "Mois":
                    indices = self.indices_par_Mois(mois_dict)
                    avg = np.average(self.precip.vals[indices[0]:indices[1]], axis=(0))
                    cm = ax.pcolormesh(self.precip.lons, self.precip.lats, avg, cmap="jet")
             
            ax.coastlines(resolution='110m')
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            plt.colorbar(cm, ax=ax, fraction=0.046, pad=0.04)
            self.canvas = FigureCanvasTkAgg(fig, self.carteFrame)
            self.canvas = self.canvas.get_tk_widget()
            self.canvas.pack(fill='x')

    def mois_min(self, dictionnaire): #Cette fonction permet de retourner l'indice du mois le chaud, froid ou precipiteux 
        mois = np.zeros((12, 360, 720)) #Cette variable permet de contenir la moyenne de temperature/premicipation par mois
        i = 0
        j2 = 0
        j1 = 0
        
        #On choisit tout d'abod le type de donnees a traiter
        if self.donneesComboboxParMois.get() == "Precipitations":
            vals = self.precip.vals
        elif self.donneesComboboxParMois.get() == "Temperatures max":
            vals = self.tmax.vals
        elif self.donneesComboboxParMois.get() == "Temperatures min":
            vals = self.tmin.vals

        #Cette boucle permet de faire la moyenne des donnees afin d'obtenir des données par mois et non par jour 
        for key, value in dictionnaire.items():
            if key == 'Janvier':
                j2 = j1 + value - 1
            else:
                j2 = j1 + value
            mois[i] = np.mean(vals[j1:j2], axis=(0)) 
            i += 1
            j1 = j2
        #Ici on va stocker dans avg la moyenne des temperatures/precipitaions par mois dans le monde
        avg = np.zeros((12))
        for i in range(12):
            avg[i]= np.mean(mois[i])
        print(avg)
        #Ces conditions permettent de rechercher l'index dans avg la valeur maximales ou minimale du mois 
        if self.autresComboboxParMois.get() == "Valeurs maximales": 
            value_index = np.unravel_index(np.ma.argmax(avg), avg.shape)
        elif self.autresComboboxParMois.get() == "Valeurs minimales":
            value_index = np.unravel_index(np.ma.argmin(avg), avg.shape)
        #min_value_index = np.unravel_index(np.ma.argmin(avg), avg.shape)

        k = 0
        i = 0
        j = 0
        for key, value in dictionnaire.items():
            if key == value_index:
                break
            else:
                i += value-1
        print(value_index)
        for key in dictionnaire.keys():
            if k == value_index[0]:
                index = key
                break
            k+=1
        j = i + dictionnaire[index]
        return [i,j]
    
    def jour_Min(self):
        #On choisit tout d'abod le type de donnees a traiter
        if self.donneesComboboxParJour.get() == "Precipitations":
            vals = self.precip.vals
        elif self.donneesComboboxParJour.get() == "Temperatures max":
            vals = self.tmax.vals
        elif self.donneesComboboxParJour.get() == "Temperatures min":
            vals = self.tmin.vals

        taille = np.shape(vals)
        print(taille[0])
        jour = np.zeros((taille[0], 360, 720))
        #Cette boucle permet de faire la moyenne des donnees afin d'obtenir des données par mois et non par jour 
        for i in range(taille[0]):
            jour[i] = np.mean(vals[i])
        #Ici on va stocker dans avg la moyenne des temperatures/precipitaions par mois dans le monde
        avg = np.zeros((taille[0]))
        for i in range(taille[0]):
            avg[i] = np.mean(jour[i])
        print(avg)
        #Ces conditions permettent de rechercher l'index dans avg la valeur maximales ou minimale du mois 
        if self.autresComboboxParJour.get() == "Valeurs maximales": 
            value_index = np.unravel_index(np.ma.argmax(avg), avg.shape)
        elif self.autresComboboxParJour.get() == "Valeurs minimales":
            value_index = np.unravel_index(np.ma.argmin(avg), avg.shape)
        #min_value_index = np.unravel_index(np.ma.argmin(avg), avg.shape)

        return value_index[0]
    







