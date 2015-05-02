from random import shuffle
from numpy import array
from scipy.stats import f_oneway
from simpy import Environment
from boarding_algorithms import BoardingAlgorithm
from models.airplane import Airplane
from models.passenger import Passenger


def setup():
    """
    Initializes the models and processes before the Environment is run
    """
    env.total_time = 0
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


def run_trials(environ, total):
    times = []
    total_trials = total

    for i in range(0, total_trials):
        environ.run()
        times.append(environ.total_time)

    return times


def reduce_by_averaging(trials, total, amount):
    """

    """
    new_averages = []

    for i in range(0, total):
        if i % amount == 0:
            new_averages.append(reduce(lambda x, y: x + y, trials[i:i+amount]) / \
                          amount)

    return new_averages


def get_mean(trials):
    return reduce(lambda x, y: x + y, trials) / len(trials)


if __name__ == "__main__":
    env = Environment()
    all_times = {}
    total_trials = 1000

    airplane, passenger_list, algorithms = setup()
    algorithms.random_ordering()
    all_times['Random'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.front_to_back()
    all_times['Front-To-Back'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.back_to_front()
    all_times['Back-To-Front'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.steffen_optimal()
    all_times['Steffen-Optimal'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.steffen_modified_optimal()
    all_times['Steffen-Modefied'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.block_boarding()
    all_times['Block-Boarding'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.wilma_method()
    all_times['Wilma-Method'] = run_trials(env, total_trials)

    airplane, passenger_list, algorithms = setup()
    algorithms.kautzka_method()
    all_times['Kautzka-Method'] = run_trials(env, total_trials)

    print
    print 'AVERAGES:'
    for algorithm in all_times.keys():
        times = all_times[algorithm]
        print "     %s: average time for %s runs = %s" % \
            (algorithm, total_trials, get_mean(times))

    random = array(all_times['Random'])
    front_to_back = array(all_times['Front-To-Back'])
    back_to_front = array(all_times['Back-To-Front'])
    steffen_optimal = array(all_times['Steffen-Optimal'])
    steffen_modefied = array(all_times['Steffen-Modefied'])
    block_method = array(all_times['Block-Boarding'])
    wilma_method = array(all_times['Wilma-Method'])
    kautzka_method = array(all_times['Kautzka-Method'])

    results = f_oneway(random, front_to_back, back_to_front,
                                steffen_optimal, steffen_modefied,
                                block_method, wilma_method, kautzka_method)

    print
    print 'ANALYSIS OF VARIANCE (ANOVA) RESULTS: F=%s (p=%s)' % \
          (results[0], results[1])