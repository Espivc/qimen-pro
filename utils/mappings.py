"""
Joey Yap Terminology Mappings
Converts kinqimen library outputs to Joey Yap standard terminology
"""

# Star Mapping (Chinese to English)
STAR_MAPPING = {
    "天蓬": "Canopy",
    "天芮": "Grass",
    "天冲": "Impulse",
    "天辅": "Assistant",
    "天禽": "Connect",
    "天心": "Heart",
    "天柱": "Pillar",
    "天任": "Ren",
    "天英": "Hero",
}

STAR_MAPPING_REVERSE = {v: k for k, v in STAR_MAPPING.items()}

# Star Elements
STAR_ELEMENTS = {
    "Canopy": "Water",
    "Grass": "Earth",
    "Impulse": "Wood",
    "Assistant": "Wood",
    "Connect": "Earth",
    "Heart": "Metal",
    "Pillar": "Metal",
    "Ren": "Earth",
    "Hero": "Fire",
}

# Star Categories
STAR_CATEGORIES = {
    "Canopy": "Inauspicious",
    "Grass": "Inauspicious",
    "Impulse": "Neutral",
    "Assistant": "Auspicious",
    "Connect": "Neutral",
    "Heart": "Auspicious",
    "Pillar": "Neutral",
    "Ren": "Auspicious",
    "Hero": "Neutral",
}

# Door Mapping (Chinese to English)
DOOR_MAPPING = {
    "开门": "Open",
    "休门": "Rest",
    "生门": "Life",
    "伤门": "Harm",
    "杜门": "Delusion",
    "景门": "Scenery",
    "死门": "Death",
    "惊门": "Fear",
}

DOOR_MAPPING_REVERSE = {v: k for k, v in DOOR_MAPPING.items()}

# Door Elements
DOOR_ELEMENTS = {
    "Open": "Metal",
    "Rest": "Water",
    "Life": "Earth",
    "Harm": "Wood",
    "Delusion": "Wood",
    "Scenery": "Fire",
    "Death": "Earth",
    "Fear": "Metal",
}

# Door Categories
DOOR_CATEGORIES = {
    "Open": "Auspicious",
    "Rest": "Auspicious",
    "Life": "Auspicious",
    "Harm": "Inauspicious",
    "Delusion": "Neutral",
    "Scenery": "Neutral",
    "Death": "Inauspicious",
    "Fear": "Inauspicious",
}

# Deity Mapping (Chinese to English)
DEITY_MAPPING = {
    "值符": "Chief",
    "腾蛇": "Serpent",
    "太阴": "Moon",
    "六合": "Six Harmony",
    "勾陈": "Hook",
    "白虎": "Tiger",
    "玄武": "Emptiness",
    "九地": "Nine Earth",
    "九天": "Nine Heaven",
}

DEITY_MAPPING_REVERSE = {v: k for k, v in DEITY_MAPPING.items()}

# Deity Natures
DEITY_NATURES = {
    "Chief": "Auspicious",
    "Serpent": "Inauspicious",
    "Moon": "Auspicious",
    "Six Harmony": "Auspicious",
    "Hook": "Inauspicious",
    "Tiger": "Inauspicious",
    "Emptiness": "Inauspicious",
    "Nine Earth": "Neutral",
    "Nine Heaven": "Auspicious",
}

# Deity Emoji
DEITY_EMOJI = {
    "Chief": "👑",
    "Serpent": "🐍",
    "Moon": "🌙",
    "Six Harmony": "🤝",
    "Hook": "🪝",
    "Tiger": "🐯",
    "Emptiness": "🌀",
    "Nine Earth": "🌍",
    "Nine Heaven": "☁️",
}

# Door Emoji
DOOR_EMOJI = {
    "Open": "🚪",
    "Rest": "😴",
    "Life": "🌱",
    "Harm": "⚔️",
    "Delusion": "🌫️",
    "Scenery": "🏞️",
    "Death": "💀",
    "Fear": "😨",
}

# Star Emoji
STAR_EMOJI = {
    "Canopy": "🎪",
    "Grass": "🌿",
    "Impulse": "⚡",
    "Assistant": "🤲",
    "Connect": "🔗",
    "Heart": "❤️",
    "Pillar": "🏛️",
    "Ren": "👤",
    "Hero": "🦸",
}

# Common Formations
FORMATIONS = {
    "dragon_return": {
        "name": "Dragon Returns to Source",
        "chinese": "回龙返首",
        "category": "Auspicious",
        "source": "#64",
        "description": "Matters succeed, returns to origin with gains",
    },
    "bird_falls": {
        "name": "Bird Falls into Cave",
        "chinese": "飞鸟跌穴",
        "category": "Auspicious",
        "source": "#64",
        "description": "Unexpected success, hidden opportunities revealed",
    },
    "ghost_entry": {
        "name": "Ghost Enters Tomb",
        "chinese": "鬼入墓",
        "category": "Inauspicious",
        "source": "#64",
        "description": "Hidden obstacles, delays and stagnation",
    },
    "tiger_escapes": {
        "name": "Tiger Escapes Prison",
        "chinese": "白虎猖狂",
        "category": "Inauspicious",
        "source": "#64",
        "description": "Dangerous situations, legal issues possible",
    },
    "jade_maiden": {
        "name": "Jade Maiden Guards Door",
        "chinese": "玉女守门",
        "category": "Auspicious",
        "source": "#73",
        "description": "Protection and support from female benefactor",
    },
    "sky_horse": {
        "name": "Sky Horse Moving",
        "chinese": "天马行空",
        "category": "Auspicious",
        "source": "#73",
        "description": "Travel benefits, swift progress",
    },
}


def translate_star(chinese_name: str) -> str:
    """Translate star from Chinese to English"""
    return STAR_MAPPING.get(chinese_name, chinese_name)


def translate_door(chinese_name: str) -> str:
    """Translate door from Chinese to English"""
    return DOOR_MAPPING.get(chinese_name, chinese_name)


def translate_deity(chinese_name: str) -> str:
    """Translate deity from Chinese to English"""
    return DEITY_MAPPING.get(chinese_name, chinese_name)


def get_star_element(star_name: str) -> str:
    """Get the element of a star"""
    return STAR_ELEMENTS.get(star_name, "Unknown")


def get_door_element(door_name: str) -> str:
    """Get the element of a door"""
    return DOOR_ELEMENTS.get(door_name, "Unknown")


def get_deity_nature(deity_name: str) -> str:
    """Get the nature of a deity"""
    return DEITY_NATURES.get(deity_name, "Unknown")
