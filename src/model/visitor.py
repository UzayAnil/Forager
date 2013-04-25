from model.audio import *


class Visitable(object):

    def __init__(self):
        super(Visitable, self).__init__()

    def accept_visitor(self, visitor):
        pass


class Visitor(object):

    def __init__(self):
        super(Visitor, self).__init__()

    def visit(self, visitable):
        pass


class AttackAudioVisitor(Visitor):

        def __init__(self):
            super(AttackAudioVisitor, self).__init__()
            self.human_attack = AudioFile('../audio/human_attack.wav')
            self.wolf_attack = AudioFile('../audio/wolf_attack.wav')

        def visit_human(self):
            self.human_attack.play()
            self.human_attack.close()

        def visit_wolf(self):
            self.wolf_attack.play()
            self.wolf_attack.close()


class HurtAudioVisitor(Visitor):  # TODO Find new sounds

    def __init__(self):
        super(HurtAudioVisitor, self).__init__()
        self.human_hit = AudioFile('../audio/human_hurt.wav')
        self.wolf_hit = AudioFile('../audio/wolf_hurt.wav')

    def visit_human(self):
        self.human_hit.play()
        self.human_hit.close()

    def visit_wolf(self):
        self.wolf_hit.play()
        self.wolf_hit.close()


class AttackMovePositionVisitor(Visitor):

    def __init__(self):
        super(AttackMovePositionVisitor, self).__init__()

    def visit(self, visitable):
        visitable.move_position_state = visitable.attack_move_position


class MovePositionVisitor(Visitor):

    def __init__(self):
        super(MovePositionVisitor, self).__init__()

    def visit(self, visitable):
        visitable.move_position_state = visitable.move_position