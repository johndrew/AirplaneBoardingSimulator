from simpy import Process
from models.aisle import Aisle


class Airplane:

    def __init__(self, rows, seats_per_row, env, generator):
        """
            Represents an airplane seating layout

            Independent of actual size of airplane, i.e. number of seats and
                number of seats per row
            """
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = []
        self.aisle = Aisle()

    def __str__(self):
        return "Airplane(totalSeats=%s)" % (self.rows*self.seats_per_row)