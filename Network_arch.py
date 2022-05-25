import Main_arch as march
import random 
import time 
import copy
''' aditional packages : slugify & graphviz '''

class Network:
    def __init__ (self, name):
        self.name = name
        self.father = None
        self.plot = [march.Neuron(0, 1) for i in range(7)]

    def __getitem__ (self, key):
        try:
            return self.plot[key]
        except IndexError:
            return march.GhostNeuron()

    def __iter__(self):
        return self.plot.__iter__()

    def __len__(self):
        return len(self.plot)
            
    def sparkacc (self, *inputs):
        """ 
        spark with output accumulation
        """
        
        """input run"""
        for n in range(len(self.input_neurons)):
            cn = self.input_neurons[n] # current_neuron
            try:
                cn += inputs[n]
            except IndexError:
                pass
            cn.depolarize(self)
        """ plot run """
        for n in self:
            n.depolarize(self)
            
        return [float(ov) for ov in self.output_neurons]
            
    def spark (self, *inputs):
        """ input run """
        self.output_clean()
        for n in range(len(self.input_neurons)):
            cn = self.input_neurons[n] # current_neuron
            try:
                cn += inputs[n]
            except IndexError:
                pass
            cn.depolarize(self) # Input is not accumulated because this 
        """ plot run """
        for n in self:
            n.depolarize(self)
            
        return [float(ov) for ov in self.output_neurons]

    def clean(self):
        for n in self:
            n.preadded_value = 0

    def output_clean(self):
        for n in self.output_neurons:
            n.preadded_value = 0

    def add_neuron (self, ans):
        activator = int(ans[2])%len(march.GhostNeuron.function_store) 
        bias = float(ans[3])
        self.plot.append(march.Neuron(bias, activator))
    
    def del_neuron(self, ans):
        plot_length =  len(self)
        if plot_length == 0:
            return None
        neuron_name = int(ans[2])%plot_length
        del self.plot[neuron_name]

    def add_axon(self, ans):
        ''' Axons to output neurons can be added.
        But axons from input neurons - can't be.'''
        plot_length = len(self)
        if plot_length == 0:
            return None
        base_neuron = int(ans[2])%plot_length
        target_neuron = int(ans[3])
        if target_neuron > 0 :
            target_neuron %= plot_length
        else:
            target_neuron = -1 * (abs(target_neuron) % len(self.output_neurons))
        weight = float(ans[4])
        new_axon = [[target_neuron, weight],]
        self[base_neuron].axons += new_axon

    def del_axon(self, ans):
        ''' Axons from  input neurons can't be deleterd.
        But axons to output neurons -can.'''
        plot_length = len(self)
        if plot_length == 0: # No neurons in Network
            return None
        neuron_name = int(ans[2])%plot_length
        axons_length = len(self[neuron_name])
        if axons_length == 0: # No axons on that neuron
            return None
        axon_name = int(ans[4])%axons_length
        del self[neuron_name].axons[axon_name]

    def chg_bias (self, ans): 
        plot_length = len(self)
        if plot_length == 0:
            return None
        neuron_name = int(ans[2])%plot_length
        bias = float(ans[3])
        self[neuron_name].bias = bias

    def chg_weight (self, ans):
        plot_length = len(self)
        if plot_length == 0:
            return None
        neuron_name = int(ans[2])%plot_length
        axons_length = len(self[neuron_name])
        if axons_length == 0:
            return None
        axon_name = int(ans[4])%axons_length
        weight = float(ans[4])
        self[neuron_name][axon_name][1] = weight

    def view_neuron(self, ans): 
        plot_length = len(self)
        if plot_length == 0:
            return [0, 0, 0, 0]
        neuron_name = int(ans[2])%plot_length
        return [self.name, neuron_name, self[neuron_name].bias, self[neuron_name].memory]

    def view_axon(self, ans): 
        plot_length = len(self)
        if plot_length == 0:
            return [0, 0, 0, 0]
        neuron_name = int(ans[2])%plot_length
        axons_length = len(self[neuron_name])
        if axons_length == 0:
            return [0, 0, 0, 0]
        axon_name = int(ans[4])%axons_length
        return [self.name, neuron_name, self[neuron_name][axon_name][0], self[neuron_name][axon_name][1]]
        
    def work (self, inputs, timeout=1, errors = None):
        strating_time  = time.time()
        self.output_clean()
        while (int(self.output_neurons[0])%2) == 0 and time.time() - strating_time < timeout: 
            outputs = self.spark(*inputs)
            if errors:
                self.backpropagation(*errors)
        return outputs
        
    def draw (self):
        from graphviz import Digraph
        dot = Digraph(name = str(self.name))
        dot.attr(rankdir='LR', rank='min')
        dot.attr('node', shape='circle')
        count = 1
        for n in self.input_neurons:
            dot.node('I' + str(count), shape = 'rarrow')
            for a in n.axons:
                dot.edge('I' + str(count), 'N' + str(int(a[0])), label = str(round(a[1], 2)))
            count += 1
        
        count = 1
        for n in self:
            neuron_type_str = ['R', 'E', 'T', 'L', 'S'][n.activator]
            dot.node('N' + str(count), neuron_type_str + str(count)
                        +'\\n' + str(round(n.bias, 2))
                        +'\\n' + str(round(n.NO, 2) ) )
            for a in n.axons:
                if a[0] > 0:
                    dot.edge('N' + str(count),'N' + str(int(a[0])), label = str(round(a[1], 2)))
                elif a[0] == 0:
                    dot.edge('N' + str(count),'G', label = str(round(a[1], 2)))
                else:
                    dot.edge('N' + str(count),'O' + str(abs(int(a[0]))), label = str(round(a[1], 2)))
            count += 1
        
        count = 1
        for n in self.output_neurons:
            if count == 1:
                dot.node('G')
            else:
                dot.node('O' + str(count-1))
            count += 1
        
        return dot
        
    def axonsum (self):
        return sum([len(n.axons) for n in self])

