import os
from PIL import Image, ImageDraw

# Create directories
os.makedirs("assets", exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)

# Color Palette (DB32 inspired)
P = {
    "black": (26, 28, 44),
    "dark_purple": (93, 39, 93),
    "red": (177, 62, 83),
    "orange": (239, 125, 87),
    "yellow": (255, 205, 117),
    "light_green": (167, 240, 112),
    "green": (56, 183, 100),
    "dark_green": (37, 113, 121),
    "dark_blue": (41, 54, 111),
    "blue": (59, 93, 201),
    "light_blue": (65, 166, 246),
    "aqua": (115, 239, 247),
    "white": (244, 244, 244),
    "light_gray": (148, 176, 194),
    "gray": (86, 108, 134),
    "dark_gray": (51, 60, 87),
    "brown": (139, 69, 19),
    "dark_brown": (80, 40, 10),
    "wood": (197, 131, 87),
    "trans": (0, 0, 0, 0),
}

# =========================================================================
# 1. TILESET (16x16 tiles, 8 columns x 8 rows = 128x128 texture)
# =========================================================================
tileset = Image.new("RGBA", (128, 128), P["trans"])
draw_tile = ImageDraw.Draw(tileset)

def fill_tile(tx, ty, color):
    draw_tile.rectangle([tx*16, ty*16, tx*16+15, ty*16+15], fill=color)

# Tile 0,0: Grass Center
fill_tile(0, 0, P["green"])
# Add grass blades
draw_tile.rectangle([0*16+4, 0*16+4, 0*16+4, 0*16+5], fill=P["light_green"])
draw_tile.rectangle([0*16+10, 0*16+9, 0*16+10, 0*16+10], fill=P["light_green"])
draw_tile.rectangle([0*16+12, 0*16+3, 0*16+13, 0*16+3], fill=P["light_green"])

# Tile 1,0: Stone Path
fill_tile(1, 0, P["gray"])
# Cobble details
draw_tile.rectangle([1*16+2, 1*16+2, 1*16+5, 1*16+5], fill=P["light_gray"])
draw_tile.rectangle([1*16+8, 1*16+3, 1*16+13, 1*16+7], fill=P["dark_gray"])
draw_tile.rectangle([1*16+3, 1*16+9, 1*16+7, 1*16+13], fill=P["light_gray"])
draw_tile.rectangle([1*16+9, 1*16+10, 1*16+13, 1*16+13], fill=P["dark_gray"])

# Tile 2,0: Dirt Road
fill_tile(2, 0, P["brown"])
draw_tile.rectangle([2*16+3, 2*16+5, 2*16+4, 2*16+6], fill=P["dark_brown"])
draw_tile.rectangle([2*16+11, 2*16+9, 2*16+12, 2*16+10], fill=P["wood"])

# Tile 3,0: Water
fill_tile(3, 0, P["blue"])
# Wave lines
draw_tile.line([3*16+2, 3*16+4, 3*16+7, 3*16+4], fill=P["aqua"])
draw_tile.line([3*16+9, 3*16+11, 3*16+14, 3*16+11], fill=P["aqua"])

# Tile 4,0: Wall Base
fill_tile(4, 0, P["dark_gray"])
# Bricks
draw_tile.line([4*16, 4*16+7, 4*16+15, 4*16+7], fill=P["black"])
draw_tile.line([4*16, 4*16+15, 4*16+15, 4*16+15], fill=P["black"])
draw_tile.line([4*16+5, 4*16, 4*16+5, 4*16+7], fill=P["black"])
draw_tile.line([4*16+11, 4*16, 4*16+11, 4*16+7], fill=P["black"])
draw_tile.line([4*16+8, 4*16+8, 4*16+8, 4*16+15], fill=P["black"])
# Highlights
draw_tile.line([4*16, 4*16, 4*16+15, 4*16], fill=P["light_gray"])

# Tile 5,0: Dark Grass (Dungeon Floor)
fill_tile(5, 0, P["dark_blue"])
draw_tile.rectangle([5*16+2, 5*16+3, 5*16+3, 5*16+4], fill=P["dark_purple"])
draw_tile.rectangle([5*16+10, 5*16+11, 5*16+11, 5*16+12], fill=P["dark_purple"])

