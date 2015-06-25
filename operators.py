# -*- coding:utf-8 -*-
"""
This file contains operators to use in the genetic algorithm.
"""
import random
import model
import copy


def init(ind_class, size, vehicles):
    """
    Initialisation operator.
    Fill the individual's first part with a random permutation of
    appointments and computes the second part with a valid vehicle
    count.
    """
    second_part = vehicles
    first_part = []

    distributed_appointments = 0

    tmp_len = len(vehicles)
    iteration_stop = 5 * tmp_len
    nb_iterations = 0

    while distributed_appointments < size and nb_iterations < iteration_stop:
        nb_iterations += 1
        index = random.randrange(0, tmp_len)
        tmp_count = vehicles[index].count()
        tmp_capacity = vehicles[index].capacity()
        if tmp_count < tmp_capacity:
            addition = random.randrange(1, tmp_capacity - tmp_count + 1)
            vehicles[index].add_to_count(addition)
            distributed_appointments += addition

    if distributed_appointments < size:
        for vehicle in vehicles:
            if vehicle.capacity() > vehicle.count():
                addition = min([vehicle.capacity() - vehicle.count(),
                                size - distributed_appointments])
                vehicle.add_to_count(addition)
                distributed_appointments += addition
                if distributed_appointments == size:
                    break

    # Create the second part of the individual
    # Chooses random values while checking the upper bound
    first_part = range(0, size)
    random.shuffle(first_part)

    ind = ind_class((first_part, second_part))
    return ind

#def init(ind_class, size, nb_vehicle):
#    """
#    Initialisation operator.
#    Fill the individual's first part with a random permutation of
#    appointment and compute the second part with a valid vehicle count.
#    """
#    remaining_size = size
#    second_part = []
#    first_part = []
#
#    # Create the second part of the individual
#    # Choose random value while checking the upper bound
#    for i in range(0, nb_vehicle):
#        vehicle_capacity = random.randrange(1, (size / nb_vehicle) * 2)
#        vehicle_capacity %= remaining_size
#        remaining_size -= vehicle_capacity
#        second_part.append(model.Vehicle(i, vehicle_capacity))
#
#    # If there is still unassigned vehicles at the end
#    # Assigns them to the last vehicle
#    if remaining_size > 0:
#        second_part[-1].add_to_count(remaining_size)
#
#    # Create the first part of the chromosome
#    # Just a random permutation of indexes
#    first_part = range(0, size)
#    random.shuffle(first_part)
#
#    # Create the individual and return it
#    ind = ind_class((first_part, second_part))
#    return ind


def evaluate(individual, data, depot, size):
    """
    Evaluate the genome.
    """
    idx = 0
    distance = 0
    load = 0
    malus = {}
    malus['conflict'] = 1000
    malus['missing_appointment'] = 1000
    malus['non_respected_load'] = 2000

    # Split the individual as a list of routes
    splitted_route = individual.split()

    # For each vehicle (route)
    # Compute the distance travelled and the load
    for route in splitted_route:
        if len(route) > 0:
            distance += model.euclidean_distance(
                depot,
                data['appointment'][route[0]])

            for gene1, gene2 in zip(route[:-1], route[1:]):
                distance += model.euclidean_distance(
                    data['appointment'][gene1],
                    data['appointment'][gene2])

            for gene1, gene2 in zip(route[:-1], route[1:]):
                load += 1

            current_vehicle = individual.vehicles[idx]

            if current_vehicle.count() > current_vehicle.capacity():
                load += malus['non_respected_load']
                distance += malus['non_respected_load']

            load -= current_vehicle.capacity()
        idx += 1

    # Set the different feasability malus.
    # Reusing "idx" so as not to have too many variables.
    idx = (size - sum([v.count() for v in individual.vehicles])) * \
        malus['missing_appointment']

    distance += idx
    distance += individual.is_time_constraint_respected(data) * \
        malus['conflict']

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
    if app1.window_start() > app2.window_start():
        return False

    if app1.window_end() > app2.window_end():
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
        if list_appointment[app_list[idx]].window_start() > \
                list_appointment[app].window_start():
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
    while idx < len(app_list[num_v]):
        # Sorting using data_element.window_start()
        if list_appointment[app_list[num_v][idx]].window_start() > \
                list_appointment[app].window_start():
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

    child1.encode(appointments_by_vehicle1, parent1)

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
    """
    return constrained_journey_swap(ind, data)

def constrained_journey_swap(ind, data):
    """
    A random journey swap following constraints.
    """
    list_appointment = data["appointment"]

    # Splits the first part of the individual as a list of routes
    # using the second part
    splitted_route = ind.split()

    print "Before: "
    print splitted_route
    # Randomly choose a non-empty route
    while True:
        rand_route = random.randrange(0, len(splitted_route))
        if len(splitted_route[rand_route]) > 0:
            break
        # Nothing to do here
        if len(splitted_route) == 1:
            return ind,

    # Choose a random appointment in the selected route
    rand_appointment = random.randrange(0, len(splitted_route[rand_route]))

    appointment_to_move = list_appointment[
        splitted_route[rand_route][rand_appointment]]
    journey = data['journey'][appointment_to_move.id_journey()]
    
    rand_appointment = []

    # Fetching the elements corresponding to the affected journey
    for index in range(0, len(splitted_route[rand_route])):

        element = list_appointment[splitted_route[rand_route][index]]

        if element.id_appointment() in journey.id_planned_elements() and \
        appointment_to_move.id_journey() == element.id_journey():
            rand_appointment.append(index)

    # Now we insert this appointment into a ramdomly selected route if
    # we can find a place where it respect constraints. If not, we do nothing
    shuffled_route = range(0, len(splitted_route))
    random.shuffle(shuffled_route)

    for i in shuffled_route:

        tmp_route = splitted_route[i][:]
        tmp_len = len(tmp_route)

        for app in rand_appointment:
            insert_appointment1d(tmp_route,
                                 splitted_route[rand_route][app],
                                 data
                                )
        if len(tmp_route) == tmp_len + len(rand_appointment):
            
            splitted_route[i] = tmp_route[:]

            for app in sorted(rand_appointment, reverse=True):
                del splitted_route[rand_route][app]

            print "After:"
            print splitted_route
            ind.encode(splitted_route, ind)
            return ind,
        
    return ind,
