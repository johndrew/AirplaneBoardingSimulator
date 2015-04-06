from Queue import Queue


class Aisle(Queue):

    def __init__(self, number_of_rows):
        self.number_of_rows = number_of_rows