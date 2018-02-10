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

skill_cost = {7: {"double_h": 16,
                  "double_v": 16,
                  "cross_d": 24,
                  "cross_h": 28,
                  "corner": 20,
                  "seeker": 20,
                  },
              10: {"double_h": 24,
                   "double_v": 24,
                   "cross_d": 36,
                   "cross_h": 42,
                   "corner": 30,
                   "seeker": 30,
                   },
              14: {"double_h": 24,
                   "double_v": 24,
                   "cross_d": 48,
                   "cross_h": 56,
                   "corner": 40,
                   "seeker": 40,
                   }
              }

tile_mode_missed = "!"
tile_mode_neutral = "_"
tile_mode_shield = "@"
tile_mode_hit = "*"
tile_mode_potential = "?"
tile_mode_ship_active = "A"

"""
    DO_NOTHING(0),
    FIRE_SHOT(1),
    DOUBLE_SHOT_VERTICAL(2),
    DOUBLE_SHOT_HORIZONTAL(3),
    CORNER_SHOT(4),
    CROSS_SHOT_DIAGOL(5),
    CROSS_SHOT_HORIZONTAL(6),
    SEEKER_MISSLE(7);
"""
