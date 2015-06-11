#-*- coding:utf8 -*-
import copy
import random

class Appointment():
    def __init__(self, idAppointment, starting_time):
        self.idAppointment = idAppointment
        self.starting_time = starting_time

    def __repr__(self):
        return "<%d, %d>" % self._asPrintable()

    def _asPrintable(self):
        return (self.idAppointment, self.starting_time)

    def _idAppointment(self):
        return self.idAppointment

    def _starting_time(self):
        return self.starting_time



class Vehicle():
    def __init__(self, idVehicle, nbAppointment):
        self.idVehicle = idVehicle
        self.nbAppointment = nbAppointment

    def _idVehicle(self):
        return self.idVehicle

    def _nbAppointment(self):
        return self.nbAppointment

    def _asPrintable(self):
        return (self.idVehicle, self.nbAppointment)

    def __repr__(self):
        return "<%d %d>" % self._asPrintable()



class MvrpIndividual():
    def __init__(self, routes, vehicles):
        sumVehicles = 0
        for i in range(0, len(vehicles)):
            sumVehicles += vehicles[i]._nbAppointment()

        if (len(routes) == sumVehicles):
            self.routes = list(routes)
            self.vehicles = list(vehicles)

    def _routes(self):
        return self.routes

    def _vehicles(self):
        return self.vehicles



def insertAppointment(app, appointment2D):

    tmp = len(appointment2D)
    no_vehicle = random.randrange(0, tmp)
    for idx in range(0, len(appointment2D[no_vehicle])):
        if (appointment2D[no_vehicle][idx]._starting_time() > app._starting_time()):
            appointment2D[no_vehicle].insert(idx, copy.deepcopy(app))
            return appointment2D

    appointment2D[no_vehicle].append(app)
    return appointment2D

def crossOver(parent1, parent2):

    random.seed(666)

    # Can't compute offspring in this case
    if (len(parent1._routes()) != len(parent2._routes())):
        return copy.deepcopy(parent1)

    appointmentsByVehicle1 = []
    appointmentsByVehicle2 = []

    tmpLen = len(parent1.vehicles)

    offset1 = 0
    offset2 = 0

    # Getting lists of lists containing all the appointments sorted by vehicle
    for i in range(0, tmpLen):

        newOffset1 = offset1 + parent1._vehicles()[i]._nbAppointment()
        newOffset2 = offset2 + parent2._vehicles()[i]._nbAppointment()

        appointmentsByVehicle1.append(
                copy.deepcopy(parent1._routes()[offset1:newOffset1])
                )

        appointmentsByVehicle2.append(
                parent2._routes()[offset2:newOffset2]
                )

        offset1 = newOffset1
        offset2 = newOffset2

    print("Before: ")
    print(appointmentsByVehicle1)
    print(appointmentsByVehicle2)

    # Picking and removing appointments associated to a vehicle in the second
    # parent from the first parent.
    tmpSelect = random.randrange(0, tmpLen)

    for element in appointmentsByVehicle2[tmpSelect]:
        for index in range(0, tmpLen):
            appointmentsByVehicle1[index] = \
                    [item for item in appointmentsByVehicle1[index] \
                    if item.idAppointment != element.idAppointment]

    # Inserting back those elements in the list corresponding to the first
    # parent.
    for element in appointmentsByVehicle2[tmpSelect]:
        appointmentsByVehicle1 = insertAppointment(
                element,
                appointmentsByVehicle1
                )

    print("After: ")
    print(appointmentsByVehicle1)

    # Making new vehicles containing the right number of appointments for the
    # offspring.
    vehicleList = []

    for index in range(0, tmpLen):
        vehicleList.append(
                Vehicle(
                    parent1._vehicles()[index]._idVehicle(),
                    len(appointmentsByVehicle1[index])
                    )
                )

        # Flattening the 2D list to create the offspring.
    appointments = [i for subList in appointmentsByVehicle1 for i in subList]

    # Yay! Offspring!
    return MvrpIndividual(appointments, vehicleList)

ap1 = Appointment(1, 1)
ap2 = Appointment(2, 2)
ap3 = Appointment(3, 3)
ap4 = Appointment(4, 4)
ap5 = Appointment(5, 5)
ap6 = Appointment(6, 6)

vehicle1 = Vehicle(1, 2)
vehicle2 = Vehicle(2, 3)
vehicle3 = Vehicle(3, 1)
vehicle4 = Vehicle(4, 1)
vehicle5 = Vehicle(5, 4)
vehicle6 = Vehicle(6, 1)

parent1 = MvrpIndividual(
        [ap1, ap2, ap3, ap4, ap5, ap6],
        [vehicle1, vehicle2, vehicle3])
parent2 = MvrpIndividual(
        [ap6, ap3, ap5, ap2, ap4, ap1],
        [vehicle4, vehicle5, vehicle6])

result = crossOver(parent1, parent2)

print("\n")
print(parent1._routes())
print(parent1._vehicles())
print("\n")
print(parent2._routes())
print(parent2._vehicles())
print("\n")
print(result._routes())
print(result._vehicles())
