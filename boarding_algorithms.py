from Queue import Queue
from models.passenger import get_seat_column, get_even_row_passengers, \
    get_odd_row_passengers


class BoardingAlgorithm:

    def __init__(self, env, airplane, passengers):
        """"""
        self.env = env
        self.airplane = airplane
        self.passengers = passengers

    def steffen_optimal(self):
        """
        Implementation of Jason Steffen's optimal boarding algorithm

        Boarding method:
            1) window seats only
                a) left side of plane, even rows
                b) right side, even rows
                c) left side, odd rows
                d) right side, odd rows
            2) middle seats only
                a) left side of plane, even rows
                b) right side, even rows
                c) left side, odd rows
                d) right side, odd rows
            3) aisle seats only
                a) left side of plane, even rows
                b) right side, even rows
                c) left side, odd rows
                d) right side, odd rows
        """
        def make_groups():
            """
            ...

            Note: change this to make it work with bigger airplanes
            """
            group_1 = get_even_row_passengers(get_seat_column('F',
                                                              self.passengers))
            group_2 = get_even_row_passengers(get_seat_column('A',
                                                              self.passengers))
            group_3 = get_odd_row_passengers(get_seat_column('F',
                                                              self.passengers))
            group_4 = get_odd_row_passengers(get_seat_column('A',
                                                              self.passengers))
            group_5 = get_even_row_passengers(get_seat_column('E',
                                                              self.passengers))
            group_6 = get_even_row_passengers(get_seat_column('B',
                                                              self.passengers))
            group_7 = get_odd_row_passengers(get_seat_column('E',
                                                              self.passengers))
            group_8 = get_odd_row_passengers(get_seat_column('B',
                                                              self.passengers))
            group_9 = get_even_row_passengers(get_seat_column('D',
                                                              self.passengers))
            group_10 = get_even_row_passengers(get_seat_column('C',
                                                              self.passengers))
            group_11 = get_odd_row_passengers(get_seat_column('D',
                                                              self.passengers))
            group_12 = get_odd_row_passengers(get_seat_column('C',
                                                              self.passengers))

            groups = [group_1, group_2, group_3, group_4, group_5, group_6,
                      group_7, group_8, group_9, group_10, group_11, group_12]

            for group in groups:
                group.sort(key=lambda x: x.get_row_number())

            return groups

        # for group in make_groups():
        #     for passenger in group:




    def steffen_modified_optimal(self):
        """
        Implementation of Jason Steffen's optimal boarding algorithm modified
        to be more practical in real boarding situations

        Boarding method:
            1) even rows
                a) left side of the plane
                b) right side
            2) odd rows
                a) left side
                b) right side
        """

    def front_to_back(self):
        """
        Implementation of the boarding method Jason Steffen labels as having
        the worst loading time.

        Boarding method (something like this):
            1) sections 1-5
            2) sections 10-15
            3) sections 15-20
            4) sections 20-25
        """

    def back_to_front_(self):
        """
        Implementation of the boarding method typically used on commercial
        aircraft. Jason Steffen identifies this as the second to worst
        boarding method.
        """

    def random_ordering(self):
        """
        Implementation of a random seating where any passenger can board in
        any order
        """

        aisle = self.airplane.get_aisle()
        while len(self.passengers):
            passenger = self.passengers.pop()
            aisle.put(passenger)
            while not aisle.empty():
                aisle.passengers_walk_aisle()