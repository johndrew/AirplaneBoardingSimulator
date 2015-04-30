from simpy import Resource
from passenger_actions import Walk, Load, Seat


class Aisle:
    def __init__(self, env, rows):
        self.env = env
        self.rows = rows
        self.space_to_walk = Resource(env, capacity=len(rows))
        self.passengers_in_aisle = []
        self.space_dict = {}  # Maps passengers to aisle space requests
        self.row_reqs = {}  # Dictionary that maps rows to their requests

        for row in rows:
            self.row_reqs[row] = None

    def add_passenger(self, passenger):
        self.space_dict[passenger] = None
        self.get_space_to_walk(passenger)

        self.passengers_in_aisle.append(passenger)
        passenger.current_row = 0

        self.get_row_space(self.rows[0])

    def get_space_to_walk(self, passenger):
        req = self.space_to_walk.request()
        self.space_dict[passenger] = req
        yield req

    def get_row_space(self, row):
        req = row.room.request()
        self.row_reqs[row] = req
        yield req

    def release_row(self, row):
        # req = self.row_reqs[row]
        # row.room.release(req)
        pass

    def release_aisle_space(self, passenger):
        # req = self.space_dict[passenger]
        # self.space_to_walk.release(req)
        pass

    def step_passengers(self):

        # Cycle through passengers in aisle until all have moved one or have
        # seated
        for passenger in self.passengers_in_aisle:

            if passenger.assigned_seat.row_number == passenger.current_row + 1:
                load = Load(self.env, passenger)
                seat = Seat(self.env, passenger)

                self.env.process(load.load_carry_on())

                row_to_release = self.rows[passenger.current_row]
                self.release_row(row_to_release)
                self.release_aisle_space(passenger)

                self.env.process(seat.seat_self())
                self.passengers_in_aisle.remove(passenger)
                passenger.is_seated = True
            else:
                next_row = self.rows[passenger.current_row + 1]
                self.get_row_space(next_row)

                row_to_release = self.rows[passenger.current_row]
                self.release_row(row_to_release)
                passenger.current_row += 1

                walk_event = Walk(self.env, passenger)

                walk_process = self.env.process(walk_event.walk_one())
                passenger.set_walk_process(walk_process)
