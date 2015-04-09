
class BoardingAlgorithm:

    def __init__(self):
        """"""

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