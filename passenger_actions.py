from simpy import Event


class Walk(Event):

    def __init__(self, env, passenger):
        super(Walk, self).__init__(env)
        self.passenger = passenger
        self.ok = True  # Have to set the ok value to be triggered

        # load = Load(env, passenger)
        # self.trigger(load)
        # self.callbacks.append(load)

    def walk_aisle(self):
        return self.passenger.walk_aisle()


class Load(Event):

    def __init__(self, env, passenger):
        super(Load, self).__init__(env)
        self.passenger = passenger
        self.ok = True  # Have to set the ok value to be triggered

        # seat = Seat(env, passenger)
        # self.trigger(seat)
        # self.callbacks.append(seat)

    def load_carry_on(self):
        print 'poop'
        yield self.passenger.load_carry_on()

    def __call__(self, *args, **kwargs):
        """
        Used when this Event is triggered by another Event
        """
        print 'load'
        self.load_carry_on()


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
        print 'seat'
        self.seat_self()


class StopPassengers(Event):

    def __init__(self, env, passengers):
        super(StopPassengers, self).__init__(env)
        self.passengers = passengers
        self.ok = True  # Have to set the ok value to be triggered

    def interrupt_passengers(self):
        print 'interrupting other passengers'
        for passenger in self.passengers:
            if passenger.walk_process:
                passenger.walk_process.interrupt()

    def __call__(self, *args, **kwargs):
        """
        Used when this Event is triggered by another Event
        """
        print 'stop'
        self.interrupt_passengers()


# class StartPassengers(Event):
#
#     def __init__(self, env, passengers):
#         super(StartPassengers, self).__init__(env)
#         self.passengers = passengers
#
#     def resume_passenger_walking(self, *args):
#         print 'resuming other passengers'


def get_other_passengers(passenger, passengers):
    others = list(passengers)
    others.remove(passenger)
    return others
