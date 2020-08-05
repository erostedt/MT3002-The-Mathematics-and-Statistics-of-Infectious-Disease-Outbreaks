from Project2.person import *
from Project2.simulator import Simulator
from Project2.building import Building
from Project2.world import World
import random as rnd

if __name__ == '__main__':
    world_size = (100, 100)
    num_people = 100

    popdist = (0.1, 0.6, 0.3)   # Goes to school, works, other such as infants and elderly.

    num_young, num_workers, num_other = [int(num_people * prop) for prop in popdist]

    avg_persons_per_household = 4
    avg_pupils_per_school = 10
    avg_persons_per_workplace = 20
    num_other_buildings = 10

    random_pos = lambda _: (rnd.uniform(0, world_size[0]), rnd.uniform(0, world_size[1]))

    homes = [Building(pos=random_pos(None), _type='Home', tightness=0.9) for i in range(num_people // avg_persons_per_household)]
    schools = [Building(pos=random_pos(None), _type='School', tightness=0.7) for i in range(num_young // avg_pupils_per_school)]
    works = [Building(pos=random_pos(None), _type='Work', tightness=0.5) for i in range(num_workers // avg_persons_per_workplace)]

    # Starts at home:
    home_which_people_live_in = [rnd.choice(homes) for person in range(num_people)]

    youngs = [Worker(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=1,
                     infection_dist=2, infection_prob=0.5, symptom_delay=rnd.gauss(7, 1),
                     time_until_recovery=rnd.gauss(14, 2), home=home_which_people_live_in[person],
                     work=rnd.choice(schools)) for person in range(0, num_young)]

    workers = [Worker(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=1,
                      infection_dist=2, infection_prob=0.5, symptom_delay=rnd.gauss(7, 1),
                      time_until_recovery=rnd.gauss(14, 2), home=home_which_people_live_in[person],
                      work=rnd.choice(works)) for person in range(num_young, num_young + num_workers)]

    others = [QuarantinePerson(infected=False, starting_pos=home_which_people_live_in[person].pos, speed=1,
                               infection_dist=2, infection_prob=0.5, symptom_delay=rnd.gauss(7, 1),
                               time_until_recovery=rnd.gauss(14, 2), home=home_which_people_live_in[person],
                               work=None) for person in range(num_young + num_workers,
                                                              num_young + num_workers + num_other)]

    persons = youngs + workers + others

    _infected = rnd.randint(0, num_people)
    persons[_infected].infected = True

    other_buildings = [Building(pos=random_pos(None), _type='Other', tightness=rnd.random()) for _ in
                       range(num_other_buildings)]

    world = World(world_size=world_size, persons=persons, buildings=homes + schools + works)

    # Make people aware of rest of world:
    for person in world.persons:
        person.world = world

    sim = Simulator(world=world, sim_time=24 * 50, dt=0.5)

    immunes = 0
    symptomatic = 0
    infected = 0
    never_infected = 0
    sim.simulate(disp=True)
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

