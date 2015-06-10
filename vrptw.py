# -*- coding:utf-8 -*-

import random
import numpy
import visualisation
import model
import copy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


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


def initIndividual(ind_class, size, nb_vehicle):
    """
    Initialisation operator. Fill the inidividual's first part with a random permutation of
    appointement and compute the second part with a valid vehicle count.
    """
    remaining_size = size 
    second_part = []
    first_part = []
    
    # Create the second part of the individual
    # Choose random value while checking the upper bound
    for i in range(0, nb_vehicle):
        vehicle_capacity = random.randrange(1, 5)
        vehicle_capacity %= remaining_size + 1
        remaining_size -= vehicle_capacity
        second_part.append(vehicle_capacity)
    
    # If there is still unassignated vehicles at the end
    # Assigned them to the last vehicle
    if remaining_size > 0:
        second_part[-1] += remaining_size
    
    # Create the first part of the chromosome 
    # Just a random permutation of indexes
    first_part = range(0, size - 1)
    random.shuffle(first_part)
    
    # Create the individual and return it
    ind = ind_class((first_part, second_part))
    return ind


def evaluate(individual, data, depot):
    """
    Evaluate the genome.
    """
    splitted_route = []
    idx = 0
    capacity_per_vehicle = 5
    distance = 0
    load = 0
    
    # Split the first part of the individual as a list of route using the second part
    for vehicle_size in individual.vehicles:
        splitted_route.append(individual.routes[idx:vehicle_size])
        idx += vehicle_size
    
    # For each vehicle (route)
    # Compute the distance travelled and the load 
    for route in splitted_route:
        if len(route) > 0:
            distance += model.euclidian_distance(depot, data[route[0]])
            for gene1, gene2 in zip(route[0:-1], route[1:]):
                distance += model.euclidian_distance(data[gene1], data[gene2])

            for gene1, gene2 in zip(route[0:-1], route[1:]):
                load += 1
            
            load -= capacity_per_vehicle

    # Return a tuple of fitness: the cost and the load 
    return distance, load


def cxRC(ind1, ind2):
    """
    Custom RC (or BCRC) crossover as describe in the article[1]
    
    [1]:
    """    
    return ind1, ind2


def constrainedSwap(ind, data):
    """
    A random swap following constraints.
    Need pretty heavy refactoring 
    """
    list_appointement = data
    splitted_route = []
    idx = 0 

    # Split the first part of the individual as a list route using the second part
    for vehicle_size in ind.vehicles:
        splitted_route.append(ind.routes[idx:vehicle_size])
        idx += vehicle_size
    
    # Randomly choose a non-empty route
    while True:
        rand_route = random.randrange(0, len(splitted_route))
        if len(splitted_route[rand_route]) > 0:
            break
    
    # Choose a random appointement in the selected route
    rand_appointement = random.randrange(0, len(splitted_route[rand_route]))
    
    # Now we insert this appointement into a ramdomly selected route if we can find
    # a place where it respect constraints. If not, we do nothing
    shuffled_route = range(0, len(splitted_route))
    random.shuffle(shuffled_route)
    
    for i in shuffled_route:
        if i != rand_route:
            ii = 0
            for appointement_idx in splitted_route[i]:
                
                # If the next element in the list start after the one we want to
                # insert, we emplace it here, and delete it from where we took it 
                if list_appointement[appointement_idx].starting_time > list_appointement[rand_appointement]:
                        splitted_route[i].insert(ii, rand_appointement)
                        del splitted_route[rand_route][rand_appointement]
                        return ind,
                
                # If the last appointement is starting before the one we want to insert,
                # We insert it at the end of of the route, and delete it from where we took it   
                elif ii == len(splitted_route[i]) - 1:
                    if list_appointement[appointement_idx].starting_time < list_appointement[rand_appointement]:
                        list_appointement.append(rand_appontement)
                        del splitted_route[rand_route][rand_appointement]
                        return ind,

    return ind,

def main():
    random.seed(666)

    # Problem's definition  
    depot = model.Point(500, 500)
    w = 1000
    h = 1000
    num_route = 2
    num_node_per_route = 5
    IND_SIZE = num_route * num_node_per_route

    # Genetic parameter
    pop_size = 300
    elite_size = 1
    crossover_probability = 0.7
    mutation_probability = 0.7
    ngen = 50
    
    # Assign the custom individual class to the toolbox
    # And set the number of wanted fitnesses 
    toolbox = base.Toolbox()
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
    creator.create("Individual", MvrpIndividual, fitness=creator.FitnessMin)
    
    # Assign the initialisation operator to the toolbox's individual
    # And describe the population initialisation  
    toolbox.register("individual", initIndividual, creator.Individual,
                     size = IND_SIZE, nb_vehicle = num_route)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Generate a the problem's data set
    # i.e: Generate N "route" of appointement 
    list_appointments = model.generate_route(num_route, 
                                             num_node_per_route,
                                             w,
                                             h,
                                             depot)
    # Set the routes color  
    color = visualisation.color_group(num_route)
    
    # Set the different genetic oprator inside the toolbox
    toolbox.register("clone", copy.deepcopy)
    toolbox.register("mate", cxRC)
    toolbox.register("mutate", constrainedSwap, data=list_appointments)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate, data=list_appointments, depot=depot)
    
    # Create the global population
    # And an elite one  

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(elite_size)
    
    # Create a statistic module to display stats at each generation 
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    
    # The genetic alogorithm in itself 
    algorithms.eaSimple(pop, 
                        toolbox,
                        crossover_probability,
                        mutation_probability,
                        ngen,
                        stats=stats, 
                        halloffame=hof)

    # Create display of the problem and of the best solution  
    root = visualisation.Tk()
    root.geometry("" + str(w) + "x" + str(h))
    app = visualisation.Example(root, 
                                list_appointments,
                                color, 
                                depot,
                                visualisation.indexes_to_appointement(hof[0], list_appointments))
    
    # Start the GUI main loop
    root.mainloop()  

if __name__ == '__main__':
    main()  
