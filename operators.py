# -*- coding:utf-8 -*-
"""
This file contains operators to use in the genetic algorithm.
"""
import random
import model
#import genome
import copy
#import itertools


def init(ind_class, size, nb_vehicle):
    """
    Initialisation operator.
    Fill the individual's first part with a random permutation of
    appointment and compute the second part with a valid vehicle count.
    """
    remaining_size = size
    second_part = []
    first_part = []

    # Create the second part of the individual
    # Choose random value while checking the upper bound
    for i in range(0, nb_vehicle):
        vehicle_capacity = random.randrange(1, (size / nb_vehicle) * 2)
        vehicle_capacity %= remaining_size
        remaining_size -= vehicle_capacity
        second_part.append(model.Vehicle(i, vehicle_capacity))

    # If there is still unassigned vehicles at the end
    # Assigns them to the last vehicle
    if remaining_size > 0:
        second_part[-1].add_to_count(remaining_size)

    # Create the first part of the chromosome
    # Just a random permutation of indexes
    first_part = range(0, size)
    random.shuffle(first_part)

    # Create the individual and return it
    ind = ind_class((first_part, second_part))
    return ind


def evaluate(individual, data, depot, size):
    """
    Evaluate the genome.
    """
    splitted_route = []
    idx = 0
    capacity_per_vehicle = 5
    distance = 0
    load = 0
    malus = {}
    malus['conflict'] = 1000
    malus['missing_appointment'] = 1000
    list_appointment = data["appointment"]
    # Split the first part of the individual as a list of route
    # using the second part

    for vehicle in individual.vehicles:
        splitted_route.append(individual.routes[idx:vehicle.count()])
        idx += vehicle.count()

    # For each vehicle (route)
    # Compute the distance travelled and the load
    for route in splitted_route:
        if len(route) > 0:
            distance += model.euclidian_distance(
                depot,
                list_appointment[route[0]])

            for gene1, gene2 in zip(route[:-1], route[1:]):
                distance += model.euclidian_distance(
                    list_appointment[gene1],
                    list_appointment[gene2])

            for gene1, gene2 in zip(route[:-1], route[1:]):
                load += 1

            load -= capacity_per_vehicle

    # Set the different feasability malus
    tmp = (size - sum([v.count() for v in individual.vehicles])) * \
        malus['missing_appointment']

    distance += tmp
    distance += individual.is_time_constraint_respected(data) * \
        malus['conflict']

    #load += tmp

    # Return a tuple of fitness: the cost and the load
    return distance, load


def window_bounds_checking(app1, app2):
    """
    Checks whether app2 is contained within app1.
    This function is used during insertion, and is therefore
    solely called in order to check whether inserting app1
    before app2 is possible.
    """

    # Checking whether app1 is before app2 (which is a constraint in this
    # case.
    if app1.window_start > app2.window_start:
        return False

    if app1.window_end > app2.window_end:
        return False
    return True


def insert_appointment1d(app_list, app, data):
    """
    Appointment inserting function. Inserts an appointment in a 1d
    appointment list.
    """
    list_appointment = data["appointment"]
    # Vehicle number
    for idx in range(0, len(app_list)):
        if list_appointment[app_list[idx]].window_start > \
                list_appointment[app].window_start:
            if window_bounds_checking(
                    list_appointment[app],
                    list_appointment[app_list[idx]]):
                app_list.insert(idx, app)
                return app_list

        if idx == (len(app_list)-1):
            if window_bounds_checking(
                    list_appointment[app_list[idx]],
                    list_appointment[app]):
                app_list.append(app)
                return app_list

    return app_list


def insert_appointment2d(app_list, app, data):
    """
    Appointment inserting function. Inserts an appointment in a 2D
    appointment list.
    """
    tmp = len(app_list)
    list_appointment = data["appointment"]

    # Vehicle index
    num_v = random.randrange(0, tmp)

    # Number of vehicles we tried to insert this element into
    tested_values = [num_v]

    idx = 0
    while idx < len(app_list[num_v]):#for idx in range(0, len(app_list[num_v])):
        # Sorting using data_element.window_start
        if list_appointment[app_list[num_v][idx]].window_start > \
                list_appointment[app].window_start:
            # Checking if the bounds are valid
            if window_bounds_checking(
                    list_appointment[app],
                    list_appointment[app_list[num_v][idx]]):
                app_list[num_v].insert(idx, app)
                return app_list
            # Bounds are invalid, let's try something else
            else:
                # Trying with another vehicle!
                idx = 0
                new_num_v = choosing_a_new_index(num_v, tested_values, tmp)

                if num_v == new_num_v:
                    return app_list
                tested_values.append(idx)
                num_v = new_num_v

        if idx == (len(app_list[num_v])-1):
            if window_bounds_checking(
                    list_appointment[app_list[num_v][idx]],
                    list_appointment[app]):
                app_list[num_v].append(app)
                return app_list
            else:
                idx = 0
                new_num_v = choosing_a_new_index(num_v, tested_values, tmp)

                if num_v == new_num_v:
                    return app_list
                tested_values.append(idx)
                num_v = new_num_v

        else:
            idx += 1

    return app_list


