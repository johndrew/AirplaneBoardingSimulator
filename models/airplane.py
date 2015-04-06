class Airplane:

    def __init__(self, rows, seats_per_row):
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = []

    def __str__(self):
        return "Airplane(totalSeats=%s)" % (self.rows*self.seats_per_row)