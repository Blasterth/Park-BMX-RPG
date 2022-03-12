from random import choice
from statistics import mode
import logging
from playsound import playsound
from time import sleep
from threading import Thread
logging.basicConfig(level=logging.DEBUG)

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

def bgm():
    while True:
        def loop_playback():
            playsound("1-01. Persona (Arrange Version).mp3", block=False)
            sleep(207)
        loop_playback()



# Battle
def game():

    # Welcome
    print("Hello.")
    player_name = input("Please enter your name/nickname.")
    if player_name == "":
        player_name = "Nameless"
    player.update({"Name" : player_name})
    logging.debug("Welcome starts.")

    # Stats of Characters (to avoid changing the values in the dicts)
    global player_health
    player_health = int(player["HP"])
    global bad_guy_health
    bad_guy_health = int(bad_guy["HP"])
    global player_offense
    player_offense = int(player["Offense"])
    global bad_guy_offense
    bad_guy_offense = int(bad_guy["Offense"])
    global player_defense
    player_defense = int(player["Defense"])
    global bad_guy_defense
    bad_guy_defense = int(bad_guy["Defense"])

    # Player's Action Record
    player_action_record_mode_all = []
    player_action_record_mode_round = []
    player_action_record_mode_recent = []
    loop_breaker_1 = []
    loop_breaker_2 = []

    # Time
    global round
    round = 1
    global turn
    turn = 1

    while (player_health > 0) and (bad_guy_health > 0):
        logging.debug("Game starts.")

        # Action Booleans
        global player_attack
        player_attack = None
        global player_defend
        player_defend = None
        bad_guy_attack = None
        bad_guy_defend = None
        global counter_attack_1
        counter_attack_1 = None
        global counter_attack_2
        counter_attack_2 = None

        # Intro
        print(f"Round {round}")
        print(f"Turn {turn}")
        print(f"{player_name}'s HP = {player_health}")
        print(f"Bad Guy's HP = {bad_guy_health}")
        logging.debug("Intro is shown.")

        # Player's Action
        def player_action():
            action = input("Attack or Defend? Type A or D.")
            logging.debug("Input is taken.")
            if action[0] == ("a" or "A"):
                global player_attack
                player_attack = True
                global player_defend
                player_defend = False
                player_action_record_mode_all.append("Attack")
                player_action_record_mode_round.append("Attack")
                player_action_record_mode_recent.append("Attack")
                loop_breaker_1.append("Attack")
                loop_breaker_2.append("Attack")
            elif action[0] == ("d" or "D"):
                player_defend = True
                player_attack = False
                player_action_record_mode_all.append("Defend")
                player_action_record_mode_round.append("Defend")
                player_action_record_mode_recent.append("Defend")
                loop_breaker_1.append("Defend")
                loop_breaker_2.append("Defend")
            else:
                print("Command not recognised!")
                logging.debug("Error message is shown.")
                player_action()
        player_action()

        # Bad Guy's Action (AI)
        strategy_1 = mode(player_action_record_mode_all)
        strategy_2 = mode(player_action_record_mode_round)
        strategy_3 = mode(player_action_record_mode_recent)

                # Round 1, Turn 1 Strategy
        if (strategy_1 and strategy_2 and strategy_3) == False:
            round_1_action_l = ["Attack", "Defend"]
            round_1_action = choice(round_1_action_l)

            # "No Data on target. Let's Attack."
            if round_1_action == "Attack":
                bad_guy_attack = True
                bad_guy_defend = False

            # "No Data on target. Let's Defend."
            elif round_1_action == "Defend":
                bad_guy_attack = False   
                bad_guy_defend = True

        # Round X, Turn 1 Strategy
        elif ((strategy_1 and strategy_3) == True) and (strategy_2 == False):

            # "The target is going to Attack. Must Defend."
            if strategy_3 == "Attack":
                bad_guy_attack = False
                bad_guy_defend = True

            # "The target is going to Defend. Must Attack."
            elif strategy_3 == "Defend":
                bad_guy_attack = True
                bad_guy_defend = False

        # Overall Strategy
        else:

            # "I'm sure the target's about to..."
            if strategy_1 == strategy_2:

                # "...Attack. Must Defend."
                if (strategy_1 or strategy_2) == "Attack":
                    bad_guy_attack = False
                    bad_guy_defend = True

                # "...Defend. Must Attack."
                elif (strategy_1 or strategy_2) == "Defend":
                    bad_guy_attack = True
                    bad_guy_defend = False

            # "I'm not sure about target's plan..."
            elif strategy_1 != strategy_2:

                # "...He might Attack. Must Defend."
                if strategy_3 == "Attack":
                    bad_guy_attack = False
                    bad_guy_defend = True

                # "...He might Attack. Must Defend."
                elif strategy_3 == "Defend":
                    bad_guy_attack = True
                    bad_guy_defend = False

        # Bad Guy's Action (AI) - Loop Breaker 1: 3-in-a-row
        if len(loop_breaker_1) == 1:
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
                bad_guy_attack = None
                bad_guy_defend = None
            elif loop_breaker_1[1] != loop_breaker_1[2]:
                counter_attack_1 = False
                loop_breaker_1.clear()
                bad_guy_attack = True
                bad_guy_defend = False

        # Bad Guy's Action (AI) - Loop Breaker 2: Zigzag
        elif len(loop_breaker_2) == 1:
            counter_attack_2 = False
        elif len(loop_breaker_2) == 2:
            if loop_breaker_2[0] != loop_breaker_2[1]:
                counter_attack_2 = False
            elif loop_breaker_2[0] == loop_breaker_2[1]:
                counter_attack_2 = False
                loop_breaker_2.clear()
        elif len(loop_breaker_2) > 2 and len(loop_breaker_2) < 10:
            if loop_breaker_2[len(loop_breaker_2) - 1] != loop_breaker_2[len(loop_breaker_2) - 2]:
                counter_attack_2 = False
            if loop_breaker_2[len(loop_breaker_2) - 1] == loop_breaker_2[len(loop_breaker_2) - 2]:
                counter_attack_2 = True
        elif len(loop_breaker_2) == 10:
            counter_attack_2 = True

        # Clash

        # Counter Attack Off
        if counter_attack_1 == False:
            logging.debug(f"Counter attack is off.")
            logging.debug(f"player_attack = {player_attack}.")
            logging.debug(f"bad_guy_attack = {bad_guy_attack}")
            logging.debug(f"player_defend = {player_defend}")
            logging.debug(f"bad_guy_defend = {bad_guy_defend}")

            # Player Attack; Bad Guy Attack
            if ((player_attack == True) and (player_defend == False)) and ((bad_guy_attack == True) and (bad_guy_defend == False)):
                player_health -= bad_guy_offense
                bad_guy_health -= player_offense
                logging.debug("Player attacks; Bad Guy attacks.")

            # Player Attack; Bad Guy Defend
            elif ((player_attack == True) and (player_defend == False)) and ((bad_guy_attack == False) and (bad_guy_defend == True)):
                bad_guy_health -= (player_offense - player_defense)
                logging.debug("Player attacks; Bad Guy defends.")

            # Player Defend; Bad Guy Attack
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_attack == True) and (bad_guy_defend == False)):
                player_health -= (bad_guy_offense - player_defense)
                logging.debug("Player defends; Bad Guy attacks.")

            # Player Defend; Bad Guy Defend
            elif ((player_attack == False) and (player_defend == True)) and ((bad_guy_attack == False) and (bad_guy_defend == True)):
                logging.debug("Player defends; Bad Guy defends.")
                pass

        # Counter Attack 1 On
        elif counter_attack_1 == True:
            logging.debug("Counter attack 1 is on.")

            # Player Attack; Bad Guy Counter Attack
            if (player_attack == True) and (player_defend == False):
                player_health -= (2 * (bad_guy_offense))
                bad_guy_health -= player_offense
                logging.debug("Player attacks; Bad Guy counter attacks.")

            # Player Defend; Bad Guy Counter Attack
            elif (player_attack == False) and (player_defend == True):
                player_health -= ((2 * bad_guy_offense) - player_defense)
                logging.debug("Player defends; Bad Guy counter attacks.")

        # Counter Attack 2 On
        elif counter_attack_2 == True:
            logging.debug("Counter attack 2 is on.")

            # Player Attack; Bad Guy Counter Attack
            if (player_attack == True) and (player_defend == False):
                if len(loop_breaker_2) < 10:
                    player_health -= (bad_guy_offense + len(loop_breaker_2))
                    bad_guy_health -= player_offense
                else:
                    player_health -= (bad_guy_offense + 13)
                    bad_guy_health -= player_offense
                logging.debug("Player attacks; Bad Guy counter attacks.")

            # Player Defend; Bad Guy Counter Attack
            elif (player_attack == False) and (player_defend == True):
                if len(loop_breaker_2) < 10:
                    player_health -= ((bad_guy_offense + len(loop_breaker_2)) - player_defense)
                else:
                    player_health -= ((bad_guy_offense + 13) - player_defense)
                logging.debug("Player attacks; Bad Guy counter attacks.")

        if (player_health > 0) and (bad_guy_health > 0):
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
                bad_guy_health += 5
                print("HP Recovered.")
                    
                # Resetting player_action_record_mode_round for the next Round
                player_action_record_mode_round.clear()

                # Updating player_action_record_mode_recent
                if len(player_action_record_mode_recent) == 5:
                    player_action_record_mode_recent.pop(0)
                
                logging.debug("Preparations for turn 5 have been made.")
        else:
                    
                # Resetting player_action_record_mode_round for the next Round
                player_action_record_mode_round.clear()

                # Updating player_action_record_mode_recent
                if len(player_action_record_mode_recent) == 5:
                    player_action_record_mode_recent.pop(0)

                logging.debug('Preprations made.')            

    # Replay
    def replay():
        replay_answer = input("Do you wish to replay?")
        logging.debug("Input is taken.")
        if replay_answer[0] == ("y" or "Y"):
            global player_health
            player_health = int(player["HP"])
            global bad_guy_health
            bad_guy_health = int(bad_guy["HP"])
            logging.debug("HPs are reset.")
            logging.debug("Game restarts.")
            game()
        elif replay_answer[0] == ("n" or "N"):
            logging.debug("Game exits.")
            input()
            exit()
        else:
            print("Command not recognised!")
            logging.debug("Error message is shown.")
            replay()

    # Outro
    def outro():
        if (player_health == 0) and (bad_guy_health != 0):
            print("GAME OVER")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy's HP = {bad_guy_health}")
            logging.debug("Results are shown.")
            replay()
        elif (player_health != 0) and (bad_guy_health == 0):
            print("YOU WIN")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = {player_health}")
            print(f"Bad Guy's HP = 0")
            logging.debug("Results are shown.")
            replay()
        elif (player_health and bad_guy_health) <= 0:
            print("DRAW")
            print(f"Round {round}")
            print(f"Turn {turn}")
            print(f"{player_name}'s HP = 0")
            print(f"Bad Guy's HP = 0")
            logging.debug("Results are shown.")
            replay()
    outro()

if __name__ == "__main__":
    
    # Threads
    rpg_game = Thread(target=game, args=())
    background_music = Thread(target=bgm, args=(), daemon=True)

    # Start Threads
    rpg_game.start()

    background_music.start()

    # Join Threads
    rpg_game.join()

logging.info("Game is fully functional!")
input()
exit()