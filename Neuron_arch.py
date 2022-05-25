from math_protocols import *
import random

class GhostNeuron:  
    function_store = [ReLU, expit, tanh, liner, expitwide, leakyReLU]
    prime_store = [ReLUprime, expitprime, tanhprime, linerprime, expitwideprime, leakyReLUprime]
    def __init__(self):
       self.preadded_value = 0
       self.axons = []
       self.NO = 0

    def __add__(self, p):
       return p + self.preadded_value
       
    def __radd__(self, p):
        return p + self.preadded_value
 
    def __sub__(self, p):
       return -1*(p - self.preadded_value)
       
    def __rsub__(self, p):
        return p - self.preadded_value

    def __iadd__(self, p):
        self.preadded_value = p + self.preadded_value
        return self
        
    def __mod__ (self, p):
        return self.preadded_value%p
        
    def __rmod__(self, p):
        return p%self.preadded_value

    def __le__(self, other):
        if self.preadded_value <= 0:
            return True
        else:
            return False

    def __int__(self):
        return int(self.preadded_value) if math.inf != self.preadded_value else 0

    def __float__(self):
        return float(self.preadded_value) 

    def __len__(self):
        return len(self.axons)

    def __getitem__ (self, key):
        try:
            return self.axons[key]
        except IndexError:
            return [0, 0]

    def __iter__(self):
        return self.axons.__iter__()

class Neuron(GhostNeuron):
    def __init__ (self, bias , activator):
        self.bias = bias 
        self.activator = activator # 0 --> ReLU; 1 --> sigmoid; 2 -->  tanh; 3--> liner; 4--> negative sigmoid; 5--> leakyReLU
        self.activator_function = self.function_store[self.activator]
        self.function_prime = self.prime_store[self.activator]
        self.memory = 0
        self.preadded_value = 0
        self.last_value = 0
        self.NO = 0
        self.axons = []
        self.learning_rate = 0.1

    def depolarize(self, Net):
        for a in self:
            target_neuron = a[0] # number class 
            weight = a[1]
            z = weight*self.preadded_value + self.bias
            potential =  float(self.activator_function(z))
            
            if target_neuron > 0:
                target_neuron = Net[int(target_neuron - 1)] # Neuron class
                if isnan(target_neuron + potential): # checking before adding
                    potential = random.random()
                target_neuron += potential
                if isnan(float(target_neuron)): # checking after adding
                    target_neuron.preadded_value = random.random()

            else:
                target_neuron = Net.output_neurons[int(abs(target_neuron))] # Neuron _class # IndexError must be avoided
                if isnan(target_neuron + potential): 
                    potential = random.random()
                target_neuron += potential # real addition
                if isnan(float(target_neuron)):
                    target_neuron.preadded_value = random.random()
            if isnan(a[1]):
                a[1] = random.random()
        self.last_value = self.preadded_value
        self.preadded_value = 0
        self.memory += 1
