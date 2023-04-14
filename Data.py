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
        
        self.chargement_masque()
        
    
    def chargement_masque(self):
        #self.mask = ma.masked_where(not ma.is_masked(self.vals[0]),self.vals[0])
        """
        self.mask = np.array([[True]*len(self.lons) for i in range(len(self.lats))])
        for i, lat in enumerate(self.lats):
            for j, lon in enumerate(self.lons):
                if ma.is_masked(self.vals[0][i][j]):
                    self.mask[i][j] = 
        """
        self.mask = np.ma.getmask(self.vals)
    
        
        


        

        





