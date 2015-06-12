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

class Example(Frame):
  
    def __init__(self, parent, list_appointement, color, depot, tour):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        
        self.initUI(list_appointement, color, depot, tour)
    
    def initUI(self, list_appointement, color, depot, mtour):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        canvas.create_oval(depot._x(), 
                           depot._y(),
                           depot._x()-5,
                           depot._y()-5,
                           outline="black",
                           fill="green",
                           width=3)

        for appointement in list_appointement:
            canvas.create_oval(appointement._x(), 
                               appointement._y(),
                               appointement._x()-3,
                               appointement._y()-3,
                               outline=translate_to_TKcolor(color[appointement.group]),
                               fill="green",
                               width=2)
        
        idx = 0
        for tour in mtour:
            tour.insert(0, model.Appointment(depot, 0, -1))
            draw_tour(tour, canvas, translate_to_TKcolor(color[idx]))
            idx += 1

        canvas.pack(fill=BOTH, expand=1)

def draw_tour(list_coord, canvas, color):
    if  len(list_coord) > 2:
        for i in range(0, len(list_coord) - 1):
            canvas.create_line(list_coord[i]._x(),
                               list_coord[i]._y(),
                               list_coord[i + 1]._x(),
                               list_coord[i + 1]._y(),
                               fill=color,
                               dash=(4, 4))

        canvas.create_line(list_coord[-1]._x(),
                           list_coord[-1]._y(),
                           list_coord[0]._x(),
                           list_coord[0]._y(),
                           fill=color,
                           dash=(4, 4))


def indexes_to_appointement(indexes, list_appointement):
    translated = []

    for index in indexes:
        translated.append(list_appointement[index])

    return translated

def individual_as_appointment(ind, list_appointement):
    splitted_route = ind.split()
    appointment_2D = []
    
    print splitted_route
    for route in splitted_route:
        appointment_2D.append(indexes_to_appointement(route, list_appointement))

    return appointment_2D

