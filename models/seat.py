class Seat:

    def __init__(self, row_number, position):
        """
        Represents a seat on a plane

        position is a string and is a letter from 'A' through 'F'
        """
        self.rowNumber = row_number
        self.position = position

    def __str__(self):
        return "Seat(row=%s, position=%s)" % (self.row_number, self.position)
