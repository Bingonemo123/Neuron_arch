import Main_arch as march
import threading
import queue

class Colony:
    def __init__ (self, **kwargs):
        ''' Colony provides several functionality. It can be used to create Niveaus of networks. It provides hiearachy to set of networks.
        networks in same Niveau have same heieararchy and compete with each other. lowest hiearchy neatorks are modifeaed by next level nerworks.
        It can be that low level Niveau  modifeas high level Niveau. This Niveau is colled crossroad. and it creates loops in Colony.
        Colony has several arguments: 1.{Scheme} -> list[int] Is list of integers and gives information about how many niveaus there are in Colony
        and how many Networks are in each Niveau. for example Scheme=[100, 80 , 60]; gives Colony class information that there are three Niveaus (by len(Scheme) )
        and in first Niveau there are 100 Networks; in second there are 80 Networks and so on. 2.{Network_mode} -> list[str] Is list of strings, coresponding
        each Niveau. Its tell Colony class, which type of Netowrks consist each Niveau. for example: Network_mode=['Deep_Pawn', 'Deep_Bishop']; tells
        Colony class that first Niveau contains network of Deep_Pawn and second - Deep_Bishop. Every mode in Network_mode, must be class name from Newtork_arch.py
        3.[Scheme_by_layer] -> list[list[list[int]]] Is complex structure list, which provides control over neurons in each individual Network. 
                '''
        '''Obligatoy Inputs'''
        self.Scheme = kwargs.get('Scheme')
        self.layer_number = len(self.Scheme)
        self.Network_mode = kwargs.get('Network_mode')
        self.younglings = {x: self.Scheme[x] for x in range(self.layer_number)} # names of youngest Networks in layers
        '''Optional Inputs'''
        self.SchemebyLayer = kwargs.get('SchemebyLayer', [])
        self.TypebyLayer = kwargs.get('TypebyLayer', [])
        
        '''Building'''
        self.population = {}
        for l in range(self.layer_number):
            layer = []
            scheme = self.SchemebyLayer[l] if l < len(self.SchemebyLayer) else 'default'  
            neuron_type = self.TypebyLayer[l] if l < len(self.TypebyLayer) else 'default'  # defailt neuron type is 0 or RELU
            for net in range(1, self.Scheme[l] + 1):
                if scheme == 'default' and neuron_type == 'default':
                    layer.append(getattr(march, self.Network_mode[l])(net))
                elif isinstance(scheme, list) and isinstance(neuron_type, int):
                    layer.append(getattr(march, self.Network_mode[l])(net, scheme=scheme, neuron_type=neuron_type))
                elif isinstance(scheme, list) :
                    layer.append(getattr(march, self.Network_mode[l])(net, scheme=scheme))
                elif isinstance(neuron_type, int):
                    layer.append(getattr(march, self.Network_mode[l])(net, neuron_type=neuron_type))
            self.population[l] = layer
                    
        
    def mathematical_analysis(self, errors):
        generator = march.chaos_generator()
        self.nationaleconomy = []
        for ant in self.population[0]:
            loss =  ant.mathematical_test(generator, errors=errors)

            count = 0
            for ne in self.nationaleconomy:
                if ne[1] > loss:
                    self.nationaleconomy = self.nationaleconomy[:count] + [(ant, loss)] +self.nationaleconomy[count:]
                    break
                count += 1
            else:
                self.nationaleconomy.append((ant,loss))
        
        self.population[0] = [ant[0] for ant in self.nationaleconomy]
        return self.population[0]
        
    def mathematical_analysis_thr(self, errors=None):
        generator = march.chaos_generator()
        self.nationalQueue = queue.Queue()
        self.nationaleconomy = []

        thr_archive = [threading.Thread(target=ant.mathematical_test, args=(generator,),
                        kwargs={'Queue': self.nationalQueue, 'errors': errors}) for ant in self.population[0]]
        start_time = march.time.time()
        thr_start = [thr.start() for thr in thr_archive]
        thr_join = [thr.join() for thr in thr_archive]
        end_time = march.time.time()
        while not self.nationalQueue.empty():
            ant, loss = self.nationalQueue.get()
            count = 0
            for ne in self.nationaleconomy:
                if ne[1] > loss:
                    self.nationaleconomy = self.nationaleconomy[:count] + [(ant, loss)] +self.nationaleconomy[count:]
                    break
                count += 1
            else:
                self.nationaleconomy.append((ant,loss))
        
        self.population[0] = [ant[0] for ant in self.nationaleconomy]
        return self.population[0], end_time - start_time
        
        
        
    def work(self, inputs, answers, method):
        if  isinstance(inputs, list):
            self.nationaleconomy = []
            for ant in self.population[0]:
                outputs = ant.work(inputs)
                loss = method(outputs, answers)
                
                count = 0
                for ne in self.nationaleconomy:
                    if ne[1] > loss:
                        self.nationaleconomy = self.nationaleconomy[:count] + [(ant, loss)] +self.nationaleconomy[count:]
                        break
                    count += 1
                else:
                    self.nationaleconomy.append((ant, loss))
            return self.nationaleconomy            
        
    def labor(self, door, method):
        inputs = door
        if  isinstance(inputs, list):
            self.nationaleconomy = []
            for ant in self.population[0]:
                outputs = ant.work(inputs)
                answers = (yield outputs)

                loss = method(outputs, answers)
                count = 0
                for ne in self.nationaleconomy:
                    if ne[1] > loss:
                        self.nationaleconomy = self.nationaleconomy[:count] + [(ant, loss)] +self.nationaleconomy[count:]
                        break
                    count += 1
                else:
                    self.nationaleconomy.append((ant, loss))
            yield self.nationaleconomy         

    def task(self, inputs, errors=None):
        if isinstance(inputs, list):
            self.nationaleconomy = []
            for ant in self.population[0]:
                outputs = ant.work(inputs, errors=errors)
                self.nationaleconomy.append((ant, outputs))
            return self.nationaleconomy
            
    def inheritance(self):
        for ant in self.population:
            if ant != 0:
                march.will(self.population[ant], self.population[ant-1])
                
    def night(self):
        for ant in self.population:
            severity = self.Scheme[-1] //2 
            for x in range(self.layer_number - ant -1):
                severity = self.Scheme[-x -1] - severity 
            self.population[ant] = self.population[ant][: -severity]
            
    def day(self):
        for ant in self.population:
            if ant!= 0:
                for x in range(self.Scheme[ant -1] - len(self.population[ant -1])):
                    self.population[ant-1].append(self.population[ant][x].create( self.population[ant-1][x] ))
                    self.younglings[ant-1]+=1
                    
    def day_thr(self):
        for ant in self.population:
            if ant != 0:
                thr_archive = []
                for x in range(self.Scheme[ant -1] - len(self.population[ant -1])):
                    self.population[ant-1].append(self.population[ant][x].create( self.population[ant-1][x] ))
                    self.younglings[ant-1]+=1
        
    def moon(self):
        # makes cirle 
        for x in range(self.Scheme[-1] - len(self.population[self.layer_number-1])):
            self.population[self.layer_number-1].append(self.population[1][x].create( self.population[self.layer_number-1][x] ) )
            
    def axoncomplexitymap(self):
        self.nationaleconomy = []
        for ant in self.population[0]:
            loss = ant.axonsum()
            count = 0
            for ne in self.nationaleconomy:
                if ne[1] < loss:
                    self.nationaleconomy = self.nationaleconomy[:count] + [(ant, loss)] +self.nationaleconomy[count:]
                    break
                count += 1
            else:
                self.nationaleconomy.append((ant, loss))
                
        self.population[0] = [ant[0] for ant in self.nationaleconomy]
        return self.population[0]
        
    def axoncomplexitymaplocal(self, x):
        self.nationaleconomylocal = []
        for ant in x:
            loss = ant.axonsum()
            count = 0
            for ne in self.nationaleconomylocal:
                if ne[1] < loss:
                    self.nationaleconomylocal = self.nationaleconomylocal[:count] + [(ant, loss)] +self.nationaleconomylocal[count:]
                    break
                count += 1
            else:
                self.nationaleconomylocal.append((ant, loss))
                
        return [ant[0] for ant in self.nationaleconomylocal]
       
    def CheckpointA(self, Scheme, Network_mode):
        for x in self.Scheme:
            if x <= 0:
                raise ColonyInputError(x, 'All numbers in Scheme must be greater than zero.')
        for x in self.Network_mode:
            if x not in dir(march):
                raise ColonyInputError(x, 'Network mode is not defined.')
        if len(Scheme) != len (Network_mode):
            raise ColonyInputError( 'Lenth of Scheme and Network modes must be equal')

    def __str__(self):
        return str([len(self.population[ant]) for ant in self.population])

class ColonyError(Exception):
    """Base class for exceptions in this module."""
    pass
    
class ColonyInputError(ColonyError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

       














































