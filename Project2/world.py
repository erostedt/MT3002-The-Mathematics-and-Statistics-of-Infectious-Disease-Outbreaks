class World:

    def __init__(self, persons, world_size):
        """
        Initialization class for a world. A world is defined as holding some persons inside and having some size.
        :param persons: List of persons inside the world.
        :param world_size: Dimensions of the world.
        """
        self.persons = persons
        self.world_size = world_size

    def update(self, time):
        """
        Updates the state of the world to the new state at time: time. All people are first moved then we check
        for new infection spread, checking for newly arisen symtoms etc.
        :param time: Current time.
        """
        self.move_people()
        for person in self.persons:
            for other in self.persons:

                if person == other:
                    pass
                else:
                    person.infect(other, time)

                person.update_conditions(time=time)

    def move_people(self):
        """
        Functions that moves all persons in the world.
        """
        for person in self.persons:
            person.move(world_size=self.world_size)
