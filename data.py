FILL_SHAPE = ((0, 0, 0, 0, 0, 0, 0, 0, 0),
              (0, 0, 0, 1, 1, 1, 0, 0, 0),
              (0, 0, 1, 1, 1, 1, 1, 0, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 1, 1, 1, 1, 1, 1, 1, 0),
              (0, 0, 1, 1, 1, 1, 1, 0, 0),
              (0, 0, 0, 1, 1, 1, 0, 0, 0),
              (0, 0, 0, 0, 0, 0, 0, 0, 0))

BORDER_SHAPE = ((0, 0, 0, 1, 1, 1, 0, 0, 0),
                (0, 1, 1, 0, 0, 0, 1, 1, 0),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (1, 0, 0, 0, 0, 0, 0, 0, 1),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
                (0, 1, 1, 0, 0, 0, 1, 1, 0),
                (0, 0, 0, 1, 1, 1, 0, 0, 0))

KEYS = ("000", "001", "010", "011", "100", "101", "110", "111")

PALETTES = ()

BG_PALETTES = ()


def make_palette(data):
    assert (len(KEYS) == len(PALETTES)), \
        "KEYS and PALETTES must have same length"

    p_index = int(data["PALETTE"], 2)
    assert (len(KEYS) >= p_index), \
        "KEYS and PALETTES do not meet requirements, see app.extract_data"

    bg_index = int(data["BG"], 2)
    assert (len(BG_PALETTES) >= bg_index), \
        "BG_PALETTES does not meet requirements, see app.extract_data"

    colors = PALETTES[p_index]
    bg = BG_PALETTES[p_index][bg_index]

    palette = {}
    for i, key in enumerate(KEYS):
        palette[key] = colors[i]
    palette["BG"] = bg

    return palette
