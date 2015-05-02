from passenger_actions import Walk, Load, Seat, next_row_occupied, wait


class Aisle:
    def __init__(self, env, rows):
        self.env = env
        self.rows = rows
        self.passengers_in_aisle = []

    def is_aisle_empty(self):
        return len(self.passengers_in_aisle) == 0

    def add_passenger(self, passenger):
        if len(self.passengers_in_aisle) <= len(self.rows):
            self.passengers_in_aisle.append(passenger)
            passenger.current_row = 1
            return True
        else:
            # Assumption: a passenger needs to wait the average amount of time
            # it takes to load a carry on in order to get into a full aisle
            self.env.process(wait(self.env))
            return False

    def step_passengers(self):

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
                        or self.only_passenger_left(passenger):
                    passenger.current_row += 1

                    walk_event = Walk(self.env, passenger)
                    self.env.process(walk_event.walk_one())
                else:
                    # Passenger must wait the average time it takes to load
                    # a carry on in order to continue walking
                    self.env.process(wait(self.env))

    def only_passenger_left(self, passenger):
        if len(self.passengers_in_aisle) == 1 and \
                self.passengers_in_aisle[0] == passenger:
            return True
        else:
            return False