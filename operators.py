# -*- coding:utf-8 -*-
import random
import model


def init(ind_class, size, nb_vehicle, data):
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
        vehicle_capacity %= remaining_size
        remaining_size -= vehicle_capacity
        second_part.append(vehicle_capacity)
    
    # If there is still unassignated vehicles at the end
    # Assigned them to the last vehicle
    if remaining_size > 0:
        second_part[-1] += remaining_size
    
    # Create the first part of the chromosome 
    # Just a random permutation of indexes
    first_part = range(0, size)
    random.shuffle(first_part)
    
    
    for appointement_idx in first_part:
        route = []
        for vehicle_size in second_part:
            for i in range(0, vehicle_size):
                insert_appointment(route, appointement_idx, data)
    
    # Create the individual and return it
    ind = ind_class((first_part, second_part))
    return ind

def insert_appointment(route, appointement_idx, list_appointment):
    appointement_to_insert = list_appointment[appointement_idx]
    it = 0 
    if len(route) == 0:
        route.append(appointement_idx)
    elif len(route) > 1:
        for idx in route:
            if list_appointment[idx].starting_time > appointement_to_insert.starting_time:
                route.insert(it, appointement_idx)
                return
            if it == len(route) and list_appointment[idx].starting_time < appointement_to_insert.starting_time:
                route.append(appointement_idx)
                return
        it +=1
        



    



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
    list_appointment = data
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
                if list_appointment[appointement_idx].starting_time > list_appointment[rand_appointement]:
                        splitted_route[i].insert(ii, rand_appointement)
                        del splitted_route[rand_route][rand_appointement]
                        return ind,
                
                # If the last appointement is starting before the one we want to insert,
                # We insert it at the end of of the route, and delete it from where we took it   
                elif ii == len(splitted_route[i]) - 1:
                    if list_appointment[appointement_idx].starting_time < list_appointment[rand_appointement]:
                        list_appointment.append(rand_appontement)
                        del splitted_route[rand_route][rand_appointement]
                        return ind,

    return ind,

