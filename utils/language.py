"""
Qi Men Pro v2.0 - Language Dictionary
Mixed Mode: English UI + Chinese metaphysics terms
Expandable to Full bilingual support
"""

# Current language mode: "en" | "zh" | "mixed"
DEFAULT_LANGUAGE = "mixed"

# ==============================================
# METAPHYSICS TERMS (Used in Mixed + Full modes)
# ==============================================

PALACE_NAMES = {
    "Kan": {"zh": "坎", "en": "Kan", "mixed": "Kan 坎"},
    "Kun": {"zh": "坤", "en": "Kun", "mixed": "Kun 坤"},
    "Zhen": {"zh": "震", "en": "Zhen", "mixed": "Zhen 震"},
    "Xun": {"zh": "巽", "en": "Xun", "mixed": "Xun 巽"},
    "Center": {"zh": "中宫", "en": "Center", "mixed": "Center 中宫"},
    "Qian": {"zh": "乾", "en": "Qian", "mixed": "Qian 乾"},
    "Dui": {"zh": "兑", "en": "Dui", "mixed": "Dui 兑"},
    "Gen": {"zh": "艮", "en": "Gen", "mixed": "Gen 艮"},
    "Li": {"zh": "離", "en": "Li", "mixed": "Li 離"},
}

DIRECTIONS = {
    "N": {"zh": "北", "en": "N", "mixed": "N 北"},
    "NE": {"zh": "东北", "en": "NE", "mixed": "NE 东北"},
    "E": {"zh": "东", "en": "E", "mixed": "E 东"},
    "SE": {"zh": "东南", "en": "SE", "mixed": "SE 东南"},
    "S": {"zh": "南", "en": "S", "mixed": "S 南"},
    "SW": {"zh": "西南", "en": "SW", "mixed": "SW 西南"},
    "W": {"zh": "西", "en": "W", "mixed": "W 西"},
    "NW": {"zh": "西北", "en": "NW", "mixed": "NW 西北"},
    "Center": {"zh": "中", "en": "Center", "mixed": "Center 中"},
}

ELEMENTS = {
    "Wood": {"zh": "木", "en": "Wood", "mixed": "Wood 木", "emoji": "🌳"},
    "Fire": {"zh": "火", "en": "Fire", "mixed": "Fire 火", "emoji": "🔥"},
    "Earth": {"zh": "土", "en": "Earth", "mixed": "Earth 土", "emoji": "🟤"},
    "Metal": {"zh": "金", "en": "Metal", "mixed": "Metal 金", "emoji": "⚪"},
    "Water": {"zh": "水", "en": "Water", "mixed": "Water 水", "emoji": "💧"},
}

HEAVEN_STEMS = {
    "Jia": {"zh": "甲", "en": "Jia", "mixed": "Jia 甲", "element": "Wood"},
    "Yi": {"zh": "乙", "en": "Yi", "mixed": "Yi 乙", "element": "Wood"},
    "Bing": {"zh": "丙", "en": "Bing", "mixed": "Bing 丙", "element": "Fire"},
    "Ding": {"zh": "丁", "en": "Ding", "mixed": "Ding 丁", "element": "Fire"},
    "Wu": {"zh": "戊", "en": "Wu", "mixed": "Wu 戊", "element": "Earth"},
    "Ji": {"zh": "己", "en": "Ji", "mixed": "Ji 己", "element": "Earth"},
    "Geng": {"zh": "庚", "en": "Geng", "mixed": "Geng 庚", "element": "Metal"},
    "Xin": {"zh": "辛", "en": "Xin", "mixed": "Xin 辛", "element": "Metal"},
    "Ren": {"zh": "壬", "en": "Ren", "mixed": "Ren 壬", "element": "Water"},
    "Gui": {"zh": "癸", "en": "Gui", "mixed": "Gui 癸", "element": "Water"},
}

STARS = {
    "Canopy": {"zh": "天蓬", "en": "Canopy", "mixed": "Canopy 天蓬"},
    "Grass": {"zh": "天芮", "en": "Grass", "mixed": "Grass 天芮"},
    "Impulse": {"zh": "天冲", "en": "Impulse", "mixed": "Impulse 天冲"},
    "Assistant": {"zh": "天辅", "en": "Assistant", "mixed": "Assistant 天辅"},
    "Connect": {"zh": "天禽", "en": "Connect", "mixed": "Connect 天禽"},
    "Heart": {"zh": "天心", "en": "Heart", "mixed": "Heart 天心"},
    "Pillar": {"zh": "天柱", "en": "Pillar", "mixed": "Pillar 天柱"},
    "Ren": {"zh": "天任", "en": "Ren", "mixed": "Ren 天任"},
    "Hero": {"zh": "天英", "en": "Hero", "mixed": "Hero 天英"},
}

