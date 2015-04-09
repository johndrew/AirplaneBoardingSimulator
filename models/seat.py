from constants import position_labels


class Seat:

    def __init__(self, row_number, position):
        """
        Represents a seat on a plane

        position is a string and is a letter from 'A' through 'F'
        """
        self.row_number = row_number
        self.position = position

        self.validate()

    def validate(self):
        assert isinstance(self.row_number, int)
        assert isinstance(self.position, str)
        assert self.position in position_labels

    def get_row_number(self):
        return self.row_number

    def get_position(self):
        return self.position

    def __str__(self):
        return "Seat(%s, %s)" % (self.row_number, self.position)
