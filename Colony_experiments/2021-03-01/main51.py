import os
import pickle 
import shutil
import datetime 
import pathlib
import Main_arch as march
import logging
import logging.handlers
'''----------------------------------------------------------------------------------------------'''
if os.name == 'posix':
    file_path = pathlib.PurePosixPath(os.path.abspath(__file__))
    path = pathlib.PurePosixPath(os.path.abspath(__file__)).parent 
    if 'Colony_experiments' in path.parts:
        path = path.parent / str(datetime.date.today())
    else:
        path = path / 'Colony_experiments'  / str(datetime.date.today())
    # After this, path is equals to current date folder
else:
    file_path = pathlib.PureWindowsPath(os.path.abspath(__file__))
    path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent 
    if 'Colony_experiments' in path.parts:
        path = path.parent / str(datetime.date.today())
    else:
        path = path / 'Colony_experiments'  / str(datetime.date.today())
    # After this, path is equals to current date folder
    
try:
    os.mkdir(str(path))
except OSError as ose:
    pass

try:
    experiment_number = pickle.load(open(str(path.parent / 'experiment_number.pkl'), 'rb+')) + 1
except FileNotFoundError:
    experiment_number = 1
pickle.dump(experiment_number, open(str(path.parent / 'experiment_number.pkl'), 'wb+'))

shutil.copy(file_path, path / (file_path.stem + str(experiment_number) + file_path.suffix) )
'''------------------------------------------------------------------------------------------------'''
def loader (x, default = None):
    try:
        data = pickle.load(open(str(path.parent / ( x + '.pkl')), 'rb')) 
    except FileNotFoundError:
        data  = default
    except EOFError:
        data = default
    return data

'''------------------------------------------------------------------------------------------------'''
archive = loader('archive', default = {}) 

def archivarius ( substance, archive = archive,):
    archive[substance.name] = substance
    pickle.dump(archive, open(path.parent / 'archive.pkl', 'wb+'))
'''-------------------------------------------------------------------------------------------------'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
"""StreamHandler"""
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG) 
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
"""FileHandler"""
rotatingfile_handler = logging.handlers.RotatingFileHandler(path.parent/'main.log', backupCount=5, maxBytes=1073741824)
rotatingfile_handler.setLevel(logging.DEBUG)
rotatingfile_handler.setFormatter(formatter)
logger.addHandler(rotatingfile_handler)

logger.info('Main Entry ' + str(experiment_number))
'''-------------------------------------------------------------------------------------------------'''


class main ():
    def __init__(self):

        self.Fungus = march.Colony(Scheme=[100, 80, 60, 40], Network_mode=['Deep_Pawn', 'Deep_Bishop', 'Deep_Bishop', 'Deep_Bishop'])
        self.Fungus.name = 'NIVARA' + str(datetime.datetime.now())

    def mainloop (self, Informator=None):
        while True:     
            print('Start')
            self.Fungus.mathematical_analysis_thr() 
            print('End')
            speech = [self.Fungus.population[0][0].axonsum(), self.Fungus.nationaleconomy[0][1]]
            logger.info('  '.join([str(sp) for sp in speech]))
            self.Fungus.inheritance()
            self.Fungus.night()
            self.Fungus.day()
            self.Fungus.moon()


ground = main()       

while True:
    try:
        ground.mainloop()
    except Exception as e:
        logger.exception(str(e))

archivarius(ground.Fungus)













































