#-*- coding:utf8 -*-
"""
This code contains tests for the functions of the class representing
an individual.
"""

#import copy
import random
import genome
import model

LIST_ORDER = []

random.seed(666)

for i in range(0, 12):
    LIST_ORDER.append([])
    for j in range(0, 2):
        LIST_ORDER[i].append(random.randrange(1, 6))
    LIST_ORDER[i].append(10-sum(LIST_ORDER[i]))

LIST_APPOINTMENTS = model.generate_route(12,
        10,
        1000,
        1000,
        model.Point(500, 500))

LIST_INDIVIDUALS = []
# print("Dataset:\n")
for i in range(0, 12):
    # print("Appointments: ")
    # print(LIST_APPOINTMENTS)
    offset = 0
    list_routes = []
    vehicle_list = LIST_ORDER[i]
    for vehicleCount in vehicle_list:
        for j in range(offset, offset+vehicleCount):
            list_routes.append(j)
            offset += vehicleCount

    LIST_INDIVIDUALS.append(
            genome.MvrpIndividual(
                [list_routes,
                    LIST_ORDER[i]]
                )
            )
    print str(LIST_INDIVIDUALS[i].decode(LIST_APPOINTMENTS)) + " " + \
            str(LIST_INDIVIDUALS[i].is_time_constraint_respected(
                LIST_APPOINTMENTS))
    #print("Time respected: ")
    #print(LIST_INDIVIDUALS[i].is_time_constraint_respected(LIST_APPOINTMENTS))
    #print("Load respected: ")
    #print(LIST_INDIVIDUALS[i].is_load_respected())
    #print(LIST_INDIVIDUALS[i].decode(LIST_APPOINTMENTS))

RANDOM_DATA = [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10, 12, 11]]
TEST_VALUE = genome.MvrpIndividual([0, 1])
TEST_VALUE.encode(RANDOM_DATA)
print RANDOM_DATA
print TEST_VALUE
