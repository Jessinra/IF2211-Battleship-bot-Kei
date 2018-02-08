import time


search_list_5x5 = [(1, 0),
                   (1, 1),
                   (0, 1),
                   (-1, 1),
                   (-1, 0),
                   (-1, -1),
                   (0, -1),
                   (1, -1),
                   (2, -1),
                   (2, 0),
                   (2, 1),
                   (2, 2),
                   (1, 2),
                   (0, 2),
                   (-1, 2),
                   (-2, 2),
                   (-2, 1),
                   (-2, 0),
                   (-2, -1),
                   (-2, -2),
                   (-1, -2),
                   (0, -2),
                   (1, -2),
                   (2, -2),
                   ]

search_list_3x3 = [(0, 0),
                   (1, 0),
                   (1, 1),
                   (0, 1),
                   (-1, 1),
                   (-1, 0),
                   (-1, -1),
                   (0, -1),
                   (1, -1)]

skill_aoe_double_h = [(1, 0), (-1, 0)]
skill_aoe_double_v = [(0, 1), (0, -1)]
skill_aoe_corner = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
skill_aoe_cross_d = [(0, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
skill_aoe_cross_h = [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)]

skill_aoe_seeker = []

tile_mode_missed = "!"
tile_mode_neutral = "~"
tile_mode_shield = "@"
tile_mode_hit = "*"


def create_battle_map(row, col):
    battle_map = []
    for x in range(0, row):

        new_row = []
        for y in range(0, col):
            new_row.append("~")

        battle_map.append(new_row)

    return battle_map


def print_battle_map(battle_map):

    for row in battle_map:
        print(row)


def attack_mode_examine_map(battle_map, pivot_x, pivot_y, usable_skill):



    for dx, dy in search_list_5x5:
        try:

            current_x = pivot_x + dx
            current_y = pivot_y + dy

            for skill in usable_skill:
                examine_result = examine_skill_effect(battle_map, current_x, current_y, skill)


        except:
            pass


def examine_skill_effect(battle_map, pivot_x, pivot_y, skill_type):

    examine_result = tile_examine_template()

    # Get list of tile to search
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

    # Check tile one by one
    for dx, dy in search_list:
        try:

            # Do something
            tile_status = tile_examine(battle_map[pivot_x + dx][pivot_y + dy])
            examine_result[tile_status] += 1

        except:
            pass

    print(examine_result)
    return examine_result


def tile_examine(tile):

    if tile == tile_mode_shield:
        return "shield"
    elif tile == tile_mode_missed:
        return "missed"
    elif tile == tile_mode_hit:
        return "hit"
    else:
        return "neutral"


def tile_examine_template():

    return {"neutral": 0,
            "missed": 0,
            "hit": 0,
            "shield": 0}


def test_aoe(aoe):

    test_map = create_battle_map(5,5)
    test_map[2][2] = "(X)"
    for x,y in aoe:
        test_map[2+x][2+y] = "%"

    print_battle_map(test_map)


def test_all_aoe():

    aoe_list = [skill_aoe_double_h,
                skill_aoe_double_v,
                skill_aoe_corner,
                skill_aoe_cross_d,
                skill_aoe_cross_h]

    for each in aoe_list:
        print(each)
        test_aoe(each)

if __name__ == '__main__':

    battle_map = create_battle_map(10, 10)
    battle_map[4][4] = "X"
    battle_map[5][4] = "!"
    battle_map[3][1] = "!"
    battle_map[4][2] = "*"
    battle_map[4][1] = "@"
    battle_map[3][3] = "*"
    battle_map[2][2] = "*"
    battle_map[3][5] = "!"
    print_battle_map(battle_map)


    usable_skill = ["cross_d", "double_h", "double_v", "corner"]
    attack_mode_examine_map(battle_map, pivot_x=4, pivot_y=4, usable_skill=usable_skill)
