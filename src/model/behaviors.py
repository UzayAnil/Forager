import random
from model.states import *
from model.visitor import *


class Move(object):
    
    MOVE_COST = 1

    def __init__(self):
        super(Move, self).__init__()

    def speed(self, actor):
        pass

    def execute(self, actor):
        print(actor.name + " " + actor.move.action_name + ".")
        actor.action_count -= 1
        actor.move_action -= self.MOVE_COST
        #actor.acted.set(1)


class Charge(Move):

    def __init__(self):
        super(Charge, self).__init__()
        self.name = "charge"
        self.action_name = "charges"
        self.ACTION_COST = 1

    def speed(self, actor):
        actor.speed *= 4

    def execute(self, actor):
        print(actor.name + " " + actor.move.name + ".")
        actor.action_count -= 1
        actor.move_action -= self.MOVE_COST
        actor.standard_action -= self.ACTION_COST
        #actor.acted.set(1)
        actor.execute_attack()


class Run(Move):

    def __init__(self):
        super(Run, self).__init__()
        self.name = "run"
        self.action_name = "runs"
        self.ACTION_COST = 1

    def speed(self, actor):
        actor.speed *= 4

    def execute(self, actor):
        print(actor.name + " " + actor.move.action_name + ".")
        actor.action_count -= 1
        actor.move_action -= self.MOVE_COST
        actor.standard_action -= self.ACTION_COST
        #actor.acted.set(1)


class Crawl(Move):

    def __init__(self):
        super(Crawl, self).__init__()
        self.name = "crawl"
        self.action_name = "crawls"

    def speed(self, actor):
        actor.speed = 1


class Hustle(Move):

    def __init__(self):
        super(Hustle, self).__init__()
        self.name = "hustle"
        self.action_name = "hustles"

    def speed(self, actor):
        actor.speed *= 2


class OneSquareStep(Move):

    def __init__(self):
        super(OneSquareStep, self).__init__()
        self.name = "one-square-step"
        self.action_name = "takes a one-square-step"

    def speed(self, actor):
        actor.speed = 1


class Sneak(Move):

    def __init__(self):
        super(Sneak, self).__init__()
        self.name = "sneak"
        self.action_name = "sneaks"

    def speed(self, actor):
        actor.speed //= 2

    def execute(self, actor):
        print(actor.name + " sneaks.")
        actor.action_count -= 1
        actor.move_action -= self.MOVE_COST
        #actor.acted.set(1)


class StandUp(Move):

    def __init__(self):
        super(StandUp, self).__init__()
        self.name = "stand up"
        self.action_name = "stands up"

    def speed(self, actor):
        actor.speed = 0

    def execute(self, actor):
        actor.set_posture(Standing())
        print(actor.name + " stands up.")
        actor.action_count -= 1
        actor.move_action -= self.MOVE_COST
        ##actor.acted.set(1)


class Swim(Move):

    def __init__(self):
        super(Swim, self).__init__()
        self.name = "swim"
        self.action_name = "swims"

    def speed(self, actor):
        actor.speed //= 2


class Walk(Move):

    def __init__(self):
        super(Walk, self).__init__()
        self.name = "walk"
        self.action_name = "walks"

    def speed(self, actor):
        actor.speed = actor.base_speed


class FreeAction(object):

    def __init__(self):
        super(FreeAction, self).__init__()
        self.action_creature_type = "free action"
        self.ACTION_COST = 0


class DropProne(FreeAction):

    def __init__(self):
        super(DropProne, self).__init__()

    def speed(self, actor):
        actor.speed = actor.base_speed

    def execute(self, actor):
        if actor.posture.name != "prone":
            actor.set_posture(Prone())
        actor.set_move(Crawl())
        print(actor.name + " drops prone.")


