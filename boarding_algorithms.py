from random import shuffle
from models.passenger import get_seat_column, get_even_row_passengers, \
    get_odd_row_passengers
from models.waiting_queue import WaitingQueue
from passenger_actions import are_passengers_seated


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

            for g in groups:
                shuffle(g)

            return groups

        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        for group in make_groups():
            self.board_passengers(group, waiting_queue, aisle)

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

        def make_groups():
            left_side = get_seat_column('A', self.passengers) + \
                        get_seat_column('B', self.passengers) + \
                        get_seat_column('C', self.passengers)
            right_side = get_seat_column('D', self.passengers) + \
                         get_seat_column('E', self.passengers) + \
                         get_seat_column('F', self.passengers)
            group_1 = get_even_row_passengers(left_side)
            group_2 = get_even_row_passengers(right_side)
            group_3 = get_odd_row_passengers(left_side)
            group_4 = get_odd_row_passengers(right_side)

            groups = [group_1, group_2, group_3, group_4]

            for g in groups:
                g.sort(key=lambda x: x.get_row_number())

            return groups

        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        for group in make_groups():
            self.board_passengers(group, waiting_queue, aisle)

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
        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        self.board_passengers(self.passengers, waiting_queue, aisle)

    def back_to_front(self):
        """
        Implementation of the boarding method typically used on commercial
        aircraft. Jason Steffen identifies this as the second to worst
        boarding method.
        """
        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        self.passengers.reverse()
        self.board_passengers(self.passengers, waiting_queue, aisle)

    def random_ordering(self):
        """
        Implementation of a random seating where any passenger can board in
        any order
        """
        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        shuffle(self.passengers)
        self.board_passengers(self.passengers, waiting_queue, aisle)

    def block_boarding(self):
        """
        Boards passengers in three equal or nearly equal sized groups. If there
        were 12 rows in a plane, first the back 4 rows would board, then the
        front 4, and finally the middle 4. Order within the groups is random.

        Note: this method is not dynamic. It is hardcoded to work with a
        Boeing 737.
        """
        def make_groups():
            group_1 = [x for x in self.passengers if x.get_row_number() >= 13]
            group_2 = [x for x in self.passengers if x.get_row_number() <= 7]
            group_3 = [x for x in self.passengers if x.get_row_number() > 7 <
                       13]

            groups = [group_1, group_2, group_3]

            for g in groups:
                shuffle(g)

            return groups

        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        for group in make_groups():
            self.board_passengers(group, waiting_queue, aisle)

    def wilma_method(self):
        """
        Boards all window seat passengers first, followed by middle seats, and
        finally the aisle seats.

        Order within each group is random.
        """
        def make_groups():
            group_1 = get_seat_column('A', self.passengers) + \
                      get_seat_column('F', self.passengers)
            group_2 = get_seat_column('B', self.passengers) + \
                      get_seat_column('E', self.passengers)
            group_3 = get_seat_column('C', self.passengers) + \
                      get_seat_column('D', self.passengers)

            groups = [group_1, group_2, group_3]

            for g in groups:
                shuffle(g)

            return groups

        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        for group in make_groups():
            self.board_passengers(group, waiting_queue, aisle)

    def kautzka_method(self):
        """
        Combines parts of the Wilma method, back-to-front boarding, and
        parallel carry-on loading as is done in Steffen's optimal method.

        It begins with the window and middle seats of the right side, even
        rows. It then does the same on the left side. Next, the aisle seats on
        the right are boarded, followed by the left side. Finally, this same
        process is repeated, but with the odd numbered rows.
        """
        def make_groups():
            group_1 = get_even_row_passengers(
                get_seat_column('F', self.passengers) +
                get_seat_column('E', self.passengers))
            group_2 = get_even_row_passengers(
                get_seat_column('A', self.passengers) +
                get_seat_column('B', self.passengers))
            group_3 = get_even_row_passengers(get_seat_column('D',
                                                              self.passengers))
            group_4 = get_even_row_passengers(get_seat_column('C',
                                                              self.passengers))
            group_5 = get_odd_row_passengers(
                get_seat_column('F', self.passengers) +
                get_seat_column('E', self.passengers))
            group_6 = get_odd_row_passengers(
                get_seat_column('A', self.passengers) +
                get_seat_column('B', self.passengers))
            group_7 = get_odd_row_passengers(get_seat_column('D',
                                                              self.passengers))
            group_8 = get_odd_row_passengers(get_seat_column('C',
                                                              self.passengers))

            groups = [group_1, group_2, group_3, group_4, group_5, group_6,
                      group_7, group_8]

            for g in groups:
                g.sort(key=lambda x: x.get_row_number())
                g.reverse()

            return groups

        aisle = self.airplane.get_aisle()
        waiting_queue = WaitingQueue()

        for group in make_groups():
            self.board_passengers(group, waiting_queue, aisle)

    def board_passengers(self, passengers, waiting_queue, aisle):
        """
        Takes a list of passengers, a queue for passengers waiting to enter the
        airplane, and an aisle object from the airplane.

        Boards the passengers
        """
        waiting_queue.add_passengers(passengers)

        # Add the first passenger to the aisle
        p = waiting_queue.get()
        aisle.add_passenger2(p)

        # Cycle through passengers waiting in queue until all are in aisle
        while not waiting_queue.empty():
            aisle.step_passengers2()

            passenger = waiting_queue.get()
            added = aisle.add_passenger2(passenger)
            if not added:
                waiting_queue.put(passenger)

        # Keep moving passengers until all are seated
        while not are_passengers_seated(passengers):
            aisle.step_passengers2()