"""
QMDJ Calculations Module
Handles chart generation using kinqimen library or fallback calculations
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
import random

# Try to import kinqimen, fall back to simulation if not available
try:
    from kinqimen import QiMen
    KINQIMEN_AVAILABLE = True
except ImportError:
    KINQIMEN_AVAILABLE = False

from utils.mappings import (
    STAR_MAPPING, DOOR_MAPPING, DEITY_MAPPING,
    STAR_ELEMENTS, DOOR_ELEMENTS, DEITY_NATURES,
    STAR_CATEGORIES, DOOR_CATEGORIES,
    translate_star, translate_door, translate_deity
)

# Element relationships for strength calculation
ELEMENT_CYCLE = {
    "Wood": {"produces": "Fire", "controls": "Earth", "produced_by": "Water", "controlled_by": "Metal"},
    "Fire": {"produces": "Earth", "controls": "Metal", "produced_by": "Wood", "controlled_by": "Water"},
    "Earth": {"produces": "Metal", "controls": "Water", "produced_by": "Fire", "controlled_by": "Wood"},
    "Metal": {"produces": "Water", "controls": "Wood", "produced_by": "Earth", "controlled_by": "Fire"},
    "Water": {"produces": "Wood", "controls": "Fire", "produced_by": "Metal", "controlled_by": "Earth"},
}

# Palace element mapping
PALACE_ELEMENTS = {
    1: "Water",   # Kan - North
    2: "Earth",   # Kun - Southwest
    3: "Wood",    # Zhen - East
    4: "Wood",    # Xun - Southeast
    5: "Earth",   # Center
    6: "Metal",   # Qian - Northwest
    7: "Metal",   # Dui - West
    8: "Earth",   # Gen - Northeast
    9: "Fire",    # Li - South
}


def calculate_strength(component_element: str, palace_element: str) -> tuple:
    """
    Calculate the strength of a component based on its element and the palace element.
    Returns (strength_name, strength_score)
    """
    if component_element == palace_element:
        return ("Timely", 2)
    elif ELEMENT_CYCLE[palace_element]["produces"] == component_element:
        return ("Prosperous", 3)
    elif ELEMENT_CYCLE[palace_element]["produced_by"] == component_element:
        return ("Resting", 0)
    elif ELEMENT_CYCLE[palace_element]["controls"] == component_element:
        return ("Confined", -2)
    elif ELEMENT_CYCLE[palace_element]["controlled_by"] == component_element:
        return ("Dead", -3)
    else:
        return ("Neutral", 0)


def get_stem_element(stem: str) -> str:
    """Get the element of a heaven/earth stem"""
    stem_elements = {
        "甲": "Wood", "乙": "Wood",
        "丙": "Fire", "丁": "Fire",
        "戊": "Earth", "己": "Earth",
        "庚": "Metal", "辛": "Metal",
        "壬": "Water", "癸": "Water",
        "Jia": "Wood", "Yi": "Wood",
        "Bing": "Fire", "Ding": "Fire",
        "Wu": "Earth", "Ji": "Earth",
        "Geng": "Metal", "Xin": "Metal",
        "Ren": "Water", "Gui": "Water",
    }
    return stem_elements.get(stem, "Unknown")


def get_stem_polarity(stem: str) -> str:
    """Get the polarity of a stem"""
    yang_stems = ["甲", "丙", "戊", "庚", "壬", "Jia", "Bing", "Wu", "Geng", "Ren"]
    return "Yang" if stem in yang_stems else "Yin"


class QMDJChart:
    """QMDJ Chart data container"""
    
    def __init__(self, dt: datetime, timezone: str = "UTC+8"):
        self.datetime = dt
        self.timezone = timezone
        self.structure = None  # Yang Dun or Yin Dun
        self.ju_number = None
        self.palaces = {}
        self._generate_chart()
    
    def _generate_chart(self):
        """Generate the QMDJ chart"""
        if KINQIMEN_AVAILABLE:
            self._generate_with_kinqimen()
        else:
            self._generate_simulated()
    
    def _generate_with_kinqimen(self):
        """Generate chart using kinqimen library"""
        try:
            qm = QiMen(
                year=self.datetime.year,
                month=self.datetime.month,
                day=self.datetime.day,
                hour=self.datetime.hour
            )
            
            # Determine structure (Yang/Yin Dun)
            self.structure = "Yang Dun" if qm.ju > 0 else "Yin Dun"
            self.ju_number = abs(qm.ju)
            
            # Extract palace data
            for palace_num in range(1, 10):
                palace_data = self._extract_palace_data(qm, palace_num)
                self.palaces[palace_num] = palace_data
                
        except Exception as e:
            print(f"Error with kinqimen: {e}")
            self._generate_simulated()
    
    def _extract_palace_data(self, qm, palace_num: int) -> Dict[str, Any]:
        """Extract data for a specific palace from kinqimen"""
        palace_element = PALACE_ELEMENTS[palace_num]
        
        try:
            # Get components from kinqimen
            heaven_stem = qm.tian_pan[palace_num - 1] if hasattr(qm, 'tian_pan') else "戊"
            earth_stem = qm.di_pan[palace_num - 1] if hasattr(qm, 'di_pan') else "己"
            door = qm.ba_men[palace_num - 1] if hasattr(qm, 'ba_men') else "开门"
            star = qm.jiu_xing[palace_num - 1] if hasattr(qm, 'jiu_xing') else "天心"
            deity = qm.ba_shen[palace_num - 1] if hasattr(qm, 'ba_shen') else "值符"
            
            # Translate to English
            door_en = translate_door(door) if door else "Open"
            star_en = translate_star(star) if star else "Heart"
            deity_en = translate_deity(deity) if deity else "Chief"
            
        except (AttributeError, IndexError):
            # Fallback to simulated data
            return self._generate_simulated_palace(palace_num)
        
        # Get elements
        heaven_element = get_stem_element(heaven_stem)
        earth_element = get_stem_element(earth_stem)
        door_element = DOOR_ELEMENTS.get(door_en, "Earth")
        star_element = STAR_ELEMENTS.get(star_en, "Metal")
        
        # Calculate strengths
        heaven_strength = calculate_strength(heaven_element, palace_element)
        earth_strength = calculate_strength(earth_element, palace_element)
        door_strength = calculate_strength(door_element, palace_element)
        star_strength = calculate_strength(star_element, palace_element)
        
        return {
            "palace_number": palace_num,
            "palace_element": palace_element,
            "heaven_stem": {
                "chinese": heaven_stem,
                "element": heaven_element,
                "polarity": get_stem_polarity(heaven_stem),
                "strength": heaven_strength[0],
                "score": heaven_strength[1],
            },
            "earth_stem": {
                "chinese": earth_stem,
                "element": earth_element,
                "polarity": get_stem_polarity(earth_stem),
                "strength": earth_strength[0],
                "score": earth_strength[1],
            },
            "door": {
                "name": door_en,
                "chinese": door if door else DOOR_MAPPING.get(door_en, ""),
                "element": door_element,
                "category": DOOR_CATEGORIES.get(door_en, "Neutral"),
                "strength": door_strength[0],
                "score": door_strength[1],
            },
            "star": {
                "name": star_en,
                "chinese": star if star else STAR_MAPPING.get(star_en, ""),
                "element": star_element,
                "category": STAR_CATEGORIES.get(star_en, "Neutral"),
                "strength": star_strength[0],
                "score": star_strength[1],
            },
            "deity": {
                "name": deity_en,
                "chinese": deity if deity else DEITY_MAPPING.get(deity_en, ""),
                "nature": DEITY_NATURES.get(deity_en, "Neutral"),
            },
        }
    
    def _generate_simulated(self):
        """Generate simulated chart data for demo/testing"""
        # Determine structure based on solar term (simplified)
        month = self.datetime.month
        self.structure = "Yang Dun" if month in [12, 1, 2, 3, 4, 5] else "Yin Dun"
        
        # Calculate ju number (simplified - real calculation is complex)
        day = self.datetime.day
        hour = self.datetime.hour
        self.ju_number = ((day + hour) % 9) + 1
        
        # Generate palace data with realistic distributions
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        doors = list(DOOR_MAPPING.keys())
        stars = list(STAR_MAPPING.keys())
        deities = list(DEITY_MAPPING.keys())
        
        # Seed random with datetime for consistent results
        random.seed(self.datetime.timestamp())
        
        for palace_num in range(1, 10):
            self.palaces[palace_num] = self._generate_simulated_palace(
                palace_num, stems, doors, stars, deities
            )
    
    def _generate_simulated_palace(
        self, 
        palace_num: int,
        stems: Optional[List[str]] = None,
        doors: Optional[List[str]] = None,
        stars: Optional[List[str]] = None,
        deities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate simulated data for a single palace"""
        if stems is None:
            stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        if doors is None:
            doors = list(DOOR_MAPPING.keys())
        if stars is None:
            stars = list(STAR_MAPPING.keys())
        if deities is None:
            deities = list(DEITY_MAPPING.keys())
        
        palace_element = PALACE_ELEMENTS[palace_num]
        
        # Select components
        heaven_stem = random.choice(stems)
        earth_stem = random.choice(stems)
        door = random.choice(doors)
        star = random.choice(stars)
        deity = random.choice(deities)
        
        # Translate
        door_en = translate_door(door)
        star_en = translate_star(star)
        deity_en = translate_deity(deity)
        
        # Get elements
        heaven_element = get_stem_element(heaven_stem)
        earth_element = get_stem_element(earth_stem)
        door_element = DOOR_ELEMENTS.get(door_en, "Earth")
        star_element = STAR_ELEMENTS.get(star_en, "Metal")
        
        # Calculate strengths
        heaven_strength = calculate_strength(heaven_element, palace_element)
        earth_strength = calculate_strength(earth_element, palace_element)
        door_strength = calculate_strength(door_element, palace_element)
        star_strength = calculate_strength(star_element, palace_element)
        
        return {
            "palace_number": palace_num,
            "palace_element": palace_element,
            "heaven_stem": {
                "chinese": heaven_stem,
                "element": heaven_element,
                "polarity": get_stem_polarity(heaven_stem),
                "strength": heaven_strength[0],
                "score": heaven_strength[1],
            },
            "earth_stem": {
                "chinese": earth_stem,
                "element": earth_element,
                "polarity": get_stem_polarity(earth_stem),
                "strength": earth_strength[0],
                "score": earth_strength[1],
            },
            "door": {
                "name": door_en,
                "chinese": door,
                "element": door_element,
                "category": DOOR_CATEGORIES.get(door_en, "Neutral"),
                "strength": door_strength[0],
                "score": door_strength[1],
            },
            "star": {
                "name": star_en,
                "chinese": star,
                "element": star_element,
                "category": STAR_CATEGORIES.get(star_en, "Neutral"),
                "strength": star_strength[0],
                "score": star_strength[1],
            },
            "deity": {
                "name": deity_en,
                "chinese": deity,
                "nature": DEITY_NATURES.get(deity_en, "Neutral"),
            },
        }
    
    def calculate_palace_score(self, palace_num: int) -> float:
        """Calculate overall score for a palace"""
        palace = self.palaces.get(palace_num, {})
        if not palace:
            return 5.0
        
        total = 0
        total += palace.get("heaven_stem", {}).get("score", 0)
        total += palace.get("earth_stem", {}).get("score", 0)
        total += palace.get("door", {}).get("score", 0)
        total += palace.get("star", {}).get("score", 0)
        
        # Add deity bonus
        deity_nature = palace.get("deity", {}).get("nature", "Neutral")
        if deity_nature == "Auspicious":
            total += 2
        elif deity_nature == "Inauspicious":
            total -= 1
        
        # Add door category bonus
        door_cat = palace.get("door", {}).get("category", "Neutral")
        if door_cat == "Auspicious":
            total += 1
        elif door_cat == "Inauspicious":
            total -= 1
        
        # Normalize to 1-10 scale (raw range is approximately -12 to +12)
        normalized = ((total + 12) / 24) * 9 + 1
        return round(max(1, min(10, normalized)), 1)
    
    def detect_formation(self, palace_num: int) -> Optional[Dict[str, Any]]:
        """Detect any special formations in a palace"""
        palace = self.palaces.get(palace_num, {})
        if not palace:
            return None
        
        heaven = palace.get("heaven_stem", {}).get("chinese", "")
        door = palace.get("door", {}).get("name", "")
        star = palace.get("star", {}).get("name", "")
        deity = palace.get("deity", {}).get("name", "")
        
        # Simple formation detection rules
        from utils.mappings import FORMATIONS
        
        # Dragon Returns - Jia at palace with Open door
        if heaven == "甲" and door == "Open":
            return FORMATIONS["dragon_return"]
        
        # Bird Falls - Hero star with Life door
        if star == "Hero" and door == "Life":
            return FORMATIONS["bird_falls"]
        
        # Ghost Entry - Grass star with Death door
        if star == "Grass" and door == "Death":
            return FORMATIONS["ghost_entry"]
        
        # Tiger Escapes - Tiger deity with Harm door
        if deity == "Tiger" and door in ["Harm", "Fear"]:
            return FORMATIONS["tiger_escapes"]
        
        # Jade Maiden - Moon deity with Rest door
        if deity == "Moon" and door == "Rest":
            return FORMATIONS["jade_maiden"]
        
        # Sky Horse - Nine Heaven with Open door
        if deity == "Nine Heaven" and door == "Open":
            return FORMATIONS["sky_horse"]
        
        return None
    
    def get_verdict(self, score: float) -> str:
        """Get verdict based on score"""
        if score >= 8.5:
            return "HIGHLY AUSPICIOUS"
        elif score >= 7.0:
            return "AUSPICIOUS"
        elif score >= 4.5:
            return "NEUTRAL"
        elif score >= 3.0:
            return "INAUSPICIOUS"
        else:
            return "HIGHLY INAUSPICIOUS"


def generate_chart(dt: datetime, timezone: str = "UTC+8") -> QMDJChart:
    """Generate a QMDJ chart for the given datetime"""
    return QMDJChart(dt, timezone)
