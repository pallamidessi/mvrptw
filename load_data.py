import model
import numpy

def load_dataset(name):
    # Pass the header
    header_offset = 10
    
    list_appointment = []

    # Read the file  
    with open("data/" + name) as f:
        solomon_data = f.readlines()
    
    array = numpy.array(map(lambda line: map(int, line.strip().split()), solomon_data[header_offset:]))

    minx, miny = array.min(axis=0)[1], array.min(axis=0)[2]
    maxx, maxy = array.min(axis=0)[1], array.min(axis=0)[2]

    # Parse a line of the dataset 
    for line in solomon_data[header_offset:]:
        parameters = map(int, line.strip().split())
        
        # Create problem's object
        list_appointment.append(model.Appointment(model.Point(parameters[1], parameters[2]),
                                                  {'start': parameters[4], 'end': parameters[5]},
                                                  1))
    return {'appointment' : list_appointment,
            'xrange' : (minx, maxx),
            'yrange' :(miny, maxy)}



