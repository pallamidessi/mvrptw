# -*- coding:utf-8 -*-
"""
This file contains functions dedicated to rendering the results of the
genetic algorithm.
"""

import model
import random

from Tkinter import Tk, Frame, Canvas, BOTH
from colorsys import hls_to_rgb
from math import sqrt

#RAD_TO_DEG = lambda r: r/2/pi*360.0
#DEG_TO_RAD = lambda r: r*2*pi/360.0
#IDENTITY = lambda r: r


def translate_to_tkcolor(color):
    """
    Translates the color passed as an argument to hex.
    """
    return rgb_to_hex(translate_rgb(color))


def translate(value, from_min, from_max, to_min, to_max):
    """
    Translates the value passed as a parameter into a corresponding value
    in the right range.
    """
    # Figure out how 'wide' each range is
    left_span = from_max - from_min
    right_span = to_max - to_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - from_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return to_min + (value_scaled * right_span)


def translate_rgb(rgb_tuple):
    """
    Translates a rgb tuple to the same tuple from the range 0-1 to the range
    0-255.
    """
    mapped_rgb_value = []
    for component in rgb_tuple:
        mapped_rgb_value.append(translate(component, 0, 1, 0, 255))

    return tuple(mapped_rgb_value)


def rgb_to_hex(rgb):
    """
    Translates a RGB color to its hex format.
    """
    return '#%02x%02x%02x' % rgb


#def color_group(max_range):
#    """
#    Generates max_range random colors and returns them in a list.
#    """
#    golden_ratio_conjugate = 0.618033988749895
#    generated_color = []
#
#    for _ in range(0, max_range):
#        color_value = random.random()
#        color_value += golden_ratio_conjugate
#        color_value %= 1
#        generated_color.append(hls_to_rgb(color_value, 0.5, 0.95))
#
#    return generated_color

def color_distance(color1, color2):
    """
    Calculates the euclidean distance between two colors
    """
    dist_h = color1[0] - color2[0]
    dist_s = color1[1] - color2[1]
    dist_v = color1[2] - color2[2]
    
    return sqrt(dist_h * dist_h + dist_s * dist_s + dist_v * dist_v)

def mutate_color(color):
    color[random.randrange(0, 3)] = random.random() % 1
    return color

def color_group(max_range):
    """
    Generates max_range random distinct colors
    """

    color = []
    
    for _ in range(0, max_range):
        col = []
        col.append(random.random() % 1)
        col.append(random.random() % 1)
        col.append(random.random() % 1)
        color.append(col)

    max_dist = 0
    dist_table = []

    for idx in range(0, max_range):
        dist_table.append([color_distance(color[idx], x) for x in color[:]])

    for _ in range(0, 50):
        max_dist = 0
        for idx_start in range(0, max_range):
            global_point_distance = sum(dist_table[idx_start])
            tmp_dist_table = dist_table[idx_start][:]
            tmp_table = color[:]
            for idx_end in range(0, max_range):
                tmp_table[idx_end] = mutate_color(color[idx_end])
                tmp_dist_table[idx_end] = color_distance(color[idx_start], color[idx_end])
            if sum(tmp_dist_table) > global_point_distance:
                dist_table[idx_start] = tmp_dist_table[:]
                color = tmp_table[:]

    return color

class Example(Frame):
    """
    This class is an example class to represent frames on the screen.
    """

    def __init__(self, parent, dict_info):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        new_dict = {}
        new_dict['data'] = dict_info['data']
        new_dict['color'] = dict_info['color']
        new_dict['depot'] = dict_info['depot']
        new_dict['tour'] = dict_info['tour']
        new_dict['zoomx'] = dict_info['zoomx']
        new_dict['zoomy'] = dict_info['zoomy']
        self.init_ui(new_dict)

    def init_ui(self, dict_info):
        """
        Initializes the UI using all the information contained in dict_info
        """

        data = dict_info['data']
        color = dict_info['color']
        depot = dict_info['depot']
        mtour = dict_info['tour']
        zoomx = dict_info['zoomx']
        zoomy = dict_info['zoomy']
 
        list_appointment = data["appointment"]
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)

        depot, mtour = zoom_before_drawing(
            depot,
            mtour,
            zoomx,
            zoomy)

        canvas = Canvas(self)

        idx = 0

        for tour in mtour:
            tour.insert(0, model.Appointment(depot, 0, -1))
            draw_tour(tour, canvas, translate_to_tkcolor(color[idx]))
            idx += 1

        canvas.create_oval(depot.get_x(),
                           depot.get_y(),
                           depot.get_x()-5,
                           depot.get_y()-5,
                           outline="black",
                           fill="green",
                           width=7)

        for appointement in list_appointment:
            
            currentx = appointement.get_x() * zoomx
            currenty = appointement.get_y() * zoomy

            canvas.create_oval(
                currentx,
                currenty,
                currentx - 3,
                currenty - 3,
                outline="red",#translate_to_tkcolor(color[appointement.group()]),
                fill="red",
                width=5)

        canvas.pack(fill=BOTH, expand=1)


def draw_tour(list_coord, canvas, color):
    """
    Draws the tour passed as a parameter on the canvas using the color also
    passed as a parameter.
    """
    if len(list_coord) >= 1:
        for i in range(0, len(list_coord) - 1):
            canvas.create_line(list_coord[i].get_x(),
                               list_coord[i].get_y(),
                               list_coord[i + 1].get_x(),
                               list_coord[i + 1].get_y(),
                               fill=color,
                               width=3)
                               #dash=(4, 4))

        canvas.create_line(list_coord[-1].get_x(),
                           list_coord[-1].get_y(),
                           list_coord[0].get_x(),
                           list_coord[0].get_y(),
                           fill=color,
                           width=3)
                           #dash=(4, 4))


def indexes_to_appointement(indices, list_appointment):
    """
    Retrieves the appointments corresponding to the list of indices passed as a
    parameter in list_appointment
    """
    translated = []

    for index in indices:
        translated.append(list_appointment[index])

    return translated


def individual_as_appointment(ind, list_appointement):
    """
    Transforms an individual into an appointment 2d list.
    """
    splitted_route = ind.split()
    appointment_2d = []

    for route in splitted_route:
        appointment_2d.append(indexes_to_appointement(
            route,
            list_appointement))

    return appointment_2d


def zoom_before_drawing(depot, list_appointment, zoomx, zoomy):
    """
    Transforms the coordinates of each appointment in order to magnify the
    view by a factor of zoom once everything's drawn.
    """
    list_to_return = []

    for index in range(0, len(list_appointment)):

        list_to_return.append([])
        for element in list_appointment[index]:

            newx = element.get_x() * zoomx
            newy = element.get_y() * zoomy

            new_coordinate = model.Point(
                newx,
                newy
            )

            zoomed_in_appointment = model.Appointment(
                new_coordinate,
                element.starting_time,
                element.group(),
                {'start': element.window_start, 'end': element.window_end}
            )
            list_to_return[index].append(zoomed_in_appointment)

    newx = depot.get_x() * zoomx
    newy = depot.get_y() * zoomy

    depot_to_return = model.Point(newx, newy)

    return depot_to_return, list_to_return
