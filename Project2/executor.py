import Project2.person as pers
import random as rnd
import Project2.simulator as simu

if __name__ == '__main__':
    persons = [pers.RandomPerson(infected=False, infection_dist=10, infection_prob=0.5, speed=5,
                                 starting_pos=[rnd.uniform(0, 100), rnd.uniform(0, 100)],
                                 symptom_delay=rnd.randint(10, 20),
                                 time_until_recovery=rnd.randint(20, 30)) for person in range(99)]

    persons.append(
        pers.RandomPerson(infected=True, infection_dist=10, infection_prob=0.5, speed=5,
                          starting_pos=[rnd.uniform(0, 100), rnd.uniform(0, 100)],
                          symptom_delay=rnd.randint(3, 6),
                          time_until_recovery=rnd.randint(20, 30))
    )

    sim = simu.Simulator(persons=persons, world_shape=(100, 100))

    immunes = 0
    symptomatic = 0
    infected = 0
    never_infected = 0
    sim.simulate(disp=True)
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

