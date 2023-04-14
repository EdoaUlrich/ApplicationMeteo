from netCDF4 import Dataset
import numpy.ma as ma
import numpy as np
from concurrent.futures import *

class Data:
    def __init__(self, source):
        print("Chargement du fichier")
        dataset = Dataset(source)
        print('Chargement Termine')

        self.lats = dataset.variables['lat'][:]
        self.lons = dataset.variables['lon'][:]
        self.times = dataset.variables['time'][:]
        if "max" in source: 
            self.vals = dataset.variables['tmax'][:]
        elif "min" in source:
            self.vals = dataset.variables['tmin'][:]
        elif "precip" in source:
            self.vals = dataset.variables['precip'][:]
        self.mask = None
        
    
        
        


        

        





