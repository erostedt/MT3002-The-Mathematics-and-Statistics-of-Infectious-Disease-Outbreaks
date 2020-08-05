import matplotlib.pyplot as plt
import statistics as stat
import seaborn as sns


class Simulator:

    def __init__(self, world, sim_time=50 * 24, dt=1):
        """
        Initialization of a simulator class. A simulator class is defined by holding a world with people,
        but also takes care of the movement of time. Used for simulating infection spread throughout the world.
        Also does visualization and relevant calculations for data analysis.
        :param persons: List of persons.
        :param world_shape: Dimensions of the world, measured as (meters, meters) -> meters^2
        :param frame_rate: Frame rate of the simulation.
                           1 -> 1 update per hour, 2 -> 2 updates per hour etc. So speeds are m/s
        """
        self.world = world
        self.time = 0
        self.sim_time = sim_time
        self.dt = dt

        self.fig, self.ax = plt.subplots()

    def __iter__(self):
        """
        Iteration function that moves throughout the time of the simulation.
        :yield self.time: New current time.
        """
        while self.time < self.sim_time:
            yield self.time

            self.time += self.dt

    def simulate(self, disp=False):
        """
        Simulates the infection spreading throughout the world.
        :param see_time:
        :param disp: True for visual simulation, false else.
        """
        for time in self:
            self.world.update(time=time)
            if disp:
                self.display()

        self.time = 0

    def display(self):
        """
        Visualises the spreading of infection throughout time.
        """
        x_ninf, y_ninf = [], []
        x_inf, y_inf = [], []
        x_quar, y_quar = [], []
        x_symp, y_symp = [], []
        x_im, y_im = [], []

        homes_x, homes_y = [], []
        schools_x, schools_y = [], []
        works_x, works_y = [], []
        other_x, other_y = [], []
        for building in self.world.buildings:
            if building._type == 'Home':
                homes_x.append(building.pos[0])
                homes_y.append(building.pos[1])

            if building._type == 'School':
                schools_x.append(building.pos[0])
                schools_y.append(building.pos[1])

            if building._type == 'Work':
                works_x.append(building.pos[0])
                works_y.append(building.pos[1])

        for person in self.world.persons:
            if person.immune:
                x_im.append(person.pos[0])
                y_im.append(person.pos[1])

            elif person.quarantined:
                x_quar.append(person.pos[0])
                y_quar.append(person.pos[1])

            elif person.symptomatic:
                x_symp.append(person.pos[0])
                y_symp.append(person.pos[1])

            elif person.infected:
                x_inf.append(person.pos[0])
                y_inf.append(person.pos[1])

            else:
                x_ninf.append(person.pos[0])
                y_ninf.append(person.pos[1])

        colors = ['brown', 'b', 'k', 'y', 'r', 'g']
        self.ax.clear()

        self.ax.scatter(homes_x, homes_y, c=colors[0], marker='s')
        self.ax.scatter(schools_x, schools_y, c=colors[0], marker='+')
        self.ax.scatter(works_x, works_y, c=colors[0], marker='^')

        self.ax.scatter(x_im, y_im, c=colors[1])
        self.ax.scatter(x_quar, y_quar, c=colors[2])
        self.ax.scatter(x_symp, y_symp, c=colors[3])

        self.ax.scatter(x_inf, y_inf, c=colors[4])
        self.ax.scatter(x_ninf, y_ninf, c=colors[5])

        self.ax.legend(['Homes', 'Schools', 'Work places', 'Immune', 'Quarantined', 'Symptomatic', 'Infected', 'Susceptible'], loc='upper right')
        self.ax.set_xlim(0, self.world.world_size[0])
        self.ax.set_ylim(0, self.world.world_size[1])
        self.ax.set_title(f'{self.time}')
        plt.show(block=False)
        plt.pause(0.01)

    def plot_distributions(self):
        one_known_exposure_delay, average_known_exposure_delay, true_delay = self.get_distributions()

        plt.figure()
        sns.distplot(one_known_exposure_delay)
        sns.distplot(average_known_exposure_delay)
        sns.distplot(true_delay)
        plt.legend(['One known exp delay', 'Average known exp delay', 'True infection delay'])
        plt.show()

    def get_distributions(self):
        one_known_exposure_delay = []
        average_known_exposure_delay = []
        true_delay = []
        for person in self.world.persons:
            if person.symptom_time != float('Inf'):

                if len(person.known_exposures) == 1:
                    one_known_exposure_delay.append(person.symptom_time - person.known_exposures[0])

                if person.known_exposures:
                    average_known_exposure_delay.append(person.symptom_time - stat.mean(person.known_exposures))

                true_delay.append(person.symptom_time - person.infected_time)

        return one_known_exposure_delay, average_known_exposure_delay, true_delay



























