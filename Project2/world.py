class World:

    def __init__(self, world_size, persons, buildings):
        """
        Initialization class for a world. A world is defined as holding some persons inside and having some size.
        :param world_size: Dimensions of the world.
        """
        self.world_size = world_size
        self.persons = persons
        self.buildings = buildings

    def update(self, time):
        """
        Updates the state of the world to the new state at time: time. All people are first moved then we check
        for new infection spread, checking for newly arisen symtoms etc.
        :param time: Current time.
        :param dt:
        """
        self.move_people(today_time=time % 24)
        for person in self.persons:
            for other in self.persons:
                if person == other:
                    pass
                else:
                    person.infect(other, time)

                person.update_conditions(time=time)

    def move_people(self, today_time):
        """
        Functions that moves all persons in the world.
        """
        for person in self.persons:
            person.move(today_time=today_time, world_size=self.world_size)
