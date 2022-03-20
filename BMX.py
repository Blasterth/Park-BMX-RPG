import logging

# Player's Stats
player = {
    "Name" : None,
    "HP" : 50,
    "Offense" : 7,
    "Defense" : 5,
    "Special" : 15
}

# Bad Guy's Stats
bad_guy = {
    "Name" : "Bad Guy",
    "HP" : 50,
    "Offense" : 7,
    "Defense" : 5
}

def welcome():
    print("Hello.")
    player_name = input("Please enter your name/nickname.")
    if player_name == "":
        player_name = "Nameless"
    player.update({"Name" : player_name})
    logging.debug("Welcome starts.")