class Seat:

    def __init__(self, rowNumber, position):
        """
        Represents a seat on a plane

        position is a string and is a letter from 'A' through 'F'
        """
        self.rowNumber = rowNumber
        self.position = position

    def __str__(self):
        return "Seat(row=%s, position=%s)" % (self.rowNumber, self.position)
