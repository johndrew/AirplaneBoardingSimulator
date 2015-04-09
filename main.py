from simpy import Environment
from models.airplane import Airplane
from models.passenger import Passenger
from models.seat import Seat


def setup(env):
    """
    Initializes the models and processes before the Environment is run
    """
    boeing_737 = Airplane(env, 'Boeing 737', 20, 6, 1, False)
    # seat = Seat(22, 'F')
    # p = Passenger(env, seat)


if __name__ == "__main__":
    env = Environment()
    setup(env)
    env.run(15)

    print 'hello'