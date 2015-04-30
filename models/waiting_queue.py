from Queue import Queue


class WaitingQueue(Queue):

    def __init__(self, *args, **kwargs):
        Queue.__init__(self, *args, **kwargs)

    def add_passengers(self, passengers):
        for passenger in passengers:
            self.put(passenger)