class Attack(object):

    ACTION_COST = 1

    def __init__(self):
        super(Attack, self).__init__()
        self.attack_range = 64
        self.critical = 2

    def trip_check(self, actor, target):
        pass

    def damage_roll(self):
        return random.randint(1, 3)

    def execute(self, actor, target, world):
        attack_audio = AttackAudioVisitor()
        actor.accept_visitor(attack_audio)
        d20 = random.randint(1, 20)
        attack_roll = d20 + actor.base_attack_bonus + actor.str_mod - actor.other
        if actor.attack.name is "shoot":  # If attacker is shooting, a prone defender gets a +4 bonus to defense
            defense = 10 + target.dex_mod + target.dodge + actor.other
        else:  # If attacker is using melee, a prone defender takes -4 to defense
            defense = 10 + target.dex_mod + target.dodge - actor.other
        damage = self.damage_roll() + actor.str_mod - target.armor

        print(actor.name + " attempts to " + actor.attack.name + " the " + target.name + ".")

        if attack_roll > defense and damage > 0:
            print("The " + actor.attack.name + " hits!")
            if d20 == 20:
                print("Critical hit!")
                if self.critical == 2:
                    damage += self.damage_roll()
                else:
                    damage += self.damage_roll() + self.damage_roll()
            if target.vigor_points > 0:
                target.vigor_points -= damage
                if target.vigor_points < 0:
                    target.wound_points += target.vigor_points
                    target.vigor_points = 0
            else:
                target.wound_points -= damage
            # TODO Fix the hurt audio. Change name to damage audio?
            # hurt_audio = HurtAudioVisitor()
            # target.accept_visitor(hurt_audio)

            if damage > 1:
                print(target.name + " takes " + str(damage) + " points of damage!")
                print(target.name + " has " + str(target.vigor_points) + " vigor and "
                      + str(target.wound_points) + " wounds remaining.")
            elif damage == 1:
                print(target.name + " takes 1 point of damage!")
                print(target.name + " has " + str(target.vigor_points) + " vigor and "
                      + str(target.wound_points) + " wounds remaining.")
            else:
                print("The " + actor.attack.name + " fails to do damage.")

            if actor.name == "wolf" and target.wound_points > 0:
                self.trip_check(actor, target)

            if target.wound_points <= target.wound_threshold:
                if target.current_state.name != "staggered":
                    target.set_state(target.get_staggered_state())
                    print(target.name + " is " + target.current_state.name + "!")

            if target.wound_points <= 0:
                target.set_state(target.get_dead_state())
                target.current_state.execute(target, world)
                print(target.name + " dies!")
        else:
            print("The " + actor.attack.name + " fails to wound.")

        if actor.current_state.name == "staggered":
            actor.staggered_action()

        actor.action_count -= 1
        actor.standard_action -= actor.attack.ACTION_COST
        #actor.acted.set(1)


class UnarmedStrike(Attack):

    def __init__(self):
        super(UnarmedStrike, self).__init__()
        self.name = "strike"
        self.result = "struck"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 3)


class Bash(Attack):

    def __init__(self):
        super(Bash, self).__init__()
        self.name = "bash"
        self.result = "bashed"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 6)


class Bite(Attack):

    def __init__(self):
        super(Bite, self).__init__()
        self.name = "bite"
        self.result = "bit"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 6)

    def trip_check(self, actor, target):
        if target.posture.name is not "prone":
            actor.execute_combat_maneuver(actor, target)


class Gore(Attack):

    def __init__(self):
        super(Gore, self).__init__()
        self.name = "gore"
        self.result = "gored"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 6)


class Hack(Attack):

    def __init__(self):
        super(Hack, self).__init__()
        self.name = "hack"
        self.result = "hacked"
        self.critical = 3

    def damage_roll(self):
        return random.randint(1, 6)


class Poke(Attack):

    def __init__(self):
        super(Poke, self).__init__()
        self.name = "poke"
        self.result = "poked"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 4)


class Slice(Attack):

    def __init__(self):
        super(Slice, self).__init__()
        self.name = "slice"
        self.result = "sliced"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 4)


class Stab(Attack):

    def __init__(self):
        super(Stab, self).__init__()
        self.name = "stab"
        self.result = "stabbed"
        self.attack_range = 64
        self.critical = 2

    def damage_roll(self):
        return random.randint(1, 8)


