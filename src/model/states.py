from tkinter import PhotoImage
from controller.distance import Distance


class ConditionState(object):

    def __init__(self):
        super(ConditionState, self).__init__()


class NormalState(ConditionState):

    def __init__(self, creature):
        super(NormalState, self).__init__()
        self.creature = creature
        self.name = "normal"

    def execute(self, creature):
        creature.action_count = 2
        creature.standard_action = 1
        creature.move_action = 2


class StaggeredState(ConditionState):

    def __init__(self, creature):
        super(StaggeredState, self).__init__()
        self.creature = creature
        self.name = "staggered"

    def execute(self, creature):
        if creature.action_count >= 1:
            creature.action_count = 1


class DeadState(ConditionState):

    def __init__(self, creature):
        super(DeadState, self).__init__()
        self.creature = creature
        self.name = "dead"

    def execute(self, creature, world):
        world.remove_world_object(creature)
        world.death(creature)
        creature.action_count = 0
        creature.standard_action = 0
        creature.move_action = 0

    def update(self):
        pass


class UnconsciousDyingState(ConditionState):

    def __init__(self, creature):
        super(UnconsciousDyingState, self).__init__()
        self.creature = creature
        self.name = "unconscious and dying"

    def execute(self, creature):
        creature.notify_death_observers(creature)
        creature.action_count = 0
        #creature.standard_action = 0
        #creature.move_action = 0


class UnconsciousStableState(ConditionState):

    def __init__(self, creature):
        super(UnconsciousStableState, self).__init__()
        self.creature = creature
        self.name = "unconscious, but stable"

    def execute(self, creature):
        creature.action_count = 0
        creature.standard_action = 0
        creature.move_action = 0


class Posture(object):

    def __init__(self):
        super(Posture, self).__init__()

    def execute(self, creature):
        pass


class Standing(Posture):

    def __init__(self):
        super(Standing, self).__init__()
        self.name = "standing"

    def execute(self, creature):
        pass


class Prone(Posture):
    """Prone

    The creature is lying on the ground.

    """

    def __init__(self):
        super(Prone, self).__init__()
        self.name = "prone"

    def execute(self, creature):
        creature.other = 4


class Facing(object):

    def __init__(self):
        super(Facing, self).__init__()


class ImageState(object):
    """Image State

    Used to change the player character's image during action.

    """

    def __init__(self):
        super(ImageState, self).__init__()
        self._sprite = None

    @property
    def sprite(self):
        return self._sprite


class StandFront(ImageState):

    def __init__(self):
        super(StandFront, self).__init__()
        self._sprite = PhotoImage(file='../images/human_stand_front.gif')


class WalkLeftFront(ImageState):

    def __init__(self):
        super(WalkLeftFront, self).__init__()
        self._sprite = PhotoImage(file='../images/human_walk_left_front.gif')


class WalkRightFront(ImageState):

    def __init__(self):
        super(WalkRightFront, self).__init__()
        self._sprite = PhotoImage(file='../images/human_walk_right_front.gif')


class WorldState(object):

    def __init__(self):
        super(WorldState, self).__init__()
        self.distance = Distance()


class AttackMovePosition(WorldState):
    """Attack Move Position

    Finds the location nearest a target location that is both greater than the attack range and
    less than the creature's speed.

    """

    def __init__(self):
        super(AttackMovePosition, self).__init__()

    def find_move_position(self, creature, end_goal):
        col_num = 1
        row_num = 1
        attack_range = creature.attack.attack_range
        target_col = end_goal[0]
        target_row = end_goal[1]
        current_col = creature.position_col
        current_row = creature.position_row
        current_position = creature.position
        while (self.distance.compute(current_position, end_goal) > attack_range and
               self.distance.compute(creature.position, current_position) < creature.speed * 64):
            if target_col < current_col:
                current_col += -col_num
            if target_col > current_col:
                current_col += +col_num
            if target_row < current_row:
                current_row += -row_num
            if target_row > current_row:
                current_row += +row_num
            current_position = [current_col, current_row]
        return current_position


class MovePosition(WorldState):
    """Move Position

    Finds the location nearest a target location that is both greater than 0 and
    less than the creature's speed.

    """

    def __init__(self):
        super(MovePosition, self).__init__()

    def find_move_position(self, creature, end_goal):
        col_num = 1
        row_num = 1
        target_col = end_goal[0]
        target_row = end_goal[1]
        current_col = creature.position_col
        current_row = creature.position_row
        current_position = creature.position
        while (self.distance.compute(current_position, end_goal) > 0 and
               self.distance.compute(creature.position, current_position) < creature.speed * 64):
            if target_col < current_col:
                current_col += -col_num
            if target_col > current_col:
                current_col += +col_num
            if target_row < current_row:
                current_row += -row_num
            if target_row > current_row:
                current_row += +row_num
            current_position = [current_col, current_row]
        return current_position