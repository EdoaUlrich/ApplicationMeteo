# Application_Meteo
Cette application a été créée dans le but de visualiser les différentres variations de températures et precipitations entre les différentes coordonnées du globe terrestre.
Afin de pouvoir compiler efficacement notre programe, il est necessaire de créer un dossier nommé "donnees" dans le même repertoire que nos fichiers sources. Celui-ci contiendra, les fichiers contenants nos données qui seront visualisées. Vous trouverez ces données sur les liens suivants:
- Températures: https://downloads.psl.noaa.gov/Datasets/cpc_global_temp/
- Précipitations: https://downloads.psl.noaa.gov/Datasets/cpc_global_precip/
Il est necessaire de télécharger des fichiers spécifiques à unique année.

En plus des fichiers de données, il est important que vous installiez un ensemble de module sur votre ordinateur:
- Cartopy:
    Pour Windows :
        1 - Installer Anaconda via le lien https://docs.anaconda.com/anaconda/install/, ou pour eviter de prendre trop d'epace vous pouvez installer miniconda via https://docs.conda.io/en/latest/miniconda.html
        2 - Si vous ne l'avez pas coché pendant l'installation, mettez à jour vos variables d'environnements
        3 - Dans un powershell administrateur, lancez la commande :
            conda install -c conda-forge cartopy
        4 - La distribution python par défaut de votre système peut maintenant utiliser le module

    Pour Ubuntu :
        1ere solution :
            sudo apt -y install libproj-dev libgeos-dev
            sudo pip3 install cartopy
        2eme solution:
            sudo apt install python3-cartopy

    Pour Mac :
        voir ici -> https://scitools.org.uk/cartopy/docs/latest/installing.html

- NetCDF4:
    Sur Anaconda ou miniconda: 
        conda install -c anaconda netcdf4
    Sur Python: 
        pip install netCDF4

- Tkinter:
    Sur Anaconda ou miniconda: 
        conda install -c anaconda tk
    Sur Python: 
        pip install tk

- Matplotlib:
    Sur Anaconda ou miniconda: 
        conda install -c conda-forge matplotlib
    Sur Python: 
        python -m pip install -U matplotlib
