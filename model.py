import random

from noise import pnoise2
from cmath import polar, rect, pi as PI, e as E, phase
from math import sqrt

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

class Point(complex):
    def __repr__(self):
        return "<Point x:%.3f y:%.3f>" % self.as_euclidian()
    
    def _x(self):
        return self.real
    def _y(self):
        return self.imag
    def as_euclidian(self):
        return (self.real, self.imag)
    def as_polar(self,measure="rad" ):
        conv = measure == "rad" and identity or rad_to_deg
        return (abs(self), conv(phase(self)))

class Appointement():
    def __repr__(self):
        return "<Appointement coordinate:%s starting_time:%s:>\n" % (self.coordinate, self.starting_time)
    
    def _x(self):
        return self.coordinate._x()
    def _y(self):
        return self.coordinate._y()
    def _group(self):
        return self.group
    def __init__(self, coordinate, time, group):
        self.coordinate = coordinate
        self.starting_time = time
        self.group = group


def generate_route(n, k, height, width, starting):
    factor = 2000
    list_appointments = []
    rand_window_factor = 10
    rand_window_h = height / rand_window_factor
    rand_window_w = width  / rand_window_factor
    rand_time = (0, 100)

    for i in range(0, n):
        lastPoint = Point(starting._x() + random.randrange(-rand_window_w, rand_window_w),
                          starting._y() + random.randrange(-rand_window_h, rand_window_h))
        appointement_time = 0
        for j in range(0, k ):
            n1 = pnoise2(lastPoint._x() / width, lastPoint._y() / height)
            n2 = pnoise2(lastPoint._y() / height, lastPoint._x() / width)
            newx = clamp(lastPoint._x() + n1 * factor, 0, width)
            newy = clamp(lastPoint._y() + n2 * factor, 0, height)
            lastPoint = Point(newx, newy)
            appointement_time += random.randrange(*rand_time)
            list_appointments.append(Appointement(lastPoint, appointement_time, i))
    
    return list_appointments

def euclidian_distance(p1, p2):
    return sqrt((p1._x() - p2._x())**2 + ((p1._y() - p2._y())**2))

