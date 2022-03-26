from random import choice
from statistics import mode
import logging
logging.basicConfig(level=logging.DEBUG)

# Player's Stats
global player
player = {
    "Name" : None,
    "HP" : 50,
    "Offense" : 7,
    "Defense" : 5,
    "SP" : 0,
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
    "Offense" : 8,
    "Defense" : 4
}

global shadow_player
shadow_player = {
    "Name" : None,
    "HP" : 150,
    "Offense" : 9,
    "Defense" : 3
}

score = 0

# Welcome
print("Hello.")
global player_name
player_name = input("Please enter your name/nickname.")
if player_name == "":
    player_name = "Nameless"
player.update({"Name" : player_name})
shadow_player.update({"Name" : f"Shadow {player_name}"})

# Stage 2
def stage2():

    # Stats of Characters (to avoid changing the values in the dicts)
    global player_health
    player_health = int(player["HP"])
    global bad_guy_1_health
    bad_guy_1_health = int(bad_guy_1["HP"])
    global player_offense
    player_offense = int(player["Offense"])
    global bad_guy_1_offense
    bad_guy_1_offense = int(bad_guy_1["Offense"])
    global player_defense
    player_defense = int(player["Defense"])
    global bad_guy_1_defense
    bad_guy_1_defense = int(bad_guy_1["Defense"])

    # Player's Action Record
    player_action_record_mode_all_2 = []
    player_action_record_mode_round_2 = []
    player_action_record_mode_recent_2 = []
    loop_breaker_1 = []
    loop_breaker_2 = []

    # Time
    global round
    round = 1
    global turn
    turn = 1

    while (player_health > 0) and (bad_guy_1_health > 0):
        logging.debug("Game starts.")

        # Action Booleans
        global player_attack
        player_attack = None
        global player_defend
        player_defend = None
        bad_guy_1_attack = None
        bad_guy_1_defend = None
        global counter_attack_1
        counter_attack_1 = None
        global counter_attack_2
        counter_attack_2 = None

        # Intro
        print(f"Round {round}")
        print(f"Turn {turn}")
        print(f"{player_name}'s HP = {player_health}")
        print(f"Bad Guy's HP = {bad_guy_1_health}")
        logging.debug("Intro is shown.")

        # Player's Action
        def player_action():
            action = input("Attack or Defend? Type A or D.")
            logging.debug("Input is taken.")
            if len(action) == 0:
                print("No input entered!") 
                logging.debug("Error message is shown.")
                player_action()
            elif action[0].lower() == "a":
                global player_attack
                player_attack = True
                global player_defend
                player_defend = False
                player_action_record_mode_all_2.append("Attack")
                player_action_record_mode_round_2.append("Attack")
                player_action_record_mode_recent_2.append("Attack")
                loop_breaker_1.append("Attack")
                loop_breaker_2.append("Attack")
            elif action[0].lower() == "d":
                player_defend = True
                player_attack = False
                player_action_record_mode_all_2.append("Defend")
                player_action_record_mode_round_2.append("Defend")
                player_action_record_mode_recent_2.append("Defend")
                loop_breaker_1.append("Defend")
                loop_breaker_2.append("Defend")
            else:
                print("Command not recognised!")
                logging.debug("Error message is shown.")
                player_action()
        player_action()

        # Bad Guy's Action (AI)
        strategy_1 = mode(player_action_record_mode_all_2)
        strategy_2 = mode(player_action_record_mode_round_2)
        strategy_3 = mode(player_action_record_mode_recent_2)

                # Round 1, Turn 1 Strategy
        if (strategy_1 and strategy_2 and strategy_3) == False:
            round_1_action_l = ["Attack", "Defend"]
            round_1_action = choice(round_1_action_l)

            # "No Data on target. Let's Attack."
            if round_1_action == "Attack":
                bad_guy_1_attack = True
                bad_guy_1_defend = False

            # "No Data on target. Let's Defend."
            elif round_1_action == "Defend":
                bad_guy_1_attack = False   
                bad_guy_1_defend = True

        # Round X, Turn 1 Strategy
        elif ((strategy_1 and strategy_3) == True) and (strategy_2 == False):

            # "The target is going to Attack. Must Defend."
            if strategy_3 == "Attack":
                bad_guy_1_attack = False
                bad_guy_1_defend = True

            # "The target is going to Defend. Must Attack."
            elif strategy_3 == "Defend":
                bad_guy_1_attack = True
                bad_guy_1_defend = False

        # Overall Strategy
        else:

            # "I'm sure the target's about to..."
            if strategy_1 == strategy_2:

                # "...Attack. Must Defend."
                if (strategy_1 or strategy_2) == "Attack":
                    bad_guy_1_attack = False
                    bad_guy_1_defend = True

                # "...Defend. Must Attack."
                elif (strategy_1 or strategy_2) == "Defend":
                    bad_guy_1_attack = True
                    bad_guy_1_defend = False

            # "I'm not sure about target's plan..."
            elif strategy_1 != strategy_2:

                # "...He might Attack. Must Defend."
                if strategy_3 == "Attack":
                    bad_guy_1_attack = False
                    bad_guy_1_defend = True

                # "...He might Attack. Must Defend."
                elif strategy_3 == "Defend":
                    bad_guy_1_attack = True
                    bad_guy_1_defend = False

        # Bad Guy's Action (AI) - Loop Breaker 1: 3-in-a-row
        if len(loop_breaker_1) <= 1:
            counter_attack_1 = False
        elif len(loop_breaker_1) == 2:
            if loop_breaker_1[0] == loop_breaker_1[1]:
                counter_attack_1 = False
            elif loop_breaker_1[0] != loop_breaker_1[1]:
                counter_attack_1 = False
                loop_breaker_1.clear()
        elif len(loop_breaker_1) == 3:
            if loop_breaker_1[1] == loop_breaker_1[2]:
                counter_attack_1 = True
                loop_breaker_1.clear()
                bad_guy_1_attack = None
                bad_guy_1_defend = None
            elif loop_breaker_1[1] != loop_breaker_1[2]:
                counter_attack_1 = False
                loop_breaker_1.clear()
                bad_guy_1_attack = True
                bad_guy_1_defend = False

        # Bad Guy's Action (AI) - Loop Breaker 2: Zigzag
        if len(loop_breaker_2) <= 1:
            counter_attack_2 = False
        elif len(loop_breaker_2) == 2:
            if loop_breaker_2[0] != loop_breaker_2[1]:
                counter_attack_2 = False
            elif loop_breaker_2[0] == loop_breaker_2[1]:
                counter_attack_2 = False
                loop_breaker_2.clear()
        elif len(loop_breaker_2) > 2:
            if loop_breaker_2[len(loop_breaker_2) - 1] != loop_breaker_2[len(loop_breaker_2) - 2]:
                counter_attack_2 = False
            if loop_breaker_2[len(loop_breaker_2) - 1] == loop_breaker_2[len(loop_breaker_2) - 2]:
                counter_attack_2 = True

        # Clash

        # Counter Attack Off
        if counter_attack_1 == False and counter_attack_2 == False:
            logging.debug(f"Counter attack is off.")
            logging.debug(f"player_attack = {player_attack}.")
            logging.debug(f"bad_guy_1_attack = {bad_guy_1_attack}")
            logging.debug(f"player_defend = {player_defend}")
            logging.debug(f"bad_guy_1_defend = {bad_guy_1_defend}")
            logging.debug(f"{loop_breaker_2}")

            # Player Attack; Bad Guy Attack
            if ((player_attack == True) and (player_defend == False)) and ((bad_guy_1_attack == True) and (bad_guy_1_defend == False)):
                player_health -= bad_guy_1_offense
                bad_guy_1_health -= player_offense
                logging.debug("Player attacks; Bad Guy attacks.")

            # Player Attack; Bad Guy Defend
            elif ((player_attack == True) and (player_defend == False)) and ((bad_guy_1_attack == False) and (bad_guy_1_defend == True)):
                bad_guy_1_health -= (player_offense - player_defense)
                logging.debug("Player attacks; Bad Guy defends.")

            # Player Defend; Bad Guy Attack
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_1_attack == True) and (bad_guy_1_defend == False)):
                player_health -= (bad_guy_1_offense - player_defense)
                logging.debug("Player defends; Bad Guy attacks.")

            # Player Defend; Bad Guy Defend
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_1_attack == False) and (bad_guy_1_defend == True)):
                logging.debug("Player defends; Bad Guy defends.")
                pass

        # Counter Attack 1 On
        elif counter_attack_1 == True:

            # Player Attack; Bad Guy Counter Attack
            if (player_attack == True) and (player_defend == False):
                player_health -= (2 * (bad_guy_1_offense))
                bad_guy_1_health -= player_offense

            # Player Defend; Bad Guy Counter Attack
            elif (player_attack == False) and (player_defend == True):
                player_health -= ((2 * bad_guy_1_offense) - player_defense)

        # Counter Attack 2 On
        elif counter_attack_2 == True:
            logging.debug("Counter attack 2 is on.")

            # Player Attack; Bad Guy Counter Attack
            if (player_attack == True) and (player_defend == False):
                    player_health -= (bad_guy_1_offense + len(loop_breaker_2))
                    bad_guy_1_health -= player_offense
                    loop_breaker_2.clear()
                    logging.debug("Player attacks; Bad Guy counter attacks.")

            # Player Defend; Bad Guy Counter Attack
            elif (player_attack == False) and (player_defend == True):
                    player_health -= ((bad_guy_1_offense + len(loop_breaker_2)) - player_defense)
                    loop_breaker_2.clear()
                    logging.debug("Player attacks; Bad Guy counter attacks.")

        if (player_health > 0) and (bad_guy_1_health > 0):
            # Preparing for the next Turn
            if turn < 5:
                turn += 1

                logging.debug("Preparations for turn 1-4 have been made.")
            elif turn == 5:
                turn = 1
                round += 1
                print("Time Out!")

                # HP Recovery
                player_health += 5
                bad_guy_1_health += 5
                print("HP Recovered.")
                    
                # Resetting player_action_record_mode_round_1 for the next Round
                player_action_record_mode_round_2.clear()

                # Updating player_action_record_mode_recent_1
                if len(player_action_record_mode_recent_2) == 5:
                    player_action_record_mode_recent_2.pop(0)
                
                logging.debug("Preparations for turn 5 have been made.")
        else:
                    
                # Resetting player_action_record_mode_round_1 for the next Round
                player_action_record_mode_round_2.clear()

                # Updating player_action_record_mode_recent_1
                if len(player_action_record_mode_recent_2) == 5:
                    player_action_record_mode_recent_2.pop(0)

                logging.debug('Preprations made.')            

    # Replay
    def replay_1_bad():
        replay_answer = input("Do you wish to replay?")
        logging.debug("Input is taken.")
        if replay_answer[0] == ("y" or "Y"):
            global player_health
            player_health = int(player["HP"])
            global bad_guy_1_health
            bad_guy_1_health = int(bad_guy_1["HP"])
            logging.debug("HPs are reset.")
            logging.debug("Game restarts.")
            stage1()
        elif replay_answer[0] == ("n" or "N"):
            logging.debug("Game exits.")
            input()
            exit()
        else:
            print("Command not recognised!")
            logging.debug("Error message is shown.")
            replay_1_bad()

    # Outro
    def outro():
        if (player_health == 0) and (bad_guy_1_health != 0):
            print("GAME OVER")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy 1's HP = {bad_guy_1_health}")
            logging.debug("Results are shown.")
            replay_1_bad()
        elif (player_health != 0) and (bad_guy_1_health == 0):
            print("YOU WIN")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = {player_health}")
            print(f"Bad Guy's HP = 0")
            logging.debug("Results are shown.")
            replay_1_bad()
        elif (player_health and bad_guy_1_health) <= 0:
            print("DRAW")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy's HP = 0")
            logging.debug("Results are shown.")
            replay_1_bad()
    outro()

