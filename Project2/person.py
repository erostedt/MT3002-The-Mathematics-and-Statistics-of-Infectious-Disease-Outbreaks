from abc import ABC, abstractmethod
import math
import random as rnd


class Person(ABC):

    def __init__(self, infected, starting_pos, speed, infection_dist, symptom_delay, time_until_recovery):
        """
        Initialization class for a person.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param speed: Persons walking speed.
        :param starting_pos: Persons starting position.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        """
        self.infected = infected
        self.pos = starting_pos
        self.speed = speed

        self.infection_dist = infection_dist

        self.symptom_delay, self.time_until_recovery = symptom_delay, time_until_recovery

        self.infected_time = 0 if infected else float('Inf')
        self.symptom_time = self.symptom_delay if infected else float('Inf')
        self.immune_time = self.time_until_recovery if infected else float('Inf')

        self.infected = infected
        self.symptomatic = False
        self.immune = False

        self.exposures = []         # All exposures.
        self.known_exposures = []   # Exposure where person was exposed by someone with symptoms.

    def infect(self, other, time):
        """
        Function that tries to spread infection from self to other.
        :param other: Other person.
        :param time: Current time
        """
        if self.infected and self.dist(other) < self.infection_dist:
            if other.symptomatic or other.immune:
                return

            if not other.infected:
                self._try_infect(other, time)

            other.exposures.append(time)
            if self.symptomatic:
                other.known_exposures.append(time)

    def gets_infected(self, time):
        """
        Update a person's state when (s)he gets infected.
        :param time: Current time
        """
        self.infected = True
        self.infected_time = time
        self.symptom_time = self.infected_time + self.symptom_delay
        self.immune_time = self.infected_time + self.time_until_recovery

    def update_conditions(self, time):
        """
        Check if persons state have changed and if so updates his/her state.
        Ex person now is immune so is no longer infected or shows symptoms.
        :param time: Current time.
        """
        if not self.infected or self.immune:
            return

        if time >= self.immune_time:
            self.infected = False
            self.symptomatic = False
            self.immune = True

        elif time >= self.symptom_time:
            self.symptomatic = True

    def dist(self, other):
        """
        Calculates (2D) distance from self to other.
        :param other:
        :return:
        """
        return math.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)

    @staticmethod
    def _inside(world_size, pos):
        """
        Checks if position is inside (2D) world.
        :param world_size: Size of the world. Eg: (100, 100) -> 100 * 100 meters^2
        :param pos: Position to be checked if inside.
        :return: True if inside the world, else false.
        """
        return 0 <= pos[0] <= world_size[0] and 0 <= pos[1] <= world_size[1]

    @abstractmethod
    def move(self, world_size):
        """
        Abstract method for moving a person.
        :param world_size: World size used for constraining the persons movement.
        """
        pass

    @abstractmethod
    def _try_infect(self, *args):
        """
        Abstract method which checks if a person should be infected granted that the other person can get infected
        by the first.
        :param args: Arguments for function, ex other and time.
        """
        pass


class RandomPerson(Person):

    def __init__(self, infected, infection_dist, infection_prob, speed,
                 starting_pos, symptom_delay, time_until_recovery):

        """
        Initialization class for a random person. A random person is defined by being an ordinary person but which
        moves in accordance to a (2D) random walk and infects a person with constant probability once another person
        is sufficiently close.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param infection_prob: Probability that person infects other if others can be infected and are close enough.
        :param speed: Persons walking speed.
        :param starting_pos: Persons starting position.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        """

        super(RandomPerson, self).__init__(infected=infected, starting_pos=starting_pos, speed=speed,
                                           infection_dist=infection_dist, symptom_delay=symptom_delay,
                                           time_until_recovery=time_until_recovery)

        self.infection_prob = infection_prob

    def move(self, world_size):
        """
        Move the person in accordance to a (2D) random walk.
        :param world_size: World size used for constraining persons walk.
        """
        angle = rnd.uniform(0, 2 * math.pi)
        dx, dy = self.speed * math.cos(angle), self.speed * math.sin(angle)
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        if self._inside(world_size, new_pos):
            self.pos = new_pos
        else:
            self.move(world_size=world_size)

    def _try_infect(self, other, time):
        """
        If other is close enough, self infects other with some probability. If other gets infected, his/her
        state is updated.
        :param other: Other person.
        :param time: Current time
        """
        if rnd.random() < self.infection_prob:
            other.gets_infected(time)
