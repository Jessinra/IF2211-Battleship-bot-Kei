from God_eye import *

""" *************************************************
                DEBUG FUNCTION 
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
    battle_map[3][8] = "@"
    battle_map[3][9] = "@"
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
    battle_map[3][7] = "*"
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


def player_map(state):
    """
    return player map (parsed) in matrix
    :param state:
    :type state:
    :return:
    :rtype:
    """

    def idx(size, i, j):
        return i * size + j

    size = state['MapDimension']
    mat = [[tile_mode_neutral for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if state['OpponentMap']['Cells'][idx(size, i, j)]['Damaged']:
                mat[i][j] = tile_mode_hit
            elif state['OpponentMap']['Cells'][idx(size, i, j)]['Missed']:
                mat[i][j] = tile_mode_missed

            elif state['PlayerMap']['Cells'][idx(size, i, j)]['ShieldHit']:
                mat[i][j] = tile_mode_shield
            else:
                mat[i][j] = tile_mode_neutral
    return mat


def determine_potential(battle_map, pivot):
    """
    Return potential tile, given pivot (x,y)
    :param battle_map:
    :type battle_map:
    :param pivot:
    :type pivot:
    :return:
    :rtype:
    """

    point = []
    right = False
    left = False
    up = False
    down = False
    x, y = pivot
    abscissa = x

    def determine_direction(battle_map, x, y):
        """
        return pair of boolean, determine checking direction
        :param battle_map:
        :type battle_map:
        :param x:
        :type x:
        :param y:
        :type y:
        :return:
        :rtype:
        """

        horizontal = True
        vertical = True

        if battle_map[x+1][y] == tile_mode_hit or battle_map[x-1][y] == tile_mode_hit:
            horizontal = False

        if battle_map[x][y+1] == tile_mode_hit or battle_map[x][y-1] == tile_mode_hit:
            vertical = False

        return horizontal, vertical

    search_horizontal, search_vertical = determine_direction(battle_map, x, y)

    if search_horizontal:

        it = 1
        while not right or not left:
            if not right:
                ordinate = y
                if y + it > len(battle_map) - 1:
                    right = True

                elif battle_map[x][y + it] == tile_mode_hit:
                    pass

                elif battle_map[x][y + it] == tile_mode_neutral:
                    right = True
                    ordinate = ordinate + it
                    point.append((abscissa, ordinate))

                else:
                    break

            if not left:
                ordinate = y
                if y - it <= 0:
                    left = True

                elif battle_map[x][y - it] == tile_mode_hit:
                    pass

                elif battle_map[x][y - it] == tile_mode_neutral:
                    left = True
                    ordinate = ordinate - it
                    point.append((abscissa, ordinate))
                else:
                    break

            it = it + 1

    if search_vertical:

        it = 1
        ordinate = y
        while (not up) or (not down):
            if not up:
                abscissa = x
                if x - it <= 0:
                    up = True

                elif battle_map[x - it][y] == tile_mode_hit:
                    pass

                elif battle_map[x - it][y] == tile_mode_neutral:
                    up = True
                    abscissa = abscissa - it
                    point.append((abscissa, ordinate))
                else:
                    break

            if not down:
                abscissa = x
                if x + it > len(battle_map) - 1:
                    down = True

                elif battle_map[x + it][y] == tile_mode_hit:
                    pass

                elif battle_map[x + it][y] == tile_mode_neutral:
                    down = True
                    abscissa = abscissa + it
                    point.append((abscissa, ordinate))
                else:
                    break

            it = it + 1

    return point


def mark_potential(battle_map, point):

    for x, y in point:
        battle_map[x][y] = tile_mode_potential


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
    n_coef = 30

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

        t_coef = not_hit * not_hit * not_hit/ (already_hit + not_hit)
        value *= t_coef

        c_coef = (already_hit + not_hit) / skill_cost[examine_result["skill"]]
        value *= c_coef

        if show:
            print(round(value, 3), examine_result)

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


# # FOR MAIN PROGRAM
# def state_attack_or_search(battle_map):
#
#     def use_skill(battle_map):
#         count = 0
#         for row in battle_map:
#             for col in row:
#                 if battle_map[row][col] == tile_mode_potential:
#                     count += 1
#
#         return count != 0
#
#     # Don't use skill if no potential tile
#     if not use_skill(battle_map):
#         pass
#        # don't attack, go search !!

if __name__ == '__main__':

    # BOT SECTION
    megumi = Player(filename)
    battle_map = player_map(megumi.state_data)

    last_hit = (1, 3)
    last_x, last_y = last_hit

    battle_map[last_x][last_y] = "X"
    potential_tile = determine_potential(battle_map, last_hit)
    mark_potential(battle_map, potential_tile)
    print_battle_map(battle_map)
    # inspect_object(megumi)

    # Check and determine which skill to use
    examine_report = attack_mode_examine_map(battle_map, pivot=last_hit, usable_skill=megumi.usable_skill)
    best_result = greedy_pick(megumi, examine_report, True)
    # print(best_result)
    write_command(best_result)
