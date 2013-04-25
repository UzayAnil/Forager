from model.things import *
from model.locations import *


class EdibleDecorator(Edible):

    def __init__(self, **kwargs):
        super(EdibleDecorator).__init__(**kwargs)


class RottenDecorator(Edible, Observable):

    def __init__(self, decorated, **kwargs):
        super(RottenDecorator).__init__(**kwargs)
        self.decorated = decorated
        self._observers = self.decorated._observers
        self.satiation_points = self.decorated.satiation_points // 2


class PerfectDecorator(Edible):

    def __init__(self, decorated, **kwargs):
        super(PerfectDecorator).__init__(**kwargs)
        self.decorated = decorated
        self.satiation_points = self.decorated.satiation_points * 2


class DeerDecorator(Deer):

    def __init__(self, **kwargs):
        super(DeerDecorator).__init__(**kwargs)


class FemaleDeer(DeerDecorator):

    def __init__(self, decorated, **kwargs):
        super(FemaleDeer).__init__(**kwargs)
        self.decorated = decorated
        self._observers = self.decorated._observers


class TreeDecorator(Tree):

    def __init__(self, **kwargs):
        super(TreeDecorator).__init__(**kwargs)


class DeadTree(TreeDecorator):

    def __init__(self, decorated, image, **kwargs):
        super(DeadTree).__init__(**kwargs)
        self.decorated = decorated
        self._observers = self.decorated._observers
        self._picture = self.decorated._picture
        self.position_col = self.decorated.position_col
        self.position_row = self.decorated.position_row
        self.name = self.decorated.name
        self.width = self.decorated.width
        self.height = self.decorated.height
        self.decorated.image = image
        self.set_sprite(tk.PhotoImage(file=self.decorated.image))