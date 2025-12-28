"""
BaZi Profile Management
Handles user BaZi profile storage and calculations
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

# Get the project root directory (parent of utils folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Default profile path - absolute path
PROFILE_DIR = PROJECT_ROOT / "data"
PROFILE_FILE = PROFILE_DIR / "user_profile.json"

# Day Master Information (Chinese key)
DAY_MASTERS = {
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

# Day Master Options (Pinyin key - for Settings UI)
DAY_MASTER_OPTIONS = {
    "Jia": {"chinese": "甲", "element": "Wood", "polarity": "Yang"},
    "Yi": {"chinese": "乙", "element": "Wood", "polarity": "Yin"},
    "Bing": {"chinese": "丙", "element": "Fire", "polarity": "Yang"},
    "Ding": {"chinese": "丁", "element": "Fire", "polarity": "Yin"},
    "Wu": {"chinese": "戊", "element": "Earth", "polarity": "Yang"},
    "Ji": {"chinese": "己", "element": "Earth", "polarity": "Yin"},
    "Geng": {"chinese": "庚", "element": "Metal", "polarity": "Yang"},
    "Xin": {"chinese": "辛", "element": "Metal", "polarity": "Yin"},
    "Ren": {"chinese": "壬", "element": "Water", "polarity": "Yang"},
    "Gui": {"chinese": "癸", "element": "Water", "polarity": "Yin"},
}

# Ten God Profiles with descriptions
TEN_GOD_PROFILES = {
    "Friend": {
        "name": "Connector",
        "traits": ["Collaborative", "Supportive", "Network-oriented"],
        "description": "Builds bridges between people and ideas"
    },
    "Rob Wealth": {
        "name": "Competitor",
        "traits": ["Ambitious", "Driven", "Assertive"],
        "description": "Thrives in competitive environments"
    },
    "Eating God": {
        "name": "Artist",
        "traits": ["Creative", "Expressive", "Appreciative"],
        "description": "Creates beauty and harmony"
    },
    "Hurting Officer": {
        "name": "Philosopher",
        "traits": ["Analytical", "Questioning", "Innovative"],
        "description": "Challenges conventions and seeks truth"
    },
    "Direct Wealth": {
        "name": "Strategist",
        "traits": ["Methodical", "Reliable", "Resource-minded"],
        "description": "Builds wealth through steady effort"
    },
    "Indirect Wealth": {
        "name": "Pioneer",
        "traits": ["Opportunistic", "Adaptable", "Bold"],
        "description": "Spots and capitalizes on opportunities"
    },
    "Direct Officer": {
        "name": "Director",
        "traits": ["Responsible", "Ethical", "Authority-respecting"],
        "description": "Leads through structure and integrity"
    },
    "7 Killings": {
        "name": "Warrior",
        "traits": ["Courageous", "Decisive", "Action-oriented"],
        "description": "Faces challenges head-on"
    },
    "Direct Resource": {
        "name": "Diplomat",
        "traits": ["Nurturing", "Patient", "Traditional"],
        "description": "Provides support and guidance"
    },
    "Indirect Resource": {
        "name": "Analyzer",
        "traits": ["Intuitive", "Perceptive", "Unconventional"],
        "description": "Sees patterns others miss"
    },
}

# Ten God Profile Options (for Settings UI dropdowns)
TEN_GOD_PROFILE_OPTIONS = {
    "Friend (Connector)": {
        "emoji": "🤝",
        "ten_god": "Friend",
        "traits": ["Collaborative", "Supportive", "Network-oriented"]
    },
    "Rob Wealth (Competitor)": {
        "emoji": "⚔️",
        "ten_god": "Rob Wealth",
        "traits": ["Ambitious", "Driven", "Assertive"]
    },
    "Eating God (Artist)": {
        "emoji": "🎨",
        "ten_god": "Eating God",
        "traits": ["Creative", "Expressive", "Appreciative"]
    },
    "Hurting Officer (Philosopher)": {
        "emoji": "🧠",
        "ten_god": "Hurting Officer",
        "traits": ["Analytical", "Questioning", "Innovative"]
    },
    "Direct Wealth (Strategist)": {
        "emoji": "📊",
        "ten_god": "Direct Wealth",
        "traits": ["Methodical", "Reliable", "Resource-minded"]
    },
    "Pioneer (Indirect Wealth)": {
        "emoji": "🎯",
        "ten_god": "Indirect Wealth",
        "traits": ["Opportunistic", "Adaptable", "Bold"]
    },
    "Director (Direct Officer)": {
        "emoji": "👔",
        "ten_god": "Direct Officer",
        "traits": ["Responsible", "Ethical", "Authority-respecting"]
    },
    "Warrior (7 Killings)": {
        "emoji": "⚡",
        "ten_god": "7 Killings",
        "traits": ["Courageous", "Decisive", "Action-oriented"]
    },
    "Diplomat (Direct Resource)": {
        "emoji": "🕊️",
        "ten_god": "Direct Resource",
        "traits": ["Nurturing", "Patient", "Traditional"]
    },
    "Analyzer (Indirect Resource)": {
        "emoji": "🔮",
        "ten_god": "Indirect Resource",
        "traits": ["Intuitive", "Perceptive", "Unconventional"]
    },
}

# Element colors for UI
ELEMENT_COLORS = {
    "Wood": "#4CAF50",
    "Fire": "#F44336",
    "Earth": "#8D6E63",
    "Metal": "#BDBDBD",
    "Water": "#2196F3",
}

# Default BaZi profile (as specified by user)
DEFAULT_PROFILE = {
    "day_master": {
        "chinese": "庚",
        "pinyin": "Geng",
        "element": "Metal",
        "polarity": "Yang",
    },
    "strength": "Weak",
    "strength_score": 4,
    "useful_gods": {
        "primary": "Earth",
        "secondary": "Metal",
        "reasoning": "Weak Metal needs Earth (resource) and Metal (friend) support"
    },
    "unfavorable_elements": {
        "primary": "Fire",
        "secondary": "Water",
        "reasoning": "Fire controls Metal; Water drains weak Metal"
    },
    "ten_god_profile": {
        "dominant_god": "Indirect Wealth",
        "profile_name": "Pioneer",
        "behavioral_traits": ["Opportunistic", "Adaptable", "Bold"]
    },
    "special_structures": {
        "wealth_vault": True,
        "nobleman_present": False,
        "other_structures": []
    },
    "settings": {
        "timezone": "UTC+8",
        "location": "Singapore",
        "theme": "dark",
        "language": "english",
        "show_chinese": True
    }
}


def ensure_data_dir():
    """Ensure the data directory exists"""
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def load_profile() -> Dict[str, Any]:
    """Load user profile from file, or return default"""
    ensure_data_dir()
    
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_PROFILE.copy()
    
    # Save default profile if none exists
    save_profile(DEFAULT_PROFILE)
    return DEFAULT_PROFILE.copy()


def save_profile(profile: Dict[str, Any]) -> bool:
    """Save user profile to file"""
    ensure_data_dir()
    
    try:
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def update_day_master(chinese_stem: str) -> Dict[str, Any]:
    """Update profile with new day master"""
    profile = load_profile()
    
    if chinese_stem in DAY_MASTERS:
        dm_info = DAY_MASTERS[chinese_stem]
        profile["day_master"] = {
            "chinese": chinese_stem,
            "pinyin": dm_info["pinyin"],
            "element": dm_info["element"],
            "polarity": dm_info["polarity"],
        }
        save_profile(profile)
    
    return profile


def update_strength(strength: str, score: int = 5) -> Dict[str, Any]:
    """Update profile strength assessment"""
    profile = load_profile()
    profile["strength"] = strength
    profile["strength_score"] = score
    save_profile(profile)
    return profile


def update_useful_gods(primary: str, secondary: str, reasoning: str = "") -> Dict[str, Any]:
    """Update useful gods"""
    profile = load_profile()
    profile["useful_gods"] = {
        "primary": primary,
        "secondary": secondary,
        "reasoning": reasoning
    }
    save_profile(profile)
    return profile


def update_ten_god_profile(dominant_god: str) -> Dict[str, Any]:
    """Update ten god profile"""
    profile = load_profile()
    
    if dominant_god in TEN_GOD_PROFILES:
        god_info = TEN_GOD_PROFILES[dominant_god]
        profile["ten_god_profile"] = {
            "dominant_god": dominant_god,
            "profile_name": god_info["name"],
            "behavioral_traits": god_info["traits"]
        }
        save_profile(profile)
    
    return profile


def calculate_bazi_alignment(profile: Dict[str, Any], palace_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate how well a QMDJ palace aligns with user's BaZi profile
    Returns alignment score and detailed breakdown
    """
    # Handle both old (dict) and new (list/string) formats
    useful_gods = profile.get("useful_gods", [])
    if isinstance(useful_gods, dict):
        useful_primary = useful_gods.get("primary", "")
        useful_secondary = useful_gods.get("secondary", "")
    elif isinstance(useful_gods, list):
        useful_primary = useful_gods[0] if len(useful_gods) > 0 else ""
        useful_secondary = useful_gods[1] if len(useful_gods) > 1 else ""
    else:
        useful_primary = ""
        useful_secondary = ""
    
    unfavorable_list = profile.get("unfavorable", profile.get("unfavorable_elements", []))
    if isinstance(unfavorable_list, dict):
        unfavorable = unfavorable_list.get("primary", "")
    elif isinstance(unfavorable_list, list):
        unfavorable = unfavorable_list[0] if len(unfavorable_list) > 0 else ""
    else:
        unfavorable = ""
    
    dm = profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        dm_element = dm.get("element", "Metal")
    else:
        # day_master is a string like "Ji", get element from profile or lookup
        dm_element = profile.get("element", "Metal")
    
    alignment = {
        "score": 5,  # Base score
        "useful_god_activation": 0,
        "dm_support": 0,
        "clash_penalty": 0,
        "details": [],
        "warnings": []
    }
    
    # Check components for useful gods
    components = []
    if "heaven_stem" in palace_data:
        components.append(("Heaven Stem", palace_data["heaven_stem"].get("element", "")))
    if "earth_stem" in palace_data:
        components.append(("Earth Stem", palace_data["earth_stem"].get("element", "")))
    if "door" in palace_data:
        components.append(("Door", palace_data["door"].get("element", "")))
    if "star" in palace_data:
        components.append(("Star", palace_data["star"].get("element", "")))
    
    for name, element in components:
        if element == useful_primary:
            alignment["useful_god_activation"] += 2
            alignment["details"].append(f"✅ {element} ({name}) = Primary useful god active")
        elif element == useful_secondary:
            alignment["useful_god_activation"] += 1
            alignment["details"].append(f"✅ {element} ({name}) = Secondary useful god active")
        elif element == unfavorable:
            alignment["clash_penalty"] -= 2
            alignment["warnings"].append(f"⚠️ {element} ({name}) = Unfavorable element present")
        elif element == dm_element:
            alignment["dm_support"] += 1
            alignment["details"].append(f"👤 {element} ({name}) = Same as Day Master")
    
    # Check for resource support (element that produces DM)
    element_producers = {
        "Wood": "Water",
        "Fire": "Wood",
        "Earth": "Fire",
        "Metal": "Earth",
        "Water": "Metal"
    }
    resource_element = element_producers.get(dm_element, "")
    
    for name, element in components:
        if element == resource_element and element not in [useful_primary, useful_secondary]:
            alignment["dm_support"] += 0.5
            alignment["details"].append(f"🔋 {element} ({name}) = Resource for Day Master")
    
    # Calculate final score
    total = 5 + alignment["useful_god_activation"] + alignment["dm_support"] + alignment["clash_penalty"]
    alignment["score"] = max(1, min(10, round(total, 1)))
    
    return alignment


