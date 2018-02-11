from God_eye import *

""" *************************************************
                DEBUG FUNCTION 
************************************************* """


def print_battle_map(battle_map):
    """
    Print battle map to console
    """

    for row in battle_map:
        print(row)


def test_aoe(aoe):
    """
    Display AOE (%) in console
    :param aoe: skill's AOE
    :type aoe: list of tuples
    """

    test_map = create_battle_map(5, 5)
    test_map[2][2] = "(X)"
    for x, y in aoe:
        test_map[2 + x][2 + y] = "%"

    print_battle_map(test_map)


def test_all_aoe():
    """
    Test all AOE available, show on map (warning: no skill name, so check the order of aoe_list below)
    """

    aoe_list = [skill_aoe_double_h,
                skill_aoe_double_v,
                skill_aoe_corner,
                skill_aoe_cross_d,
                skill_aoe_cross_h]

    for each in aoe_list:
        print(each)
        test_aoe(each)


def test_populate_map(battle_map):
    """
    Populate battle_map with dummy value
    :param battle_map: battle_map
    :type battle_map: list of list
    """

    battle_map[5][4] = "!"
    battle_map[3][1] = "!"
    battle_map[4][2] = "*"
    battle_map[4][1] = "@"
    battle_map[3][4] = "*"
    battle_map[2][2] = "*"
    battle_map[3][5] = "!"
    battle_map[7][6] = "!"
    battle_map[5][3] = "!"
    battle_map[6][4] = "*"
    battle_map[6][3] = "@"
    battle_map[5][5] = "*"
    battle_map[8][5] = "*"
    battle_map[6][7] = "!"

    battle_map[3][2] = "!"
    battle_map[5][1] = "!"
    battle_map[8][3] = "*"
    battle_map[4][6] = "?"
    battle_map[3][8] = "*"
    battle_map[3][3] = "*"
    battle_map[6][6] = "!"
    battle_map[3][6] = "!"
    battle_map[7][7] = "!"
    battle_map[7][2] = "*"
    battle_map[2][6] = "@"
    battle_map[7][4] = "*"
    battle_map[4][2] = "*"
    battle_map[6][7] = "!"

    battle_map[2][2] = "!"
    battle_map[2][3] = "!"
    battle_map[2][4] = "*"
    battle_map[2][5] = "@"
    battle_map[2][6] = "*"
    battle_map[6][2] = "*"
    battle_map[6][3] = "!"
    battle_map[6][4] = "!"
    battle_map[6][5] = "!"
    battle_map[6][6] = "*"
    battle_map[3][6] = "@"
    battle_map[4][8] = "?"
    battle_map[5][6] = "*"
    battle_map[3][2] = "@"
    battle_map[4][2] = "*"
    battle_map[5][2] = "*"

    battle_map[3][4] = "*"
    battle_map[5][4] = "@"
    battle_map[3][3] = "*"
    battle_map[4][3] = "*"
    battle_map[5][3] = "!"


""" *************************************************
                USABLE FUNCTION 
************************************************* """


def create_battle_map(row, col):
    """
    Create matrix rox x col, initialize with neutral tile
    :param row: battle map row
    :type row: int
    :param col: battle map col
    :type col: int
    :return: battle map
    :rtype: list of list
    """

    battle_map = []
    for x in range(0, row):

        new_row = []
        for y in range(0, col):
            new_row.append(tile_mode_neutral)

        battle_map.append(new_row)

    return battle_map


def attack_mode_examine_map(battle_map, pivot, usable_skill):
    """
    Function to examine 5x5 tiles around pivot, to find best skill to use on best position
    :param battle_map: battle_map
    :type battle_map: list of list
    :param pivot: searching pivot
    :type pivot: int,int
    :param usable_skill: list of usable skill to check
    :type usable_skill: list
    :return: examine report
    :rtype:
    """

    pivot_x, pivot_y = pivot
    examine_report = []

    # Iterate spiral (inside - out) 5x5 from pivot
    for dx, dy in search_list_5x5:
        try:

            current_x = pivot_x + dx
            current_y = pivot_y + dy

            # For each skill, evaluate it
            for skill in usable_skill:
                examine_result = examine_skill_effect(battle_map, (current_x, current_y), skill)

                examine_result["skill"] = skill
                examine_result["x"] = current_x
                examine_result["y"] = current_y

                examine_report.append(examine_result)
        except:
            pass

    return examine_report


