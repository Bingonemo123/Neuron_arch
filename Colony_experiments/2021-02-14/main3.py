import os
import pickle 
import shutil
import datetime 
import pathlib
import Main_arch as march
'''----------------------------------------------------------------------------------------------'''
path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent 
if 'Colony_experiments' in path.parts:
    path = path.parent / str(datetime.date.today())
else:
    path = path / 'Colony_experiments'  / str(datetime.date.today())
# After this, path is equals to current date folder
    
try:
    os.mkdir(str(path))
except OSError as ose:
    print ("Creation of the directory %s failed" % str(path))
    print (ose)
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

def archivarius ( substance, archive = archive,):
    archive[substance.name] = substance
    pickle.dump(archive, open(path.parent / 'archive.pkl', 'wb+'))
'''-------------------------------------------------------------------------------------------------'''


Fungus = march.Colony(Scheme=[100, 80, 60, 40], Network_mode=['Deep_Pawn', 'Deep_Bishop', 'Deep_Bishop', 'Deep_Bishop'])
print(Fungus)






