def choosing_a_new_index(num_v, tested_values, length):
    """
    If there're still vehicles the function hasn't tried
    inserting our element into, the function gets a new id to
    give it a try.
    If it's not the case, the function just returns the current id.
    """
    new_num_v = num_v
    while new_num_v in tested_values and length > len(tested_values):
        new_num_v = random.randrange(0, length)

    return new_num_v


def appointment_removal(parent, list_to_remove):
    """
    Removes the appointment in list_to_remove from parent.
    """
    for element in list_to_remove:
        for index in range(0, len(parent)):
            parent[index] = \
                [item for item in parent[index]
                    if item != element]
    return parent


def cx_rc(parent1, parent2, data):
    """
    Custom RC (or BCRC) crossover as describe in the article[1]

    [1]:
    """

    child1 = copy.deepcopy(parent1)

    child1.routes = []
    child1.vehicles = []

    # Can't compute offspring in this case
    if len(parent1.routes) != len(parent2.routes):
        return copy.deepcopy(parent1)

    appointments_by_vehicle1 = parent1.split()
    appointments_by_vehicle2 = parent2.split()

    # Picking and removing appointments associated to a vehicle in the second
    # parent from the first parent.
    tmp_select = random.randrange(0, len(parent1.vehicles))

    appointments_by_vehicle1 = appointment_removal(
        appointments_by_vehicle1,
        appointments_by_vehicle2[tmp_select])

    # Inserting back those elements in the list corresponding to the first
    # parent.
    for element in appointments_by_vehicle2[tmp_select]:
        appointments_by_vehicle1 = insert_appointment2d(
            appointments_by_vehicle1,
            element,
            data
        )

    # Making new vehicles containing the right number of appointments for the
    # offspring.

    child1.encode(appointments_by_vehicle1)

    # Yay! Offspring!
    return child1


def crossover(parent1, parent2, data):
    """
    Uses cx_rc to get children from parent1 and parent2.
    """
    child1 = cx_rc(parent1, parent2, data)
    child2 = cx_rc(parent2, parent1, data)

    return child1, child2


def constrained_swap(ind, data):
    """
    A random swap following constraints.
    Need pretty heavy refactoring
    """
    list_appointment = data["appointment"]
    splitted_route = []
    idx = 0

    # Splits the first part of the individual as a list of routes
    # using the second part
    for vehicle in ind.vehicles:
        splitted_route.append(ind.routes[idx:vehicle.count()])
        idx += vehicle.count()

    # Randomly choose a non-empty route
    while True:
        rand_route = random.randrange(0, len(splitted_route))
        if len(splitted_route[rand_route]) > 0:
            break
        # Nothing to do here
        if len(splitted_route) == 1:
            return ind,

    # Choose a random appointement in the selected route
    rand_appointement = random.randrange(0, len(splitted_route[rand_route]))

    # Now we insert this appointement into a ramdomly selected route if
    # we can find a place where it respect constraints. If not, we do nothing
    shuffled_route = range(0, len(splitted_route))
    random.shuffle(shuffled_route)

    for i in shuffled_route:
        if i != rand_route:
            counter = 0
            for appointement_idx in splitted_route[i]:

                # If the next element in the list start after the one we want
                # to insert, we place it here, and delete it from where we took
                # it
                if list_appointment[appointement_idx].starting_time > \
                        list_appointment[rand_appointement]:
                    splitted_route[i].insert(counter, rand_appointement)
                    del splitted_route[rand_route][rand_appointement]
                    return ind,

                # If the last appointement is starting before the one we want
                # to insert, we insert it at the end of of the route,
                # and delete it from where we took it
                elif counter == len(splitted_route[i]) - 1:
                    if list_appointment[appointement_idx].starting_time < \
                            list_appointment[rand_appointement]:
                        list_appointment.append(rand_appointement)
                        del splitted_route[rand_route][rand_appointement]
                        return ind,

    return ind,