# Tile 6,0: Tree Trunk
fill_tile(6, 0, P["trans"])
draw_tile.rectangle([6*16+6, 6*16, 6*16+9, 6*16+15], fill=P["dark_brown"])
draw_tile.line([6*16+7, 6*16, 6*16+7, 6*16+15], fill=P["brown"])

# Tile 7,0: Tree Leaves
fill_tile(7, 0, P["trans"])
draw_tile.ellipse([7*16, 7*16, 7*16+15, 7*16+15], fill=P["dark_green"], outline=P["black"])
draw_tile.ellipse([7*16+2, 7*16+2, 7*16+11, 7*16+11], fill=P["green"])

# Tile 0,1: Signpost
fill_tile(0, 1, P["trans"])
draw_tile.rectangle([0*16+7, 0*16+8, 0*16+8, 0*16+15], fill=P["dark_brown"])
draw_tile.rectangle([0*16+2, 0*16+2, 0*16+13, 0*16+8], fill=P["wood"], outline=P["black"])

# Tile 1,1: Chest
fill_tile(1, 1, P["trans"])
draw_tile.rectangle([1*16+2, 1*16+4, 1*16+13, 1*16+14], fill=P["brown"], outline=P["black"])
draw_tile.line([1*16+2, 1*16+8, 1*16+13, 1*16+8], fill=P["black"])
draw_tile.rectangle([1*16+7, 1*16+7, 1*16+8, 1*16+9], fill=P["yellow"])

# Tile 2,1: Glowing Portal / Spawner
fill_tile(2, 1, P["dark_purple"])
draw_tile.ellipse([2*16+2, 2*16+2, 2*16+13, 2*16+13], fill=P["trans"], outline=P["aqua"])
draw_tile.ellipse([2*16+5, 2*16+5, 2*16+10, 2*16+10], fill=P["aqua"])

# Tile 3,1: Dungeon Wall / Pillar
fill_tile(3, 1, P["black"])
draw_tile.rectangle([3*16+2, 3*16+2, 3*16+13, 3*16+15], fill=P["dark_purple"], outline=P["dark_blue"])

tileset.save("assets/tileset.png")

# =========================================================================
# 2. CHARACTERS (Grid of 3x4 layout for each character. Frame size: 32x32)
# Layout: 3 columns of characters, 3 rows of characters (Total size: 288x384)
# Cols: 0=Idle, 1=Walk1, 2=Walk2
# Rows: 0=Down, 1=Up, 2=Left, 3=Right
# =========================================================================
chars_img = Image.new("RGBA", (288, 384), P["trans"])
draw_chars = ImageDraw.Draw(chars_img)

