# -*- coding:utf-8 -*-

"""
This file contains the description of the class individual.
"""

import itertools
from operators import window_bounds_checking
import model
import copy
import json

class MvrpIndividual(object):
    """
    Genome definition. The genome is implemented a two-part chromosome
    described in the [insert link here] article[1].

    routes : A list of integer, referencing appointment by their indexes

    vehicles : A list of integer, where each values represent a vehicle and how
    many appointments it contained starting from the head of the list.

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
        self.loads = []

    def __repr__(self):
        return ("<Individual routes %s vehicle %s> \n" %
                (self.routes, self.vehicles))

    def split(self):
        """
        Split the first part of the individual as a list of route using the
        second part
        """
        splitted_route = []
        idx = 0

        for vehicle in self.vehicles:
            splitted_route.append(self.routes[idx:vehicle.count() + idx])
            idx += vehicle.count()

        return splitted_route

    def is_time_constraint_respected(self, data):
        """
        Checks how many time constraints are violated by the individual.
        """
        tmp = self.decode(data)
        result = 0
        for sublist in tmp:
            if len(sublist) != 0:
                current = sublist[0]
                test = current.duration() > \
                    (current.window_end() - current.window_start())
                for i in range(1, len(sublist)):
                    if not window_bounds_checking(current, sublist[i]) or test:
                        result += 1
                    current = sublist[i]
        return result

    def is_load_respected(self, data):
        """
        Simple operation to check whether the individual respects the load
        constraint.
        """
        self.compute_loads(data)
        #print '=====================VEHICLE==================='
        #print self.split()
        #print '==============================================='
        #print '======================LOADS===================='
        #print self.loads
        #print '==============================================='
        violated = 0
        for idx in range(0, len(self.loads)):
            for elem in self.loads[idx]:
                if elem > self.vehicles[idx].capacity():
                    violated += 1
        return violated

    def compute_loads(self, data):
        """
        Compute the load at each appointment for each vehicle.
        """
        list_appointment = data['appointment']
        self.loads = []
        splitted_routes = self.split()
        for vehicle in splitted_routes:
            current_load = 0
            tmp_route = []
            for element in vehicle:

                if list_appointment[element].get_type() == \
                   model.RequiredElementTypes.Departure.value:
                    current_load += 1
                else:
                    current_load -= 1

                #if current_load < 0:
                #    print splitted_routes
                #    print vehicle
                tmp_route.append(current_load)
            self.loads.append(tmp_route)

    def vehicles_used(self):
        """
        Returns the vehicles used by the individual.
        """
        return len([v for v in self.vehicles if v.count() > 0])

    def decode(self, data):
        """
        Decodes the individual using a dictionary of data.
        """
        list_appointment = data["appointment"]
        tmp = self.split()
        to_return = []
        index = 0
        for sublist in tmp:
            to_return.append([])
            for element in sublist:
                to_return[index].append(list_appointment[element])
            index += 1
        return to_return

    def encode_from_vehicle(self, list_journeys, parent):
        """
        Encodes the individual using a list of journeys and the vehicles
        of parent.
        """
        self.vehicles = copy.deepcopy(parent.vehicles)
        self.routes = list(itertools.chain.from_iterable(list_journeys))

    def encode(self, list_appointment, parent):
        """
        Encodes the individual using a list of appointments
        """
        tmp_vehicles = []
        index = 0
        for vehicle in parent.vehicles:
            tmp_vehicles.append(copy.deepcopy(vehicle))
            tmp_vehicles[index].set_count(0)
            index += 1

        index = 0
        for sublist in list_appointment:
            tmp_vehicles[index].set_count(len(sublist))
            index += 1

        self.vehicles = tmp_vehicles
        self.routes = list(itertools.chain.from_iterable(list_appointment))

    def make_json(self, dict_info):
        """
        Transforms an individual into the json representing it.
        """
        list_appointment = dict_info['data']['appointment']
        to_return = []
        splitted_routes = self.split()

        for idx in range(0, len(splitted_routes)):
            current_vehicle = self.vehicles[idx].id_vehicle()
            for element in splitted_routes[idx]:
                new_dict = {}
                new_dict['id_vehicle'] = current_vehicle
                new_dict['id_journey'] = \
                    dict_info['data']['journey'] \
                    [list_appointment[element].id_journey()].id_journey()
                new_dict['id_planned_element'] = \
                    list_appointment[element].id_appointment()
                to_return.append(new_dict)

        return json.dumps(to_return, separators=(',',':'))
