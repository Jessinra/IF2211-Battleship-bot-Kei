import json
from pprint import pprint

#  DEBUG & TESTING PURPOSE
game_round = 74
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


if __name__ == '__main__':

    megumi = Player(state_data)
    inspect_object(megumi)

    past_megumi = Player(state_data_old)
    inspect_object(past_megumi)

    reash = Opponent(state_data)
    inspect_object(reash)
