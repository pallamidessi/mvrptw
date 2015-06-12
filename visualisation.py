# -*- coding:utf-8 -*-

import model
import random
import genome

from Tkinter import Tk, Frame, Canvas, BOTH
from colorsys import hls_to_rgb

rad_to_deg = lambda r : r/2/PI*360.0
deg_to_rad = lambda r : r*2*PI/360.0
identity = lambda r: r

def translate_to_TKcolor(color):
    return rgb_to_hex(translate_rgb(color))

def translate(value, fromMin, fromMax, toMin, toMax):
    # Figure out how 'wide' each range is
    leftSpan = fromMax - fromMin
    rightSpan = toMax - toMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - fromMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return toMin + (valueScaled * rightSpan)

def translate_rgb(rgb_tuple):
    mapped_rgb_value = []
    for component in rgb_tuple:
        mapped_rgb_value.append(translate(component, 0, 1, 0, 255))

    return tuple(mapped_rgb_value)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def color_group(n):
    golden_ratio_conjugate = 0.618033988749895
    generated_color = []

    for i in range(0, n):
        h = random.random()
        h += golden_ratio_conjugate
        h %= 1
        generated_color.append(hls_to_rgb(h, 0.5, 0.95))

    return generated_color

class MainGUI(Frame):

    def __init__(self, parent, list_appointment, color, depot, tour):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI(list_appointment, color, depot, tour)

    def initUI(self, list_appointment, color, depot, mtour):
        self.parent.title("Simple")
        canvas = Canvas(self)
        draw_node(depot, 3, outline_color="black")

        for appointment in list_appointment:
            color = translate_to_TKcolor(color[appointment.group])
            draw_node(appointment.coordinate, 2, color)

        idx = 0
        for tour in mtour:
            tour.insert(0, model.Appointment(depot, 0, -1))
            draw_tour(tour, canvas, translate_to_TKcolor(color[idx]))
            idx += 1

        canvas.pack(fill=BOTH, expand=1)


def draw_node(node_coord, size, outline_color):
    canvas.create_oval(node_coord._x(),
                       node_coord._y(),
                       node_coord._x() - size,
                       node_coord._y() - size,
                       outline=outline_color,
                       fill="green",
                       width=size)


def draw_tour(list_coord, canvas, color):
    if  len(list_coord) > 2:
        for i in range(0, len(list_coord) - 1):
            canvas.create_line(list_coord[i]._x(),
                               list_coord[i]._y(),
                               list_coord[i + 1]._x(),
                               list_coord[i + 1]._y(),
                               fill=color,
                               dash=(4, 4))

        # Draw the return from the last appointement to the depot 
        canvas.create_line(list_coord[-1]._x(),
                           list_coord[-1]._y(),
                           list_coord[0]._x(),
                           list_coord[0]._y(),
                           fill=color,
                           dash=(4, 4))


def indexes_to_appointment(indexes, list_appointment):
    translated = []

    for index in indexes:
        translated.append(list_appointment[index])

    return translated

def individual_as_appointment(ind, list_appointment):
    splitted_route = ind.split()
    appointment_2D = []

    for route in splitted_route:
        appointment_2D.append(indexes_to_appointment(route, list_appointment))

    return appointment_2D

def createGUI(best_individual, data):
    root = visualisation.Tk()
    root.geometry("" + str(w) + "x" + str(h))
    app = visualisation.MainGUI(root,
                                list_appointment,
                                color,
                                depot,
                                best_individual.decode(), data)

    return root
