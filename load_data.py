"""
File containing functions used for file loading.
"""

import model
import numpy


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

    array = []

    for line in solomon_data[header_offset:]:
        array.append([int(a) for a in line.strip().split()])
    #pylint: disable=E1101
    array = numpy.array(array)
    #pylint: disable=E1101

    minx, miny = array.min(axis=0)[1], array.min(axis=0)[2]
    maxx, maxy = array.min(axis=0)[1], array.min(axis=0)[2]

    # Parse a line of the dataset
    for line in solomon_data[header_offset:]:
        parameters = [int(l) for l in line.strip().split()]

        # Create problem's object
        list_appointment.append(
            model.Appointment(
                model.Point(parameters[1], parameters[2]),
                {'start': parameters[4], 'end': parameters[5]},
                1))

    return {'appointment': list_appointment,
            'xrange': (minx, maxx),
            'yrange': (miny, maxy)}


def load_protobuf(name):
    """
    Loads data using protobuf.
    """
