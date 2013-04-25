import tkinter as tk
from model.drawable import GameDrawable
from model.observer import Observer, Observable


class Location(Observable, GameDrawable):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))
        self.width = width
        self.height = height

    def move_update(self, creature):
        pass


class Campsite(Location, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))
        self.width = width
        self.height = height

    def move_update(self, creature):
        possible_move_col = int(creature.possible_move_col)
        possible_move_row = int(creature.possible_move_row)
        position_col = int(self.position_col)
        position_row = int(self.position_row)
        if (possible_move_col in range(position_col - self.width, position_col + self.width + 1) and
                possible_move_row in range(position_row - self.height, position_row + self.height + 1)):
            creature.prepare_move = False


class Grass(Location, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))
        self.width = width
        self.height = height


class TallGrass(Location, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))
        self.width = width
        self.height = height

    def move_update(self, creature):
        pass
        # Force move to walking speed // 2 while in tall grass


class Tree(Location, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.image = image
        self.set_sprite(tk.PhotoImage(file=self.image))
        self.width = width
        self.height = height

    def move_update(self, creature):
        possible_move_col = int(creature.possible_move_col)
        possible_move_row = int(creature.possible_move_row)
        position_col = int(self.position_col)
        position_row = int(self.position_row)
        if (possible_move_col in range(position_col - self.width, position_col + self.width + 1) and
                possible_move_row in range(position_row - self.height, position_row + self.height + 1)):
            creature.prepare_move = False


class Rock(Location, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))
        self.width = width
        self.height = height

    def move_update(self, creature):
        possible_move_col = int(creature.possible_move_col)
        possible_move_row = int(creature.possible_move_row)
        position_col = int(self.position_col)
        position_row = int(self.position_row)
        if (possible_move_col in range(position_col - self.width, position_col + self.width + 1) and
                possible_move_row in range(position_row - self.height, position_row + self.height + 1)):
            creature.prepare_move = False


class Water(Location, Observer):

    def __init__(self, col, row, name, image, **kwargs):
        super(Location, self).__init__(**kwargs)
        self.position_col = col
        self.position_row = row
        self.name = name
        self.set_sprite(tk.PhotoImage(file=image))

    def move_update(self, creature):
        possible_move_col = int(creature.possible_move_col)
        possible_move_row = int(creature.possible_move_row)
        position_col = int(self.position_col)
        position_row = int(self.position_row)
        if (possible_move_col in range(position_col - self.width, position_col + self.width + 1) and
                possible_move_row in range(position_row - self.height, position_row + self.height + 1)):
            creature.prepare_move = False