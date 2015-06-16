#-*- coding:utf8 -*-
"""
File dedicated to unit testing.
"""
import operators as op
import genome
import unittest


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

    #def test_crossover(self):
    #    """
    #    Checks if the crossover works fine
    #    """
    #    self.parent.encode(self.list_appointment)
    #    #print op.crossover(self.parent, self.parent, self.dataset)

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


if __name__ == "__main__":
    unittest.main()
