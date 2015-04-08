from simpy import Process


class Passenger(Process):

    def __init__(self, env, generator):
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
        super(Passenger, self).__init__(env, generator)

    # def walk_aisle(self):
    #     yield