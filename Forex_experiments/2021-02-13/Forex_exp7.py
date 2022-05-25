import os
import pickle 
import shutil
import datetime 
import pathlib

path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent 
if 'Forex_experiments' in path.parts:
    path = path.parent / str(datetime.date.today())
else:
    path = path / 'Forex_experiments'  / str(datetime.date.today())
# After this, path is equals to current date folder
    
try:
    os.mkdir(str(path))
except OSError:
    print ("Creation of the directory %s failed" % str(path))
else:
    print ("Successfully created the directory %s " % str(path))

try:
    experiment_number = pickle.load(open(str(path.parent / 'experiment_number.pkl'), 'rb+')) + 1
except FileNotFoundError:
    experiment_number = 1
pickle.dump(experiment_number, open(str(path.parent / 'experiment_number.pkl'), 'wb+'))

file_path = pathlib.PureWindowsPath(os.path.abspath(__file__))
shutil.copy(file_path, path / (file_path.stem + str(experiment_number) + file_path.suffix) )
'''------------------------------------------------------------------------------------------------'''
def loader (x, default = None):
    try:
        data = pickle.load(open(str(path.parent / ( x + '.pkl')), 'rb+')) 
    except FileNotFoundError:
        data  = default
        
    return data

'''------------------------------------------------------------------------------------------------'''
archive = loader('archive', default = {}) 

def archivarius ( Network, archive = archive,):
    archive[Network.name] = Newtork
    pickle.dump(archive, open('archive.pkl', 'rb+'))
'''-------------------------------------------------------------------------------------------------'''
from forex_python.converter import CurrencyRates
Informator = CurrencyRates()












































