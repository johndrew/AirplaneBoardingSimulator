from simpy import Resource
from passenger_actions import Walk, Load, Seat


class Aisle:
    def __init__(self, env, rows):
        self.env = env
        self.rows = rows
        self.space_to_walk = Resource(env, capacity=len(rows))
        self.passengers_in_aisle = []

    def add_passenger(self, passenger):

        # Check if there is room in the aisle
        with self.space_to_walk.request() as req:
            yield req

            self.passengers_in_aisle.append(passenger)
            passenger.current_row = 1
            yield self.rows[1].room.request()

    def walk_passengers(self):

        # Cycle through passengers in aisle until all are seated
        for passenger in self.passengers_in_aisle:
            walk_event = Walk(self.env, passenger)

            walk_process = self.env.process(walk_event.walk_aisle())
            passenger.set_walk_process(walk_process)

    def step_passengers(self):

        # Cycle through passengers in aisle until all have moved one
        for passenger in self.passengers_in_aisle:
            if passenger.assigned_seat.row_number == passenger.current_row:
                self.rows[passenger.current_row].room.release()

                load = Load(self.env, passenger)
                seat = Seat(self.env, passenger)


            else:
                yield self.rows[passenger.current_row + 1].room.request()

                self.rows[passenger.current_row].room.release()
                passenger.current_row += 1

                walk_event = Walk(self.env, passenger)

                walk_process = self.env.process(walk_event.walk_one())
                passenger.set_walk_process(walk_process)