def draw_character_frame(cx, cy, frame_idx, dir_idx, color_scheme, is_monster=False):
    # cx, cy: character grid coord (0 to 2)
    # frame_idx: 0=Idle, 1=Walk1, 2=Walk2
    # dir_idx: 0=Down, 1=Up, 2=Left, 3=Right
    ox = cx * 96 + frame_idx * 32
    oy = cy * 128 + dir_idx * 32
    
    body_color = color_scheme.get("body", P["blue"])
    head_color = color_scheme.get("head", P["yellow"])
    acc_color = color_scheme.get("acc", P["red"])
    skin_color = color_scheme.get("skin", P["white"])
    
    # Simple squash/stretch variables for walk animation
    walk_offset = 0
    if frame_idx > 0:
        walk_offset = 1 if frame_idx == 1 else -1

    # Drawing character parts
    # Feet
    if dir_idx == 2 or dir_idx == 3: # Side
        draw_chars.rectangle([ox+12, oy+28, ox+20, oy+31], fill=P["black"])
    else: # Down/Up
        if frame_idx == 1:
            draw_chars.rectangle([ox+10, oy+27, ox+13, oy+30], fill=P["black"])
            draw_chars.rectangle([ox+18, oy+28, ox+21, oy+31], fill=P["black"])
        elif frame_idx == 2:
            draw_chars.rectangle([ox+10, oy+28, ox+13, oy+31], fill=P["black"])
            draw_chars.rectangle([ox+18, oy+27, ox+21, oy+30], fill=P["black"])
        else:
            draw_chars.rectangle([ox+10, oy+28, ox+13, oy+31], fill=P["black"])
            draw_chars.rectangle([ox+18, oy+28, ox+21, oy+31], fill=P["black"])

    # Body / Robe / Armor
    draw_chars.rectangle([ox+10, oy+14, ox+21, oy+27], fill=body_color, outline=P["black"])
    if "cloak" in color_scheme:
        draw_chars.rectangle([ox+9, oy+15, ox+10, oy+26], fill=color_scheme["cloak"])
        draw_chars.rectangle([ox+21, oy+15, ox+22, oy+26], fill=color_scheme["cloak"])

    # Head / Helmet / Face
    draw_chars.rectangle([ox+10, oy+4, ox+21, oy+13], fill=skin_color, outline=P["black"])
    if head_color != skin_color:
        # Draw hat / helmet
        draw_chars.rectangle([ox+9, oy+2, ox+22, oy+7], fill=head_color, outline=P["black"])
        if color_scheme.get("hat_type") == "wizard":
            # Pointy top
            draw_chars.rectangle([ox+13, oy, ox+18, oy+2], fill=head_color)
            draw_chars.rectangle([ox+14, oy-2, ox+17, oy], fill=acc_color)
            
    # Face details (Eyes)
    if dir_idx == 0: # Down
        draw_chars.rectangle([ox+12, oy+8, ox+13, oy+9], fill=P["black"])
        draw_chars.rectangle([ox+18, oy+8, ox+19, oy+9], fill=P["black"])
        if is_monster:
            draw_chars.rectangle([ox+12, oy+8, ox+13, oy+8], fill=P["red"])
            draw_chars.rectangle([ox+18, oy+8, ox+19, oy+8], fill=P["red"])
    elif dir_idx == 2: # Left
        draw_chars.rectangle([ox+11, oy+8, ox+12, oy+9], fill=P["black"])
        if is_monster:
            draw_chars.rectangle([ox+11, oy+8, ox+11, oy+8], fill=P["red"])
    elif dir_idx == 3: # Right
        draw_chars.rectangle([ox+19, oy+8, ox+20, oy+9], fill=P["black"])
        if is_monster:
            draw_chars.rectangle([ox+20, oy+8, ox+20, oy+8], fill=P["red"])

    # Weapons/Accessories based on Direction
    w_color = color_scheme.get("weapon_color", P["light_gray"])
    if "weapon" in color_scheme:
        w_type = color_scheme["weapon"]
        if dir_idx == 0: # Down
            if w_type == "sword":
                draw_chars.rectangle([ox+22, oy+14, ox+24, oy+25], fill=w_color, outline=P["black"])
                draw_chars.rectangle([ox+20, oy+21, ox+25, oy+22], fill=P["yellow"]) # Hilt
            elif w_type == "staff":
                draw_chars.line([ox+23, oy+10, ox+23, oy+26], fill=P["brown"])
                draw_chars.rectangle([ox+22, oy+8, ox+24, oy+10], fill=P["aqua"])
            elif w_type == "bow":
                draw_chars.arc([ox+22, oy+12, ox+26, oy+24], -90, 90, fill=P["wood"])
                draw_chars.line([ox+22, oy+12, ox+22, oy+24], fill=P["white"])
        elif dir_idx == 1: # Up (on back)
            if w_type == "sword":
                draw_chars.line([ox+10, oy+22, ox+22, oy+10], fill=w_color)
            elif w_type == "bow":
                draw_chars.arc([ox+11, oy+13, ox+20, oy+23], 0, 180, fill=P["wood"])
        elif dir_idx == 2: # Left
            if w_type == "sword":
                draw_chars.rectangle([ox+4, oy+16+walk_offset, ox+9, oy+18+walk_offset], fill=w_color, outline=P["black"])
            elif w_type == "staff":
                draw_chars.line([ox+6, oy+8, ox+6, oy+26], fill=P["brown"])
                draw_chars.rectangle([ox+5, oy+6, ox+7, oy+8], fill=P["aqua"])
            elif w_type == "bow":
                draw_chars.arc([ox+4, oy+12, ox+8, oy+24], 90, 270, fill=P["wood"])
                draw_chars.line([ox+8, oy+12, ox+8, oy+24], fill=P["white"])
        elif dir_idx == 3: # Right
            if w_type == "sword":
                draw_chars.rectangle([ox+22, oy+16+walk_offset, ox+27, oy+18+walk_offset], fill=w_color, outline=P["black"])
            elif w_type == "staff":
                draw_chars.line([ox+25, oy+8, ox+25, oy+26], fill=P["brown"])
                draw_chars.rectangle([ox+24, oy+6, ox+26, oy+8], fill=P["aqua"])
            elif w_type == "bow":
                draw_chars.arc([ox+23, oy+12, ox+27, oy+24], -90, 90, fill=P["wood"])
                draw_chars.line([ox+23, oy+12, ox+23, oy+24], fill=P["white"])

