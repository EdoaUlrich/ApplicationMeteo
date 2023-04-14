from os import times
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk
from netCDF4 import Dataset
from Data import *
from VueGlobale import *
from VueLocale import *
# -*- coding: utf-8 -*-

class Interface:
    def __init__(self):
        self.root = Tk()
        self.frameAnnee = tk.Frame(self.root)
        self.frameOnglet = tk.Frame(self.root)
        self.anneeText = Label(self.frameAnnee, text="Annee: ")
        years = [str(i) for i in range(1991, 2023)]
        self.anneeCombobox = tk.Combobox(self.frameAnnee, values=years)
        self.chargerBouton = tk.Button(self.frameAnnee, text="Charger", command=lambda:self.Charger_donnees(self.anneeCombobox.get()))

        self.vueGlobale = None
        self.vueLocale = None

        #Création de onglets Vue Globale et Courbe Locale
        self.Onglets = tk.Notebook(self.frameOnglet)
        self.ongletVueGlobale = tk.Frame(self.Onglets)
        self.ongletCourbeLocale = tk.Frame(self.Onglets)
        self.Onglets.add(self.ongletVueGlobale, text="Vue globale")
        self.Onglets.add(self.ongletCourbeLocale, text="Courbe locale")

        self.frameAnnee.pack(side='top', fill='x')
        self.frameOnglet.pack(fill='x')
        self.anneeText.pack(side='left')
        self.anneeCombobox.pack(side='left')
        self.chargerBouton.pack(side='left')
        self.Onglets.pack(fill='x')

        self.root.geometry("700x500") # Dimensions de notre fenetre
        self.root.mainloop()

    def Charger_donnees(self, year):
        print(year)
        if year != "":
            self.tmin = Data('./donnees/tmin.{}.nc'.format(year))
            self.tmax = Data('./donnees/tmax.{}.nc'.format(year))
            self.precip = Data('./donnees/precip.{}.nc'.format(year))
            #executor = ThreadPoolExecutor(max_workers=4)
            #tache1 = executor.submit(self.tmin.chargement_masque)
            #tache2 = executor.submit(self.tmax.chargement_masque)
            #tache3 = executor.submit(self.precip.chargement_masque)
            if self.vueGlobale == None:
                self.vueGlobale = VueGlobale(self.ongletVueGlobale, self.tmin, self.tmax, self.precip, year)
                self.vueLocale = VueLocale(self.ongletCourbeLocale, self.tmin, self.tmax, self.precip, year)
            else:
                self.vueGlobale.parametres.destroy()
                self.vueLocale.main.destroy()
                self.vueGlobale = VueGlobale(self.ongletVueGlobale, self.tmin, self.tmax, self.precip, year)
                self.vueLocale = VueLocale(self.ongletCourbeLocale, self.tmin, self.tmax, self.precip, year)
            self.root.mainloop()
        else:
            messagebox.showerror('Erreur','Selectionnez une annee')





