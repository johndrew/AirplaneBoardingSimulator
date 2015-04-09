from simpy import Environment
from models.airplane import Airplane
from models.passenger import Passenger


def setup():
    """
    Initializes the models and processes before the Environment is run
    """
    boeing_737 = Airplane(env, 'Boeing 737', 20, 6, 1, False)
    passengers = []

    for i in range(0, boeing_737.get_number_of_seats()):
        seats = boeing_737.get_seats()
        passenger = Passenger(env, seats[i], boeing_737)
        passengers.append(passenger)


if __name__ == "__main__":
    env = Environment()
    setup()
    env.run(15)

    print 'hello'