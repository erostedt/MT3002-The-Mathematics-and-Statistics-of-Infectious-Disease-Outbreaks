from abc import ABC, abstractmethod
import math
import random as rnd


class Person(ABC):

    def __init__(self, infected, starting_pos, speed, infection_dist, infection_prob, symptom_delay,
                 time_until_recovery, home, work):
        """
        Initialization class for a person.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param speed: Persons walking speed.
        :param starting_pos: Persons starting position.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        :param home: Home building.
        :param work: Work Building (None if person does not have a job).
        """
        self.pos = starting_pos
        self.speed = speed

        self.infection_dist = infection_dist
        self.infection_prob = infection_prob

        self.symptom_delay, self.immune_delay = symptom_delay, time_until_recovery

        self.home = home
        self.work = work

        self.infected_time = 0 if infected else float('Inf')
        self.symptom_time = self.symptom_delay if infected else float('Inf')
        self.immune_time = self.immune_delay if infected else float('Inf')

        self.quarantine = False
        self.infected = infected
        self.symptomatic = False
        self.immune = False

        self.exposures = []         # All exposures.
        self.known_exposures = []   # Exposure where person was exposed by someone with symptoms.

    def infect(self, other, time):
        """
        Function that tries to spread infection from self to other.
        :param other: Other person.
        :param time: Current time.
        """
        if self.infected and self.dist(other) < self.infection_dist:
            if not self.quarantine or (self.quarantine and other.home is self.home):    # If quarantine, can only infect other's in the same home.

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
        self.immune_time = self.infected_time + self.immune_delay

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
            if not isinstance(self, RandomPerson):
                self.quarantine = True

    def dist(self, other):
        """
        Calculates (2D) distance from self to other.
        :param other: Other person
        :return: Distance between self and other.
        """
        return math.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)

    def set_world(self, world):
        """

        (UNUSED!)

        Makes the person aware of all other info in the world
        :param world: World in which person lives in.
        """
        self.world = world

    @staticmethod
    def _inside(world_size, pos):
        """
        Checks if position is inside (2D) world.
        :param world_size: Size of the world. Eg: (100, 100) -> 100 * 100 meters^2
        :param pos: Position to be checked if inside.
        :return: True if inside the world, else false.
        """
        return 0 <= pos[0] <= world_size[0] and 0 <= pos[1] <= world_size[1]

    def get_buildings(self):
        """

        (UNUSED!)

        Fetches all buildings in the world.
        :return: List of buildings in the world.
        """
        return self.world.buildings

    def get_others_pos(self):
        """

        (UNUSED!)

        Finds position of all other persons.
        :return: List of other persons positions.
        """
        return [person.pos for person in self.world.persons if person is not self]

    def random_walk(self, world_size):
        """
        Function for a constrained 2D random walk.
        :param world_size: Size of the world.
        :return: New position.
        """
        new_pos = (-1, -1)
        while not self._inside(world_size, new_pos):
            angle = rnd.uniform(0, 2 * math.pi)
            dx, dy = self.speed * math.cos(angle), self.speed * math.sin(angle)
            x, y = self.pos
            new_pos = (x + dx, y + dy)
        return new_pos

    @abstractmethod
    def move(self, *args):
        """
        Abstract method for moving a person.
        :param args: Arguments.
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

    def __init__(self, infected, starting_pos, speed, infection_dist, infection_prob, symptom_delay,
                 time_until_recovery, home, work):

        """
        Initialization class for a random person. A random person is defined by being an ordinary person but which
        moves in accordance to a (2D) random walk and infects a person with constant probability once another person
        is sufficiently close.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param speed: Persons walking speed.
        :param starting_pos: Persons starting position.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        :param home: Home building.
        :param work: Work Building (None if person does not have a job).
        """

        super().__init__(infected=infected, starting_pos=starting_pos, speed=speed,
                         infection_dist=infection_dist, infection_prob=infection_prob,
                         symptom_delay=symptom_delay, time_until_recovery=time_until_recovery,
                         home=home, work=work)

        self.quarantined = False

    def move(self, today_time, world_size, dt=None):
        """
        Moves the person in accordance to a (2D) random walk.
        :param today_time: Time of the day.
        :param dt:
        :param world_size: World size, used for constraining persons walk.
        """
        self.pos = self.random_walk(world_size=world_size)

    def _try_infect(self, other, time):
        """
        If other is close enough, self infects other with some probability. If other gets infected, his/her
        state is updated.
        :param other: Other person.
        :param time: Current time
        """
        if rnd.random() < self.infection_prob:
            other.gets_infected(time)


class QuarantinePerson(Person):

    def __init__(self, infected, starting_pos, speed, infection_dist, infection_prob, symptom_delay,
                 time_until_recovery, home, work):

        """
        Random walks during the day and sleeps at night.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param speed: Persons walking speed.
        :param starting_pos: Persons starting position.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        :param home: Home building.
        :param work: Work Building (None if person does not have a job).
        """

        super().__init__(infected=infected, starting_pos=starting_pos, speed=speed,
                         infection_dist=infection_dist, infection_prob=infection_prob,
                         symptom_delay=symptom_delay, time_until_recovery=time_until_recovery,
                         home=home, work=work)

        self.quarantined = False

    def move(self, today_time, world_size, dt=None):
        """
        Moves the person in accordance to a (2D) random walk.
        :param today_time: Time of the day.
        :param dt: Time step.
        :param world_size: World size, used for constraining persons walk.
        """
        if self.quarantined:
            self.pos = self.home.pos
            return

        if 6 <= today_time <= 22:
            self.pos = self.random_walk(world_size=world_size)
        else:
            self.pos = self.home.pos    # Sleeps

    def _try_infect(self, other, time):
        """
       If other is close enough, self infects other with some probability. If other gets infected, his/her
       state is updated.
       :param other: Other person.
       :param time: Current time
       """
        if rnd.random() < self.infection_prob:
            other.gets_infected(time=time)


class Worker(Person):

    def __init__(self, infected, starting_pos, speed, infection_dist, infection_prob, symptom_delay,
                 time_until_recovery, home, work):

        """
        Person that goes into quarantine when getting symptoms.
        :param infected: If person is infected or not.
        :param infection_dist: Distance that person can infect others.
        :param infection_prob: Probability that person infects other if others can be infected and are close enough.
        :param speed: Persons walking speed.
        :param symptom_delay: Delay between being infected and showing symptoms.
        :param time_until_recovery: Time from getting sick and recovering.
        """

        super().__init__(infected=infected, starting_pos=starting_pos, speed=speed,
                         infection_dist=infection_dist, infection_prob=infection_prob,
                         symptom_delay=symptom_delay, time_until_recovery=time_until_recovery,
                         home=home, work=work)

        self.quarantined = False
        self._carry = 0

    def move(self, today_time, world_size, dt=1):
        """
        Moves the person in accordance to a (2D) random walk.
        :param today_time: Time of the day.
        :param dt:
        :param world_size: World size, used for constraining persons walk.
        """

        if self.quarantined:
            self.pos = self.home.pos
            return
        """
        Work hours = 8 -> 16, So assumed to be commuting at 7.00 and 16.00. We let the person
        be able to infect during commute at 7->8 and 16->17 (just when leaving home and just before coming home)
        Then assume that person random walks after work and prior to sleep.
        """
        if 7 <= today_time < 8:
            self.pos = (self.home.pos[0] + self._carry * dt * (self.work.pos[0] - self.home.pos[0]),
                        self.home.pos[1] + self._carry * dt * (self.work.pos[1] - self.home.pos[1]))    # Going to work.

            self._carry += 1    # Used to evenly space out work commute

        elif 8 <= today_time <= 16:
            self.pos = self.work.pos
            self._carry = 0

        elif 16 < today_time <= 17:
            self.pos = (self.work.pos[0] + self._carry * dt * (self.home.pos[0] - self.work.pos[0]),
                        self.work.pos[1] + self._carry * dt * (self.home.pos[1] - self.work.pos[1]))    # Going home.
            self._carry += 1

        elif 17 < today_time <= rnd.uniform(17, 22):    # Has a random chance to go home prior to 22.
            self.pos = self.random_walk(world_size=world_size)

        else:
            self.pos = self.home.pos
            self._carry = 0

    def _try_infect(self, other, time):
        """
        If other is close enough, self infects other with some probability. If other gets infected, his/her
        state is updated.
        :param other: Other person.
        :param time: Current time
        """
        if self.pos == self.home.pos:
            infection_prob = self.infection_prob * self.home.tightness

        elif self.pos == self.work.pos:
            infection_prob = self.infection_prob * self.work.tightness

        else:
            infection_prob = self.infection_prob

        if rnd.random() < infection_prob:
            other.gets_infected(time=time)
