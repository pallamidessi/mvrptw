import random
import numpy
import visualisation
import model

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


def evaluate(individual, data, depot):
    distance = model.euclidian_distance(depot, data[individual[0]])
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += model.euclidian_distance(data[gene1], data[gene2])
    return distance,


def main():
    random.seed(666)
    depot = model.Point(500, 500)
    w = 1000
    h = 1000
    num_route = 2
    num_node_per_route = 5

    toolbox = base.Toolbox()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    IND_SIZE = num_route * num_node_per_route

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    list_appointments = model.generate_route(num_route, 
                                             num_node_per_route,
                                             w,
                                             h,
                                             depot)
    color = visualisation.color_group(num_route)

    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=5)
    toolbox.register("evaluate", evaluate, data=list_appointments, depot=depot)

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 50, stats=stats, 
                    halloffame=hof)

    root = Tk()
    root.geometry("100x100+300+300")
    app = Example(root, 
                  list_appointments,
                  color, 
                  depot,
                  visualisation.indexes_to_appointement(hof[0], list_appointments))

    root.mainloop()  

if __name__ == '__main__':
    main()  
