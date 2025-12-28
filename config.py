"""
Qi Men Pro v2.0 Configuration
Enhanced with Professional Styling
"""

# App Info
APP_NAME = "Qi Men Pro"
APP_VERSION = "2.0"
APP_TITLE = "🌟 Qi Men Pro v2.0"

# Theme Colors
COLORS = {
    "background": "#1a1a2e",
    "card_bg": "#16213e",
    "card_border": "#2a3f5f",
    "primary_accent": "#d4af37",  # Gold
    "secondary_accent": "#e6c860",
    "text_primary": "#ffffff",
    "text_secondary": "#b8b8b8",
    "success": "#4CAF50",
    "warning": "#FFC107",
    "error": "#F44336",
    # Element colors
    "wood": "#4CAF50",
    "fire": "#F44336",
    "earth": "#8D6E63",
    "metal": "#BDBDBD",
    "water": "#2196F3",
}

# Alias for settings page
THEME_COLORS = COLORS

# Element Colors (capitalized keys for easy access)
ELEMENT_COLORS = {
    "Wood": "#4CAF50",
    "Fire": "#F44336",
    "Earth": "#8D6E63",
    "Metal": "#BDBDBD",
    "Water": "#2196F3",
}

# Element emoji mapping
ELEMENT_EMOJI = {
    "Wood": "🌳",
    "Fire": "🔥",
    "Earth": "🟤",
    "Metal": "⚪",
    "Water": "💧",
}

# Palace Information (Enhanced with Chinese names and positions)
PALACE_INFO = {
    1: {"name": "Kan", "chinese": "坎", "direction": "N", "element": "Water", "position": (2, 1)},
    2: {"name": "Kun", "chinese": "坤", "direction": "SW", "element": "Earth", "position": (0, 2)},
    3: {"name": "Zhen", "chinese": "震", "direction": "E", "element": "Wood", "position": (1, 0)},
    4: {"name": "Xun", "chinese": "巽", "direction": "SE", "element": "Wood", "position": (0, 0)},
    5: {"name": "Center", "chinese": "中", "direction": "Center", "element": "Earth", "position": (1, 1)},
    6: {"name": "Qian", "chinese": "乾", "direction": "NW", "element": "Metal", "position": (2, 2)},
    7: {"name": "Dui", "chinese": "兑", "direction": "W", "element": "Metal", "position": (1, 2)},
    8: {"name": "Gen", "chinese": "艮", "direction": "NE", "element": "Earth", "position": (2, 0)},
    9: {"name": "Li", "chinese": "離", "direction": "S", "element": "Fire", "position": (0, 1)},
}

# Luo Shu Grid Order (for display)
LUO_SHU_GRID = [
    [4, 9, 2],  # SE, S, SW
    [3, 5, 7],  # E, Center, W
    [8, 1, 6],  # NE, N, NW
]

# Heaven Stems with Chinese characters
HEAVEN_STEMS = {
    "甲": {"pinyin": "Jia", "element": "Wood", "polarity": "Yang"},
    "乙": {"pinyin": "Yi", "element": "Wood", "polarity": "Yin"},
    "丙": {"pinyin": "Bing", "element": "Fire", "polarity": "Yang"},
    "丁": {"pinyin": "Ding", "element": "Fire", "polarity": "Yin"},
    "戊": {"pinyin": "Wu", "element": "Earth", "polarity": "Yang"},
    "己": {"pinyin": "Ji", "element": "Earth", "polarity": "Yin"},
    "庚": {"pinyin": "Geng", "element": "Metal", "polarity": "Yang"},
    "辛": {"pinyin": "Xin", "element": "Metal", "polarity": "Yin"},
    "壬": {"pinyin": "Ren", "element": "Water", "polarity": "Yang"},
    "癸": {"pinyin": "Gui", "element": "Water", "polarity": "Yin"},
}

# Ten God Profiles with Emojis and Traits (Enhanced)
TEN_GOD_PROFILES = {
    "Friend (Connector)": {
        "emoji": "🤝", 
        "traits": ["Collaborative", "Supportive", "Network-oriented"]
    },
    "Rob Wealth (Competitor)": {
        "emoji": "⚔️", 
        "traits": ["Ambitious", "Driven", "Assertive"]
    },
    "Eating God (Artist)": {
        "emoji": "🎨", 
        "traits": ["Creative", "Expressive", "Appreciative"]
    },
    "Hurting Officer (Philosopher)": {
        "emoji": "🧠", 
        "traits": ["Analytical", "Questioning", "Innovative"]
    },
    "Direct Wealth (Strategist)": {
        "emoji": "📊", 
        "traits": ["Methodical", "Reliable", "Resource-minded"]
    },
    "Pioneer (Indirect Wealth)": {
        "emoji": "🎯", 
        "traits": ["Opportunistic", "Adaptable", "Bold"]
    },
    "Director (Direct Officer)": {
        "emoji": "👔", 
        "traits": ["Responsible", "Ethical", "Authority-respecting"]
    },
    "Warrior (7 Killings)": {
        "emoji": "⚡", 
        "traits": ["Courageous", "Decisive", "Action-oriented"]
    },
    "Diplomat (Direct Resource)": {
        "emoji": "🕊️", 
        "traits": ["Nurturing", "Patient", "Traditional"]
    },
    "Analyzer (Indirect Resource)": {
        "emoji": "🔮", 
        "traits": ["Intuitive", "Perceptive", "Unconventional"]
    },
}

# Database file paths
DB_PATH = "data/qmdj_bazi_patterns.csv"
PROFILE_PATH = "data/user_profile.json"

# Default timezone and location
DEFAULT_TIMEZONE = "UTC+8"
DEFAULT_LOCATION = "Singapore"
