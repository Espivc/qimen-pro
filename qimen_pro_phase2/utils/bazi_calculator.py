"""
Pure Python BaZi Calculator
No external dependencies - works on any system

Calculates Four Pillars (Year, Month, Day, Hour) from birth date/time
Uses the Hsia Calendar (夏历) sexagenary cycle method
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

# ==============================================================================
# CONSTANTS
# ==============================================================================

# Heavenly Stems (天干) - 10 stems
HEAVENLY_STEMS = [
    {"chinese": "甲", "pinyin": "Jia", "element": "Wood", "polarity": "Yang"},
    {"chinese": "乙", "pinyin": "Yi", "element": "Wood", "polarity": "Yin"},
    {"chinese": "丙", "pinyin": "Bing", "element": "Fire", "polarity": "Yang"},
    {"chinese": "丁", "pinyin": "Ding", "element": "Fire", "polarity": "Yin"},
    {"chinese": "戊", "pinyin": "Wu", "element": "Earth", "polarity": "Yang"},
    {"chinese": "己", "pinyin": "Ji", "element": "Earth", "polarity": "Yin"},
    {"chinese": "庚", "pinyin": "Geng", "element": "Metal", "polarity": "Yang"},
    {"chinese": "辛", "pinyin": "Xin", "element": "Metal", "polarity": "Yin"},
    {"chinese": "壬", "pinyin": "Ren", "element": "Water", "polarity": "Yang"},
    {"chinese": "癸", "pinyin": "Gui", "element": "Water", "polarity": "Yin"},
]

# Earthly Branches (地支) - 12 branches
EARTHLY_BRANCHES = [
    {"chinese": "子", "pinyin": "Zi", "animal": "Rat", "element": "Water", "polarity": "Yang"},
    {"chinese": "丑", "pinyin": "Chou", "animal": "Ox", "element": "Earth", "polarity": "Yin"},
    {"chinese": "寅", "pinyin": "Yin", "animal": "Tiger", "element": "Wood", "polarity": "Yang"},
    {"chinese": "卯", "pinyin": "Mao", "animal": "Rabbit", "element": "Wood", "polarity": "Yin"},
    {"chinese": "辰", "pinyin": "Chen", "animal": "Dragon", "element": "Earth", "polarity": "Yang"},
    {"chinese": "巳", "pinyin": "Si", "animal": "Snake", "element": "Fire", "polarity": "Yin"},
    {"chinese": "午", "pinyin": "Wu", "animal": "Horse", "element": "Fire", "polarity": "Yang"},
    {"chinese": "未", "pinyin": "Wei", "animal": "Goat", "element": "Earth", "polarity": "Yin"},
    {"chinese": "申", "pinyin": "Shen", "animal": "Monkey", "element": "Metal", "polarity": "Yang"},
    {"chinese": "酉", "pinyin": "You", "animal": "Rooster", "element": "Metal", "polarity": "Yin"},
    {"chinese": "戌", "pinyin": "Xu", "animal": "Dog", "element": "Earth", "polarity": "Yang"},
    {"chinese": "亥", "pinyin": "Hai", "animal": "Pig", "element": "Water", "polarity": "Yin"},
]

# Hour branches mapping (Chinese hours are 2-hour periods)
# 子时 23:00-01:00, 丑时 01:00-03:00, etc.
HOUR_BRANCHES = [
    (23, 1, 0),   # 子 Zi - 23:00-00:59
    (1, 3, 1),    # 丑 Chou - 01:00-02:59
    (3, 5, 2),    # 寅 Yin - 03:00-04:59
    (5, 7, 3),    # 卯 Mao - 05:00-06:59
    (7, 9, 4),    # 辰 Chen - 07:00-08:59
    (9, 11, 5),   # 巳 Si - 09:00-10:59
    (11, 13, 6),  # 午 Wu - 11:00-12:59
    (13, 15, 7),  # 未 Wei - 13:00-14:59
    (15, 17, 8),  # 申 Shen - 15:00-16:59
    (17, 19, 9),  # 酉 You - 17:00-18:59
    (19, 21, 10), # 戌 Xu - 19:00-20:59
    (21, 23, 11), # 亥 Hai - 21:00-22:59
]

# Reference date for calculation (Known: Jan 1, 1900 = 庚子年 甲子月 甲戌日)
# Using a known reference point to calculate cycles
REFERENCE_DATE = datetime(1900, 1, 31)  # Chinese New Year 1900
REFERENCE_YEAR_STEM = 6   # 庚 (Geng)
REFERENCE_YEAR_BRANCH = 0  # 子 (Zi)

# Solar terms for month calculation (approximate dates)
# Month stems depend on year stem, month branches are fixed by solar terms
SOLAR_TERMS = [
    (2, 4),   # 立春 Start of Spring - Month 1 (寅)
    (3, 6),   # 惊蛰 Awakening - Month 2 (卯)
    (4, 5),   # 清明 Clear and Bright - Month 3 (辰)
    (5, 6),   # 立夏 Start of Summer - Month 4 (巳)
    (6, 6),   # 芒种 Grain in Ear - Month 5 (午)
    (7, 7),   # 小暑 Minor Heat - Month 6 (未)
    (8, 8),   # 立秋 Start of Autumn - Month 7 (申)
    (9, 8),   # 白露 White Dew - Month 8 (酉)
    (10, 8),  # 寒露 Cold Dew - Month 9 (戌)
    (11, 7),  # 立冬 Start of Winter - Month 10 (亥)
    (12, 7),  # 大雪 Major Snow - Month 11 (子)
    (1, 6),   # 小寒 Minor Cold - Month 12 (丑)
]


# ==============================================================================
# CALCULATION FUNCTIONS
# ==============================================================================

def get_day_stem_branch(date: datetime) -> Tuple[int, int]:
    """
    Calculate the Heavenly Stem and Earthly Branch for a given day.
    Uses the standard formula based on Julian Day Number.
    
    Returns: (stem_index, branch_index)
    """
    # Calculate Julian Day Number
    year = date.year
    month = date.month
    day = date.day
    
    # Julian Day Number formula
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    # Day stem cycles every 10 days, branch cycles every 12 days
    # Reference: JDN 0 = 甲子 (Jia Zi) stem=0, branch=0
    # Adjustment for actual historical alignment
    stem_index = (jdn + 9) % 10
    branch_index = (jdn + 1) % 12
    
    return stem_index, branch_index


def get_year_stem_branch(date: datetime) -> Tuple[int, int]:
    """
    Calculate Year Pillar based on Chinese lunar year.
    Chinese year starts at 立春 (Start of Spring, ~Feb 4).
    
    Returns: (stem_index, branch_index)
    """
    year = date.year
    month = date.month
    day = date.day
    
    # Check if before Start of Spring (approximately Feb 4)
    # If before, use previous year
    if month < 2 or (month == 2 and day < 4):
        year -= 1
    
    # 1984 is 甲子 (Jia Zi) year - stem=0, branch=0
    # Use this as reference
    base_year = 1984
    diff = year - base_year
    
    stem_index = diff % 10
    branch_index = diff % 12
    
    # Adjust for negative years
    if stem_index < 0:
        stem_index += 10
    if branch_index < 0:
        branch_index += 12
    
    return stem_index, branch_index


def get_month_stem_branch(date: datetime, year_stem: int) -> Tuple[int, int]:
    """
    Calculate Month Pillar.
    Month branch is determined by solar terms.
    Month stem depends on year stem (五虎遁).
    
    Returns: (stem_index, branch_index)
    """
    month = date.month
    day = date.day
    
    # Determine which Chinese month based on solar terms
    # Each month starts at specific solar term
    chinese_month = 0
    
    for i, (term_month, term_day) in enumerate(SOLAR_TERMS):
        if month > term_month or (month == term_month and day >= term_day):
            chinese_month = i
    
    # Month branch: 寅(2) for month 1, 卯(3) for month 2, etc.
    branch_index = (chinese_month + 2) % 12
    
    # Month stem calculation (五虎遁 - Five Tigers Method)
    # Year stem determines starting month stem
    # 甲己年起丙寅, 乙庚年起戊寅, 丙辛年起庚寅, 丁壬年起壬寅, 戊癸年起甲寅
    year_stem_group = year_stem % 5
    month_stem_start = [2, 4, 6, 8, 0][year_stem_group]  # 丙,戊,庚,壬,甲
    
    stem_index = (month_stem_start + chinese_month) % 10
    
    return stem_index, branch_index


def get_hour_stem_branch(hour: int, day_stem: int) -> Tuple[int, int]:
    """
    Calculate Hour Pillar.
    Hour branch is determined by time of day.
    Hour stem depends on day stem (五鼠遁).
    
    Returns: (stem_index, branch_index)
    """
    # Determine hour branch
    branch_index = 0
    
    if hour == 23 or hour == 0:
        branch_index = 0  # 子
    else:
        branch_index = (hour + 1) // 2
    
    # Hour stem calculation (五鼠遁 - Five Rats Method)
    # Day stem determines starting hour stem
    # 甲己日起甲子, 乙庚日起丙子, 丙辛日起戊子, 丁壬日起庚子, 戊癸日起壬子
    day_stem_group = day_stem % 5
    hour_stem_start = [0, 2, 4, 6, 8][day_stem_group]  # 甲,丙,戊,庚,壬
    
    stem_index = (hour_stem_start + branch_index) % 10
    
    return stem_index, branch_index


def calculate_bazi(birth_date: datetime, birth_hour: int = 12) -> Dict:
    """
    Calculate complete BaZi (Four Pillars) from birth date and time.
    
    Args:
        birth_date: Date of birth
        birth_hour: Hour of birth (0-23)
    
    Returns:
        Dictionary with all four pillars and Day Master info
    """
    # Calculate each pillar
    year_stem, year_branch = get_year_stem_branch(birth_date)
    month_stem, month_branch = get_month_stem_branch(birth_date, year_stem)
    day_stem, day_branch = get_day_stem_branch(birth_date)
    hour_stem, hour_branch = get_hour_stem_branch(birth_hour, day_stem)
    
    # Build result
    day_master = HEAVENLY_STEMS[day_stem]
    
    result = {
        "birth_date": birth_date.strftime("%Y-%m-%d"),
        "birth_hour": birth_hour,
        
        # Day Master (most important)
        "day_master": {
            "stem_index": day_stem,
            "pinyin": day_master["pinyin"],
            "chinese": day_master["chinese"],
            "element": day_master["element"],
            "polarity": day_master["polarity"],
        },
        
        # Four Pillars
        "year_pillar": {
            "stem": HEAVENLY_STEMS[year_stem],
            "branch": EARTHLY_BRANCHES[year_branch],
            "display": f"{HEAVENLY_STEMS[year_stem]['chinese']}{EARTHLY_BRANCHES[year_branch]['chinese']}",
        },
        "month_pillar": {
            "stem": HEAVENLY_STEMS[month_stem],
            "branch": EARTHLY_BRANCHES[month_branch],
            "display": f"{HEAVENLY_STEMS[month_stem]['chinese']}{EARTHLY_BRANCHES[month_branch]['chinese']}",
        },
        "day_pillar": {
            "stem": HEAVENLY_STEMS[day_stem],
            "branch": EARTHLY_BRANCHES[day_branch],
            "display": f"{HEAVENLY_STEMS[day_stem]['chinese']}{EARTHLY_BRANCHES[day_branch]['chinese']}",
        },
        "hour_pillar": {
            "stem": HEAVENLY_STEMS[hour_stem],
            "branch": EARTHLY_BRANCHES[hour_branch],
            "display": f"{HEAVENLY_STEMS[hour_stem]['chinese']}{EARTHLY_BRANCHES[hour_branch]['chinese']}",
        },
        
        # Animal sign (from year branch)
        "animal_sign": EARTHLY_BRANCHES[year_branch]["animal"],
    }
    
    return result


def analyze_strength(bazi: Dict) -> Dict:
    """
    Analyze Day Master strength based on supporting/controlling elements.
    
    This is a simplified analysis - real BaZi requires deeper consideration
    of seasonal strength, hidden stems, etc.
    
    Returns strength assessment and suggested useful gods.
    """
    dm_element = bazi["day_master"]["element"]
    
    # Element cycle
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    dm_idx = elements.index(dm_element)
    
    # What produces DM (parent)
    producing = elements[(dm_idx - 1) % 5]
    # What DM produces (child)  
    produced = elements[(dm_idx + 1) % 5]
    # What controls DM (克我)
    controlling = elements[(dm_idx - 2) % 5]
    # What DM controls (我克)
    controlled = elements[(dm_idx + 2) % 5]
    # Same element
    same = dm_element
    
    # Count supporting vs draining elements in pillars
    support_count = 0
    drain_count = 0
    
    for pillar in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]:
        stem_elem = bazi[pillar]["stem"]["element"]
        branch_elem = bazi[pillar]["branch"]["element"]
        
        for elem in [stem_elem, branch_elem]:
            if elem == same or elem == producing:
                support_count += 1
            elif elem == controlling or elem == produced:
                drain_count += 1
    
    # Determine strength
    if support_count >= 5:
        strength = "Strong"
        useful_gods = [controlled, produced]  # Need to drain
        unfavorable = [producing, same]
    elif support_count <= 2:
        strength = "Weak"
        useful_gods = [producing, same]  # Need support
        unfavorable = [controlling, controlled]
    else:
        strength = "Balanced"
        useful_gods = [producing]
        unfavorable = [controlling]
    
    return {
        "strength": strength,
        "support_count": support_count,
        "drain_count": drain_count,
        "useful_gods": useful_gods,
        "unfavorable": unfavorable,
        "element_analysis": {
            "produces_dm": producing,
            "dm_produces": produced,
            "controls_dm": controlling,
            "dm_controls": controlled,
        }
    }


def get_ten_god_profile(dm_element: str, strength: str) -> Dict:
    """
    Suggest Ten God profile based on Day Master element and strength.
    This is a simplified suggestion - real profiling requires full chart analysis.
    """
    profiles = {
        ("Wood", "Weak"): {"profile": "Diplomat (Direct Resource)", "emoji": "🤝"},
        ("Wood", "Strong"): {"profile": "Philosopher (Hurting Officer)", "emoji": "🎭"},
        ("Fire", "Weak"): {"profile": "Analyzer (Indirect Resource)", "emoji": "🔍"},
        ("Fire", "Strong"): {"profile": "Artist (Eating God)", "emoji": "🎨"},
        ("Earth", "Weak"): {"profile": "Director (Direct Officer)", "emoji": "👔"},
        ("Earth", "Strong"): {"profile": "Strategist (Direct Wealth)", "emoji": "📊"},
        ("Metal", "Weak"): {"profile": "Pioneer (Indirect Wealth)", "emoji": "🎯"},
        ("Metal", "Strong"): {"profile": "Warrior (7 Killings)", "emoji": "⚔️"},
        ("Water", "Weak"): {"profile": "Connector (Friend)", "emoji": "🌐"},
        ("Water", "Strong"): {"profile": "Competitor (Rob Wealth)", "emoji": "🏆"},
    }
    
    key = (dm_element, strength if strength in ["Weak", "Strong"] else "Weak")
    return profiles.get(key, {"profile": "Pioneer (Indirect Wealth)", "emoji": "🎯"})


def calculate_full_profile(birth_date: datetime, birth_hour: int = 12) -> Dict:
    """
    Calculate complete BaZi profile with strength analysis and suggestions.
    
    Args:
        birth_date: Date of birth
        birth_hour: Hour of birth (0-23)
    
    Returns:
        Complete profile ready for Settings page
    """
    # Calculate BaZi
    bazi = calculate_bazi(birth_date, birth_hour)
    
    # Analyze strength
    analysis = analyze_strength(bazi)
    
    # Get profile suggestion
    profile_suggestion = get_ten_god_profile(
        bazi["day_master"]["element"],
        analysis["strength"]
    )
    
    # Build complete profile
    return {
        "bazi": bazi,
        "analysis": analysis,
        "profile_suggestion": profile_suggestion,
        
        # Ready for Settings page
        "settings_profile": {
            "day_master": bazi["day_master"]["pinyin"],
            "chinese": bazi["day_master"]["chinese"],
            "element": bazi["day_master"]["element"],
            "polarity": bazi["day_master"]["polarity"],
            "strength": analysis["strength"],
            "useful_gods": analysis["useful_gods"],
            "unfavorable": analysis["unfavorable"],
            "profile": profile_suggestion["profile"],
            "profile_emoji": profile_suggestion["emoji"],
            "special_structures": {
                "wealth_vault": False,
                "nobleman": False,
                "traveling_horse": False,
                "other": []
            },
            "four_pillars": {
                "year": bazi["year_pillar"]["display"],
                "month": bazi["month_pillar"]["display"],
                "day": bazi["day_pillar"]["display"],
                "hour": bazi["hour_pillar"]["display"],
            },
            "animal_sign": bazi["animal_sign"],
        }
    }


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def format_four_pillars(bazi: Dict) -> str:
    """Format four pillars for display."""
    return (
        f"Year: {bazi['year_pillar']['display']} | "
        f"Month: {bazi['month_pillar']['display']} | "
        f"Day: {bazi['day_pillar']['display']} | "
        f"Hour: {bazi['hour_pillar']['display']}"
    )


def get_hour_branch_name(hour: int) -> str:
    """Get Chinese hour name for display."""
    if hour == 23 or hour == 0:
        idx = 0
    else:
        idx = (hour + 1) // 2
    
    branch = EARTHLY_BRANCHES[idx]
    return f"{branch['chinese']}时 ({branch['pinyin']})"


# ==============================================================================
# TEST
# ==============================================================================

if __name__ == "__main__":
    # Test with a sample date
    test_date = datetime(1985, 10, 15)
    test_hour = 14
    
    result = calculate_full_profile(test_date, test_hour)
    
    print("=" * 50)
    print("BaZi Calculator Test")
    print("=" * 50)
    print(f"Birth Date: {test_date.strftime('%Y-%m-%d')}")
    print(f"Birth Hour: {test_hour}:00 ({get_hour_branch_name(test_hour)})")
    print()
    print("Four Pillars:")
    print(format_four_pillars(result["bazi"]))
    print()
    print(f"Day Master: {result['bazi']['day_master']['chinese']} {result['bazi']['day_master']['pinyin']}")
    print(f"Element: {result['bazi']['day_master']['element']} ({result['bazi']['day_master']['polarity']})")
    print(f"Animal Sign: {result['bazi']['animal_sign']}")
    print()
    print(f"Strength: {result['analysis']['strength']}")
    print(f"Useful Gods: {', '.join(result['analysis']['useful_gods'])}")
    print(f"Unfavorable: {', '.join(result['analysis']['unfavorable'])}")
    print()
    print(f"Suggested Profile: {result['profile_suggestion']['emoji']} {result['profile_suggestion']['profile']}")
