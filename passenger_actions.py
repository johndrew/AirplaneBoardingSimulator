from simpy import Event


class Walk(Event):

    def __init__(self, env, passenger):
        super(Walk, self).__init__(env)
        self.passenger = passenger

        # self.trigger(Load)

    def walk_aisle(self):
        print 'passenger %s is walking' % self.passenger.id

        for i in range(1, self.passenger.airplane.get_number_of_rows()):
            yield self.walk_one_row()
            if self.passenger.assigned_seat.get_row_number() == i:
                print 'passenger %s has reached assigned seat %s' % \
                      (self.passenger.id,
                       self.passenger.assigned_seat)
                break

    def walk_one_row(self):
        """
        Simulates a passenger walking a single row.
        """
        print 'passenger %s is walking a row' % self.passenger.id
        return self.env.timeout(self.passenger.walking_speed)


class Load(Event):

    def __init__(self, env, passenger):
        super(Load, self).__init__(env)
        self.passenger = passenger

    def load_carry_on(self):
        """
        Process of a passenger loading a carry on item.

        It is assumed that each passenger has only 1 carry on and that no
        passenger does not have a carry on.

        Initially it is assumed that there is room for every passenger's
        bags in the overhead compartment directly above th passenger's seat
        """
        print 'passenger %s is loading a carry on item' % self.passenger.id
        yield self.env.timeout(self.passenger.loading_speed)


class StopPassengers(Event):

    def __init__(self, env, passengers):
        super(StopPassengers, self).__init__(env)
        self.passengers = passengers
        # self.action = env.process(self.interrupt_passengers())

    def interrupt_passengers(self, *args):
        print 'interrupting other passengers'
        for passenger in self.passengers:
            yield passenger.stop_walking()


def get_other_passengers(passenger, passengers):
        others = list(passengers)
        others.remove(passenger)
        return others