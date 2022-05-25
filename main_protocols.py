import random
import math

def will_versions(algo):
    def second_version(parent, child):
        reserve = []
        reserve_names = []
        for c in child:
            if c.father != None and c.father not in reserve:
                for p in parent:
                    if p.name == c.father:
                        reserve.append(p)
                        reserve_names.append(p.name)
                        
        for p in parent:
            if p not in reserve:
                reserve.append(p)
                
        return reserve
        
    def third_version(parent, child):
        reserve = [None for p in range(max(len(parent),len(child)))]
        
        for p in parent:
            count = 0
            childcount = []
            for c in child:
                count += 1
                if c.father == p.name and (True if len(childcount) == 0 else c.name > childcount[1].name):
                    childcount = [count, c]
            
            if len(childcount) == 0:
                reserve.append(p)
            else:

                reserve[childcount[0] - 1] = p 
                
            final = [ k for k in reserve if k != None ]
        
        return final
            
        
    return third_version

def choice_versions (fun):
    def second_version(sample, entropy):
        sample_len = len(sample)
        pseudo_sample = [i for i in range(sample_len)]
        deviation = 0.9*entropy + 0.1
        weights = [math.erf(i/(deviation*math.sqrt(2))) - math.erf((i -1)/(deviation*math.sqrt(2))) for i in range(1, sample_len+1)]
        better_pseudo_sample = []
        for j in range(sample_len):
            if sum(weights) == 0:
                weights = [i + 1 for i in weights]
            renumbered_pseudo_sample = range(len(pseudo_sample))
            d = random.choices(renumbered_pseudo_sample, weights = weights, k=1)[0]
            better_pseudo_sample.append(pseudo_sample[d])
            del pseudo_sample[d]
            del weights[d]
        return [sample[j] for j in better_pseudo_sample]
        
    def thrid_version(sample, entropy):
        sample_len = len(sample)
        pseudo_sample = [i for i in range(sample_len)]
        deviation = 9.86159778*entropy + 0.13840222
        weights = [math.erf(i/(deviation*math.sqrt(2))) - math.erf((i -1)/(deviation*math.sqrt(2))) for i in range(1, sample_len+1)]
        better_pseudo_sample = []
        for j in range(sample_len):
            if sum(weights) == 0:
                weights = [i + 1 for i in weights]
            renumbered_pseudo_sample = range(len(pseudo_sample))
            d = random.choices(renumbered_pseudo_sample, weights = weights, k=1)[0]
            better_pseudo_sample.append(pseudo_sample[d])
            del pseudo_sample[d]
            del weights[d]
        return [sample[j] for j in better_pseudo_sample]
        
    return second_version

@will_versions
def will(parent, child):
    parent_copy = []
    for c in child:
        if c.father != None:
            for p in range(len(parent)):
                if parent[p].name == c.father:
                    parent_copy.append(parent[p])
                    del parent[p]
                    break
    parent_copy += parent
    return parent_copy

def shufflness (x):
    s = 0
    for i in range(len(x)):
        n = x[i]
        s += abs( n - i ) 
    return s
        
def chaos_generator():
    test_input = [random.randrange(10), random.randrange(10)]
    while True:
        yield test_input
        
    
@choice_versions
def choice (sample):
    sample_len = len(sample)
    pseudo_sample = [i for i in range(sample_len)]
    weights = [math.erf(i/math.sqrt(2)) - math.erf((i -1)/math.sqrt(2)) for i in range(1, sample_len+1)]
    better_pseudo_sample = []
    for j in range(sample_len):
        renumbered_pseudo_sample = range(len(pseudo_sample))
        d = random.choices(renumbered_pseudo_sample, weights = weights, k=1)[0]
        better_pseudo_sample.append(pseudo_sample[d])
        del pseudo_sample[d]
        del weights[d]
    return [sample[j] for j in better_pseudo_sample]
    