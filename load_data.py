"""
File containing functions used for file loading.
"""

import model
import numpy
import sys

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

        # Create problem's object
        list_appointment.append(
            model.Appointment(
                model.Point(parameters[1], parameters[2]),
                {'start': parameters[4], 'end': parameters[5]},
                1))

    #pylint: disable=E1101
    array = numpy.array(tmp_list)
    #pylint: disable=E1101

    minx, miny = array.min(axis=0)[1], array.min(axis=0)[2]
    maxx, maxy = array.max(axis=0)[1], array.max(axis=0)[2]

    return {'appointment': list_appointment,
            'xrange': (minx, maxx),
            'yrange': (miny, maxy)}


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

    # Loading Cube
    with open(path_prefix + "/cube.bin") as open_file:
        cube = cube_pb2.List_CubeItem()
        cube.ParseFromString(open_file.read())
        proto_dict['cube'] = cube

    return proto_dict

#def load_vehicle(vehicle_param, vehicle_list):
#    """
#    Loads a protobuf vehicle and adds it to a vehicle_list, which it also
#    returns.
#    """
