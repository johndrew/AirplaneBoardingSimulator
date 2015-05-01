from simpy import Resource
from passenger_actions import Walk, Load, Seat, next_row_occupied, wait


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
        space_req = self.get_space_to_walk(passenger)

        self.passengers_in_aisle.append(passenger)
        passenger.current_row = 0

        row_req = self.get_row_space(self.rows[0])

    def get_space_to_walk(self, passenger):
        with self.space_to_walk.request() as req:
            self.space_dict[passenger] = req
            return req

    def get_row_space(self, row):
        with row.room.request() as req:
            self.row_reqs[row] = req
            return req

    def release_row(self, row):
        req = self.row_reqs[row]
        row.room.release(req)

    def release_aisle_space(self, passenger):
        req = self.space_dict[passenger]
        self.space_to_walk.release(req)

    def step_passengers(self):

        # Cycle through passengers in aisle until all have moved one or have
        # seated
        for passenger in self.passengers_in_aisle:
            with self.space_to_walk.request() as space_req:

                yield space_req

                if passenger.assigned_seat.row_number == passenger.current_row + 1:
                    load = Load(self.env, passenger)
                    seat = Seat(self.env, passenger)

                    self.env.process(load.load_carry_on())
                    # yield load.load_carry_on()

                    row_to_release = self.rows[passenger.current_row]
                    self.release_row(row_to_release)
                    self.release_aisle_space(passenger)

                    self.env.process(seat.seat_self())
                    # yield seat.seat_self()
                    self.passengers_in_aisle.remove(passenger)
                    passenger.is_seated = True
                else:
                    next_row = self.rows[passenger.current_row + 1]
                    # row_req = self.get_row_space(next_row)
                    with next_row.room.request() as row_req:
                        yield row_req

                        row_to_release = self.rows[passenger.current_row]
                        self.release_row(row_to_release)
                        passenger.current_row += 1

                        walk_event = Walk(self.env, passenger)

                        self.env.process(walk_event.walk_one())
                        # yield walk_event.walk_one()
                        # walk_process = self.env.process(walk_event.walk_one())
                        # passenger.set_walk_process(walk_process)

    def is_aisle_empty(self):
        return len(self.passengers_in_aisle) == 0

    def add_passenger2(self, passenger):
        if len(self.passengers_in_aisle) <= len(self.rows):
            self.passengers_in_aisle.append(passenger)
            passenger.current_row = 1
            return True
        else:
            # self.env.process(wait(self.env))
            return False

    def step_passengers2(self):

        for passenger in self.passengers_in_aisle:
            if passenger.assigned_seat.row_number == passenger.current_row:
                load = Load(self.env, passenger)
                seat = Seat(self.env, passenger)

                self.env.process(load.load_carry_on())
                self.env.process(seat.seat_self())

                self.passengers_in_aisle.remove(passenger)
                passenger.is_seated = True
                passenger.current_row = None
            else:
                if not next_row_occupied(passenger, self.passengers_in_aisle) \
                        or self.only_passener_left(passenger):
                    passenger.current_row += 1

                    walk_event = Walk(self.env, passenger)
                    self.env.process(walk_event.walk_one())
                else:
                    self.env.process(wait(self.env))


    def only_passener_left(self, passenger):
        if len(self.passengers_in_aisle) == 1 and \
                self.passengers_in_aisle[0] == passenger:
            return True
        else:
            return False