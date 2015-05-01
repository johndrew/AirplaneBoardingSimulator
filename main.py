from random import shuffle
from simpy import Environment
from boarding_algorithms import BoardingAlgorithm
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
    for j in range(0, boeing_737.get_number_of_seats()):
        passenger = Passenger(env, seats[j], boeing_737)
        passengers.append(passenger)

    _algorithms = BoardingAlgorithm(env, boeing_737, passengers)

    return boeing_737, passengers, _algorithms


def setup_test():
    test_airplane = Airplane(env, 'Test Airplane', 3, 3, 1, False)
    seats = test_airplane.get_seats()
    passengers = []

    for j in range(0, test_airplane.get_number_of_seats()):
        passenger = Passenger(env, seats[j], test_airplane)
        passengers.append(passenger)

    _algorithms = BoardingAlgorithm(env, test_airplane, passengers)

    return test_airplane, passengers, _algorithms


def board(e, passengers):
    shuffle(passengers)
    for p in passengers:
        e.process(p.board())


if __name__ == "__main__":
    env = Environment()
    env.total_time = 0
    # airplane, passenger_list, algorithms = setup_test()
    airplane, passenger_list, algorithms = setup()

    # algorithms.random_ordering()
    # algorithms.back_to_front()
    # algorithms.front_to_back()
    algorithms.steffen_optimal()

    times = []
    total_trials = 1000

    for i in range(0, total_trials):
        env.run()
        times.append(env.total_time)
        # times.append(env.now)

    print "Average time for %s runs: %s" % (total_trials,
                                            reduce(lambda x, y: x + y, times)
                                            / len(times))