import math
import os
import pickle 
import shutil
import datetime 
import pathlib
import Main_arch as march
import logging
import logging.handlers
'''----------------------------------------------------------------------------------------------'''
path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent 
if 'Forex_experiments' in path.parts:
    path = path.parent / str(datetime.date.today())
else:
    path = path / 'Forex_experiments'  / str(datetime.date.today())
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

file_path = pathlib.PureWindowsPath(os.path.abspath(__file__))
shutil.copy(file_path, path / (file_path.stem + str(experiment_number) + file_path.suffix) )
'''------------------------------------------------------------------------------------------------'''
def loader (x, default = None):
    try:
        data = pickle.load(open(str(path.parent / ( x + '.pkl')), 'rb')) 
    except FileNotFoundError:
        data  = default
        
    return data

'''------------------------------------------------------------------------------------------------'''
archive = loader('archive', default = {}) 

def archivarius ( substance, archive = archive,):
    archive[substance.name] = substance
    pickle.dump(archive, open(path.parent / 'archive.pkl', 'rb+'))
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
from forex_python.converter import CurrencyRates

class main ():
    def __init__(self):

        self.Fungus = march.Colony(Scheme=[100, 80, 60, 40], 
                              Network_mode=['Deep_Pawn', 'Deep_Bishop', 'Deep_Bishop', 'Deep_Bishop'],
                              SchemebyLayer=[ [100, 80, 60, 40, 20, 10, 5, 2] ])
        self.Fungus.name = 'NIVARA' + str(datetime.datetime.now())

        self.Inf = []
        self.diapason = 100
        self.origin_date =  datetime.datetime(2000, 3, 12 )
        self.precision = [0, 0]
        self.waves = [0, 0, 0] # Up , Neural, Down
        
    def mainloop (self, Informator):
        while self.origin_date <= datetime.datetime.today():
            self.Inf.append(Informator.get_rate('USD', 'GBP', self.origin_date))
            
            if len(self.Inf) > self.diapason:
                flag = None
                if self.Inf[-2] < self.Inf[-1]:
                    flag = 1
                    self.waves[0] += 1         
                elif self.Inf[-2] > self.Inf[-1]:
                    flag = -1
                    self.waves[2] += 1
                elif flag == None:
                    flag = 0
                    self.waves[1] += 1
                    
                priority = []
                for ant in self.Fungus.nationaleconomy:
                    loss = 0 if (2*(int(ant[1][1])%2)-1) == flag else 1
                    loss = 0 if flag == 0 else loss
                    
                    count = 0
                    for ne in priority:
                        if ne[1] > loss:
                            priority = priority[:count] + [(ant[0], loss)] + priority[count:]
                            break
                        count += 1
                    else:
                        priority.append((ant[0], loss))
                   
                logger.info(str(flag)+'  '+str(100 - sum([ant[1] for ant in priority])) )
                if flag == 0:
                    pass
                elif priority[0][1] == 0:
                    self.precision[0] += 1
                else:
                    self.precision[1] += 1
                    
                    
                self.Fungus.population[0] = [ant[0] for ant in priority]
                self.Fungus.inheritance()
                self.Fungus.night()
                self.Fungus.day()
                self.Fungus.moon()
                
                
            self.Inf = self.Inf[-100:] if len(self.Inf) > 100 else self.Inf
            
            if len(self.Inf) >= self.diapason:
                self.Fungus.task(self.Inf[-self.diapason:])
            self.origin_date += datetime.timedelta(days=1)
            logger.info(str(self.origin_date) + '  ' + str(self.precision))
       
ground = main()       

while ground.origin_date <= datetime.datetime.today():
    try:
        Informator = CurrencyRates()
        ground.mainloop(Informator)
    except Exception as e:
        logger.exception(str(e))
    finally:
        archivarius(ground.Fungus)

archivarius(ground.Fungus)












































































