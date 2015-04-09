from random import shuffle
from simpy import Environment
from models.airplane import Airplane
from models.passenger import Passenger


def setup():
    """
    Initializes the models and processes before the Environment is run
    """
    boeing_737 = Airplane(env, 'Boeing 737', 20, 6, 1, False)
    boeing_737.make_rows()
    seats = boeing_737.get_seats()
    passengers = []

    # create a passenger for every seat on the plane
    for i in range(0, boeing_737.get_number_of_seats()):
        passenger = Passenger(env, seats[i], boeing_737)
        passengers.append(passenger)

    return boeing_737, passengers


def board(e, passengers):
    shuffle(ps)
    print passengers is None
    for p in passengers:
        e.process(p.board())

if __name__ == "__main__":
    env = Environment()
    airplane, ps = setup()

    board(env, ps)

    env.run()

    print
    print 'hello at %s' % env.now