import uuid
from random import uniform
from constants import time_to_pass_one_row as walking_speeds, \
    time_to_load_carry_on as loading_speeds, \
    time_to_install_in_seat as seating_speeds


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
        self.walking_speed = get_process_speed(walking_speeds)
        self.loading_speed = get_process_speed(loading_speeds)
        self.seating_speed = get_process_speed(seating_speeds)
        self.airplane = airplane

    def board(self):
        yield self.env.process(self.walk_aisle())
        yield self.env.process(self.load_carry_on())

    def walk_aisle(self):
        print 'passenger %s is walking' % self.id

        for i in range(1, self.airplane.get_number_of_rows()):
            self.walk_one_row()
            if self.assigned_seat.get_row_number() == i:
                print 'passenger %s has reached assigned seat' % self.id
                break

    def walk_one_row(self):
        """
        Simulates a passenger walking a single row.
        """
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

    def seat_self(self):
        """
        Process of a passenger seating him or herself.
        """
        print 'passenger %s is now seating' % self.id
        yield self.env.timeout(self.seating_speed)

    def get_assigned_seat(self):
        return self.assigned_seat

    def get_row_number(self):
        return self.assigned_seat.get_row_number()

    def __str__(self):
        return "Passenger(seat=%s%s)" % (self.assigned_seat.get_row_number(),
                                         self.assigned_seat.get_position())


def get_process_speed(speed_dict):
    """
    Returns a speed for the action that speed_dict represents.

    Gets a random value between the min and max of speed_dict, and then
    takes the average of this random value with the average of speed_dict.
    Returns this value.
    """
    random_speed = uniform(speed_dict['minimum'],
                           speed_dict['maximum'])

    # below calculation gets a random value closer to the average
    return (random_speed + speed_dict['average']) / 2


def get_seat_column(label, passengers):
    """
    Returns all passengers with a seat in the given seat column.

    A seat column is one of the position_labels in constants.py
    """
    return [p for p in passengers if p.get_assigned_seat().get_position()
            == label]


def get_even_row_passengers(passengers):
    """
    Returns all passengers witch a seat in an even row.
    """
    return [p for p in passengers if p.get_assigned_seat().get_row_number()
            % 2 == 0]


def get_odd_row_passengers(passengers):
    """
    Returns all passengers witch a seat in an even row.
    """
    return [p for p in passengers if p.get_assigned_seat().get_row_number()
            % 2 != 0]