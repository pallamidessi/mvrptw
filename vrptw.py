# -*- coding:utf-8 -*-
import argparse
import random
import numpy
import visualisation
import model
import genome
import operators
import copy
import load_data

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


def main():

    # Parsing arguments
    parser = argparse.ArgumentParser(description='Calculates optimal journeys')
    parser.add_argument('-s', '--size', metavar='pop_size', type=int, nargs=1,
            help='the population size for the GA', default=1000)
    parser.add_argument('-ve', '--vehicle', metavar='num_route', type=int, nargs=1,
            help='the number of vehicles to use', default=100)
    parser.add_argument('-d', '--depot', metavar='depot', type=int, nargs=2,
            help='the coordinates of the starting point', default=[75, 75])
    parser.add_argument('-no', '--node', metavar='num_node', type=int, nargs=1,
            help='the number of nodes associated with each vehicle', default=4)
    parser.add_argument('-m', '--mutation', metavar='mutation_probability', type=int, nargs=1,
            help='the probability of mutation for each individual', default=0.3)
    parser.add_argument('-g', '--generation', metavar='ngen', type=int, nargs=1,
            help='the number of generations', default=10)
    parser.add_argument('-c', '--crossover', metavar='crossover_probability', type=int, nargs=1,
            help='the probability of crossover for two individuals', default=0.7)
    parser.add_argument('-e', '--elite', metavar='elite_size', type=int, nargs=1,
            help='the elite size for the GA', default=1)
    args = parser.parse_args()
    
    random.seed(666)

    # Problem's definition  
    depot = model.Point(args.depot[0], args.depot[1])
    w = 300
    h = 300
    num_route = args.vehicle
    num_node_per_route = args.node
    IND_SIZE = num_route * num_node_per_route

    # Genetic parameter
    pop_size = args.size
    elite_size = args.elite
    crossover_probability = args.crossover
    mutation_probability = args.mutation
    ngen = args.generation
    mu = pop_size
    _lambda = pop_size
    
    # Generate a the problem's data set
    # i.e: Generate N "route" of appointement
    list_appointment = model.generate_route(num_route, 
                                             num_node_per_route,
                                             w,
                                             h,
                                             depot)
    # Set the routes color  
    color = visualisation.color_group(num_route)

    list_appointment = load_data.load_dataset('C1_4_8.TXT')

    # Assign the custom individual class to the toolbox
    # And set the number of wanted fitnesses 
    toolbox = base.Toolbox()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", genome.MvrpIndividual, fitness=creator.FitnessMulti)

    # Assign the initialisation operator to the toolbox's individual
    # And describe the population initialisation  
    toolbox.register("individual", operators.init, creator.Individual,
                     size = IND_SIZE, nb_vehicle = num_route, data = list_appointment)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Set the different genetic oprator inside the toolbox
    toolbox.register("clone", copy.deepcopy)
    toolbox.register("mate", operators.crossover, data=list_appointment)
    toolbox.register("mutate", operators.constrainedSwap, data=list_appointment)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", operators.evaluate, data=list_appointment, depot=depot, size=IND_SIZE)

    # Create the global population
    # And an elite one  

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(elite_size)

    # Create a statistic module to display stats at each generation 
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)


    # The genetic alogorithm in itself 
    algorithms.eaMuPlusLambda(pop, 
            toolbox,
            mu,
            _lambda,
            crossover_probability,
            mutation_probability,
            ngen,
            stats=stats, 
            halloffame=hof)
    
    # Create display of the problem and of the best solution  
    gui = visualisation.createGUI()

    # Start the GUI main loop
    gui.mainloop()  

if __name__ == '__main__':
    main()  
