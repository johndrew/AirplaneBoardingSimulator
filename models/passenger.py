import uuid


class Passenger:

    def __init__(self):
        self.id = uuid.uuid4()
        self.seat = None

    def add_seat(self, seat):
        self.seat = seat

    def __str__(self):
        return "Passenger(id=%s)" % self.id