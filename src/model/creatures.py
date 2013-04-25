import tkinter as tk
from model.observer import *
from controller.distance import Distance
from model.drawable import GameDrawable
from model.states import *
from model.behaviors import *
import random


class Creature(Observable, GameDrawable):

    def __init__(self, **kwargs):
        super(Creature, self).__init__(**kwargs)
        self._name = ""
        self._creature_type = ""

        # States
        self.current_state = NormalState(self)
        self.normal_state = NormalState(self)
        self.staggered_state = StaggeredState(self)
        self.unconscious_stable_state = UnconsciousStableState(self)
        self.unconscious_dying_state = UnconsciousDyingState(self)
        self.dead_state = DeadState(self)

        # Behaviors
        self.attack = Attack()
        self.combat_maneuver = CombatManeuver()
        self.move = Move()
        self.posture = Posture()
        self.skill = Skill()

        # Abilities
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10

        # Ability Modifiers
        self._str_mod = (self.strength // 2) - 5
        self._dex_mod = (self.dexterity // 2) - 5
        self._con_mod = (self.constitution // 2) - 5
        self._int_mod = (self.intelligence // 2) - 5
        self._wis_mod = (self.wisdom // 2) - 5

        # Other
        self._standard_action = 1
        self._move_action = 2
        self._vigor_points = 1
        self._speed = 6
        self._other = 0
        self._armor = 0
        self._base_attack_bonus = 0
        self._dodge = 0
        self._wound_points = self.constitution
        self._wound_threshold = self.constitution // 2
        self._position_col = 0
        self._position_row = 0
        self._position = (0, 0)
        self._possible_move_col = 0
        self._possible_move_row = 0
        self._possible_move = [0, 0]
        self._action_count = 2
        self._inventory = list()
        self._target = None
        self._prepare_attack = False
        self._prepare_attack_move = False
        self._prepare_move = False
        self._hide = False
        self._width = 0
        self._height = 0
        self._lineofsight = 500
        self.distance = Distance()
        self._hidden = list()

    @property
    def hidden(self):
        return self._hidden

    def add_hidden(self, creature):
        if creature not in self._hidden:
            self._hidden.append(creature)

    def remove_hidden(self, creature):
        if creature in self._hidden:
            self._hidden.remove(creature)

    @property
    def hide(self):
        return self._hide

    @hide.setter
    def hide(self, hide):
        self._hide = hide

    @property
    def lineofsight(self):
        return self._lineofsight

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name    

    @property
    def creature_type(self):
        return self._creature_type

    @creature_type.setter
    def creature_type(self, creature_type):
        self._creature_type = creature_type

    @property
    def prepare_move(self):
        return self._prepare_move

    @prepare_move.setter
    def prepare_move(self, value):
        self._prepare_move = value

    @property
    def prepare_attack(self):
        return self._prepare_attack

    @prepare_attack.setter
    def prepare_attack(self, value):
        self._prepare_attack = value

    @property
    def prepare_attack_move(self):
        return self._prepare_attack_move

    @prepare_attack_move.setter
    def prepare_attack_move(self, value):
        self._prepare_attack_move = value

    @property
    def str_mod(self):
        return self._str_mod

    @property
    def dex_mod(self):
        return self._dex_mod

    @property
    def con_mod(self):
        return self._con_mod

    @property
    def int_mod(self):
        return self._int_mod

    @property
    def wis_mod(self):
        return self._wis_mod

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def move_action(self):
        return self._move_action

    @move_action.setter
    def move_action(self, move_action):
        self._move_action = move_action

    @property
    def standard_action(self):
        return self._standard_action

    @standard_action.setter
    def standard_action(self, standard_action):
        self._standard_action = standard_action

    @property
    def dodge(self):
        return self._dodge

    @dodge.setter
    def dodge(self, dodge):
        self._dodge = dodge

    @property
    def base_attack_bonus(self):
        return self._base_attack_bonus

    @base_attack_bonus.setter
    def base_attack_bonus(self, base_attack_bonus):
        self._base_attack_bonus = base_attack_bonus

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, armor):
        self._armor = armor

    @property
    def other(self):
        return self._other

    @other.setter
    def other(self, other):
        self._other = other

    @property
    def speed(self):
        return self._speed

    @speed.setter   
    def speed(self, speed):
        self._speed = speed

    @property
    def base_speed(self):
        return self._base_speed

    @base_speed.setter
    def base_speed(self, base_speed):
        self._base_speed = base_speed

    @property
    def hunger_points(self):
        return self._hunger_points

    @hunger_points.setter
    def hunger_points(self, hunger_points):
        self._hunger_points = hunger_points
    
    @property
    def action_count(self):
        return self._action_count
    
    @action_count.setter
    def action_count(self, action_count):
        self._action_count = action_count

    @property
    def vigor_points(self):
        return self._vigor_points

    @vigor_points.setter
    def vigor_points(self, vigor_points):
        self._vigor_points = vigor_points
        
    @property
    def wound_threshold(self):
        return self._wound_threshold

    @property
    def wound_points(self):
        return self._wound_points

    @wound_points.setter
    def wound_points(self, wound_points):
        self._wound_points = wound_points

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = position

    @property
    def possible_move(self):
        return self._possible_move

    @possible_move.setter
    def possible_move(self, possible_move):
        self._possible_move = possible_move
        self._possible_move_col = possible_move[0]
        self._possible_move_row = possible_move[1]
        
    @property
    def position_col(self):
        return self._position_col
    
    @position_col.setter
    def position_col(self, position_col):
        self._position_col = position_col

    @property
    def position_row(self):
        return self._position_row

    @position_row.setter
    def position_row(self, position_row):
        self._position_row = position_row

    @property
    def possible_move_col(self):
        return self._possible_move_col

    @possible_move_col.setter
    def possible_move_col(self, possible_move_col):
        self._possible_move_col = possible_move_col

    @property
    def possible_move_row(self):
        return self._possible_move_row

    @possible_move_row.setter
    def possible_move_row(self, possible_move_row):
        self._possible_move_row = possible_move_row

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    def set_state(self, state):  # Change state to condition?
        self.current_state = state

    def get_normal_state(self):
        return self.normal_state

    def get_staggered_state(self):
        return self.staggered_state

    def get_dead_state(self):
        return self.dead_state

    def get_unconscious_dying_state(self):
        return self.unconscious_dying_state

    def get_unconscious_stable_state(self):
        return self.unconscious_stable_state

    def set_move(self, move):
        self.move = move
        self.move.speed(self)

    def set_attack(self, attack):
        self.attack = attack

    def set_combat_maneuver(self, combat_maneuver):
        self.combat_maneuver = combat_maneuver

    def set_skill(self, skill):
        self.skill = skill

    def set_posture(self, posture):
        self.posture = posture
        self.posture.execute(self)

    def execute_move(self, actor):
        self.move.execute(actor)

    def execute_attack(self, actor, target, world):
        self.attack.execute(actor, target, world)

    def execute_combat_maneuver(self, actor, target):
        self.combat_maneuver.execute(actor, target)

    def execute_skill(self, actor, target):
        self.skill.execute(actor, target)

    def eat(self):
        print("I eat.")

    def sleep(self):
        print("I sleep.")

    def add_inventory(self, item):
        self._inventory.append(item)

    def remove_inventory(self, item):
        self._inventory.remove(item)

    def change_move(self, key_press):
        """Change Move

        Changes the current move to the move associated with each key below.

        """
        if key_press == "w":
            self.set_move(Walk())
        if key_press == "r":
            self.set_move(Run())
        if key_press == "s":
            self.set_move(Sneak())
        if key_press == "h":
            self.set_move(Hustle())
        if key_press == "o":
            self.set_move(OneSquareStep())

    def initiative_check(self):
        initiative_roll = random.randint(1, 20)
        return initiative_roll + self.dex_mod

    def staggered_action(self):
        self.wound_points -= 1
        print("The " + self._name + " is feeling weak and loses a wound.")
        print("The " + self._name + " has " + str(self.vigor_points) + " vigor and "
              + str(self.wound_points) + " wounds remaining.")
        if self.wound_points <= 0:
            self.set_state(self.get_dead_state())
            print("The " + self._name + " dies.")
        con_check = random.randint(1, 20) + self.con_mod
        if con_check < 10:
            self.set_state(self.get_dead_state())
            print("The " + self._name + " looses consciousness and dies.")

    def stealth_update(self, world, creature):
        if self.distance.compute(self.position, creature.position) > 500:
            creature.set_skill(Stealth())
            creature.skill.execute(world, creature, self)

    def perception_update(self, world, creature):
        name = self.move.name
        if name is "sneak" and self.distance.compute(self.position, creature.position) <= creature.lineofsight:
            # creature.target = self
            creature.set_skill(Perception())
            creature.skill.execute(world, creature, self)

    def move_update(self, creature):
        possible_move_col = int(creature.possible_move_col)
        possible_move_row = int(creature.possible_move_row)
        position_col = int(self.position_col)
        position_row = int(self.position_row)
        position = (self.position_col, self.position_row)
        creature_position = (creature.position_col, creature.position_row)

        if (possible_move_col in range(position_col - self.width, position_col + self.width + 1) and
                possible_move_row in range(position_row - self.height, position_row + self.height + 1)):
            if creature is not self:
                creature.prepare_move = False
            if (creature is not self and
                    self.distance.compute(position, creature_position) <= creature.attack.attack_range):
                creature.prepare_attack = True
                creature.target = self

    def attack_range_update(self, creature):
        position = (self.position_col, self.position_row)
        creature_position = (creature.position_col, creature.position_row)
        if (creature is not self and
                self.distance.compute(position, creature_position) <= creature.attack.attack_range and
                self not in creature.hidden):
            creature.prepare_attack = True
            creature.target = self

    def attack_move_update(self, creature):
        position = (self.position_col, self.position_row)
        creature_position = (creature.position_col, creature.position_row)
        attack_range = creature.attack.attack_range
        if (creature is not self and self not in creature.hidden and
                self.distance.compute(position, creature_position) <= ((creature.speed * 64) + attack_range)):
            creature.prepare_attack_move = True
            creature.target = self

    def death_update(self, actor):
        self.remove_observer(actor)

    def display(self):
        pass


class Human(Creature, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Human, self).__init__(**kwargs)
        self._name = name
        self._creature_type = "human"
        self._position_col = col
        self._position_row = row
        self._position = [self.position_col, self.position_row]
        self._possible_move_col = 0
        self._possible_move_row = 0
        self._possible_move = [0, 0]
        self._width = width
        self._height = height
        self._base_speed = 8
        self._speed = 4
        self._hunger_points = 10
        self._experience_points = 200
        self._target = None
        self._prepare_attack = False
        self._prepare_attack_move = False
        self._prepare_move = False
        self.set_sprite(tk.PhotoImage(file=image))
        
        # Strategies
        self.attack = Stab()
        self.combat_maneuver = Trip()
        self.move = Sneak()
        self.skill = Craft()
        self.posture = Standing()

        # Condition States
        self.normal_state = NormalState(self)
        self.staggered_state = StaggeredState(self)
        self.dead_state = DeadState(self)
        self.unconscious_dying_state = UnconsciousDyingState(self)
        self.unconscious_stable_state = UnconsciousStableState(self)
        self.current_state = NormalState(self)
        
        # Image States
        self._image_state = StandFront()
        self._stand_front = StandFront()
        self._walk_left_front = WalkLeftFront()
        self._walk_right_front = WalkRightFront()

        # Abilities
        self.strength = 15
        self.dexterity = 15
        self.constitution = 14
        self.intelligence = 10
        self.wisdom = 12

        # Ability Modifiers
        self._str_mod = (self.strength // 2) - 5
        self._dex_mod = (self.dexterity // 2) - 5
        self._con_mod = (self.constitution // 2) - 5
        self._int_mod = (self.intelligence // 2) - 5
        self._wis_mod = (self.wisdom // 2) - 5

        # Combat
        self._base_attack_bonus = 1
        self._armor = 0
        self._dodge = 1
        self._other = 0
        self._vigor_points = 12
        self._wound_points = self.constitution
        self._wound_threshold = self.constitution // 2

        # Skills
        self.acrobatics = 5
        self.craft = 5
        self.perception = 4
        self.stealth = 6
        self.survival = 5

        # Other
        self._standard_action = 1
        self._move_action = 2
        self._action_count = 2
        self.end_turn = tk.BooleanVar()
        self.distance = Distance()
        self.image_list = [self.stand_front, self.walk_left_front, self.stand_front, self.walk_right_front]

    def display(self):
        print("Human's turn.")

    def accept_visitor(self, visitor):
        visitor.visit_human()

    def set_image_state(self, state):
        self._image_state = state
        self.set_sprite(self._image_state.sprite)

    @property
    def stand_front(self):
        return self._stand_front

    @property
    def walk_left_front(self):
        return self._walk_left_front

    @property
    def walk_right_front(self):
        return self._walk_right_front


class Deer(Creature, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Deer, self).__init__(**kwargs)
        self._position_col = col
        self._position_row = row
        self._position = [self.position_col, self.position_row]
        self._possible_move_col = 0
        self._possible_move_row = 0
        self._possible_move = [0, 0]
        self._width = width
        self._height = height
        self._creature_type = "deer"
        self._base_speed = 8
        self._speed = 8
        self._hunger_points = 10
        self._experience_points = 100
        self._prepare_attack = False
        self._prepare_attack_move = False
        self._target = None
        self._prepare_move = False
        self._name = name
        self.set_sprite(tk.PhotoImage(file=image))

        # Strategies
        self.attack = Gore()
        self.combat_maneuver = Trip()
        self.move = Walk()
        self.skill = Stealth()
        self.posture = Standing()

        # States
        self.normal_state = NormalState(self)
        self.staggered_state = StaggeredState(self)
        self.dead_state = DeadState(self)
        self.unconscious_dying_state = UnconsciousDyingState(self)
        self.unconscious_stable_state = UnconsciousStableState(self)
        self.current_state = NormalState(self)

        # Abilities
        self.strength = 12
        self.dexterity = 15
        self.constitution = 12
        self.intelligence = 2
        self.wisdom = 14

        # Ability Modifiers
        self._str_mod = (self.strength // 2) - 5
        self._dex_mod = (self.dexterity // 2) - 5
        self._con_mod = (self.constitution // 2) - 5
        self._int_mod = (self.intelligence // 2) - 5
        self._wis_mod = (self.wisdom // 2) - 5

        # Combat
        self._base_attack_bonus = 1
        self._armor = 1
        self._dodge = 1
        self._other = 0
        self._vigor_points = 11
        self._wound_points = self.constitution
        self._wound_threshold = self.constitution // 2

        # Skills
        self.acrobatics = 2
        self.perception = 10
        self.stealth = 10
        self.survival = 10

        # Other
        self._standard_action = 1
        self._move_action = 2
        self._action_count = 2
        self.distance = Distance()

    def display(self):
        print("Deer's turn.")

    # def deer_move(self):


class Rabbit(Creature, Observer):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Rabbit, self).__init__(**kwargs)
        self._position_col = col
        self._position_row = row
        self._position = [self.position_col, self.position_row]
        self._possible_move_col = 0
        self._possible_move_row = 0
        self._possible_move = [0, 0]
        self._width = width
        self._height = height
        self._creature_type = "rabbit"
        self._base_speed = 8
        self._speed = 8
        self._hunger_points = 10
        self._experience_points = 100
        self._prepare_attack = False
        self._target = None
        self._prepare_move = False
        self._name = name
        self.set_sprite(tk.PhotoImage(file=image))

        # Strategies
        self.attack = Bite()
        self.combat_maneuver = Trip()
        self.move = Walk()
        self.posture = Standing()
        self.skill = Stealth()

        # States
        self.normal_state = NormalState(self)
        self.staggered_state = StaggeredState(self)
        self.dead_state = DeadState(self)
        self.unconscious_dying_state = UnconsciousDyingState(self)
        self.unconscious_stable_state = UnconsciousStableState(self)
        self.current_state = NormalState(self)

        # Abilities
        self.strength = 2
        self.dexterity = 15
        self.constitution = 11
        self.intelligence = 2
        self.wisdom = 13

        # Ability Modifiers
        self._str_mod = (self.strength // 2) - 5
        self._dex_mod = (self.dexterity // 2) - 5
        self._con_mod = (self.constitution // 2) - 5
        self._int_mod = (self.intelligence // 2) - 5
        self._wis_mod = (self.wisdom // 2) - 5

        # Combat
        self._base_attack_bonus = 0
        self._dodge = 0
        self._armor = 0
        self._other = 0
        self._vigor_points = 3
        self._wound_points = self.constitution
        self._wound_threshold = self.constitution // 2

        # Skills
        self.acrobatics = 2
        self.perception = 5
        self.stealth = 14
        self.survival = 10

        # Other
        self._standard_action = 1
        self._move_action = 2
        self._action_count = 2
        self.distance = Distance()

    def display(self):
        print("I am a rabbit.")


class Wolf(Creature, Observer, Visitable):

    def __init__(self, col, row, name, image, width, height, **kwargs):
        super(Wolf, self).__init__(**kwargs)
        self._position_col = col
        self._position_row = row
        self._position = [self.position_col, self.position_row]
        self._possible_move_col = 0
        self._possible_move_row = 0
        self._possible_move = [0, 0]
        self._width = width
        self._height = height
        self._creature_type = "wolf"
        self._base_speed = 10
        self._speed = 10
        self._hunger_points = 10
        self._experience_points = 400
        self._prepare_attack = False
        self._prepare_attack_move = False
        self._target = None
        self._prepare_move = False
        self._name = name
        self.set_sprite(tk.PhotoImage(file=image))

        # Strategies
        self.attack = Bite()
        self.combat_maneuver = Trip()
        self.move = Walk()
        self.posture = Standing()
        self.skill = Stealth()

        # Condition States
        self.normal_state = NormalState(self)
        self.staggered_state = StaggeredState(self)
        self.dead_state = DeadState(self)
        self.unconscious_dying_state = UnconsciousDyingState(self)
        self.unconscious_stable_state = UnconsciousStableState(self)
        self.current_state = NormalState(self)

        # Abilities
        self.strength = 13
        self.dexterity = 15
        self.constitution = 15
        self.intelligence = 2
        self.wisdom = 12

        # Ability Modifiers
        self._str_mod = (self.strength // 2) - 5
        self._dex_mod = (self.dexterity // 2) - 5
        self._con_mod = (self.constitution // 2) - 5
        self._int_mod = (self.intelligence // 2) - 5
        self._wis_mod = (self.wisdom // 2) - 5

        # Combat
        self._base_attack_bonus = 1
        self._dodge = 0
        self._armor = 2
        self._other = 0
        self._vigor_points = 9
        self._wound_points = self.constitution
        self._wound_threshold = self.constitution // 2

        # Skills
        self.acrobatics_ranks = 0
        self.acrobatics = 2
        self.perception_ranks = 0
        self.perception = 8
        self.stealth_ranks = 0
        self.stealth = 6
        self.survival_ranks = 0
        self.survival = 1

        # Other
        self._standard_action = 1
        self._move_action = 2
        self._action_count = 2
        self.distance = Distance()
        self.max_move = 40

    def accept_visitor(self, visitor):
        visitor.visit_wolf()

    def display(self):
        print("Wolf's turn.")