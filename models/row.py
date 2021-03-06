from simpy import Resource
from models.seat import Seat
from constants import position_labels


class Row:
    """
    Represents a row in an airplane.

    Number of seats may vary depending on the type of plane
    """

    def __init__(self, env, row_num, num_seats):
        self.row_num = row_num
        self.num_seats = num_seats
        self.seats = []
        self.room = Resource(env, capacity=1)

        self.make()

    def make(self):
        """
        Creates the row object
        """
        labels = position_labels

        for i in range(0, self.num_seats):
            seat = Seat(self.row_num, labels[i])
            self.seats.append(seat)

    def get_seats(self):
        return self.seats

    def __str__(self):
        result = 'Row('
        for seat in self.seats:
            result += seat.__str__() + ', '
        result += ')'
        return result
