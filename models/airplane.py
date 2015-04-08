from boarding_algorithms import Boarding_Algorithm
from models.aisle import Aisle


class Airplane:

    def __init__(self, env, rows, seats_per_row):
        """
            Represents an airplane seating layout

            Independent of actual size of airplane, i.e. number of seats and
                number of seats per row
            """
        self.env = env
        self.action = env.process(self.run())
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = []
        self.aisle = Aisle()
        self.algorithms = Boarding_Algorithm()

    def run(self):
        print 'airplane'

    def board(self):
        print 'board'

    def __str__(self):
        return "Airplane(totalSeats=%s)" % (self.rows*self.seats_per_row)