DOORS = {
    "Open": {"zh": "开门", "en": "Open", "mixed": "Open 开门"},
    "Rest": {"zh": "休门", "en": "Rest", "mixed": "Rest 休门"},
    "Life": {"zh": "生门", "en": "Life", "mixed": "Life 生门"},
    "Harm": {"zh": "伤门", "en": "Harm", "mixed": "Harm 伤门"},
    "Delusion": {"zh": "杜门", "en": "Delusion", "mixed": "Delusion 杜门"},
    "Scenery": {"zh": "景门", "en": "Scenery", "mixed": "Scenery 景门"},
    "Death": {"zh": "死门", "en": "Death", "mixed": "Death 死门"},
    "Fear": {"zh": "惊门", "en": "Fear", "mixed": "Fear 惊门"},
}

DEITIES = {
    "Chief": {"zh": "值符", "en": "Chief", "mixed": "Chief 值符"},
    "Serpent": {"zh": "腾蛇", "en": "Serpent", "mixed": "Serpent 腾蛇"},
    "Moon": {"zh": "太阴", "en": "Moon", "mixed": "Moon 太阴"},
    "Six Harmony": {"zh": "六合", "en": "Six Harmony", "mixed": "Six Harmony 六合"},
    "Hook": {"zh": "勾陈", "en": "Hook", "mixed": "Hook 勾陈"},
    "Tiger": {"zh": "白虎", "en": "Tiger", "mixed": "Tiger 白虎"},
    "Emptiness": {"zh": "玄武", "en": "Emptiness", "mixed": "Emptiness 玄武"},
    "Nine Earth": {"zh": "九地", "en": "Nine Earth", "mixed": "Nine Earth 九地"},
    "Nine Heaven": {"zh": "九天", "en": "Nine Heaven", "mixed": "Nine Heaven 九天"},
}

FORMATIONS = {
    "Dragon Returns": {"zh": "回龙返首", "en": "Dragon Returns", "mixed": "Dragon Returns 回龙返首"},
    "Bird Falls": {"zh": "飞鸟跌穴", "en": "Bird Falls", "mixed": "Bird Falls 飞鸟跌穴"},
    "Ghost Entry": {"zh": "鬼入墓", "en": "Ghost Entry", "mixed": "Ghost Entry 鬼入墓"},
    "Tiger Escapes": {"zh": "虎遁", "en": "Tiger Escapes", "mixed": "Tiger Escapes 虎遁"},
    "Jade Maiden": {"zh": "玉女守门", "en": "Jade Maiden", "mixed": "Jade Maiden 玉女守门"},
    "Sky Horse": {"zh": "天马", "en": "Sky Horse", "mixed": "Sky Horse 天马"},
}

STRENGTHS = {
    "Timely": {"zh": "当令", "en": "Timely", "mixed": "Timely 当令"},
    "Prosperous": {"zh": "旺", "en": "Prosperous", "mixed": "Prosperous 旺"},
    "Resting": {"zh": "休", "en": "Resting", "mixed": "Resting 休"},
    "Confined": {"zh": "囚", "en": "Confined", "mixed": "Confined 囚"},
    "Dead": {"zh": "死", "en": "Dead", "mixed": "Dead 死"},
}

VERDICTS = {
    "HIGHLY AUSPICIOUS": {"zh": "大吉", "en": "HIGHLY AUSPICIOUS", "mixed": "HIGHLY AUSPICIOUS 大吉"},
    "AUSPICIOUS": {"zh": "吉", "en": "AUSPICIOUS", "mixed": "AUSPICIOUS 吉"},
    "NEUTRAL": {"zh": "中", "en": "NEUTRAL", "mixed": "NEUTRAL 中"},
    "INAUSPICIOUS": {"zh": "凶", "en": "INAUSPICIOUS", "mixed": "INAUSPICIOUS 凶"},
    "HIGHLY INAUSPICIOUS": {"zh": "大凶", "en": "HIGHLY INAUSPICIOUS", "mixed": "HIGHLY INAUSPICIOUS 大凶"},
}

