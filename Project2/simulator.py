from Project2.world import World
import matplotlib.pyplot as plt


class Simulator:

    def __init__(self, persons, world_shape=(100, 100), sim_time=100, frame_rate=1):
        """
        Initialization of a simulator class. A simulator class is defined by holding a world with people,
        but also takes care of the movement of time. Used for simulating infection spread throughout the world.
        Also does visualization and relevant calculations for data analysis.
        :param persons: List of persons.
        :param world_shape: Dimensions of the world, measured as (meters, meters) -> meters^2
        :param frame_rate: Frame rate of the simulation.
                           1 -> 1 update per sec, 2 -> 2 updates per sec etc. So speeds are m/s
        """
        if frame_rate != 1:
            for person in persons:
                person.speed /= frame_rate

        self.world = World(persons=persons, world_size=world_shape)
        self.frame_rate = frame_rate
        self.time = 0
        self.sim_time = sim_time

    def __iter__(self):
        """
        Iteration function that moves throughout the time of the simulation.
        :yield self.time: New current time.
        """
        while self.time < self.sim_time:
            yield self.time

            self.time += self.frame_rate

    def simulate(self, disp=False):
        """
        Simulates the infection spreading throughout the world.
        :param disp: True for visual simulation, false else.
        """
        for time in self:
            print(time)
            self.world.update(time=time)
            if disp:
                self.display()

    def display(self):
        """
        Visualises the spreading of infection throughout time.
        """
        x_ninf, y_ninf = [], []
        x_inf, y_inf = [], []
        x_symp, y_symp = [], []
        x_im, y_im = [], []

        for person in self.world.persons:
            if person.immune:
                x_im.append(person.pos[0])
                y_im.append(person.pos[1])

            elif person.symptomatic:
                x_symp.append(person.pos[0])
                y_symp.append(person.pos[1])

            elif person.infected:
                x_inf.append(person.pos[0])
                y_inf.append(person.pos[1])

            else:
                x_ninf.append(person.pos[0])
                y_ninf.append(person.pos[1])

        fig, ax = plt.subplots()
        colors = ['b', 'y', 'r', 'g']
        ax.scatter(x_im, y_im, c=colors[0])
        ax.scatter(x_symp, y_symp, c=colors[1])

        ax.scatter(x_inf, y_inf, c=colors[2])
        ax.scatter(x_ninf, y_ninf, c=colors[3])

        ax.legend(['Immune', 'Symptomatic', 'Infected', 'Susceptible'], loc='upper right')
        ax.set_xlim(0, self.world.world_size[0])
        ax.set_ylim(0, self.world.world_size[1])
        plt.show(block=False)
        plt.pause(0.1)
        plt.close()

    def get_distribution(self):
        pass