class Shoot(Attack):

    def __init__(self):
        super(Shoot, self).__init__()
        self.name = "shoot"
        self.result = "shot"
        self.attack_range = 640

    def damage_roll(self):
        return random.randint(1, 6)


class CombatManeuver(object):

    def __init__(self):
        super(CombatManeuver, self).__init__()
        self.ACTION_COST = 1

    def combat_maneuver_roll(self):
        pass


class Trip(CombatManeuver):

    def __init__(self):
        super(Trip, self).__init__()

    def execute(self, actor, target):
        combat_maneuver_bonus = actor.base_attack_bonus + actor.str_mod  # FIX ME: -1 if small
        d20 = random.randint(1, 20)
        combat_maneuver_check = d20 + combat_maneuver_bonus
        combat_maneuver_defense = 10 + target.base_attack_bonus + target.str_mod

        print(actor.name + " attempts to trip the " + target.name + ".")

        if combat_maneuver_check > combat_maneuver_defense:
            target.set_posture(Prone())
            print(target.name + " trips and falls prone.")
        else:
            print(target.name + " continues to stand.")


class Skill(object):

    def __init__(self):
        super(Skill, self).__init__()
        self.target = None
        self.ACTION_COST = 1


class Acrobatics(Skill):

    def __init__(self):
        super(Acrobatics, self).__init__()
        self.name = "acrobatics"

    def execute(self, actor, target):
        skill_check = random.randint(1, 20) + actor.acrobatics
        combat_maneuver_defense = 10 + target.base_attack_bonus + target.str_mod

        print(actor.name + " attempts to move by the " + target.name + ".")

        if skill_check >= combat_maneuver_defense:
            print(actor.name + " is successful.")
        else:
            print(target.name + " gets an attack of opportunity!")
            target.attack.execute(target, actor)
        actor.action_count -= 1
        actor.standard_action -= self.ACTION_COST


class Craft(Skill):
    def __init__(self):
        super(Craft, self).__init__()
        self.name = "craft"

    def execute(self, actor):
        skill_check = random.randint(1, 20) + actor.perception
        difficulty_class = 12

        print(actor.name + " attempts to craft something.")

        if skill_check > difficulty_class:
            print(actor.name + " crafts something.")
        else:
            print(actor.name + " fails to craft something.")
        print("Action cost is " + str(self.ACTION_COST))
        actor.action_count -= 1
        actor.standard_action -= self.ACTION_COST


class Perception(Skill):
    def __init__(self):
        super(Perception, self).__init__()
        self.name = "perception"

    def execute(self, world, actor, target):
        if actor is not target and target in actor.hidden:
            skill_check = random.randint(1, 20) + actor.perception
            difficulty_class = random.randint(1, 20) + target.stealth

            if skill_check >= difficulty_class:
                print(actor.name + " perceives the " + target.name + ".")
                if actor.creature_type is "human":
                    world.perceive(target)
                target.remove_hidden(actor)
                    # target.hide = False


class Stealth(Skill):

    def __init__(self):
        super(Stealth, self).__init__()
        self.name = "stealth"

    def execute(self, world, actor, target):
        if actor is not target:
            # print(actor.name + " attempts to use stealth.")
            skill_check = random.randint(1, 20) + actor.stealth
            difficulty_class = random.randint(1, 20) + target.perception

            if skill_check >= difficulty_class:
                if target not in actor.hidden:
                    print(actor.name + " hides from the " + target.name + ".")
                    if target.creature_type is "human":
                        world.hide(actor)
                    actor.add_hidden(target)
            else:
                if target in actor.hidden:
                    print(actor.name + " fails to hide from the " + target.name + ".")
                    if target.creature_type is "human":
                        world.perceive(actor)
                    actor.remove_hidden(target)


class Survival(Skill):

    def __init__(self):
        super(Survival, self).__init__()
        self.name = "survival"

    def execute(self, actor):
        skill_check = random.randint(1, 20) + actor.survival
        difficulty_class = 12

        print(actor.name + " attempts to use survival skills.")

        if skill_check > difficulty_class:
            print(actor.name + " successful.")
        else:
            print(actor.name + " fails.")
        actor.standard_action -= self.ACTION_COST