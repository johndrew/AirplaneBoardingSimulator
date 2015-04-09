import uuid
from random import uniform
from constants import time_to_pass_one_row as walking_speeds, \
    time_to_load_carry_on as loading_speeds


class Passenger:

    def __init__(self, env, seat, airplane):
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
        # self.action = env.process(self.run())
        self.assigned_seat = seat
        self.id = uuid.uuid4()
        self.walking_speed = get_walking_speed()
        self.loading_speed = get_loading_speed()
        self.airplane = airplane

    def board(self):
        yield self.env.process(self.walk_aisle())
        yield self.env.process(self.load_carry_on())

    def walk_aisle(self):
        print 'passenger %s is walking' % self.id

        for i in range(1, self.airplane.get_number_of_rows()):
            if self.assigned_seat.get_row_number() == i:
                print 'passenger %s has reached assigned seat' % self.id
                break
            else:
                yield self.env.timeout(self.walking_speed)

    def load_carry_on(self):
        """
        Process of a passenger loading a carry on item.

        It is assumed that each passenger has only 1 carry on and that no
        passenger does not have a carry on.

        Initially it is assumed that there is room for every passenger's
        bags in the overhead compartment directly above th passenger's seat
        """
        print 'passenger %s is loading a carry on item' % self.id
        yield self.env.timeout(self.loading_speed)


def get_walking_speed():
    """
    Returns a walking speed for this passenger.

    The speed equals how long it takes (in seconds) for a passenger to
    pass one row
    """
    random_speed = uniform(walking_speeds['minimum'],
                             walking_speeds['maximum'])

    # below calculation gets a random value closer to the average
    return (random_speed + walking_speeds['average']) / 2


def get_loading_speed():
    """
    Returns a loading speed for this passenger.

    The speed equals how long it takes (in seconds) for a passenger to load
    a carry on item in the overhead compartment.

    It is assumed there is enough room to do this
    """
    random_time = uniform(loading_speeds['minimum'],
                          loading_speeds['maximum'])

    # below calculation gets a random value closer to the average
    return (random_time + loading_speeds['average']) / 2