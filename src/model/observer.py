

class Observable(object):

    def __init__(self, **kwargs):
        super(Observable, self).__init__(**kwargs)
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    # def notify_observers(self, creature):
        # for observer in self._observers:
            # observer.update(creature)

    def notify_death_observers(self, creature):
        for observer in self._observers:
            observer.death_update(creature)

    def notify_move_observers(self, creature):
        for observer in self._observers:
            observer.move_update(creature)

    def notify_perception_observers(self, world, creature):
        for observer in self._observers:
            observer.perception_update(world, creature)

    def notify_stealth_observers(self, world, creature):
        for observer in self._observers:
            observer.stealth_update(world, creature)

    def notify_attack_range_observers(self, creature):
        for observer in self._observers:
            observer.attack_range_update(creature)

    def notify_attack_move_observers(self, creature):
        for observer in self._observers:
            observer.attack_move_update(creature)


class Observer(object):

    def __init__(self, **kwargs):
        super(Observer, self).__init__(**kwargs)

    # def update(self, creature):
        # pass

    def death_update(self, creature):
        pass

    def move_update(self, creature):
        pass

    def perception_update(self, world, creature):
        pass

    def stealth_update(self, world, creature):
        pass

    def attack_range_update(self, creature):
        pass

    def attack_move_update(self, creature):
        pass