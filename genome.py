# -*- coding:utf-8 -*-
import itertools
from operators import window_bounds_checking

class MvrpIndividual(object):
    """
    Genome definition. The genome is implemented a two-part chromosome describe in
    the \\\ article[1].
    
    routes : A list of integer, referencing appointement by their indexes
    
    vehicles : A list of integer, where each values represent a vehicle and how many
    appointement it contained starting from the head of the list.
    
    Example:

    |1|2|3|4|5|6| || |2|2|2|

    Vehicle_1 contains |1|2|
    Vehicle_2 contains |3|4|
    Vehicle_3 contains |5|6|
    
    [1]:
    """
    def __init__(self, attributes):
        self.routes = attributes[0]
        self.vehicles = attributes[1]

    def __repr__(self):
        return ("<Individual routes %s vehicle %s> \n" % (self.routes, self.vehicles))
    
    def split(self):
        """ 
        Split the first part of the individual as a list of route using the second part 
        """
        splitted_route = []
        idx = 0

        for vehicle_size in self.vehicles:
            splitted_route.append(self.routes[idx:vehicle_size + idx])
            idx += vehicle_size

        print splitted_route
        print self
        return splitted_route

    def is_time_constraint_respected(self, data):
        tmp = self.decode(data)
        result = 0
        for sublist in tmp:
            if len(sublist) != 0:
                current = sublist[0]
                for i in range(1, len(sublist)):
                    if not window_bounds_checking(current, sublist[i]):
                        result += 1
                    current = sublist[i]
        return result

    def is_load_respected(self):
        tmp = self.split()
        for sublist in tmp:
            if len(sublist) < 5:
                return False
        return True

    def decode(self, data):
        tmp = self.split()
        to_return = []
        index = 0
        for sublist in tmp:
            to_return.append([])
            for element in sublist:
                to_return[index].append(data[element])
            index += 1
        return to_return

    def encode(self, data):
        self.vehicles = []
        for sublist in data:
            self.vehicles.append(len(sublist))
        self.routes = list(itertools.chain.from_iterable(data))