STRUCTURES = {
    "Yang Dun": {"zh": "阳遁", "en": "Yang Dun", "mixed": "Yang Dun 阳遁"},
    "Yin Dun": {"zh": "阴遁", "en": "Yin Dun", "mixed": "Yin Dun 阴遁"},
}

OUTCOMES = {
    "SUCCESS": {"zh": "成功", "en": "SUCCESS", "mixed": "SUCCESS 成功"},
    "PARTIAL": {"zh": "部分成功", "en": "PARTIAL", "mixed": "PARTIAL 部分"},
    "FAILURE": {"zh": "失败", "en": "FAILURE", "mixed": "FAILURE 失败"},
    "PENDING": {"zh": "待定", "en": "PENDING", "mixed": "PENDING 待定"},
    "NOT_APPLICABLE": {"zh": "不适用", "en": "N/A", "mixed": "N/A 不适用"},
}

# ==============================================
# UI LABELS (For Full mode - expandable later)
# ==============================================

UI_LABELS = {
    # Page titles
    "dashboard": {"zh": "主页", "en": "Dashboard", "mixed": "Dashboard"},
    "chart": {"zh": "排盘", "en": "Chart", "mixed": "Chart"},
    "export": {"zh": "导出", "en": "Export", "mixed": "Export"},
    "history": {"zh": "历史", "en": "History", "mixed": "History"},
    "settings": {"zh": "设置", "en": "Settings", "mixed": "Settings"},
    
    # Common buttons
    "generate": {"zh": "生成", "en": "Generate", "mixed": "Generate"},
    "save": {"zh": "保存", "en": "Save", "mixed": "Save"},
    "copy": {"zh": "复制", "en": "Copy", "mixed": "Copy"},
    "export_btn": {"zh": "导出", "en": "Export", "mixed": "Export"},
    "clear": {"zh": "清除", "en": "Clear", "mixed": "Clear"},
    "reset": {"zh": "重置", "en": "Reset", "mixed": "Reset"},
    
    # Labels
    "date": {"zh": "日期", "en": "Date", "mixed": "Date"},
    "time": {"zh": "时间", "en": "Time", "mixed": "Time"},
    "purpose": {"zh": "用途", "en": "Purpose", "mixed": "Purpose"},
    "palace": {"zh": "宫位", "en": "Palace", "mixed": "Palace"},
    "score": {"zh": "评分", "en": "Score", "mixed": "Score"},
    "verdict": {"zh": "结论", "en": "Verdict", "mixed": "Verdict"},
    "formation": {"zh": "格局", "en": "Formation", "mixed": "Formation"},
    "components": {"zh": "组件", "en": "Components", "mixed": "Components"},
    
    # BaZi terms
    "day_master": {"zh": "日主", "en": "Day Master", "mixed": "Day Master 日主"},
    "useful_gods": {"zh": "用神", "en": "Useful Gods", "mixed": "Useful Gods 用神"},
    "unfavorable": {"zh": "忌神", "en": "Unfavorable", "mixed": "Unfavorable 忌神"},
    "strength": {"zh": "强弱", "en": "Strength", "mixed": "Strength"},
    "strong": {"zh": "强", "en": "Strong", "mixed": "Strong 强"},
    "weak": {"zh": "弱", "en": "Weak", "mixed": "Weak 弱"},
    
    # Purposes
    "general_forecast": {"zh": "综合预测", "en": "General Forecast", "mixed": "General Forecast"},
    "wealth_business": {"zh": "财运事业", "en": "Wealth/Business", "mixed": "Wealth/Business"},
    "relationship": {"zh": "感情关系", "en": "Relationship", "mixed": "Relationship"},
    "strategic_decision": {"zh": "战略决策", "en": "Strategic Decision", "mixed": "Strategic Decision"},
    "date_selection": {"zh": "择日", "en": "Date Selection", "mixed": "Date Selection 择日"},
    
    # Messages
    "chart_generated": {"zh": "排盘完成", "en": "Chart generated", "mixed": "Chart generated"},
    "saved_successfully": {"zh": "保存成功", "en": "Saved successfully", "mixed": "Saved successfully"},
    "copy_prompt": {"zh": "复制分析提示词", "en": "Copy Analysis Prompt", "mixed": "Copy Analysis Prompt"},
}


# ==============================================
# HELPER FUNCTIONS
# ==============================================

def get_text(dictionary: dict, key: str, lang: str = "mixed") -> str:
    """Get text from dictionary in specified language"""
    if key in dictionary:
        return dictionary[key].get(lang, dictionary[key].get("en", key))
    return key


