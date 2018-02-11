import json
from Database import *
from pprint import pprint


#  DEBUG & TESTING PURPOSE FILENAME CHECK
filename = "./sample/Phase 2 - Round 42/A/state.json"
filename_old = "./sample/Phase 2 - Round 42/A/state.json"
filename_hit_log = "./sample/storage.txt"


def inspect_object(object_instance):
    """
    << DEBUG >> Show object structure
    """

    print("==================== Object:", object_instance.__class__.__name__, "=========================")
    pprint(vars(object_instance))
    print("======================= end ======================\n\n")


class Player:

    def __init__(self, filename):

        self.__get_state(filename)
        self.__get_points()
        self.__get_energy()
        self.__get_remaining_ship()
        self.__get_active_ship()
        self.__get_usable_skill()
        self.__get_shield_info()
        self.__get_skill_cost()
        self.__evaluate_usable_skill()

    def __get_state(self, filename):
        """
        Get state data
        """

        retry = 5
        self.state_data = None
        while retry > 0:
            try:
                self.state_data = json.load(open(filename))
                retry = 0
            except:
                retry -= 1

    def __get_points(self):
        """
        Get player points
        """

        try:
            self.points = self.state_data["PlayerMap"]["Owner"]["Points"]
        except:
            self.points = None

    def __get_energy(self):
        """
        Get player energy
        """

        try:
            self.energy = self.state_data["PlayerMap"]["Owner"]["Energy"]
        except:
            self.energy = None

    def __get_remaining_ship(self):
        """
        Get player remaining_ship
        """

        try:
            self.remaining_ship = self.state_data["PlayerMap"]["Owner"]["ShipsRemaining"]
        except:
            self.remaining_ship = None

    def __get_active_ship(self):
        """
        Get player ACTIVE ship
        """

        try:
            self.ship = []

            # Search for active ship
            for ship in self.state_data["PlayerMap"]["Owner"]["Ships"]:

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

    def __get_usable_skill(self):
        """
        Get player usable_skill
        """

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

        except Exception as e:
            print(e)
            self.usable_skill = []

    def __get_shield_info(self):
        """
        Get player shield
        """

        try:
            self.shield = self.state_data["PlayerMap"]["Owner"]["Shield"]

        except:
            self.shield = None

    def __get_skill_cost(self):

        self.cost = {"normal": 1}
        for skill in self.usable_skill:
            self.cost[skill] = skill_cost[self.state_data["MapDimension"]][skill]

    def __evaluate_usable_skill(self):

        filtered_skill = ["normal"]
        for skill in self.usable_skill:

            if self.energy >= self.cost[skill]:
                filtered_skill.append(skill)

        self.usable_skill = filtered_skill


class Opponent:

    def __init__(self, state_data):

        self.__get_active_ship(state_data)
        
    def __get_active_ship(self, state_data):
        
        try:
            self.active_ship = []

            for ship in state_data["OpponentMap"]["Ships"]:
                if not ship["Destroyed"]:
                    self.active_ship.append(ship["ShipType"])
        except:
            self.active_ship = []


class Game:

    def __init__(self, state_data):

        self.__get_round(state_data)
        self.__get_dimension(state_data)

    def __get_round(self, state_data):

        try:
            self.round = state_data["Round"]
        except:
            self.round = None

    def __get_dimension(self, state_data):

        try:
            self.dimension = state_data["MapDimension"]
        except:
            self.dimension = None


class GodEye:

    def __init__(self, filename):

        filename = GodEye.check_filename(filename)
        self.__get_state(filename)
        self.__get_ship(filename)

    def __get_state(self, filename):
        """
        Get state data
        """

        retry = 5
        self.state_data = None
        while retry > 0:
            try:
                self.state_data = json.load(open(filename))
                retry = 0
            except Exception as e:

                retry -= 1

    def __get_ship(self, filename):
        """
        Get ship data
        """

        player = Player(filename)
        ship_data = []

        for ship in player.ship:

            for ship_name in ship:

                for tile in ship[ship_name]:

                    if not tile["hit"] and not tile["shield"]:
                        x = tile['x']
                        y = tile['y']
                        ship_data.append((x, y))

        self.__ships = ship_data

    def ship(self):
        return self.__ships

    @staticmethod
    def check_filename(filename):

        index_start = filename.find("Round") + 6
        index_stop = filename.rfind("/state.json")

        game_data = filename[index_start:index_stop].split('/')
        game_round = int(game_data[0])
        game_player = game_data[1]

        if game_player == "A":
            return filename[:index_start] + str(game_round - 1) + "/B/state.json"

        if game_player == "B":
            return filename[:index_start] + str(game_round) + "/A/state.json"

    @staticmethod
    def last_hit(player_current, player_past):
        """
        Get last tile hit
        :param player_current: player current state
        :type player_current: player
        :param player_past: player past state
        :type player_past: player
        :return: last hit position x and y
        :rtype: int, int
        """
        storage = open(filename_hit_log, 'a')

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
                        storage.write(str(last_hit_x) + "," + str(last_hit_y)+"\n")

        try:
            storage = open(filename_hit_log, 'r')
            last_hit = None
            for line in storage:
                last_hit = line.strip()
            split_last_hit = last_hit.split(',')
            return int(split_last_hit[0]), int(split_last_hit[1])
        except:
            return None, None
