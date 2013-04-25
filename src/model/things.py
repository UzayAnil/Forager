from model.creatures import *


class Edible(object):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    @property
    def satiation_points(self):
        return self._satiation_points

    @satiation_points.setter
    def satiation_points(self, value):
        self._satiation_points = value

    def eat(self):
        pass


class BirdMeat(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "bird"

    def eat(self):
        pass


class DeerMeat(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "venison"

    def eat(self):
        pass


class FishMeat(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "fish"

    def eat(self):
        pass


class RabbitMeat(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "rabbit"

    def eat(self):
        pass


class Berries(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 2

    name = "berries"

    def eat(self):
        pass


class Herb(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "herb"

    def eat(self):
        pass


class Nuts(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "nuts"

    def eat(self):
        pass


class Root(Edible):

    def __init__(self):
        super(Edible, self).__init__()
        self._satiation_points = 0

    name = "root"

    def eat(self):
        pass


class Equipment(object):

    def __init(self):
        super(Equipment, self).__init__()
        self._name = ""

    pass


class Dart(Equipment):

    def __init(self):
        super(Equipment, self).__init__()

    name = "dart"


class Clothing(Equipment):

    def __init(self):
        super(Equipment, self).__init__()

    name = "set of clothing"

    def equip(self, actor):
        actor.armor += 2

    def unequip(self, actor):
        actor.armor -= 2


class Cordage(Equipment):

    def __init(self):
        super(Equipment, self).__init__()

    name = "cordage"


class FireStarter(Equipment):

    def __init(self):
        super(Equipment, self).__init__()

    name = "fire starter"


class Resource(object):

    def __init(self):
        super(Resource, self).__init__()

    pass


class Chert(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "piece of chert"


class Wood(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "piece of wood"


class DeerHide(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "deer hide"


class RabbitPelt(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "rabbit pelt"


class WolfPelt(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "wolf pelt"


class Tendons(Resource):

    def __init(self):
        super(Resource, self).__init__()

    name = "tendons"


class Weapon(object):

    def __init(self):
        super(Weapon, self).__init__()

    def equip(self, actor):
        pass

    def unequip(self, actor):
        actor.set_attack(UnarmedStrike())


class Club(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "club"

    def equip(self, actor):
        actor.set_attack(Bash())


class DartThrower(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "dart thrower"

    def equip(self, actor):
        actor.set_attack(Shoot())


class HandAxe(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "handaxe"

    def equip(self, actor):
        actor.set_attack(Hack())


class Knife(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "knife"

    def equip(self, actor):
        actor.set_attack(Slice())


class SharpStick(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "sharp stick"

    def equip(self, actor):
        actor.set_attack(Poke())


class Spear(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "spear"

    def equip(self, actor):
        actor.set_attack(Stab())


class Unarmed(Weapon):

    def __init(self):
        super(Weapon, self).__init__()

    name = "unarmed"

    def equip(self, actor):
        actor.set_attack(UnarmedStrike())