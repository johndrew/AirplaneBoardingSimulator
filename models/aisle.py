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

        for passenger in passengers:
            print "passenger %s is %s and is at %s" % \
                  (passenger.id, passengers.index(passenger),
                   passenger.assigned_seat)

            passenger_walk = Walk(self.env, passenger)

            stop = StopPassengers(self.env, get_other_passengers(passenger,
                                                                 passengers))

            # passenger_walk.trigger(stop)
            # passenger_walk.callbacks.insert(0, stop)

            walk_process = self.env.process(passenger_walk.walk_aisle())
            passenger.set_walk_process(walk_process)

    def remove_from_aisle(self, passenger):
        self.get(passenger)
