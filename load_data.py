"""
File containing functions used for file loading.
"""

import model
import numpy
import sys
import random

sys.path.insert(0, './gen/protobuf')

import address_pb2
import crew_pb2
import cube_pb2
import journey_pb2
import requiredElement_pb2
import vehicle_pb2


def load_dataset(name):
    """
    Loads the dataset passed as a parameter.
    """

    # Pass the header
    header_offset = 10

    list_appointment = []

    # Read the file
    with open("data/" + name) as open_file:
        solomon_data = open_file.readlines()

    tmp_list = []

    # Parse a line of the dataset
    for line in solomon_data[header_offset:]:
        parameters = [int(l) for l in line.strip().split()]
        if parameters == []:
            continue

        tmp_list.append(parameters)

        app_time = sum([parameters[4], parameters[5]]) / 2

        # Create problem's object
        list_appointment.append(
            model.Appointment(
                model.Point(parameters[1], parameters[2]),
                time=app_time,
                group=0,
                duration=2,
                time_window_before=app_time - parameters[4],
                time_window_after=parameters[5] - app_time))

    #pylint: disable=E1101
    array = numpy.array(tmp_list)
    #pylint: disable=E1101

    minx, miny = array.min(axis=0)[1], array.min(axis=0)[2]
    maxx, maxy = array.max(axis=0)[1], array.max(axis=0)[2]

    return {'appointment': list_appointment,
            'xrange': (minx, maxx),
            'yrange': (miny, maxy)}


def coef_from_scale(value, scale):
    """
    Scales a time value in seconds.
    """
    if scale == 0:
        return value * 86400
    if scale == 1:
        return value * 3600
    if scale == 2:
        return value * 60
    if scale == 4:
        return value / 1000
    return value


def load_protobuf(path_prefix):
    """
    Loads data using protobuf.
    """

    # Creating a dictionary to return everything
    proto_dict = {}

    # Loading Crews
    with open(path_prefix + "/ProtoCrew.bin") as open_file:
        crew_list = crew_pb2.List_Crew()
        crew_list.ParseFromString(open_file.read())
        proto_dict['crew'] = crew_list

    # Loading Journeys
    with open(path_prefix + "/ProtoJourneys.bin") as open_file:
        journey_list = journey_pb2.List_Journey()
        journey_list.ParseFromString(open_file.read())
        proto_dict['journey'] = journey_list

    # Loading Required Elements
    with open(path_prefix + "/ProtoRequiredElement.bin") as open_file:
        required_element_list = requiredElement_pb2.List_RequiredElement()
        required_element_list.ParseFromString(open_file.read())
        proto_dict['required_element'] = required_element_list

    # Loading Vehicles
    with open(path_prefix + "/ProtoVehicle.bin") as open_file:
        vehicle_list = vehicle_pb2.List_Vehicle()
        vehicle_list.ParseFromString(open_file.read())
        proto_dict['vehicle'] = vehicle_list

    # Loading Addresses
    with open(path_prefix + "/ProtoAddress.bin") as open_file:
        address_list = address_pb2.List_Address()
        address_list.ParseFromString(open_file.read())
        proto_dict['address'] = address_list

    """
    # Loading Cube
    with open(path_prefix + "/cube.bin") as open_file:
        cube = cube_pb2.List_CubeItem()
        cube.ParseFromString(open_file.read())
        proto_dict['cube'] = cube
    """

    vehicle_list = [model.Vehicle(id_vehicle=v.IdVehicle,
                                  count=0,
                                  capacity=v.MaxOccupant,
                                  vehicle_type=v.TypeOfVehicle,
                                  cost_per_km=v.CostPerKm,
                                  cost_per_hour=v.CostPerHour)
                    for v in proto_dict['vehicle'].items]

    randx = random.randrange(0, 1300)
    randy = random.randrange(0, 700)
    """
    cubeitem_list = [model.CubeItem(c.Id,
                                    c.DepartureAddress,
                                    c.ArrivalAddress,
                                    c.Duration,
                                    c.Distance,
                                    c.IdCubeTimeRange)
                    for c in proto_dict['cube'].items]
    """

    appointment_list = [model.Appointment(
        model.Point(
            random.randrange(0, 1300),
            random.randrange(0, 700)),
        time=coef_from_scale(
            re.PlannedDate.value,
            re.PlannedDate.scale),
        group=0,
        duration=re.Duration,
        #time_window_before=15,
        #time_window_after=15,
        app_type=re.TypeOfRequiredElement,
        app_id=re.IdRequiredElement,
        address=re.IdAddress
        )
        for re in proto_dict['required_element'].items]

    journey_list = [model.Journey(id_journey=j.IdJourney,
                                  is_conccurentable=j.IsConccurentable,
                                  number_of_occupant=j.NumberOfOccupant,
                                  required_type_of_vehicle=
                                  j.RequiredTypeOfVehicle,
                                  type_of_journey=j.TypeOfJourney,
                                  id_customer=j.IdCustomer,
                                  base_price=j.BasePrice,
                                  id_planned_elements=j.IdPlannedElements
                                  )
                    for j in proto_dict['journey'].items]

    to_return = {}
    to_return['vehicle'] = vehicle_list
    to_return['appointment'] = appointment_list[:50]

    minx = min([appointment.get_x() for appointment in appointment_list])
    miny = min([appointment.get_y() for appointment in appointment_list])

    maxx = max([appointment.get_x() for appointment in appointment_list])
    maxy = max([appointment.get_y() for appointment in appointment_list])

    to_return['xrange'] = (minx, maxx)
    to_return['yrange'] = (miny, maxy)

    #print appointment_list
    #print vehicle_list

    #for idx in range(0, len(proto_dict['vehicle'].items)):
    #    print proto_dict['vehicle'].items[idx].CostPerKm

    return to_return

#def load_vehicle(vehicle_param, vehicle_list):
#    """
#    Loads a protobuf vehicle and adds it to a vehicle_list, which it also
#    returns.
#    """