# Character Specs
CHAR_SCHEMES = [
    # 0: Warrior (Knight)
    {"body": P["dark_gray"], "head": P["yellow"], "acc": P["red"], "skin": P["white"], "weapon": "sword", "weapon_color": P["light_gray"]},
    # 1: Mage
    {"body": P["dark_purple"], "head": P["dark_purple"], "hat_type": "wizard", "acc": P["yellow"], "skin": P["white"], "weapon": "staff"},
    # 2: Archer
    {"body": P["green"], "head": P["green"], "acc": P["wood"], "skin": P["white"], "weapon": "bow"},
    # 3: NPC Quest Giver (Old Elder)
    {"body": P["brown"], "head": P["white"], "skin": P["orange"], "cloak": P["dark_brown"]},
    # 4: NPC Merchant (Trader)
    {"body": P["blue"], "head": P["yellow"], "skin": P["orange"], "cloak": P["wood"]},
    # 5: Slime (Monsters are slightly custom)
    {"body": P["aqua"], "head": P["aqua"], "skin": P["aqua"]},
    # 6: Goblin
    {"body": P["dark_green"], "head": P["dark_green"], "skin": P["light_green"], "weapon": "sword", "weapon_color": P["orange"]},
    # 7: Skeleton
    {"body": P["gray"], "head": P["white"], "skin": P["white"], "weapon": "sword"},
    # 8: Demon Boss (Large and scary)
    {"body": P["black"], "head": P["red"], "acc": P["orange"], "skin": P["red"], "weapon": "staff", "weapon_color": P["red"]},
]

# Draw all standard characters
for cy in range(3):
    for cx in range(3):
        idx = cy * 3 + cx
        scheme = CHAR_SCHEMES[idx]
        is_m = idx >= 5
        # Draw 4 directions
        for d in range(4):
            # Draw 3 animation frames
            for f in range(3):
                # Slime needs custom drawing because it's a blob, let's override it
                if idx == 5:
                    # Draw a bouncy blob
                    ox = cx * 96 + f * 32
                    oy = cy * 128 + d * 32
                    # Bouncy slime y-offset
                    so = 4 if f > 0 else 0
                    draw_chars.ellipse([ox+6, oy+14+so, ox+25, oy+30], fill=P["aqua"], outline=P["black"])
                    # Eyes
                    draw_chars.rectangle([ox+10, oy+20+so, ox+11, oy+21+so], fill=P["black"])
                    draw_chars.rectangle([ox+20, oy+20+so, ox+21, oy+21+so], fill=P["black"])
                    draw_chars.rectangle([ox+14, oy+24+so, ox+17, oy+25+so], fill=P["red"]) # Pink cheeks
                else:
                    draw_character_frame(cx, cy, f, d, scheme, is_monster=is_m)

chars_img.save("assets/characters.png")

# =========================================================================
# 3. ICONS (32x32 icons, 4 columns x 4 rows = 128x128 texture)
# =========================================================================
icons = Image.new("RGBA", (128, 128), P["trans"])
draw_icon = ImageDraw.Draw(icons)

def draw_icon_box(ix, iy, draw_func):
    ox = ix * 32
    oy = iy * 32
    # Draw border
    draw_icon.rectangle([ox, oy, ox+31, oy+31], fill=P["trans"])
    draw_func(ox, oy)

# Row 0, Col 0: Health Potion
def draw_hp_pot(ox, oy):
    # Bottle shape
    draw_icon.rectangle([ox+10, oy+12, ox+21, oy+27], fill=P["dark_blue"], outline=P["black"])
    draw_icon.rectangle([ox+11, oy+14, ox+20, oy+26], fill=P["red"])
    # Liquid highlight
    draw_icon.rectangle([ox+13, oy+16, ox+15, oy+19], fill=P["orange"])
    # Neck and cork
    draw_icon.rectangle([ox+13, oy+6, ox+18, oy+11], fill=P["wood"], outline=P["black"])
    draw_icon.rectangle([ox+14, oy+2, ox+17, oy+5], fill=P["orange"])

