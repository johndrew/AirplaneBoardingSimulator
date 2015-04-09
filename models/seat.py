from constants import position_labels


class Seat:

    def __init__(self, row_number, position):
        """
        Represents a seat on a plane

        position is a string and is a letter from 'A' through 'F'
        """
        self.rowNumber = row_number
        self.position = position

        self.validate()

    def validate(self):
        if type(self.rowNumber) != int:
            raise TypeError("row number must be an int")
        if type(self.position) != str:
            raise TypeError("position must be a string")
        if self.position not in position_labels:
            raise TypeError("position must be one of these: %s" %
                            position_labels)

    def __str__(self):
        return "Seat(%s, %s)" % (self.row_number, self.position)
