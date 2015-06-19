# -*- coding:utf-8 -*-
"""
Main file of the project.
"""
#pylint: disable=E1101
import argparse
import random
import numpy
import visualisation
import model
import genome
import operators
import copy
#import algorithms
import load_data

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


def init_toolbox(ind_size, vehicle_list, data_dict, depot):
    """
    Initializes the toolbox used for the genetic algorithm.
    """
    # Assign the custom individual class to the toolbox
    # And set the number of wanted fitnesses
    toolbox = base.Toolbox()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
    creator.create(
        "Individual",
        genome.MvrpIndividual,
        fitness=creator.FitnessMulti)

    # Assign the initialisation operator to the toolbox's individual
    # And describe the population initialisation
    toolbox.register(
        "individual", operators.init, creator.Individual,
        size=ind_size, vehicles=vehicle_list)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Set the different genetic oprator inside the toolbox
    toolbox.register("clone", copy.deepcopy)
    toolbox.register("mate", operators.crossover, data=data_dict)
    toolbox.register("mutate", operators.constrained_swap, data=data_dict)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register(
        "evaluate", operators.evaluate, data=data_dict,
        depot=depot, size=ind_size)

    return toolbox


def init_parser():
    """
    Initializes the parsing of the arguments passed to the function.
    """
    # Parsing arguments
    parser = argparse.ArgumentParser(description='Calculates optimal journeys')
    parser.add_argument(
        '-s', '--size', metavar='pop_size', type=int,
        help='the population size for the GA', default=1000)
    parser.add_argument(
        '-ve', '--vehicle', metavar='num_route', type=int,
        help='the number of vehicles to use', default=100)
    parser.add_argument(
        '-d', '--depot', metavar='depot', type=int, nargs=2,
        help='the coordinates of the starting point', default=[75, 75])
    parser.add_argument(
        '-no', '--node', metavar='num_node', type=int,
        help='the number of nodes associated with each vehicle', default=4)
    parser.add_argument(
        '-m', '--mutation', metavar='mutation_probability',
        type=int, help='the probability of mutation for each individual',
        default=0.3)
    parser.add_argument(
        '-g', '--generation', metavar='ngen', type=int,
        help='the number of generations', default=10)
    parser.add_argument(
        '-c', '--crossover', metavar='crossover_probability',
        type=int, help='the probability of crossover for two individuals',
        default=0.7)
    parser.add_argument(
        '-e', '--elite', metavar='elite_size', type=int,
        help='the elite size for the GA', default=1)
    parser.add_argument(
        '-p', '--path', metavar='dataset_path', type=str,
        help='the path of the dataset to use',
        default='400_customers/S-C1-400/C1_4_8.TXT')
    parser.add_argument(
        '-z', '--zoom', metavar='zoom', type=int,
        help='the zooming factor for visualisation', default=3)
    return parser


def main():
    """
    Main function of the project.
    """
    args = init_parser().parse_args()

    random.seed(490)

    dict_info = {}

    proto_dict = load_data.load_protobuf("protobuf_data/set1")

    # Problem's definition
    dict_info['depot'] = model.Point(args.depot[0], args.depot[1])
    width, height = 1300, 700
    ind_size = args.vehicle * args.node
    dict_info['zoom'] = args.zoom

    # Genetic parameter
    crossover_probability = args.crossover
    mutation_probability = args.mutation
    ngen = args.generation
    _mu = args.size
    _lambda = args.size

    # Generate a the problem's data set
    # i.e: Generate N "route" of appointement
    #list_appointment = model.generate_route(num_route,
    #        num_node_per_route,
    #        width,
    #        height,
    #        dict_info['depot'])

    dict_info['data'] = load_data.load_dataset(args.path)
    # Set the routes color
    dict_info['color'] = visualisation.color_group(args.vehicle)

    # Adjusting values based on the dataset size
    ind_size = len(dict_info['data']['appointment'])

    dict_info['zoomx'] = 1250 / max([
        dict_info['data']['xrange'][1], dict_info['depot'].get_x()])
    dict_info['zoomy'] = 702 / max([
        dict_info['data']['yrange'][1], dict_info['depot'].get_y()])

    if args.vehicle > ind_size:
        args.vehicle = ind_size / 2 + 1

    toolbox = init_toolbox(
        ind_size,
        proto_dict['vehicle'],
        dict_info['data'],
        dict_info['depot'])

    # Create the global population
    # And an elite one

    pop = toolbox.population(n=args.size)
    hof = tools.HallOfFame(args.elite)

    # Create a statistic module to display stats at each generation
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    root = visualisation.Tk()
    root.geometry(str(width) + "x" + str(height))

    # The genetic algorithm in itself
    algorithms.eaMuPlusLambda(
        pop,
        toolbox,
        _mu,
        _lambda,
        crossover_probability,
        mutation_probability,
        ngen,
        stats=stats,
        halloffame=hof)

    print hof[0]

    dict_info['tour'] = visualisation.individual_as_appointment(
        hof[0],
        dict_info['data']['appointment']
        )

    # Create display of the problem and of the best solution
    visualisation.Example(root, dict_info)

    # Start the GUI main loop
    root.mainloop()

if __name__ == '__main__':
    main()
