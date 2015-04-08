from simpy import Environment
from models.passenger import Passenger


if __name__ == "__main__":
    env = Environment()
    p = Passenger(env)
    env.run(15)

    print 'hello'