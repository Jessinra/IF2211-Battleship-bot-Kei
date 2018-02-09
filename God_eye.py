import json
from pprint import pprint

#  DEBUG & TESTING PURPOSE
game_round = 79
game_player = 'A'

#  DEBUG & TESTING PURPOSE FILENAME CHECK
filename = "./sample/Phase 2 - Round {1}/{0}/state.json".format(game_player, game_round)
state_data = json.load(open(filename))

filename_old = "./sample/Phase 2 - Round {1}/{0}/state.json".format(game_player, game_round-4)
state_data_old = json.load(open(filename_old))


def inspect_object(object):
    """
    << DEBUG >> Show object structure
    """

    print("==================== Object:", object.__class__.__name__, "=========================")
    pprint(vars(object))
    print("======================= end ======================\n\n")


class Player:

    def __init__(self, state_data):

        # Get player points
        try:
            self.points = state_data["PlayerMap"]["Owner"]["Points"]
        except:
            self.points = None

        # Get player energy
        try:
            self.energy = state_data["PlayerMap"]["Owner"]["Energy"]
        except:
            self.energy = None

        # Get player remaining_ship
        try:
            self.remaining_ship = state_data["PlayerMap"]["Owner"]["ShipsRemaining"]
        except:
            self.remaining_ship = None

        # Get player ACTIVE ship
        try:
            self.ship = []

            # Search for active ship
            for ship in state_data["PlayerMap"]["Owner"]["Ships"]:

                if not ship["Destroyed"]:

                    # Gather ship's location and status
                    locations = []
                    for tile in ship["Cells"]:
                        record = {"x": tile["X"],
                                  "y": tile["Y"],
                                  "hit": tile["Hit"],
                                  "shieldhit": tile["ShieldHit"],
                                  "shield": tile["Shielded"]}
                        locations.append(record)

                    # Insert ship data to user ship list
                    ship_data = {ship["ShipType"]: locations}
                    self.ship.append(ship_data)

        except:
            self.ship = []

        # Get player usable_skill
        try:
            self.usable_skill = []

            for ship in self.ship:
                for ship_name in ship:
                    if "Submarine" in ship_name:
                        self.usable_skill.append("seeker")

                    elif "Destroyer" in ship_name:
                        self.usable_skill.append("double_h")
                        self.usable_skill.append("double_v")

                    elif "Battleship" in ship_name:
                        self.usable_skill.append("cross_d")

                    elif "Cruiser" in ship_name:
                        self.usable_skill.append("cross_h")

                    elif "Carrier" in ship_name:
                        self.usable_skill.append("corner")

                    else:
                        continue

        except :
            self.usable_skill = []

        # Get player shield
        try:
            self.shield = state_data["PlayerMap"]["Owner"]["Shield"]

        except:
            self.shield = None


class Opponent:

    def __init__(self, state_data):

        try:
            self.unsunken_ship = []

            for ship in state_data["OpponentMap"]["Ships"]:
                if not ship["Destroyed"]:
                    self.unsunken_ship.append(ship["ShipType"])
        except:
            self.unsunken_ship = []


class Game:

    def __init__(self):

        try:
            self.round = state_data["Round"]
        except:
            self.round = None

        try:
            self.dimension = state_data["MapDimension"]
        except:
            self.dimension = None


def last_hit(player_current, player_past):
    """
    Get last tile hit
    :param player_current: player current state
    :type player_current: object
    :param player_past: player past state
    :type player_past: object
    :return: last hit position (X,Y)
    :rtype: int, int
    """

    for i in range(0, len(player_current.ship)):

        for ship_name in player_current.ship[i]:

            for j in range(0, len(player_current.ship[i][ship_name])):

                hit = player_current.ship[i][ship_name][j]['hit']
                s_hit = player_current.ship[i][ship_name][j]['shieldhit']

                past_hit = player_past.ship[i][ship_name][j]['hit']
                past_s_hit = player_past.ship[i][ship_name][j]['shieldhit']

                if (hit != past_hit) or (s_hit != past_s_hit):

                    last_hit_x = player_past.ship[i][ship_name][j]['x']
                    last_hit_y = player_past.ship[i][ship_name][j]['y']

                    return last_hit_x, last_hit_y



if __name__ == '__main__':

    megumi = Player(state_data)
    inspect_object(megumi)

    past_megumi = Player(state_data_old)

    last_hit_x, last_hit_y = last_hit(megumi, past_megumi)
    print("LAST HIT :",last_hit_x, last_hit_y)

    reash = Opponent(state_data)
    inspect_object(reash)
