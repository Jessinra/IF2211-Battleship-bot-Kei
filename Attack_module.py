from Database import *

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
    battle_map[3][3] = "*"
    battle_map[2][2] = "*"
    battle_map[3][5] = "!"
    battle_map[7][6] = "!"
    battle_map[5][3] = "!"
    battle_map[6][4] = "*"
    battle_map[6][3] = "@"
    battle_map[5][5] = "*"
    battle_map[8][5] = "*"
    battle_map[6][7] = "!"


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


def attack_mode_examine_map(battle_map, pivot_x, pivot_y, usable_skill):
    """
    Function to examine 5x5 tiles around pivot, to find best skill to use on best position
    :param battle_map: battle_map
    :type battle_map: list of list
    :param pivot_x: searching pivot x
    :type pivot_x: int
    :param pivot_y: searching pivot y
    :type pivot_y: int
    :param usable_skill: list of usable skill to check
    :type usable_skill: list
    :return:
    :rtype:
    """

    # Iterate spiral (inside - out) 5x5 from pivot
    for dx, dy in search_list_5x5:
        try:

            current_x = pivot_x + dx
            current_y = pivot_y + dy

            # For each skill, evaluate it
            for skill in usable_skill:
                examine_result = examine_skill_effect(battle_map, current_x, current_y, skill)

        except:
            pass


def examine_skill_effect(battle_map, pivot_x, pivot_y, skill_type):
    """
    Function to examine skill effect if activate on pivot
    :param battle_map: battle_map
    :type battle_map: list of list
    :param pivot_x: pivot of skill activation (X)
    :type pivot_x: int
    :param pivot_y: pivot of skill activation (Y)
    :type pivot_y: int
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

        return {"neutral": 0,
                "missed": 0,
                "hit": 0,
                "shield": 0}

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
            search_list = []

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
        else:
            return "neutral"

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

    # Print result for visual check only
    print(examine_result)
    return examine_result





if __name__ == '__main__':

    battle_map = create_battle_map(10, 10)
    battle_map[4][4] = "X"
    test_populate_map(battle_map)
    print_battle_map(battle_map)


    usable_skill = ["cross_d", "double_h", "double_v", "corner"]
    attack_mode_examine_map(battle_map, pivot_x=4, pivot_y=4, usable_skill=usable_skill)
