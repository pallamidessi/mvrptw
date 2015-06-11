import model

def load_dataset(name):
    # Pass the header
    header_offset = 10
    
    list_appointment = []

    # Read the file  
    with open("data/" + name) as f:
        solomon_data = f.readlines()
    
    # Parse a line of the dataset 
    for line in solomon_data[header_offset:]:
        parameters = map(int, line.strip().split())
        
        # Create problem's object
        list_appointment.append(model.Appointment(model.Point(parameters[1], parameters[2]),
                                                  {'start': parameters[4], 'end': parameters[5]},
                                                  1))
    return list_appointment



