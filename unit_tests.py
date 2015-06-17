#-*- coding:utf8 -*-
"""
File dedicated to unit testing.
"""
import operators as op
import model as mo
import genome
import unittest


class Appointment(object):
    """
    Represents an appointment object, for the sake of unit testing.
    """

    def __init__(self):
        self.window_start = 0
        self.window_end = 0

    def get_window_start(self):
        """
        Returns _window_start
        """
        return self.window_start

    def get_window_end(self):
        """
        Returns _window_end
        """
        return self.window_end

    def set_window_start(self, value):
        """
        Sets _window_start
        """
        self.window_start = value

    def set_window_end(self, value):
        """
        Sets _window_end
        """
        self.window_end = value


class TestIndividual(unittest.TestCase):
    """
    This class implements unit tests.
    """
    def setUp(self):

        self.dataset = {'appointment': [8, 4, 2, 5, 7, 6, 15, 8451, 14]}
        self.list_appointment = [[1, 4, 2], [0, 3, 5, 6, 7], [8]]
        self.parent = genome.MvrpIndividual([0, 0])

    def tearDown(self):
        pass

    def test_encoding(self):
        """
        Tests whether the encoding of a list of appointments works well.
        """
        self.parent.encode(self.list_appointment)
        self.assertEqual(
            self.parent.routes,
            [item for sublist in self.list_appointment for item in sublist],
            'Incorrect encoding')
        self.assertEqual(
            len(self.parent.vehicles),
            len(self.list_appointment),
            'Incorrect encoding')

    def test_decoding(self):
        """
        Checks if decoding works fine
        """
        self.parent.encode(self.list_appointment)
        self.assertEqual(
            self.parent.decode(self.dataset),
            [[4, 7, 2], [8, 5, 6, 15, 8451], [14]],
            'Incorrect decoding')

    def test_appointment_removal(self):
        """
        Checks if appointment removal works fine.
        """
        self.assertEqual(
            op.appointment_removal(
                [[1, 2], [3, 4, 5]],
                [2, 4]),
            [[1], [3, 5]],
            'Incorrect appointment removal')

    def test_route_generation(self):
        """
        Checks if route generation works fine.
        """
        route = mo.generate_route(100, 12, 300, 300, mo.Point(20, 20))
        self.assertEqual(len(route), 100*12, 'Incorrect route generation')

    def test_new_index_choice(self):
        """
        Checks if choosing a new index works fine.
        """
        current_index = 1
        length = 3
        tested_values = [0, 1]
        self.assertEqual(
            op.choosing_a_new_index(
                current_index,
                tested_values,
                length
            ),
            2
        )

    def test_1d_insertion(self):
        """
        Checks if 1D insertion works fine.
        """
        data = []
        offset = 0
        for _ in range(0, 6):
            tmp = Appointment()
            tmp.set_window_start(offset)
            tmp.set_window_end(offset+1000)
            offset = offset+1001
            data.append(tmp)

        to_insert = Appointment()
        to_insert.set_window_start(2700)
        to_insert.set_window_end(4000)

        dico = {}
        dico['appointment'] = data

        self.assertEqual(
            op.insert_appointment1d(
                [1, 2, 4, 5],
                3,
                dico),
            [1, 2, 3, 4, 5],
            'Incorrect 1d insertion')


if __name__ == "__main__":
    unittest.main()
