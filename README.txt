[Forager]
Version 0.2 (alpha)

[CONTENTS]

1. INTRODUCTION
2. GAMEPLAY
3. CREDITS
4. PATTERNS


1. [INTRODUCTION]

[General Information]
Forager is a turn based game of hunting (gathering was never added). Currently, you can move around the map, change your move speed, and attack. On his turn, the Wolf will start chasing you down, if you are within his attack distance. If you move outside his attack distance, he will move to his "home". 

I had some pretty grand plans at the beginning of the term that, unfortunately, did not come to full fruition. In the end, I was able to create movement and combat systems which allow the player to move around the world, attacking and being attacked by a wolf. I had originally hoped to include both more creatures and additional game systems for item management and crafting (the gathering part). The latter would have made the game much more interesting. I had a great time with this project and I plan to continue working on it.

[Dependencies]
Forager is written in Python 3.3.
The game uses the third party pyaudio library. (http://people.csail.mit.edu/hubert/pyaudio/)

[Starting the game]
To play Forager run '../Forager/scripts/main.py'. The game will load a start screen. Click start to begin or click quit to end.


2. [GAMEPLAY]

[General]
Each turn, creatures, including the player character, can make two move actions, a move action and a standard action, or a full round action. Move actions include walking and sneaking, standard actions include attacking, and the only full round action currently available is running. After you have completed your actions, you will no longer be able to do anything until you click the end turn button at the bottom left.

[Movement]
On your turn, you may attempt to move around by clicking on an empty spot on the map. The following keys set the Human’s speed.
‘w’: Move is set to walk
‘h’: Move is set to hustle
‘r’: Move is set to run

[Attacking and Death]
If your Human is near a creature and you click on them, you will attack. "Attack!" will be displayed above their head to indicate you clicked in the correct space. If a creature’s wounds are reduced to at or below their wound threshold they become staggered and can only make one move or one attack each turn. If a creature’s wounds are reduced to 0 or below it dies.

Wolf starts out nearby and if he won the initiative check he will move toward you and attack. He will always attack you if you are nearby and he has a free standard action.

[Rounds]
There are 25 rounds in the game. At the beginning of Round 26 the sun goes down and the game is over.

[Turns]
Each round there are a number of turns equal to the number of currently living creatures.


3. [CREDITS]

[Artwork]
Most game art was created by the fine artists of Little Workshop for Mozilla's BrowserQuest. They most graciously licensed their work under the Creative Commons (CC-BY-SA 3.0).

It is all available at the following address:
https://github.com/mozilla/BrowserQuest

Everything else was drawn by me, though sometimes by tracing other designs. In particular, the wolf is patterned on images from arthurs-clipart.com.

[Audio]
Audio is from http://sounds.beachware.com/ who offer their sounds free for non-commercial use. 

The code in the audio package is a slightly modified version of the basic demo code the developers provide with the library.


4. [PATTERNS]

[Model/View/Controller]
The entire program is organized using this pattern. Generally speaking, the model includes static elements like the creatures and locations, the controller (mainly the world package) uses the model to generate dynamic activity, and the view displays that activity using a tkinter canvas.

[Strategy]
The strategy pattern is used throughout the program. The main places to look are in the behaviors and creatures packages. In behaviors, you will see all the different classes of attack, move, skill, etc. In creatures, you will see how each creature has various behaviors that can be changed in different ways.

[Observer]
The observer pattern is used mainly to facilitate communication between the model and the controller. You can find the code in the observer, world, and other packages. The actors notify the world, which notifies the world objects, which update the world, which tells the interface to draw the objects to the canvas.

[Decorator]
The decorator pattern is, to be frank, not my favorite pattern. It is used in an admittedly gimmicky fashion to change the image of one tree. I had previously attempted other uses and you will see them in the decorator package. I hope this is enough to display my knowledge of the pattern. You can see this in the main script and the decorators package.

[State]
The state pattern is found in the state and creature packages. Creatures have a state that changes between normal, staggered, and dead (and unconscious, but this was never implemented). These depend on their health. The player character has a state used to change his image as he moves. The world has a state that switches between two different versions of a find_move_position method. This is used by the non-player characters to decide where they will move.

[Visitor]
The visitor pattern is found in the visitor package. It is used to play audio when a creature attacks. This is done in the behavior package in the Attack class. The other use is integrated into one of the state patterns. It changes the state of the world so it can use two different find_move_position methods, discussed above.