class Deep_Network (Network):
    def __init__ (self, name):
        self.name = name
        self.father = None
        self.plot = [ ]
        self.layers = { }
        self.last_layer = 0
        self.last_neuron = 0

    def setup_inputs(self, numb):
        self.input_neurons = [march.Neuron(0, 3) for i in range(numb)]

    def setup_outputs(self, numb):
        self.output_neurons = [march.Neuron(0, 3) for i in range(numb)]
        
    def setup_learning_rate(self, rate):
        for n in self:
            n.learning_rate = rate

    def add_layer(self, numb, neuron_type,  randomness = False):
        self.plot += [march.Neuron(0, neuron_type) for i in range(numb)]
        if self.last_layer == 0:
            for input_neuron in self.input_neurons:
                input_neuron.axons = [ [i+1,  0.5 ] for i in range(numb)]
        else:
            for neuron in self.layers[self.last_layer]:
                self[neuron].axons = [ [i+1, random.random() if randomness else 0.5  ] for  i in range (self.last_neuron, self.last_neuron + numb)]
        self.last_neuron += numb
        self.last_layer += 1	
        self.layers[self.last_layer] = [i for i in range(self.last_neuron - numb, self.last_neuron)]

    def touch_up (self): # refine
        for neuron in self.layers[self.last_layer]:
                self[neuron].axons = [ [-1*i, 0.5 ] for i in range(len(self.output_neurons))]
                
    def build(self, architecture, neuron_type, randomness=False):
        self.setup_inputs(architecture[0])
        self.setup_outputs(architecture[-1])
        for layer in architecture[1:-1]:
            self.add_layer(layer, neuron_type, randomness=randomness)
        self.touch_up()
    
    def clean_NO(self):
        for n in self:
            n.NO = 0

    def backpropagation (self, *errors):
        self.clean_NO()  # NO accumulation
        for n in reversed(self.plot):
            for a in n:
                if a[0] <= 0:
                    cost_value = (self.output_neurons[abs(a[0])] - errors[abs(a[0])])
                    z = n.last_value * a[1] + n.bias
                    d_w = cost_value * n.function_prime(z) * n.last_value
                    w = a[1] - (n.learning_rate * d_w)
                    a[1] = w
                    n.NO += cost_value * w
                elif a[0] > 0:
                    forward_NO = self[a[0]].NO 
                    z = n.last_value * a[1] + n.bias
                    d_w = forward_NO * n.function_prime(z) * n.last_value 
                    w = a[1] - (n.learning_rate * d_w)
                    a[1] = w
                    n.NO += forward_NO * w

