from God_eye import *
from Attack_module import create_battle_map, print_battle_map

""" *************************************************
                DEBUG FUNCTION 
************************************************* """


def test_populate_map(battle_map):
    """
    Populate battle_map with dummy value
    :param battle_map: battle_map
    :type battle_map: list of list
    """

    battle_map[5][4] = "!"
    battle_map[3][1] = "!"
    battle_map[4][2] = "A"
    battle_map[4][1] = "A"
    battle_map[3][4] = "A"
    battle_map[2][2] = "A"
    battle_map[3][5] = "!"
    battle_map[7][6] = "!"
    battle_map[5][3] = "!"
    battle_map[6][4] = "A"
    battle_map[6][3] = "A"
    battle_map[5][5] = "A"
    battle_map[8][5] = "A"
    battle_map[6][7] = "!"

    battle_map[3][2] = "!"
    battle_map[5][1] = "!"
    battle_map[8][3] = "*"
    battle_map[4][6] = "A"
    battle_map[3][8] = "*"
    battle_map[3][3] = "A"
    battle_map[6][6] = "A"
    battle_map[3][6] = "A"
    battle_map[7][7] = "!"
    battle_map[7][2] = "*"
    battle_map[2][6] = "A"
    battle_map[7][4] = "*"
    battle_map[4][2] = "*"
    battle_map[6][7] = "!"

    battle_map[1][4] = "A"
    battle_map[9][2] = "A"
    battle_map[4][0] = "!"
    battle_map[7][1] = "!"
    battle_map[4][5] = "!"
    battle_map[6][1] = "A"
    battle_map[3][1] = "A"
    battle_map[5][7] = "A"
    battle_map[8][8] = "A"
    battle_map[4][8] = "!"


""" *************************************************
                USABLE FUNCTION 
************************************************* """


def examine_best_shield_position(player, battle_map, pivot):
    """
    Whole process of determining where to put shield
    :param player: player instance
    :type player: Player
    :param battle_map:
    :type battle_map:
    :param pivot: last user ship tile hit by enemy
    :type pivot:
    :return:
    :rtype:
    """

    def get_protect_list():
        """

        :return: list of active ship's tile
        :rtype: list
        """

        protect_list = []
        for ship in player.ship:
            for detail in ship.values():
                for tile in detail:
                    if not tile["hit"]:
                        protect_list.append((tile["x"], tile["y"]))

        return protect_list

    def evaluate_map():
        """
        Evaluate certain radius from last hit tile, to choose best shield pivot
        :return:
        :rtype:
        """

        radius = shield_info["CurrentRadius"]

        examine_report = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):

                try:
                    current_x = pivot_x + dx
                    current_y = pivot_y + dy
                    examine_result = examine_shield_effect(battle_map, (current_x, current_y), radius)

                    examine_result["x"] = current_x
                    examine_result["y"] = current_y

                    examine_report.append(examine_result)
                except:
                    pass

                    # print(examine_result)

        return examine_report

    pivot_x, pivot_y = pivot
    shield_info = player.shield
    protect_list = get_protect_list()

    # Check flag
    flag_charged = shield_info["CurrentCharges"] > 0
    flag_max_charged = shield_info["CurrentRadius"] == shield_info["MaxRadius"]
    flag_defensive = len(protect_list) <= 10
    flag_absolute_defense = len(protect_list) <= 5

    if flag_charged and (flag_absolute_defense or (flag_max_charged and flag_defensive)):

        # search
        examine_report = evaluate_map()

        return examine_report
    else:
        return "no need to shield"


def examine_shield_effect(battle_map, pivot, radius):
    """
    examine each tile, to find shield performance
    :param battle_map:
    :type battle_map:
    :param pivot:
    :type pivot:
    :param radius:
    :type radius:
    :return:
    :rtype:
    """

    def tile_examine(tile):
        """
        Function to Examine each tile
        :param tile: which tile to check
        :type tile: list element
        :return: type of tile
        :rtype: string
        """

        if tile == tile_mode_ship_active:
            return "active"
        elif tile == tile_mode_hit:
            return "hit"
        else:
            return "neutral"

    def tile_examine_template():
        """
        Create basic template
        :return: template
        :rtype: dict
        """

        return {"x": None,
                "y": None,
                "neutral": 0,
                "hit": 0,
                "active": 0}

    pivot_x, pivot_y = pivot
    examine_result = tile_examine_template()

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):

            try:
                tile_status = tile_examine(battle_map[pivot_x + dx][pivot_y + dy])
                examine_result[tile_status] += 1

            except:
                pass

    return examine_result


def greedy_pick(examine_report):

    best = examine_report[0]
    value_max = -888

    n_coef = 5
    a_coef = 50
    h_coef = -5


    for examine_result in examine_report:

        value = 0
        value += examine_result["neutral"] * n_coef
        value += examine_result["active"] * a_coef
        value += examine_result["hit"] * h_coef

        protected = examine_result["neutral"] + examine_result["active"]

        t_coef = protected / (protected + examine_result["hit"])
        value *= t_coef

        # print(value, examine_result)

        if value > value_max:
            best = examine_result
            value_max = value

    return best


def write_command(decision):

    output = "8,{},{}".format(decision["x"], decision["y"])
    print(output)


if __name__ == '__main__':

    # TESTING PURPOSE
    battle_map = create_battle_map(10, 10)
    test_populate_map(battle_map)
    battle_map[2][3] = "X"
    print_battle_map(battle_map)

    megumi = Player(filename)
    last_hit = (2, 2)
    examine_report = examine_best_shield_position(megumi, battle_map, last_hit)
    if examine_report != "no need to shield":
        best = greedy_pick(examine_report)
        write_command(best)
