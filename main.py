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
except OSError:
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
from mnist import MNIST
mndata = MNIST(r"..\..\mnist")
images, labels = mndata.load_training()


class main ():
    def __init__(self):
        self.Tree = march.Deep_Network(1)
        self.Tree.build([784]  + [784 - i for i in range(1, 774, 10)] + [10, 10], 
                        5, randomness=True)
        for j in range(10):
            self.Tree.plot[-j-1].axons = [[ j - 9, 0.5]]
        self.Tree.setup_learning_rate(1)

        self.Fungus = march.Colony(Scheme=[100, 80, 60, 40], 
                                    Network_mode=['Deep_Pawn', 'Deep_Bishop', 'Deep_Bishop', 'Deep_Bishop'],
                                    TypebyLayer = [])
        self.Fungus.name = 'NIVARA' + str(datetime.datetime.now())


    def mainloop(self):
        for image, label in zip(images, labels):
            output = self.Tree.spark(*image)
            intout = 0
            greatest = max(output)
            for n in output:
                if greatest != n:
                    intout += 1
                else:
                    break
            
            logger.info(output + [intout])
            logger.info([0 if i!= label else 1 for i in range(10) ] + [label])
            self.Tree.backpropagation(*[0 if i!= label else 1 for i in range(10) ])

ground = main()
ground.mainloop()
archivarius(ground.Tree)













































