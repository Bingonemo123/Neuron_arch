import math

def expit(x):
    try:
        return 1/(1+ math.e**(-x))
    except ArithmeticError:
        if x > 0:
            return 1
        else:
            return 0

def cosh (x):
    try:
        return 1/2 * (math.e**(x) + math.e**(-x))
    except ArithmeticError:
        return float('inf')

def sinh (x):
    try:
        return 1/2 * (math.e**(x) - math.e**(-x))
    except ArithmeticError:
        if x > 0:
            return float('inf')
        else:
            return float('-inf')

def tanh (x):
    return sinh(x)/cosh(x)

def ReLU(x):
    if x > 0:
        return x 
    else:
        return 0

def liner(x):
    return x
    
def expitwide(x):
    return 2*expit(x)-1

def leakyReLU(x):
    return x * (x > 0) + (0.01 * x) * (x < 0)

""" derivatives """
def ReLUprime(x):
    return 1 * (x > 0) 

def expitprime(x):
    return float(expit(x) * (1 - expit(x)))

def tanhprime(x):
    return float((1 / cosh(x)) ** 2)

def linerprime(x):
    return 1
    
def expitwideprime(x):
    return 2*expitprime(x)
    
def leakyReLUprime(x):
    return 1 * (x > 0) + 0.01 * (x <= 0)
    
def isnan(x):
    return math.isnan(x)