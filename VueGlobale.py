from tkinter import *
import tkinter.ttk as tk


class VueGlobale(Frame):
    def __init__(self,root, tmin, tmax, precip, year):
        self.parametres = tk.Notebook(root)
        self.parJour = tk.Frame(self.parametres)
        self.parMois = tk.Frame(self.parametres)

        self.parametres.add(self.parJour, text="Par jour")
        self.parametres.add(self.parMois, text="Par mois")

        self.parametres.pack()