def examine_skill_effect(battle_map, pivot, skill_type):
    """
    Function to examine skill effect if activate on pivot
    :param battle_map: battle_map
    :type battle_map: list of list
    :param pivot: pivot of skill activation
    :type pivot: int,int
    :param skill_type: type of skill used
    :type skill_type: string
    :return: examine result
    :rtype: dict
    """

    def tile_examine_template():
        """
        Create basic template
        :return: template
        :rtype: dict
        """

        return {"skill": None,
                "x": None,
                "y": None,
                "neutral": 0,
                "missed": 0,
                "hit": 0,
                "shield": 0,
                "potential": 0}

    def get_search_list():
        """
        Function to get search list based on skill typ
        :return: skill AOE
        :rtype: list
        """

        if skill_type == "double_h":
            search_list = skill_aoe_double_h
        elif skill_type == "double_v":
            search_list = skill_aoe_double_v
        elif skill_type == "corner":
            search_list = skill_aoe_corner
        elif skill_type == "cross_d":
            search_list = skill_aoe_cross_d
        elif skill_type == "cross_h":
            search_list = skill_aoe_cross_h
        # elif skill_type == "seeker":
        #     search_list = skill_aoe_seeker
        else:
            search_list = [(0, 0)]

        return search_list

    def tile_examine(tile):
        """
        Function to Examine each tile
        :param tile: which tile to check
        :type tile: list element
        :return: type of tile
        :rtype: string
        """

        if tile == tile_mode_shield:
            return "shield"
        elif tile == tile_mode_missed:
            return "missed"
        elif tile == tile_mode_hit:
            return "hit"
        elif tile == tile_mode_potential:
            return "potential"
        else:
            return "neutral"

    # def mark_potential(tile):

    # Separate x and y
    pivot_x, pivot_y = pivot

    # Create basic template
    examine_result = tile_examine_template()

    # Get list of tile to search
    search_list = get_search_list()

    # Check tile one by one
    for dx, dy in search_list:
        try:

            # Examine
            tile_status = tile_examine(battle_map[pivot_x + dx][pivot_y + dy])
            examine_result[tile_status] += 1

        except:
            pass

    return examine_result


def greedy_pick(player, examine_report, show=False):
    """
    Find best record
    :param player:
    :type player:
    :param examine_report:
    :type examine_report:
    :return:
    :rtype:
    """

    best_record = examine_report[0]
    skill_cost = player.cost
    max_value = -888

    # Coefficient to adjust
    p_coef = 125
    n_coef = 20

    m_coef = -20
    h_coef = -20
    s_coef = -20

    # Calculate
    for examine_result in examine_report:

        value = 0
        value += examine_result["potential"] * p_coef   # adjacent tile (has best potential) - diurus regi
        value += examine_result["neutral"] * n_coef     # not hit

        value += examine_result["missed"] * m_coef
        value += examine_result["hit"] * h_coef
        value += examine_result["shield"] * s_coef

        not_hit = examine_result["potential"] + examine_result["neutral"]
        already_hit = examine_result["missed"] + examine_result["hit"] + examine_result["shield"] + 1

        t_coef = not_hit * not_hit / (already_hit + not_hit)
        value *= t_coef

        c_coef = (already_hit + not_hit) / skill_cost[examine_result["skill"]]
        value *= c_coef

        if show:
            print(value, examine_result)

        # Find best one
        if value > max_value:
            max_value = value
            best_record = examine_result

    return best_record


def write_command(decision):

    code = 0
    pos_x = decision["x"]
    pos_y = decision["y"]

    skill = decision["skill"]
    if skill == "normal":
        code = 1
    elif skill == "double_v":
        code = 2
    elif skill == "double_h":
        code = 3
    elif skill == "corner":
        code = 4
    elif skill == "cross_d":
        code = 5
    elif skill == "cross_h":
        code = 6
    elif skill == "seeker":
        code = 7
    elif skill == "shield":
        code = 8

    output = "{},{},{}".format(code, pos_x, pos_y)

    # CHANGE IT TO TXT LATER
    print(output)


if __name__ == '__main__':

    # TESTING PURPOSE
    battle_map = create_battle_map(10, 10)
    test_populate_map(battle_map)
    battle_map[4][9] = "X"
    print_battle_map(battle_map)

    # BOT SECTION
    megumi = Player(filename)
    # inspect_object(megumi)
    last_hit = (4, 7)

    # Check and determine which skill to use
    examine_report = attack_mode_examine_map(battle_map, pivot=last_hit, usable_skill=megumi.usable_skill)
    best_result = greedy_pick(megumi, examine_report)

    print(best_result)
    write_command(best_result)
