from Queue import Queue
from passenger_actions import Walk, StopPassengers, get_other_passengers


class Aisle(Queue):
    def __init__(self, env, number_of_rows):
        Queue.__init__(self)
        self.env = env
        self.number_of_rows = number_of_rows

    def unpack_aisle(self):
        """
        Removes all of the passengers from the queue so some action can be
        performed on them.

        Queue (self) will be empty by the end of execution of this method
        """
        passengers = []
        while not self.empty():
            passengers.append(self.get())
        return passengers

    def pack_aisle(self, passengers):
        """
        Takes a list of passengers and puts them back in the queue.

        Used after unpacking the aisle.
        """
        for passenger in passengers:
            self.put(passenger)
        return self

    def passengers_walk_aisle(self):
        """

        """
        passengers = self.unpack_aisle()
        walk_events = []

        for passenger in passengers:
            print "passenger %s is %s and is at %s" % \
                  (passenger.id, passengers.index(passenger),
                   passenger.assigned_seat)
            passenger_walk = Walk(self.env, passenger)  # walk event
            walk_events.append(passenger_walk)
            others = get_other_passengers(passenger, passengers)
            stop = StopPassengers(self.env, others)
            stop.ok = True

            passenger_walk.trigger(stop)
            passenger_walk.callbacks.append(stop.interrupt_passengers)
            self.env.process(passenger_walk.walk_aisle())

        return walk_events

    def remove_from_aisle(self, passenger):
        self.get(passenger)
