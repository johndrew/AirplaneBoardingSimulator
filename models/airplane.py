from boarding_algorithms import BoardingAlgorithm
from models.aisle import Aisle
from models.row import Row


class Airplane:
    """
    Represents an airplane seating layout

    Independent of actual size of airplane, i.e. number of seats and
        number of seats per row

    Currently, only the economy class is created.
    """

    def __init__(self, env, name, rows, seats, aisles, has_middle):
        self.env = env
        # self.action = env.process(self.run())

        self.name = name
        self.number_of_rows = rows
        self.seats_per_row = seats
        self.number_of_aisles = aisles
        self.has_middle = has_middle

        # self.algorithms = BoardingAlgorithm()

        # containers
        self.rows = []
        self.seats = []

    def run(self):
        self.make_rows()

        # if this is removed, there are errors. It needs some form of yield
        yield self.env.timeout(0)

    def make_rows(self):
        """
        Creates all of the row objects for this plane

        Adds newly created rows to a list of rows and adds the seat objects
        created by the row class to a seats list.

        Since only the economy class is being modeled, row numbers will
        start at 1, which would normally be the first, first-class row number
        """
        for row_number in range(1, self.number_of_rows+1):
            row = Row(row_number, self.seats_per_row)
            self.rows.append(row)
            self.seats += row.get_seats()

    def get_number_of_seats(self):
        return self.number_of_rows * self.seats_per_row

    def get_seats(self):
        return self.seats

    def get_number_of_rows(self):
        return self.number_of_rows

    def __str__(self):
        return "Airplane(totalSeats=%s)" % (self.number_of_rows *
                                            self.seats_per_row)