class Pawn(Network):
    def __init__(self, name, mode = 'dynamic'):
        Network.__init__(self, name)
        getattr(self, mode)()
        
    def mathematical_test (self, generator, timeout = 1, errors=None, Queue=None):
        strating_time  = time.time()
        self.output_clean()
        numbers = next(generator)
        correct_ans = sum(numbers)
        while (int(self.output_neurons[0])%2) == 0 and time.time() - strating_time < timeout: 
            self.spark(*numbers)
            if errors:
                self.backpropagation(1, correct_ans)
        if Queue:
            Queue.put((self, abs(self.output_neurons[1] -  correct_ans)))
        return abs(self.output_neurons[1] -  correct_ans)

    def static (self):
        self.output_neurons = [march.Neuron(0, 3), march.Neuron(0, 3)]
        self.input_neurons = [march.Neuron(0, 3), march.Neuron(0, 3)]
        self.input_neurons[0].axons = [[1, 1],]
        self.input_neurons[1].axons = [[2, 1],]
        self.plot[0].axons = [[2, 0.5],[3, 0.5],[4, 0.5],[5, 0.5]] # neuron 1
        self.plot[1].axons = [[1, 0.5],[3, 0.5],[4, 0.5],[5, 0.5]] # neuron 2
        self.plot[2].axons = [[2, 0.5],[1, 0.5],[4, 0.5],[5, 0.5]] # neuron 3
        self.plot[3].axons = [[2, 0.5],[3, 0.5],[1, 0.5],[5, 0.5],[6, 0.5]] # neuron 4
        self.plot[4].axons = [[2, 0.5],[3, 0.5],[4, 0.5],[1, 0.5],[7, 0.5]] # neuron 5
        self.plot[5].axons = [[4, 0.5],[7, 0.5],[-1, 0.5]] # neuron 6
        self.plot[6].axons = [[5, 0.5],[6, 0.5],[0, 0.5]] # neuron 7
     
    def dynamic (self):
        self.output_neurons = [march.Neuron(0, 3), march.Neuron(0, 3)]
        self.input_neurons = [march.Neuron(0, 3), march.Neuron(0, 3)]
        self.input_neurons[0].axons = [[1, 1],]
        self.input_neurons[1].axons = [[2, 1],]
        self.plot[0].axons = [[2, random.random()],[3, random.random()],[4, random.random()],[5, random.random()]] # neuron 1
        self.plot[1].axons = [[1, random.random()],[3, random.random()],[4, random.random()],[5, random.random()]] # neuron 2
        self.plot[2].axons = [[2, random.random()],[1, random.random()],[4, random.random()],[5, random.random()]] # neuron 3
        self.plot[3].axons = [[2, random.random()],[3,random.random()],[1, random.random()],[5, random.random()],[6, random.random()]] # neuron 4
        self.plot[4].axons = [[2, random.random()],[3, random.random()],[4, random.random()],[1, random.random()],[7, random.random()]] # neuron 5
        self.plot[5].axons = [[4, random.random()],[7, random.random()],[-1, random.random()]] # neuron 6
        self.plot[6].axons = [[5, random.random()],[6, random.random()],[0, random.random()]] # neuron 7
      
class Bishop(Network):
    def __init__(self, name):
        self.output_neurons = [march.Neuron(0, 3) for k in range(5)] # ground; operator type; neuron_name; bias ; weight
        self.input_neurons = [march.Neuron(0, 3) for k in range(4)]
        self.input_neurons[0].axons = [[1, 1], [2, 1], [3, 1], [4, 1]]
        self.input_neurons[1].axons = [[1, 1], [2, 1], [3, 1], [4, 1]]
        self.input_neurons[2].axons = [[1, 1], [2, 1], [3, 1], [4, 1]]
        self.input_neurons[3].axons = [[1, 1], [2, 1], [3, 1], [4, 1]]
        Network.__init__(self, name)
        self[0].axons = [[5, 0.5],[6, 0.5],[7, 0.5]] # neuron 1
        self[1].axons = [[5, 0.5],[6, 0.5],[7, 0.5]] # neuron 2
        self[2].axons = [[5, 0.5],[6, 0.5],[7, 0.5]] # neuron 3
        self[3].axons = [[5, 0.5],[6, 0.5],[7, 0.5]] # neuron 4
        self[4].axons = [[0, 0.5],[-1, 0.5],[-2, 0.5],[-3, 0.5],[-4, 0.5]] # neuron 5
        self[5].axons = [[0, 0.5],[-1, 0.5],[-2, 0.5],[-3, 0.5],[-4, 0.5]] # neuron 6
        self[6].axons = [[0, 0.5],[-1, 0.5],[-2, 0.5],[-3, 0.5],[-4, 0.5]] # neuron 7

    def create(self, prototype, timeout = 2, entropy = 1):
        strating_time  = time.time()
        child = copy.deepcopy(prototype) # identical Network to prototype
        self.actions = [self.chaos, self.peace,
            child.add_neuron, child.del_neuron, 
            child.add_axon, child.del_axon,
            child.chg_bias, child.chg_weight,
            child.view_neuron, child.view_axon]
        input_checkpoint = []
        self.output_clean()
        while (int(self.output_neurons[0])%2) == 0 and time.time() - strating_time < timeout:
            self.spark(*input_checkpoint)

            operator_type = self.actions[int(self.output_neurons[1])%len(self.actions)]
            operator_type = random.choices([self.chaos, operator_type],
                            weights=[entropy, 1 - entropy])[0]

            respond = operator_type(self.output_neurons)
            if respond: input_checkpoint = respond
        self.clean()
        child.father = self.name
        return child

    def peace (self, ans):
        pass

    def chaos (self, ans):
        respond = random.choice(self.actions)(ans)
        return respond
        
class Deep_Pawn(Deep_Network, Pawn):
    def __init__(self, name, scheme = [2, 10, 10, 10, 2], neuron_type = 0, randomness=True):
        Deep_Network.__init__(self, name)
        self.build(scheme, neuron_type, randomness=randomness)
        
class Deep_Bishop(Deep_Network, Bishop):
    def __init__(self, name, scheme = [4, 10, 10, 10, 5], neuron_type = 0, randomness=True):
        Deep_Network.__init__(self, name)
        self.build(scheme, neuron_type, randomness=randomness)
   
