"""
File containing the model classes for the project
"""

import random
from enum import Enum
from noise import pnoise2
# from cmath import polar, rect, pi as PI, e as E, phase
from math import sqrt

CLAMP = lambda n, minn, maxn: max(min(maxn, n), minn)


class Point(complex):
    """
    This class describes a 2D point based on the 'complex' class.
    It therefore contains the following data:

    - its x coordinate
    - its y coordinate
    """

    def __repr__(self):
        return "<Point x:%.3f y:%.3f>" % self.as_euclidean()

    def get_x(self):
        """
        Gets the real part (x coordinate) of the point.
        """
        return self.real

    def get_y(self):
        """
        Gets the imaginary part (y coordinate) of the point.
        """
        return self.imag

    def as_euclidean(self):
        """
        Returns the point as an euclidean tuple of coordinates.
        """
        return (self.real, self.imag)

    #def as_polar(self, measure="rad"):
    #    """
    #    Returns the point as a polar tuple of coordinates.
    #    """
    #    conv = measure == "rad" and identity or rad_to_deg
    #    return (abs(self), conv(phase(self)))


class RequiredElementTypes(Enum):
    """
    An enumeration of the possible types for a required element.
    """
    Departure = 0
    Arrival = 1


class RequiredInternFleetElementTypes(Enum):
    """
    An enumeration of the possible types for an intern fleet required element.
    """
    One = 0


class Appointment(object):
    """
    This class describes an appointments and contains the following
    information:

    - its coordinates (namely one point)
    - its starting_time (should disappear in a while)
    - the start date of its time window
    - the end date of its time window
    """

    def __repr__(self):
        return "<Appointment coordinate:%s starting_time:%s w_start:%s \
            w_end:%s>\n" % \
            (
                self._coordinate,
                self._starting_time,
                self._window_start,
                self._window_end
                )

    def get_x(self):
        """
        Gets the x coordinate of the appointment.
        """
        return self._coordinate.get_x()

    def get_y(self):
        """
        Gets the y coordinate of the appointment.
        """
        return self._coordinate.get_y()

    def group(self):
        """
        Gets the group to which the appointment belongs.
        """
        return self._group

    def starting_time(self):
        """
        Gets the starting time of the appointment/
        """

    def duration(self):
        """
        Gets the duration of the appointment.
        """
        return self._duration

    def window_start(self):
        """
        Gets the start of the time window associated with the appointment.
        """
        return self._window_start

    def window_end(self):
        """
        Gets the end of the time window associated with the appointment.
        """
        return self._window_end

    def __init__(self,
                 coordinate,
                 time,
                 group,
                 window=None,
                 duration=0,
                 load=1):

        self._duration = duration
        self._coordinate = coordinate
        self._starting_time = time

        if window is None:
            self._window_start = 0
            self._window_end = 0
        else:
            self._window_start = window['start']
            self._window_end = window['end']

        self._group = group
        self._load = load


class VehicleTypes(Enum):
    """
    This class enumerates the vehicle types.
    """
    VSL = 0
    TPMR = 1
    Ambulance = 2
    Taxi = 3


class Vehicle(object):
    """
    This class represents a Vehicle which has the following attributes:

    - an id (_id_vehicle)

    - a number of appointments to go to (_count)
    """

    def __repr__(self):
        return "<Vehicle _id_vehicle: %s, _count: %s, " % (
            self._id_vehicle,
            self._count) + \
            "_capacity: %s, _vehicle_type: %s, " % (
                self._capacity,
                VehicleTypes(self._vehicle_type).name) + \
            "_cost_per_km: %s, _cost_per_hour: %s>\n" % (
                self._cost_per_km,
                self._cost_per_hour)

    def id_vehicle(self):
        """
        Returns the identificator of the vehicle.
        """
        return self._id_vehicle

    def capacity(self):
        """
        Returns the vehicle's capacity.
        """
        return self._capacity

    def vehicle_type(self):
        """
        Returns the vehicle's type.
        """
        return self._vehicle_type

    def cost_per_km(self):
        """
        Returns the vehicle's cost per km.
        """
        return self._cost_per_km

    def cost_per_hour(self):
        """
        Returns the vehicle's cost per hour.
        """
        return self._cost_per_hour

    def count(self):
        """
        Returns the number of appointments the vehicle has to meet.
        """
        return self._count

    def set_count(self, amount):
        """
        Sets _count to amount.
        """
        self._count = amount

    def add_to_count(self, amount):
        """
        Adds amount appointments to the existing count of appointments.
        """
        self._count += amount

    def __init__(self,
                 id_vehicle,
                 count,
                 capacity=0,
                 vehicle_type=VehicleTypes.VSL,
                 cost_per_km=0,
                 cost_per_hour=0):

        self._id_vehicle = id_vehicle
        self._count = count
        self._capacity = capacity
        self._vehicle_type = vehicle_type
        self._cost_per_km = cost_per_km
        self._cost_per_hour = cost_per_hour


def make_last_point(last_point, width, height, factor):
    """
    Generates a new last point in order to help with the route generation.
    It uses the following parameters:

    - last_point (the former last point)
    - width (the width of the window)
    - height (the height of the window)
    - factor (a user-chosen factor)
    """
    newx = \
        pnoise2(last_point.get_x() / width, last_point.get_y() / height)
    newy = \
        pnoise2(last_point.get_y() / height, last_point.get_x() / width)
    newx = CLAMP(last_point.get_x() + newx * factor, 0, width)
    newy = CLAMP(last_point.get_y() + newy * factor, 0, height)
    return Point(newx, newy)


def generate_route(nb_routes, k, height, width, starting):
    """
    Generates nb_routes routes of k appointments on a grid of height * width
    with a starting point named "starting".
    """
    factor = 2000
    list_appointments = []
    rand_window_factor = 10
    rand_window = {
        'h': height / rand_window_factor,
        'w': width / rand_window_factor
        }
    rand_time = (0, 100)

    for i in range(0, nb_routes):
        last_point = Point(
            starting.get_x() +
            random.randrange(-rand_window['w'], rand_window['w']),
            starting.get_y() +
            random.randrange(-rand_window['h'], rand_window['h']))

        appointment_time = 0
        for _ in range(0, k):
            last_point = make_last_point(last_point, width, height, factor)
            window_start = random.randrange(0, 1000)
            appointment_time += random.randrange(rand_time[0], rand_time[1])
            list_appointments.append(
                Appointment(
                    last_point,
                    appointment_time,
                    i,
                    {
                        "start": window_start,
                        "end": random.randrange(window_start+1, 2000)
                        }
                    )
                )

    return list_appointments


def euclidean_distance(point1, point2):
    """
    Calculates the euclidean distance between point1 and point2.
    """
    return sqrt(
        (point1.get_x() - point2.get_x())**2 +
        ((point1.get_y() - point2.get_y())**2))
