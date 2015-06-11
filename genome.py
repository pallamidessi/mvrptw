# -*- coding:utf-8 -*-

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


