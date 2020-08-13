import matplotlib.pyplot as plt
import statistics as stat
import seaborn as sns


class Simulator:

    def __init__(self, world):
        """
        Initialization of a simulator class. A simulator class is defined by holding a world with people,
        but also takes care of the movement of time. Used for simulating infection spread throughout the world.
        Also does visualization and relevant calculations for data analysis.
        :param world: List of persons.
        """
        self.world = world
        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        self.disp = False
        self.prog = 1

    def simulate(self, time=0, dt=1, sim_time=50 * 24, disp=False, see_progress=False):
        """
        Simulates the infection spreading throughout the world.
        :param time: Start time.
        :param dt: Size of time step.
        :param sim_time: Simulation duration.
        :param disp: True for visual simulation, false else.
        :param see_progress: True for print outs of % done of the simulation.
        """
        self.disp = disp
        while time < sim_time:
            if see_progress:
                if 100 * (time / sim_time) > self.prog:
                    print(f'{self.prog:.2f}%')
                    self.prog += 1
            self.world.update(time=time, dt=dt)
            if disp:
                self.display(time)
            time += dt

        self.time = 0
        self.prog = 1

    def display(self, time):
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

        self.ax.legend(['Homes', 'Schools', 'Work places', 'Immune', 'Quarantined', 'Symptomatic', 'Infected',
                        'Susceptible'], bbox_to_anchor=(1.125, 1.1))

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        self.ax.set_xlim(0, self.world.world_size[0])
        self.ax.set_ylim(0, self.world.world_size[1])
        self.ax.set_title(f'Day: {time // 24} Hour: {time % 24}')
        plt.show(block=False)
        plt.pause(0.01)

    def plot_distributions(self):
        """
        Plots the Infected time distributions.
        """
        one_known_exposure_infection_time, average_known_exposure_infection_time, true_infection_time = \
            self.get_infection_time_distributions()

        print('Length of one known:', len(one_known_exposure_infection_time))
        print('Lenght of average:', len(average_known_exposure_infection_time))
        print('Len of true', len(true_infection_time))

        try:
            if self.disp:
                plt.figure()
            sns.distplot(one_known_exposure_infection_time)
            sns.distplot(average_known_exposure_infection_time)
            sns.distplot(true_infection_time)
            plt.legend(['One known exposure', 'Average known exposures', 'True infected time'])
            plt.xlabel('Days')
            plt.ylabel('P(infected time = x)')
            plt.title('Infected time distributions')
            plt.show()

        except RuntimeError('Cannot plot empty lists'):
            pass

    def get_infection_time_distributions(self):
        """
        Estimates the infection time distributions for two estimations methods and also fetches the true distribution.
        Method 1: Take only persons with one known exposure.
        Method 2: Take average of all known exposures.
        """
        one_known_exposure_infection_time = []
        average_known_exposure_infection_time = []
        true_infection_time = []
        for person in self.world.persons:
            if person.immune_time != float('Inf'):

                if len(person.known_exposures) == 1:
                    one_known_exposure_infection_time.append((person.immune_time - person.known_exposures[0]) / 24)

                if person.known_exposures:
                    average_known_exposure_infection_time.append((person.immune_time - stat.mean(person.known_exposures)) / 24)

                true_infection_time.append((person.immune_time - person.infected_time) / 24)

        return one_known_exposure_infection_time, average_known_exposure_infection_time, true_infection_time



























