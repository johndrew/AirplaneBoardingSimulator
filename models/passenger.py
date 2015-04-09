from simpy import Process


class Passenger:

    def __init__(self, env, seat):
        """
            Represents a passenger boarding the airplane.

            Passengers:
                - walk to seat
                - load carry on
                - sit down

            Variables:
                - waiting in line
                - loading carry on away from seat
                - passenger has to unseat for this passenger to seat
            """
        self.env = env
        self.action = env.process(self.run())
        self.assigned_seat = seat

    def run(self):
        yield self.env.process(self.walk_aisle())

    def walk_aisle(self):
        print 'walking'
        yield self.env.timeout(5)

        print 'waiting'
        yield self.env.timeout(2)