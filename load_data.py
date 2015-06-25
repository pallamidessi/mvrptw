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


def load_cube(cube_list):
    """
    Creates a list of the elements contained in the cube using the class
    created in model.py.
    """
    cube = [model.CubeItem(c.Id,
                           c.DepartureAddress,
                           c.ArrivalAddress,
                           c.Duration,
                           c.Distance,
                           c.IdCubeTimeRange)
            for c in cube_list]
    return cube


def load_crews(crews):
    """
    Creates a list of crews using the class created in model.py.
    """
    crew_list = [model.Crew(id_crew=c.IdCrew,
                            employees=[e.IdEmployee for e in c.Employees])
                 for c in crews]

    return crew_list


def load_addresses(addresses):
    """
    Creates a list of addresses using the class created in model.py.
    """
    address_list = [model.Address(id_address=addr.IdAddress,
                                  id_agglomeration=addr.IdAgglomeration,
                                  is_pick_up_plan=addr.IsPickUpPlan,
                                  id_zone=addr.IdZone)
                    for addr in addresses]

    return address_list


def load_employees(crews):
    """
    Creates a list of employees using the class created in model.py.
    """
    employee_list = list(set([model.Employee(
        id_employee=e.IdEmployee,
        crews=[item.IdCrew for item in e.Crews],
        id_pause_address=e.IdPauseAddress,
        is_graduated=e.IsGraduated,
        working_hours_cost=e.WorkingHoursCost,
        beginning_hours_cost=e.BeginingHoursCost
        )
        for e in [
            item for sublist in [
                c.Employees for c in crews]
            for item in sublist]]))

    return employee_list


def load_journeys(journeys):
    """
    Creates a list of journeys using the class created in model.py.
    """

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
                    for j in journeys]

    return journey_list


def load_vehicles(vehicles):
    """
    Creates a list of vehicles using the class created in model.py.
    """
    vehicle_list = [model.Vehicle(id_vehicle=v.IdVehicle,
                                  count=0,
                                  capacity=v.MaxOccupant,
                                  vehicle_type=v.TypeOfVehicle,
                                  cost_per_km=v.CostPerKm,
                                  cost_per_hour=v.CostPerHour)
                    for v in vehicles]

    return vehicle_list


def load_appointments(appointments, journeys):
    """
    Creates a list of appointments using the class created in model.py.
    """
    appointment_list = []
    for index in range(0, len(journeys)):
        journey = journeys[index]
        for id_element in journey.id_planned_elements():
            appointment_list.append([
                model.Appointment(
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
                    address=re.IdAddress,
                    id_journey=index
                    )
                for re in appointments
                if re.IdRequiredElement == id_element]
            )

    appointment_list = [it for sublist in appointment_list for it in sublist]
    #appointment_list = [model.Appointment(
    #    model.Point(
    #        random.randrange(0, 1300),
    #        random.randrange(0, 700)),
    #    time=coef_from_scale(
    #        re.PlannedDate.value,
    #        re.PlannedDate.scale),
    #    group=0,
    #    duration=re.Duration,
    #    #time_window_before=15,
    #    #time_window_after=15,
    #    app_type=re.TypeOfRequiredElement,
    #    app_id=re.IdRequiredElement,
    #    address=re.IdAddress
    #    )
    #    for re in appointments]

    return appointment_list


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
        appointment_list = requiredElement_pb2.List_RequiredElement()
        appointment_list.ParseFromString(open_file.read())
        proto_dict['required_element'] = appointment_list

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

    to_return = {}
    to_return['vehicle'] = load_vehicles(proto_dict['vehicle'].items)
    to_return['journey'] = load_journeys(proto_dict['journey'].items)
    to_return['appointment'] = load_appointments(
        proto_dict['required_element'].items,
        to_return['journey']
        )
    to_return['cube'] = load_cube(proto_dict['cube'].items)
    to_return['employee'] = load_employees(proto_dict['crew'].items)
    to_return['crew'] = load_crews(proto_dict['crew'].items)
    to_return['address'] = load_addresses(proto_dict['address'].items)

    for key in to_return:
        if key != 'crew' and key != 'employee':
            print to_return[key]
        if key == 'employee':
            print [e.id_employee() for e in to_return[key]]

    to_return['xrange'] = (min([appointment.get_x() for appointment
                                in to_return['appointment']]),
                           max([appointment.get_x() for appointment
                                in to_return['appointment']]))
    to_return['yrange'] = (min([appointment.get_y() for appointment
                                in to_return['appointment']]),
                           max([appointment.get_y() for appointment
                                in to_return['appointment']]))

    return to_return

#def load_vehicle(vehicle_param, vehicle_list):
#    """
#    Loads a protobuf vehicle and adds it to a vehicle_list, which it also
#    returns.
#    """