# Stage 1
def stage1():

    # Stats of Characters (to avoid changing the values in the dicts)
    global player_health
    player_health = int(player["HP"])
    global bad_guy_1_health
    bad_guy_1_health = int(bad_guy_1["HP"])
    global player_offense
    player_offense = int(player["Offense"])
    global bad_guy_1_offense
    bad_guy_1_offense = int(bad_guy_1["Offense"])
    global player_defense
    player_defense = int(player["Defense"])
    global bad_guy_1_defense
    bad_guy_1_defense = int(bad_guy_1["Defense"])

    # Player's Action Record
    player_action_record_mode_all_1 = []
    player_action_record_mode_round_1 = []
    player_action_record_mode_recent_1 = []
    loop_breaker_1 = []

    # Time
    global round
    round = 1
    global turn
    turn = 1

    while (player_health > 0) and (bad_guy_1_health > 0):

        # Action Booleans
        global player_attack
        player_attack = None
        global player_defend
        player_defend = None
        bad_guy_1_attack = None
        bad_guy_1_defend = None
        global counter_attack_1
        counter_attack_1 = None
        global counter_attack_2
        counter_attack_2 = None

        # Intro
        print(f"Round {round}")
        print(f"Turn {turn}")
        print(f"{player_name}'s HP = {player_health}")
        print(f"Bad Guy's HP = {bad_guy_1_health}")

        # Player's Action
        def player_action():
            action = input("Attack or Defend? Type A or D.")
            logging.debug("Input is taken.")
            if len(action) == 0:
                print("No input entered!") 
                logging.debug("Error message is shown.")
                player_action()
            elif action[0].lower() == "a":
                global player_attack
                player_attack = True
                global player_defend
                player_defend = False
                player_action_record_mode_all_1.append("Attack")
                player_action_record_mode_round_1.append("Attack")
                player_action_record_mode_recent_1.append("Attack")
                loop_breaker_1.append("Attack")
            elif action[0].lower() == "d":
                player_defend = True
                player_attack = False
                player_action_record_mode_all_1.append("Defend")
                player_action_record_mode_round_1.append("Defend")
                player_action_record_mode_recent_1.append("Defend")
                loop_breaker_1.append("Defend")
            else:
                print("Command not recognised!")
                logging.debug("Error message is shown.")
                player_action()
        player_action()

        # Bad Guy's Action (AI)
        strategy_1 = mode(player_action_record_mode_all_1)
        strategy_2 = mode(player_action_record_mode_round_1)
        strategy_3 = mode(player_action_record_mode_recent_1)

                # Round 1, Turn 1 Strategy
        if (strategy_1 and strategy_2 and strategy_3) == False:
            round_1_action_l = ["Attack", "Defend"]
            round_1_action = choice(round_1_action_l)

            # "No Data on target. Let's Attack."
            if round_1_action == "Attack":
                bad_guy_1_attack = True
                bad_guy_1_defend = False

            # "No Data on target. Let's Defend."
            elif round_1_action == "Defend":
                bad_guy_1_attack = False   
                bad_guy_1_defend = True

        # Round X, Turn 1 Strategy
        elif ((strategy_1 and strategy_3) == True) and (strategy_2 == False):

            # "The target is going to Attack. Must Defend."
            if strategy_3 == "Attack":
                bad_guy_1_attack = False
                bad_guy_1_defend = True

            # "The target is going to Defend. Must Attack."
            elif strategy_3 == "Defend":
                bad_guy_1_attack = True
                bad_guy_1_defend = False

        # Overall Strategy
        else:

            # "I'm sure the target's about to..."
            if strategy_1 == strategy_2:

                # "...Attack. Must Defend."
                if (strategy_1 or strategy_2) == "Attack":
                    bad_guy_1_attack = False
                    bad_guy_1_defend = True

                # "...Defend. Must Attack."
                elif (strategy_1 or strategy_2) == "Defend":
                    bad_guy_1_attack = True
                    bad_guy_1_defend = False

            # "I'm not sure about target's plan..."
            elif strategy_1 != strategy_2:

                # "...He might Attack. Must Defend."
                if strategy_3 == "Attack":
                    bad_guy_1_attack = False
                    bad_guy_1_defend = True

                # "...He might Attack. Must Defend."
                elif strategy_3 == "Defend":
                    bad_guy_1_attack = True
                    bad_guy_1_defend = False

        # Bad Guy's Action (AI) - Loop Breaker 1: 3-in-a-row
        if len(loop_breaker_1) <= 1:
            counter_attack_1 = False
        elif len(loop_breaker_1) == 2:
            if loop_breaker_1[0] == loop_breaker_1[1]:
                counter_attack_1 = False
            elif loop_breaker_1[0] != loop_breaker_1[1]:
                counter_attack_1 = False
                loop_breaker_1.clear()
        elif len(loop_breaker_1) == 3:
            if loop_breaker_1[1] == loop_breaker_1[2]:
                counter_attack_1 = True
                loop_breaker_1.clear()
                bad_guy_1_attack = None
                bad_guy_1_defend = None
            elif loop_breaker_1[1] != loop_breaker_1[2]:
                counter_attack_1 = False
                loop_breaker_1.clear()
                bad_guy_1_attack = True
                bad_guy_1_defend = False

        # Clash

        # Counter Attack Off
        if counter_attack_1 == False:

            # Player Attack; Bad Guy Attack
            if ((player_attack == True) and (player_defend == False)) and ((bad_guy_1_attack == True) and (bad_guy_1_defend == False)):
                player_health -= bad_guy_1_offense
                bad_guy_1_health -= player_offense

            # Player Attack; Bad Guy Defend
            elif ((player_attack == True) and (player_defend == False)) and ((bad_guy_1_attack == False) and (bad_guy_1_defend == True)):
                bad_guy_1_health -= (player_offense - player_defense)

            # Player Defend; Bad Guy Attack
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_1_attack == True) and (bad_guy_1_defend == False)):
                player_health -= (bad_guy_1_offense - player_defense)

            # Player Defend; Bad Guy Defend
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_1_attack == False) and (bad_guy_1_defend == True)):
                pass

        # Counter Attack 1 On
        elif counter_attack_1 == True:

            # Player Attack; Bad Guy Counter Attack
            if (player_attack == True) and (player_defend == False):
                player_health -= (2 * (bad_guy_1_offense))
                bad_guy_1_health -= player_offense

            # Player Defend; Bad Guy Counter Attack
            elif (player_attack == False) and (player_defend == True):
                player_health -= ((2 * bad_guy_1_offense) - player_defense)

        if (player_health > 0) and (bad_guy_1_health > 0):
            # Preparing for the next Turn
            if turn < 5:
                turn += 1

            elif turn == 5:
                turn = 1
                round += 1
                print("Time Out!")

                # HP Recovery
                player_health += 5
                bad_guy_1_health += 5
                print("HP Recovered.")
                    
                # Resetting player_action_record_mode_round_1 for the next Round
                player_action_record_mode_round_1.clear()

                # Updating player_action_record_mode_recent_1
                if len(player_action_record_mode_recent_1) == 5:
                    player_action_record_mode_recent_1.pop(0)
        else:
                    
                # Resetting player_action_record_mode_round_1 for the next Round
                player_action_record_mode_round_1.clear()

                # Updating player_action_record_mode_recent_1
                if len(player_action_record_mode_recent_1) == 5:
                    player_action_record_mode_recent_1.pop(0)    

    # Replay-1-Bad
    def replay_1_bad():
        replay_answer = input("Do you wish to replay?")
        if replay_answer[0] == ("y" or "Y"):
            global player_health
            player_health = int(player["HP"])
            global bad_guy_1_health
            bad_guy_1_health = int(bad_guy_1["HP"])
            stage1()
        elif replay_answer[0] == ("n" or "N"):
            input()
            exit()
        else:
            print("Command not recognised!")
            replay_1_bad()

    # Replay-1-Good
    def replay_1_good():
        stage_2_answer = input("Do you wish to proceed to Stage 2?")
        if stage_2_answer[0] == ("y" or "Y"):
            print("Development of Stage 2 is in progress.\nYou can find its incomplete code in the Stages.py.\nThank you 4 your patience.")
            replay_1_bad()
        if stage_2_answer[0] == ("n" or "N"):
            replay_1_bad()

    # Outro
    def outro():
        if (player_health <= 0) and (bad_guy_1_health >= 0):
            print("GAME OVER")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy 1's HP = {bad_guy_1_health}")
            replay_1_bad()
        elif (player_health >= 0) and (bad_guy_1_health <= 0):
            print("YOU WIN")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = {player_health}")
            print(f"Bad Guy's HP = 0")
            replay_1_good()
        elif (player_health <= 0) and (bad_guy_1_health <= 0):
            print("DRAW")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy's HP = 0")
            replay_1_bad()
    outro()

stage2()