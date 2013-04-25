import tkinter as tk
from src.controller.world import GameWorld
from src.model.creatures import *
from src.model.locations import *
from src.model.decorators import *
from src.view.start_window import StartWindow
from src.view.interface import Interface


world = GameWorld()
interface = Interface(2560, 2560, game_world=world)
world.interface = interface
interface.world = world
interface.scrolling_handler()

grass = Grass(1280, 1280, 'map', '../images/grass.gif', 1280, 1280)
tree01 = Tree(106, 166, 'tree01', '../images/tree.gif', 96, 128)
tree02 = Tree(1806, 806, 'tree02', '../images/tree.gif', 96, 128)
tree03 = Tree(1006, 1006, 'tree03', '../images/tree.gif', 96, 128)
tree04 = Tree(1306, 126, 'tree04', '../images/tree.gif', 96, 128)
tree05 = Tree(106, 1306, 'tree05', '../images/tree.gif', 96, 128)
tree06 = Tree(506, 706, 'tree06', '../images/tree.gif', 96, 128)
tree07 = Tree(2006, 2006, 'tree07', '../images/tree.gif', 96, 128)
tree08 = Tree(1506, 606, 'tree08', '../images/tree.gif', 96, 128)
tree09 = Tree(2406, 306, 'tree09', '../images/tree.gif', 96, 128)
tree10 = Tree(606, 1506, 'tree10', '../images/tree.gif', 96, 128)
tree11 = DeadTree(Tree(2400, 2400, 'tree11', '../images/tree.gif', 96, 128), '../images/dead_tree.gif')
rock01 = Rock(1200, 700, 'rock01', '../images/big_rock.gif', 72, 82)
tall_grass01 = TallGrass(1080, 430, 'tall grass', '../images/tall_grass.gif', 256, 128)

campsite01 = Campsite(300, 150, 'campsite01', '../images/fire01.gif', 32, 32)

location_list = [grass, tree01, tree02, tree03, tree04, tree05, tree06, tree07, tree08, tree09, tree10, rock01,
                 campsite01, tall_grass01, tree11]
for location in location_list:
    world.add_stationary_world_object(location)

wolf = Wolf(540, 128, 'Wolf', '../images/wolf.gif', 32, 34)
buck = Deer(512, 1024, 'Buck', '../images/buck.gif', 33, 33)
doe = Deer(580, 1024, 'Doe', '../images/doe.gif', 33, 33)
human = Human(384, 128, 'Human', '../images/human_stand_front.gif', 32, 32)

creature_list = [human, wolf]
for creature in creature_list:
    world.add_world_object(creature)

world.creature_list = creature_list
interface.creature_list = creature_list
world.player = human

interface._canvas.update()
root = interface._root
StartWindow(root, interface, world)

tk.mainloop()