def get_palace(name: str, lang: str = "mixed") -> str:
    """Get palace name in specified language"""
    return get_text(PALACE_NAMES, name, lang)


def get_direction(direction: str, lang: str = "mixed") -> str:
    """Get direction in specified language"""
    return get_text(DIRECTIONS, direction, lang)


def get_element(element: str, lang: str = "mixed", with_emoji: bool = False) -> str:
    """Get element in specified language"""
    text = get_text(ELEMENTS, element, lang)
    if with_emoji and element in ELEMENTS:
        return f"{ELEMENTS[element].get('emoji', '')} {text}"
    return text


def get_stem(stem: str, lang: str = "mixed") -> str:
    """Get heaven stem in specified language"""
    return get_text(HEAVEN_STEMS, stem, lang)


def get_star(star: str, lang: str = "mixed") -> str:
    """Get star in specified language"""
    return get_text(STARS, star, lang)


def get_door(door: str, lang: str = "mixed") -> str:
    """Get door in specified language"""
    return get_text(DOORS, door, lang)


def get_deity(deity: str, lang: str = "mixed") -> str:
    """Get deity in specified language"""
    return get_text(DEITIES, deity, lang)


def get_formation(formation: str, lang: str = "mixed") -> str:
    """Get formation in specified language"""
    return get_text(FORMATIONS, formation, lang)


def get_strength(strength: str, lang: str = "mixed") -> str:
    """Get strength in specified language"""
    return get_text(STRENGTHS, strength, lang)


def get_verdict(verdict: str, lang: str = "mixed") -> str:
    """Get verdict in specified language"""
    return get_text(VERDICTS, verdict, lang)


def get_structure(structure: str, lang: str = "mixed") -> str:
    """Get structure (Yin/Yang Dun) in specified language"""
    return get_text(STRUCTURES, structure, lang)


def get_outcome(outcome: str, lang: str = "mixed") -> str:
    """Get outcome in specified language"""
    return get_text(OUTCOMES, outcome, lang)


def get_ui(key: str, lang: str = "mixed") -> str:
    """Get UI label in specified language"""
    return get_text(UI_LABELS, key, lang)


def format_component(name: str, chinese: str, lang: str = "mixed") -> str:
    """Format component name based on language mode"""
    if lang == "zh":
        return chinese
    elif lang == "mixed":
        return f"{name} {chinese}"
    else:
        return name


class LanguageHelper:
    """Helper class for easy language access in UI components"""
    
    def __init__(self, lang: str = "mixed"):
        self.lang = lang
    
    def palace(self, name_or_num) -> str:
        """Get palace name - accepts name string or palace number"""
        if isinstance(name_or_num, int):
            # Look up palace name from number
            palace_map = {1: "Kan", 2: "Kun", 3: "Zhen", 4: "Xun", 
                         5: "Center", 6: "Qian", 7: "Dui", 8: "Gen", 9: "Li"}
            name = palace_map.get(name_or_num, "")
        else:
            name = name_or_num
        return get_palace(name, self.lang)
    
    def direction(self, direction: str) -> str:
        return get_direction(direction, self.lang)
    
    def element(self, element: str, with_emoji: bool = False) -> str:
        return get_element(element, self.lang, with_emoji)
    
    def stem(self, stem: str) -> str:
        return get_stem(stem, self.lang)
    
    def star(self, star: str) -> str:
        return get_star(star, self.lang)
    
    def door(self, door: str) -> str:
        return get_door(door, self.lang)
    
    def deity(self, deity: str) -> str:
        return get_deity(deity, self.lang)
    
    def formation(self, formation: str) -> str:
        return get_formation(formation, self.lang)
    
    def strength(self, strength: str) -> str:
        return get_strength(strength, self.lang)
    
    def verdict(self, verdict: str) -> str:
        return get_verdict(verdict, self.lang)
    
    def structure(self, structure: str) -> str:
        return get_structure(structure, self.lang)
    
    def outcome(self, outcome: str) -> str:
        return get_outcome(outcome, self.lang)
    
    def ui(self, key: str) -> str:
        return get_ui(key, self.lang)
    
    def get(self, key: str) -> str:
        """Alias for ui() - get UI label"""
        return get_ui(key, self.lang)


def get_lang(lang: str = "mixed") -> LanguageHelper:
    """Get a language helper instance"""
    return LanguageHelper(lang)
