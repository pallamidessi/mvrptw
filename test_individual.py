#-*- coding:utf8 -*-
import copy
import random
import genome
import model

list_order = []

random.seed(666)

for i in range(0, 12):
    list_order.append([])
    for j in range(0, 2):
        list_order[i].append(random.randrange(1, 6))
    list_order[i].append(10-sum(list_order[i]))

list_appointments = model.generate_route(12,
        10,
        1000,
        1000,
        model.Point(500, 500))

list_individuals = []
# print("Dataset:\n")
for i in range(0, 12):
    # print("Appointments: ")
    # print(list_appointments)
    offset = 0
    list_routes = []
    vehicle_list = list_order[i]
    for vehicleCount in vehicle_list:
        for j in range(offset, offset+vehicleCount):
            list_routes.append(j)
            offset += vehicleCount

    list_individuals.append(
            genome.MvrpIndividual(
                [list_routes,
                    list_order[i]]
                )
            )
    print(str(list_individuals[i].decode(list_appointments)) + " " + str(list_individuals[i].is_time_constraint_respected(list_appointments)))
    #print("Time respected: ")
    #print(list_individuals[i].is_time_constraint_respected(list_appointments))
    #print("Load respected: ")
    #print(list_individuals[i].is_load_respected())
    #print(list_individuals[i].decode(list_appointments))

random_data = [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10, 12, 11]]
test_value = genome.MvrpIndividual([0, 1])
test_value.encode(random_data)
print(random_data)
print(test_value)