def get_profile_display_text(profile: Dict[str, Any]) -> str:
    """Generate display text for profile"""
    dm = profile.get("day_master", {})
    strength = profile.get("strength", "Unknown")
    useful = profile.get("useful_gods", {})
    ten_god = profile.get("ten_god_profile", {})
    
    return f"""
Day Master: {dm.get('chinese', '')} {dm.get('pinyin', '')} {dm.get('element', '')} ({dm.get('polarity', '')})
Strength: {strength}
Useful Gods: {useful.get('primary', '')} (primary), {useful.get('secondary', '')} (secondary)
Profile: {ten_god.get('profile_name', '')} ({ten_god.get('dominant_god', '')})
""".strip()


def get_dm_options() -> List[tuple]:
    """Get day master options for dropdown"""
    return [(f"{k} {v['pinyin']} ({v['element']})", k) for k, v in DAY_MASTERS.items()]


def get_profile_options() -> List[tuple]:
    """Get ten god profile options for dropdown"""
    return [(f"{v['name']} ({k})", k) for k, v in TEN_GOD_PROFILES.items()]


def get_default_profile() -> Dict[str, Any]:
    """Return the default BaZi profile for a Weak Geng Metal Pioneer"""
    return {
        "day_master": "Geng",
        "chinese": "庚",
        "element": "Metal",
        "polarity": "Yang",
        "strength": "Weak",
        "useful_gods": ["Earth", "Metal"],
        "unfavorable": ["Fire"],
        "profile": "Pioneer (Indirect Wealth)",
        "profile_emoji": "🎯",
        "special_structures": {
            "wealth_vault": True,
            "nobleman": False,
            "traveling_horse": False,
            "other": []
        }
    }
