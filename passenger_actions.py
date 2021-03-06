from simpy import Event, Interrupt
from constants import time_to_load_carry_on as loading_speeds


class Walk(Event):

    def __init__(self, env, passenger):
        super(Walk, self).__init__(env)
        self.passenger = passenger
        self.ok = True  # Have to set the ok value to be triggered

    def walk_aisle(self):
        return self.passenger.walk_aisle()

    def walk_one(self):
        yield self.passenger.walk_one_row()


class Load(Event):

    def __init__(self, env, passenger):
        super(Load, self).__init__(env)
        self.passenger = passenger
        self.ok = True  # Have to set the ok value to be triggered

    def load_carry_on(self):
        return self.passenger.load_carry_on()

    def __call__(self, *args, **kwargs):
        """
        Used when this Event is triggered by another Event
        """
        self.env.process(self.load_carry_on())


class Seat(Event):

    def __init__(self, env, passenger):
        super(Seat, self).__init__(env)
        self.passenger = passenger
        self.ok = True  # Have to set the ok value to be triggered

    def seat_self(self):
        yield self.passenger.seat_self()

    def __call__(self, *args, **kwargs):
        """
        Used when this Event is triggered by another Event
        """
        self.env.process(self.seat_self())


def get_other_passengers(passenger, passengers):
    others = list(passengers)
    others.remove(passenger)
    return others


def are_passengers_seated(passengers):
    for passenger in passengers:
        if not passenger.is_seated:
            return False

    return True


def next_row_occupied(current_passenger, passengers):
    current_row = current_passenger.current_row

    for passenger in passengers:
        if current_passenger == passenger or not current_passenger.current_row:
            continue
        elif passenger.current_row == current_row + 1:
            return True

    return False


def wait(env):
    loading_average = (loading_speeds['minimum'] + loading_speeds['maximum']) \
                      / 2
    waiting_time = (loading_average + loading_speeds['average']) / 2
    env.total_time += waiting_time
    yield env.timeout(waiting_time)