draw_icon_box(0, 0, draw_hp_pot)

# Row 0, Col 1: Mana Potion
def draw_mp_pot(ox, oy):
    draw_icon.rectangle([ox+10, oy+12, ox+21, oy+27], fill=P["dark_blue"], outline=P["black"])
    draw_icon.rectangle([ox+11, oy+14, ox+20, oy+26], fill=P["blue"])
    draw_icon.rectangle([ox+13, oy+16, ox+15, oy+19], fill=P["aqua"])
    draw_icon.rectangle([ox+13, oy+6, ox+18, oy+11], fill=P["wood"], outline=P["black"])
    draw_icon.rectangle([ox+14, oy+2, ox+17, oy+5], fill=P["orange"])

draw_icon_box(1, 0, draw_mp_pot)

# Row 0, Col 2: Gold Pile
def draw_gold(ox, oy):
    draw_icon.ellipse([ox+6, oy+16, ox+18, oy+26], fill=P["orange"], outline=P["black"])
    draw_icon.ellipse([ox+12, oy+10, ox+25, oy+22], fill=P["yellow"], outline=P["black"])
    draw_icon.ellipse([ox+14, oy+18, ox+22, oy+26], fill=P["yellow"], outline=P["black"])

draw_icon_box(2, 0, draw_gold)

# Row 0, Col 3: Rusty Sword
def draw_rusty_sword(ox, oy):
    # Diagonal sword
    for i in range(16):
        draw_icon.rectangle([ox+6+i, oy+24-i, ox+8+i, oy+26-i], fill=P["gray"], outline=P["black"])
    # Hilt
    draw_icon.rectangle([ox+5, oy+25, ox+7, oy+27], fill=P["wood"])
    draw_icon.line([ox+4, oy+24, ox+8, oy+28], fill=P["orange"]) # Guard

draw_icon_box(3, 0, draw_rusty_sword)

# Row 1, Col 0: Apprentice Staff
def draw_app_staff(ox, oy):
    draw_icon.line([ox+6, oy+26, ox+24, oy+8], fill=P["dark_brown"], width=2)
    # Orb
    draw_icon.ellipse([ox+22, oy+4, ox+28, oy+10], fill=P["aqua"], outline=P["black"])

draw_icon_box(0, 1, draw_app_staff)

# Row 1, Col 1: Short Bow
def draw_short_bow(ox, oy):
    draw_icon.arc([ox+6, oy+6, ox+24, oy+24], -45, 135, fill=P["wood"])
    draw_icon.line([ox+6, oy+24, ox+24, oy+6], fill=P["white"])

draw_icon_box(1, 1, draw_short_bow)

# Row 1, Col 2: Iron Sword (Tier 2)
def draw_iron_sword(ox, oy):
    for i in range(16):
        draw_icon.rectangle([ox+6+i, oy+24-i, ox+8+i, oy+26-i], fill=P["light_gray"], outline=P["black"])
    # Guard and Gem
    draw_icon.line([ox+4, oy+24, ox+8, oy+28], fill=P["yellow"])
    draw_icon.rectangle([ox+5, oy+25, ox+7, oy+27], fill=P["blue"])

draw_icon_box(2, 1, draw_iron_sword)

# Row 1, Col 3: Fire Staff (Tier 2)
def draw_fire_staff(ox, oy):
    draw_icon.line([ox+6, oy+26, ox+24, oy+8], fill=P["dark_purple"], width=2)
    draw_icon.ellipse([ox+22, oy+4, ox+28, oy+10], fill=P["orange"], outline=P["red"])

draw_icon_box(3, 1, draw_fire_staff)

# Row 2, Col 0: Hunter Bow (Tier 2)
def draw_hunter_bow(ox, oy):
    draw_icon.arc([ox+4, oy+4, ox+26, oy+26], -45, 135, fill=P["dark_green"], width=2)
    draw_icon.line([ox+4, oy+26, ox+26, oy+4], fill=P["aqua"])

draw_icon_box(0, 2, draw_hunter_bow)

