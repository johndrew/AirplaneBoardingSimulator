from Queue import Queue
import simpy


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
            passengers += self.get()
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
        """"""
        passengers = self.unpack_aisle()
        for passenger in passengers:
            # try:
            self.env.process(passenger.walk_aisle())
            # except simpy.Interrupt:
