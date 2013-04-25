import tkinter as tk
from model.observer import *
from model.drawable import GameDrawable
from model.visitor import *
from model.states import AttackMovePosition, MovePosition
from controller.distance import Distance
from view.info_pane import InfoPane
# from model.behaviors import Sneak


class GameWorld(Observer, Observable, Visitable):

    def __init__(self):
        super(GameWorld, self).__init__()
        self._rounds = 1
        self._moveable_list = list()
        self._immovable_list = list()
        self._text_object_list = list()
        self._drawable = list()
        self._creature_list = list()
        self._player = None
        self._interface = None
        self.index = 0
        self.image_state = 0
        self.name = "game world"
        self._current_turn = ""
        self.start = False
        self.end_turn_boolean = True
        self.dark = False
        self.tk_end_turn_boolean = tk.BooleanVar
        self.distance = Distance()
        
        # Visitors
        self.attack_move_position_visitor = AttackMovePositionVisitor()
        self.move_position_visitor = MovePositionVisitor()
        
        # Move Position States
        self._attack_move_position = AttackMovePosition()
        self._move_position = MovePosition()
        self._move_position_state = None

    def accept_visitor(self, visitor):
        visitor.visit(self)

    def find_move_position(self, creature, end_goal):
        return self.move_position_state.find_move_position(creature, end_goal)

    @property
    def attack_move_position(self):
        return self._attack_move_position

    @property
    def move_position(self):
        return self._move_position

    @property
    def move_position_state(self):
        return self._move_position_state

    @move_position_state.setter
    def move_position_state(self, state):
        self._move_position_state = state

    @property
    def current_turn(self):
        return self._current_turn

    @current_turn.setter
    def current_turn(self, current_turn):
        self._current_turn = current_turn

    @property
    def creature_list(self):
        return self._creature_list

    @creature_list.setter
    def creature_list(self, creature_list):
        self._creature_list = creature_list

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        assert player in self._moveable_list
        self._player = player

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, game_canvas):
        assert self._interface is None
        self._interface = game_canvas

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        self._rounds = value

    def game_over(self):  # TODO Check if this works.
        if self._moveable_list[0].creature_type is "human":
            print("You are the only creature left alive.")
        else:
            print("You died.")
        print("Game over.")
        exit()

    def start_day(self, start_menu):
        start_menu.destroy()
        day_count = 1
        self.day(day_count)

    def day(self, day_count):
        self.creature_list.sort(key=lambda x: x.initiative_check())
        # TODO Remove creatures from list when they die, not just remove from observers?
        print("The sun comes up.")
        self.dark = False
        print("Day " + str(day_count))
        print("Turn Order:")
        for creature in self.creature_list:
            print(creature.name)
        self.round()
        day_count += 1
        self.day(day_count)

    def round(self):
        print("")
        print("Round " + str(self.rounds))
        if self.rounds > 25:
            self.dark = True
            print("")
            print("The sun goes down.")
            exit()
        self.turn()

    def turn(self):
        creature = self.creature_list[self.index]
        if len(self._moveable_list) == 1:
            self.game_over()
        self.info_pane = InfoPane(self.interface._root, self.interface.canvas, self, self.player)
        self.end_turn_boolean = True
        # creature.prepare_attack = False
        self.current_turn = creature.name
        if creature.hunger_points == 0:
            print("The human is starving.")
        print(creature.name + " attempts to perceive.")
        self.notify_perception_observers(self, creature)
        while self.end_turn_boolean:
            if creature.action_count <= 0:
                self.info_pane.end_turn()
            elif creature.creature_type is "human":
                self.interface.canvas.wait_variable(creature.end_turn)
            elif creature.current_state.name is not "dead":
                self.creature_action(creature)

    def end_turn(self, info_pane):
        info_pane.destroy()
        self.end_turn_boolean = False
        if self.index < (len(self.creature_list) - 1):
            self.index += 1
            self.turn()
        else:
            self.index = 0
            for creature in self.creature_list:
                if (creature.current_state.name == "unconscious and dying" or
                        creature.current_state.name == "unconscious, but stable" or
                        creature.current_state.name == "dead"):
                    creature.action_count = 0
                    creature.standard_action = 0
                    creature.move = 0
                if creature.current_state.name == "staggered":
                    creature.action_count = 1
                    creature.standard_action = 1
                    creature.move_action = 1
                else:
                    creature.action_count = 2
                    creature.standard_action = 1
                    creature.move_action = 2
            self.rounds += 1
            self.round()

    def creature_action(self, creature):
        """Creature Action

        Determines a type of action for the creature. A location is sent to the action method.
        Called by the turn method when on a non-human turn.

        Args:
            creature: the acting creature

        """
        # TODO Sneak is broken.
        # if creature.move.name is not "sneak":
            # creature.set_move(Sneak())
        # self.notify_stealth_observers(self, creature)

        if creature.creature_type is "wolf":
            if creature.standard_action > 0:
                creature.notify_attack_range_observers(creature)
            if creature.prepare_attack and creature.standard_action > 0:
                end = [creature.target.position_col, creature.target.position_row]
                self.action(creature, end)
            elif creature.prepare_attack and creature.standard_action <= 0:
                creature.action_count = 0
            else:
                creature.notify_attack_move_observers(creature)
                if creature.prepare_attack_move:
                    creature.prepare_attack_move = False
                    end_goal = [creature.target.position_col, creature.target.position_row]
                    self.accept_visitor(self.attack_move_position_visitor)
                    end = self.find_move_position(creature, end_goal)
                else:
                    start = [2024, 384]
                    if creature.position == start:
                        end = [creature.position_col - (creature.speed * 64), creature.position_row]
                    else:
                        self.accept_visitor(self.move_position_visitor)
                        end = self.find_move_position(creature, start)
                self.action(creature, end)
        else:
            # TODO Add deer action.
            creature.action_count -= 2
        self.redraw()

    def player_action(self, event):
        """Player Action

        Takes an event and turns it into a location.
        Called by the interface when the user clicks the screen.

        Args:
            event: a click event

        """
        event_col = int(self.interface.canvas.canvasx(event.x))
        event_row = int(self.interface.canvas.canvasy(event.y))
        end = [event_col, event_row]
        self.action(self.player, end)

    def action(self, creature, end):
        """Action

        Decides whether the action is a move or an attack and calls the right method.
        Both creature_action and player_action call action after a location is determined.

        Args:
            creature: the acting creature
            end: the end location for either an attack, a movement, or some other interaction

        """
        interval = 64
        move_distance = creature.speed * interval
        start = [creature.position_col, creature.position_row]
        distance = int(self.distance.compute(start, end))
        if creature.action_count > 0:
            if distance <= move_distance:
                creature.possible_move = end
                creature.prepare_move = True

            creature.notify_move_observers(creature)

            # TODO Add location interaction check
            # It should also be impossible to move through a location, instead it needs to find the best path
            # around the object.

            if creature.prepare_attack and creature.standard_action > 0:
                creature.possible_move_col = creature.position_col
                creature.possible_move_row = creature.position_row
                creature.prepare_move = False
                col = creature.position_col
                row = creature.position_row
                possible_col = creature.possible_move_col
                possible_row = creature.possible_move_row
                if (possible_col in range(int(col) - interval, int(col) + interval) and
                        possible_row in range(int(row) - interval, int(row) + interval)):
                    creature.execute_attack(creature, creature.target, self)
                    self.interface.action_text(creature)
                creature.prepare_attack = False
            elif creature.prepare_move:
                creature.execute_move(creature)
                self.move(creature)
                creature.prepare_move = False

    def move(self, creature):
        """Move

        Gradually moves changes a creatures location. Changes the human player's image for every step.
        Called by action.

        Args:
            creature: the acting creature

        """
        col_num = 4
        row_num = 4
        while (creature.possible_move_col != creature.position_col or
               creature.possible_move_row != creature.position_row):
            if creature.prepare_move:
                if creature.possible_move_col < creature.position_col:
                    creature.position_col += -col_num
                if creature.possible_move_col > creature.position_col:
                    creature.position_col += +col_num
                if creature.possible_move_row < creature.position_row:
                    creature.position_row += -row_num
                if creature.possible_move_row > creature.position_row:
                    creature.position_row += +row_num
                if self.image_state < 4 and creature.creature_type == "human":
                    # TODO This is happening too quickly
                    self.image_state += 1
                    if self.image_state == 4:
                        self.image_state = 0
                    creature.set_image_state(creature.image_list[self.image_state])
                creature.position = [creature.position_col, creature.position_row]
                if self.distance.compute(creature.possible_move, creature.position) < 4:
                    col_num = 1
                    row_num = 1
                self.redraw()
        self.image_state = 0
        if creature.creature_type == "human":
            creature.set_image_state(creature.image_list[self.image_state])
            self.redraw()

    def hide(self, creature):
        self._unregister_drawable(creature)
        self.redraw()

    def perceive(self, creature):
        self._register_drawable(creature)

    def death(self, creature):
        self._creature_list.remove(creature)

    def add_text_object(self, new_object):
        self._text_object_list.append(new_object)

    def remove_text_object(self, new_object):
        self._text_object_list.remove(new_object)

    def add_stationary_world_object(self, new_object):
        self._immovable_list.append(new_object)
        new_object.add_observer(self)
        self.add_observer(new_object)
        if isinstance(new_object, GameDrawable):
            self._drawable.append(new_object)

    def add_world_object(self, new_object):
        self._moveable_list.append(new_object)
        new_object.add_observer(self)
        self.add_observer(new_object)
        if isinstance(new_object, GameDrawable):
            self._register_drawable(new_object)

    def remove_world_object(self, old_object):
        if old_object in self._moveable_list:
            self._moveable_list.remove(old_object)
            old_object.remove_observer(self)
            self.remove_observer(old_object)
        if old_object in self._immovable_list:
            self._immovable_list.remove(old_object)
        if old_object in self._drawable:
            self._unregister_drawable(old_object)
        self.redraw()

    def _register_drawable(self, obj):
        assert isinstance(obj, GameDrawable)
        assert obj not in self._drawable
        self._drawable.append(obj)
        self.redraw()

    def _unregister_drawable(self, obj):
        assert isinstance(obj, GameDrawable)
        assert obj in self._drawable
        self._drawable.remove(obj)

    def redraw(self):
        self.interface.redraw(self._drawable)

    def move_update(self, player):
        self.notify_move_observers(player)

    def attack_range_update(self, creature):
        self.notify_attack_range_observers(creature)

    def attack_move_update(self, creature):
        self.notify_attack_move_observers(creature)

    def change_move(self, key_press):
        self.player.change_move(key_press)