from boarding_algorithms import BoardingAlgorithm
from models.aisle import Aisle
from models.row import Row


class Airplane:
    """
    Represents an airplane seating layout

    Independent of actual size of airplane, i.e. number of seats and
        number of seats per row
    """

    def __init__(self, env, name, row_num, seats_per_row, aisles, has_middle):
        self.env = env
        self.action = env.process(self.run())

        self.name = name
        self.row_num = row_num
        self.seats_per_row = seats_per_row
        self.seats = []
        self.aisle = Aisle()
        self.algorithms = BoardingAlgorithm()
        self.number_of_aisles = aisles
        self.has_middle = has_middle

        # containers
        self.rows = []

    def run(self):
        print 'airplane'

    def make_rows(self):
        """
        Creates all of the row objects for this plane
        """
        for row_num in self.row_num:
            row = Row(row_num, self.seats_per_row)
            self.rows.append(row)

    def __str__(self):
        return "Airplane(totalSeats=%s)" % (self.rows*self.seats_per_row)