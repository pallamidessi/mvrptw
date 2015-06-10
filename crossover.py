#-*- coding:utf8 -*-
import copy
import random

class Appointment():
    def __init__(self, idAppointment, timestamp):
        self.idAppointment = idAppointment;
        self.timestamp = timestamp;

    def __repr__(self):
        return "<%d, %d>" % self._asPrintable();

    def _asPrintable(self):
        return (self.idAppointment, self.timestamp);

    def _idAppointment(self):
        return self.idAppointment;

    def _timestamp(self):
        return self.timestamp;



class Vehicle():
    def __init__(self, idVehicle, nbAppointment):
        self.idVehicle = idVehicle;
        self.nbAppointment = nbAppointment;

    def _idVehicle(self):
        return self.idVehicle;

    def _nbAppointment(self):
        return self.nbAppointment;

    def _asPrintable(self):
        return (self.idVehicle, self.nbAppointment);

    def __repr__(self):
        return "<%d %d>" % self._asPrintable();



class Individual():
    def __init__(self, appointments, vehicles):
        sumVehicles = 0;
        for i in range(0, len(vehicles)):
            sumVehicles += vehicles[i]._nbAppointment();

        if (len(appointments) == sumVehicles):
            self.appointments = list(appointments);
            self.vehicles = list(vehicles);

    def _appointments(self):
        return self.appointments;

    def _vehicles(self):
        return self.vehicles;



def insertAppointment(app, appointment2D):

    tmp = len(appointment2D);
    for listIdx in range(0, tmp):
        for idx in range(0, len(appointment2D[listIdx])):
            if (appointment2D[listIdx][idx]._timestamp() > app._timestamp()):
                appointment2D[listIdx].insert(idx, copy.deepcopy(app));
                return appointment2D;

    appointment2D[tmp-1].append(copy.deepcopy(app));
    return appointment2D;

def crossOver(parent1, parent2):

    random.seed(666);

    # Can't compute offspring in this case
    if (len(parent1._appointments()) != len(parent2._appointments())):
        return copy.deepcopy(parent1);

    appointmentsByVehicle1 = [];
    appointmentsByVehicle2 = [];

    tmpLen = len(parent1.vehicles);
    
    offset1 = 0;
    offset2 = 0;
    
    # Getting lists of lists containing all the appointments sorted by vehicle
    for i in range(0, tmpLen):

        newOffset1 = offset1 + parent1._vehicles()[i]._nbAppointment();
        newOffset2 = offset2 + parent2._vehicles()[i]._nbAppointment();

        appointmentsByVehicle1.append(
                copy.deepcopy(parent1._appointments()[offset1:newOffset1])
                );

        appointmentsByVehicle2.append(
                copy.deepcopy(parent2._appointments()[offset2:newOffset2])
                );

        offset1 = newOffset1;
        offset2 = newOffset2;

    print("Before: ")
    print(appointmentsByVehicle1);

    # Picking and removing appointments associated to a vehicle in the second
    # parent from the first parent.
    tmpSelect = random.randrange(0, tmpLen);

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
                );
    
    print("After: ")
    print(appointmentsByVehicle1);

    # Making new vehicles containing the right number of appointments for the
    # offspring.
    vehicleList = [];

    for index in range(0, tmpLen):
        vehicleList.append(
                Vehicle(
                    parent1._vehicles()[index]._idVehicle(),
                    len(appointmentsByVehicle1[index])
                )
            );

    # Flattening the 2D list to create the offspring.
    appointments = [i for subList in appointmentsByVehicle1 for i in subList];
    
    # Yay! Offspring!
    return Individual(appointments, vehicleList);

ap1 = Appointment(1, 1);
ap2 = Appointment(2, 2);
ap3 = Appointment(3, 3);
ap4 = Appointment(4, 4);
ap5 = Appointment(5, 5);
ap6 = Appointment(6, 6);

vehicle1 = Vehicle(1, 2);
vehicle2 = Vehicle(2, 3);
vehicle3 = Vehicle(3, 1);
vehicle4 = Vehicle(4, 1);
vehicle5 = Vehicle(5, 4);
vehicle6 = Vehicle(6, 1);

parent1 = Individual(
        [ap1, ap2, ap3, ap4, ap5, ap6],
        [vehicle1, vehicle2, vehicle3]);
parent2 = Individual(
        [ap6, ap3, ap5, ap2, ap4, ap1],
        [vehicle4, vehicle5, vehicle6]);

result = crossOver(parent1, parent2);

print("\n")
print(result._appointments());
print(result._vehicles());
