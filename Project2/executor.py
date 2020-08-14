from person import *
from simulator import Simulator
from building import Building
from world import World
import random as rnd

if __name__ == '__main__':

    def random_world(world_size=(1000, 1000), num_people=500, num_initially_infected=1,  pop_distr=(0.6, 0.3, 0.1),
                     infection_prob=0.02, infection_dist=2, speed=10, avg_persons_per_household=4,
                     avg_pupils_per_school=100, avg_persons_per_workplace=50, tightness=(0.9, 0.3, 0.1),
                     delay=(rnd.gauss, 7, 1), recovery=(rnd.gauss, 14, 2)):

        """
        Constructs a society with Random walkers.
        :param world_size: Size of the world.
        :param num_people: Number of people in the world.
        :param num_initially_infected: Number of initially infected
        :param pop_distr: Proportions of people. Eg. (0.6, 0.3, 0.1) means 60% workers, 30% students and 10% others.
        :param infection_prob: Probability of infecting.
        :param infection_dist: Max distance infection can spread.
        :param speed: Speed of person.
        :param avg_persons_per_household: Average number people living in a house.
        :param avg_pupils_per_school: Average number of students per school.
        :param avg_persons_per_workplace: Average number of people per work place.
        :param tightness: Tightness scaling parameter to tackle differences in sparseness and denseness in different buildings.
        :param delay: Delay information, (density function, parameter 1, parameter 2)
        :param recovery: Recovery information, (density function, parameter 1, parameter 2)
        :return: World.
        """
        world_size = world_size
        num_people = num_people

        random_pos = lambda _: (rnd.uniform(0, world_size[0]), rnd.uniform(0, world_size[1]))

        delay_func, delay_param1, delay_param2 = delay
        recovery_func, recovery_param1, recovery_param2 = recovery

        persons = [RandomPerson(infected=False, starting_pos=random_pos(None), speed=speed, infection_dist=infection_dist,
                                infection_prob=infection_prob, symptom_delay=delay_func(delay_param1, delay_param2),
                                time_until_recovery=recovery_func(recovery_param1, recovery_param2), home=None,
                                work=None) for _ in range(num_people)]

        rnd.shuffle(persons)
        for i in range(num_initially_infected):
            persons[i].gets_infected(time=0)

        return World(world_size=world_size, persons=persons, buildings=[])

    def quarantine_world(world_size=(1000, 1000), num_people=500, num_initially_infected=1, pop_distr=(0.6, 0.3, 0.1),
                         infection_prob=0.02, infection_dist=2, speed=10, avg_persons_per_household=4,
                         avg_pupils_per_school=100, avg_persons_per_workplace=50, tightness=(0.9, 0.3, 0.1),
                         delay=(rnd.gauss, 7, 1), recovery=(rnd.gauss, 14, 2)):

        """
        Constructs a society with Quarantine persons.
        :param world_size: Size of the world.
        :param num_people: Number of people in the world.
        :param num_initially_infected: Number of initially infected.
        :param pop_distr: Proportions of people. Eg. (0.6, 0.3, 0.1) means 60% workers, 30% students and 10% others.
        :param infection_prob: Probability of infecting.
        :param infection_dist: Max distance infection can spread.
        :param speed: Speed of person.
        :param avg_persons_per_household: Average number people living in a house.
        :param avg_pupils_per_school: Average number of students per school.
        :param avg_persons_per_workplace: Average number of people per work place.
        :param tightness: Tightness scaling parameter to tackle differences in sparseness and denseness in different buildings.
        :param delay: Delay information, (density function, parameter 1, parameter 2)
        :param recovery: Recovery information, (density function, parameter 1, parameter 2)
        :return: World.
        """

        world_size = world_size
        num_people = num_people

        random_pos = lambda _: (rnd.uniform(0, world_size[0]), rnd.uniform(0, world_size[1]))

        homes = [Building(pos=random_pos(None), _type='Home', tightness=tightness[0])
                 for _ in range(max(1, num_people // avg_persons_per_household))]

        # Starts at home:
        home_which_people_live_in = [rnd.choice(homes) for _ in range(num_people)]

        delay_func, delay_param1, delay_param2 = delay
        recovery_func, recovery_param1, recovery_param2 = recovery

        persons = [QuarantinePerson(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=speed,
                                    infection_dist=infection_dist, infection_prob=infection_prob,
                                    symptom_delay=delay_func(delay_param1, delay_param2),
                                    time_until_recovery=recovery_func(recovery_param1, recovery_param2),
                                    home=home_which_people_live_in[person], work=None)
                   for person in range(num_people)]

        rnd.shuffle(persons)
        for i in range(num_initially_infected):
            persons[i].gets_infected(time=0)

        return World(world_size=world_size, persons=persons, buildings=homes)

    def worker_world(world_size=(1000, 1000), num_people=500, num_initially_infected=1, pop_distr=(0.6, 0.3, 0.1),
                     infection_prob=0.02, infection_dist=2, speed=10, avg_persons_per_household=4,
                     avg_pupils_per_school=100, avg_persons_per_workplace=50, tightness=(0.9, 0.3, 0.1),
                     delay=(rnd.gauss, 7, 1), recovery=(rnd.gauss, 14, 2)):

        """
        Constructs a society with workers, students and others.
        :param world_size: Size of the world.
        :param num_people: Number of people in the world.
        :param num_initially_infected: Number of initially infected.
        :param pop_distr: Proportions of people. Eg. (0.6, 0.3, 0.1) means 60% workers, 30% students and 10% others.
        :param infection_prob: Probability of infecting.
        :param infection_dist: Max distance infection can spread.
        :param speed: Speed of person.
        :param avg_persons_per_household: Average number people living in a house.
        :param avg_pupils_per_school: Average number of students per school.
        :param avg_persons_per_workplace: Average number of people per work place.
        :param tightness: Tightness scaling parameter to tackle differences in sparseness and denseness in different buildings.
        :param delay: Delay information, (density function, parameter 1, parameter 2)
        :param recovery: Recovery information, (density function, parameter 1, parameter 2)
        :return: World.
        """

        world_size = world_size
        num_people = num_people

        pop_distr = pop_distr   # Proportion that oes to school, works, other such as infants and elderly.

        num_young, num_workers, num_other = [int(num_people * prop) for prop in pop_distr]

        random_pos = lambda _: (rnd.uniform(0, world_size[0]), rnd.uniform(0, world_size[1]))

        homes = [Building(pos=random_pos(None), _type='Home', tightness=tightness[0])
                 for _ in range(max(1, num_people // avg_persons_per_household))]
        schools = [Building(pos=random_pos(None), _type='School', tightness=tightness[1])
                   for _ in range(max(1, num_young // avg_pupils_per_school))]
        works = [Building(pos=random_pos(None), _type='Work', tightness=tightness[2])
                 for _ in range(max(1, num_workers // avg_persons_per_workplace))]

        # Starts at home:
        home_which_people_live_in = [rnd.choice(homes) for _ in range(num_people)]

        delay_func, delay_param1, delay_param2 = delay
        recovery_func, recovery_param1, recovery_param2 = recovery

        youngs = [Worker(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=speed,
                         infection_dist=infection_dist, infection_prob=infection_prob,
                         symptom_delay=delay_func(delay_param1, delay_param2),
                         time_until_recovery=recovery_func(recovery_param1, recovery_param2),
                         home=home_which_people_live_in[person],
                         work=rnd.choice(schools)) for person in range(0, num_young)]

        workers = [Worker(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=speed,
                          infection_dist=infection_dist, infection_prob=infection_prob,
                          symptom_delay=delay_func(delay_param1, delay_param2),
                          time_until_recovery=recovery_func(recovery_param1, recovery_param2),
                          home=home_which_people_live_in[person], work=rnd.choice(works))
                   for person in range(num_young, num_young + num_workers)]

        others = [QuarantinePerson(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=speed,
                                   infection_dist=infection_dist, infection_prob=infection_prob,
                                   symptom_delay=delay_func(delay_param1, delay_param2),
                                   time_until_recovery=recovery_func(recovery_param1, recovery_param2),
                                   home=home_which_people_live_in[person], work=None)
                  for person in range(num_young + num_workers, num_young + num_workers + num_other)]

        persons = youngs + workers + others

        rnd.shuffle(persons)
        for i in range(num_initially_infected):
            persons[i].gets_infected(time=0)

        return World(world_size=world_size, persons=persons, buildings=homes + schools + works)

    ####################################################################################################################
    # MODIFY FROM HERE!
    R_0 = 2.5

    dt = 0.5
    tau = 14 * 24

    kwargs = {
        'world_size': (300, 300),
        'num_people': 432,
        'num_initially_infected': 50,
        'pop_distr': (0.6, 0.3, 0.1),
        'infection_prob': dt * (R_0 / tau),  # R_0 = beta * tau -> beta = R_0 / tau, to adjust for
        # different step sizes we multiply by dt
        'infection_dist': 1.9,    # maximum is 1.9m since 2m are advised distancing.
        'speed': dt * 100,    # Moves 0.1km/h when random walking
        # (might seem slow, but may be reasonable since people usually stops and sit down most time when outside)
        'avg_persons_per_household': 4,
        'avg_pupils_per_school': 100,
        'avg_persons_per_workplace': 50,
        'tightness': (0.8, 0.3, 0.1),   # Homes are usually very tight, then schools are tighter than companies.
        'delay': (rnd.gauss, 7*24, 1 * 24),
        'recovery': (rnd.gauss, tau, 2 * 24)
    }

    sim = Simulator(world=quarantine_world(**kwargs))

    immunes = 0
    symptomatic = 0
    infected = 0
    never_infected = 0
    sim.simulate(time=0, dt=dt, sim_time=50 * 24, disp=False, see_progress=True)
    sim.plot_distributions()
    for person in sim.world.persons:
        if person.immune:
            immunes += 1

        elif person.symptomatic:
            symptomatic += 1

        elif person.infected:
            infected += 1

        else:
            never_infected += 1

    print('Immunes: ', immunes)
    print('Symptomatic:', symptomatic)
    print('Infected:', infected)
    print('Never infected:', never_infected)

