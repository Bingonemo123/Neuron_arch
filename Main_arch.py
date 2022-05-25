import inspect
import pathlib
if __name__ != '__main__':
    for frame in inspect.stack()[1:]:
        if frame.filename[0] != '<':
            path = pathlib.PureWindowsPath(frame.filename).stem
            break

if path != 'math_protocols':
    from math_protocols import *
if path != 'main_protocols':
    from main_protocols import *
if path != 'Neuron_arch':
    from Neuron_arch import *
if path != 'Network_arch':
    from Network_arch import *
if path != 'Colony_arch':
    from Colony_arch import *