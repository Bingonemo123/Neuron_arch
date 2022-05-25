import sys
sys.path.append('C:\\Users\\envy\\Documents\\MEGAsync\\Python\\repos\\Neuron_arch')
import temples
import random
import pickle 
import datetime
import copy
archive = {}
def archivarius (archive, Network):
    archive[Network.name] = Newtork
    pickle.dump(archive, open('archive.pkl', 'rb+'))
from forex_python.converter import CurrencyRates
Informator = CurrencyRates()

# Only long and short learning without neutral
Inf = []
dates = []
origin_date =  datetime.datetime(2000, 3, 12 )
relu_net = temples.Deep_network(5)
archive[5] = relu_net
rang = 20
relu_net.build([20, 15, 10, 5, 2, 1], 1)
precision = [0, 0]
flags = [0, 0, 0] # Down , Neural, Up

while origin_date <= datetime.datetime.today():
    Inf.append(Informator.get_rate('USD', 'GBP', origin_date))
    dates.append(origin_date)
    
    plateau = ''
    if len(Inf) > rang:
        flag = None
        if Inf[-2] > Inf[-1]:
            relu_net.backpropagation(-1)
            flag = -1
            flags[0] += 1
            plateau = 'Down'
        elif Inf[-2] < Inf[-1]:
            relu_net.backpropagation(1)
            flag = 1
            flags[2] += 1
            plateau = 'Up'
            
        if flag == None:
            plateau = 'plateau'
        elif prediction == flag:
            precision[0] += 1
           
        else:
            precision[1] += 1
         
    Inf = Inf[-100:] if len(Inf) > 100 else Inf[0:]
    dates = dates[-100:] if len(dates) > 100 else dates[0:]
    
    if len(dates) >= rang:
        prediction = relu_net.spark(*Inf[-rang:])
        
        prediction = prediction[0]
        if prediction < 0:
            prediction = -1
        elif prediction >= 0:
            prediction = 1
            
        print("Prediction " + str(prediction) + ";", precision, flags, plateau)

    
    origin_date += datetime.timedelta(days=1)