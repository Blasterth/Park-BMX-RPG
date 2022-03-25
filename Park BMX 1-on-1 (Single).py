import logging
import Stages
logging.basicConfig(level=logging.DEBUG)

# Player's Stats
global player
player = {
    "Name" : None,
    "HP" : 50,
    "Offense" : 7,
    "Defense" : 5,
    "Special" : 15
}

# Bad Guys' Stats
global bad_guy_1
bad_guy_1 = {
    "Name" : "Bad Guy 1",
    "HP" : 50,
    "Offense" : 7,
    "Defense" : 5
}

global bad_guy_2
bad_guy_2 = {
    "Name" : "Bad Guy 2",
    "HP" : 65,
    "Offense" : 7,
    "Defense" : 5
}
global bad_guy_3
bad_guy_3 = {
    "Name" : "Bad Guy 3",
    "HP" : 80,
    "Offense" : 7,
    "Defense" : 5
}
global johnny
johnny = {
    "Name" : "Johnny",
    "HP" : 100,
    "Offense" : 7,
    "Defense" : 5
}
global shadow_player
shadow_player = {
    "Name" : None,
    "HP" : 150,
    "Offense" : 9,
    "Defense" : 3
}

score = 0

# Game
Stages.stage1()
input()
exit()