# Row 2, Col 1: Plate Armor
def draw_plate_armor(ox, oy):
    draw_icon.rectangle([ox+8, oy+6, ox+23, oy+26], fill=P["light_gray"], outline=P["black"])
    draw_icon.rectangle([ox+10, oy+8, ox+21, oy+14], fill=P["gray"])
    draw_icon.rectangle([ox+13, oy+12, ox+18, oy+25], fill=P["dark_gray"])
    # Gold lining
    draw_icon.line([ox+8, oy+6, ox+23, oy+6], fill=P["yellow"])
    draw_icon.line([ox+8, oy+6, ox+8, oy+20], fill=P["yellow"])
    draw_icon.line([ox+23, oy+6, ox+23, oy+20], fill=P["yellow"])

draw_icon_box(1, 2, draw_plate_armor)

# Row 2, Col 2: Sage Robe
def draw_sage_robe(ox, oy):
    draw_icon.rectangle([ox+8, oy+6, ox+23, oy+26], fill=P["dark_purple"], outline=P["black"])
    # Gold sash
    draw_icon.line([ox+8, oy+16, ox+23, oy+16], fill=P["yellow"])
    draw_icon.rectangle([ox+12, oy+8, ox+19, oy+14], fill=P["blue"])

draw_icon_box(2, 2, draw_sage_robe)

# Row 2, Col 3: Ranger Tunic
def draw_ranger_tunic(ox, oy):
    draw_icon.rectangle([ox+8, oy+6, ox+23, oy+26], fill=P["green"], outline=P["black"])
    # Leather belts
    draw_icon.line([ox+8, oy+12, ox+23, oy+18], fill=P["wood"])
    draw_icon.rectangle([ox+10, oy+8, ox+21, oy+11], fill=P["dark_green"])

draw_icon_box(3, 2, draw_ranger_tunic)

# Row 3, Col 0: Slime Core (Quest Item)
def draw_slime_core(ox, oy):
    draw_icon.ellipse([ox+8, oy+8, ox+23, oy+23], fill=P["aqua"], outline=P["blue"])
    draw_icon.ellipse([ox+12, oy+12, ox+19, oy+19], fill=P["white"])

draw_icon_box(0, 3, draw_slime_core)

# Row 3, Col 1: Wolf Claw (Quest Item)
def draw_wolf_claw(ox, oy):
    # Triple claw lines
    draw_icon.line([ox+10, oy+6, ox+8, oy+24], fill=P["white"], width=2)
    draw_icon.line([ox+15, oy+8, ox+15, oy+26], fill=P["white"], width=2)
    draw_icon.line([ox+20, oy+6, ox+22, oy+24], fill=P["white"], width=2)
    # Tips
    draw_icon.rectangle([ox+7, oy+23, ox+9, oy+25], fill=P["gray"])
    draw_icon.rectangle([ox+14, oy+25, ox+16, oy+27], fill=P["gray"])
    draw_icon.rectangle([ox+21, oy+23, ox+23, oy+25], fill=P["gray"])

draw_icon_box(1, 3, draw_wolf_claw)

# Row 3, Col 2: Demon Heart (Boss Item)
def draw_demon_heart(ox, oy):
    draw_icon.ellipse([ox+8, oy+8, ox+16, oy+20], fill=P["red"], outline=P["black"])
    draw_icon.ellipse([ox+15, oy+8, ox+23, oy+20], fill=P["red"], outline=P["black"])
    # Pointy bottom
    draw_icon.polygon([(ox+8, oy+15), (ox+23, oy+15), (ox+16, oy+26)], fill=P["red"])
    # Outer outline
    draw_icon.line([ox+8, oy+15, ox+16, oy+26], fill=P["black"])
    draw_icon.line([ox+23, oy+15, ox+16, oy+26], fill=P["black"])
    # Glowing vein
    draw_icon.line([ox+15, oy+10, ox+15, oy+22], fill=P["orange"])

draw_icon_box(2, 3, draw_demon_heart)

# Row 3, Col 3: Steel Shield
def draw_steel_shield(ox, oy):
    draw_icon.polygon([(ox+6, oy+6), (ox+25, oy+6), (ox+25, oy+16), (ox+16, oy+26), (ox+6, oy+16)], fill=P["gray"], outline=P["black"])
    draw_icon.polygon([(ox+10, oy+10), (ox+21, oy+10), (ox+21, oy+15), (ox+16, oy+21), (ox+10, oy+15)], fill=P["light_gray"])
    draw_icon.rectangle([ox+15, oy+6, ox+16, oy+25], fill=P["yellow"])

draw_icon_box(3, 3, draw_steel_shield)

icons.save("assets/icons.png")

print("Assets generated successfully!")
