"""
Export Formatter Module
Formats chart data for export to Project 1 (Analyst Engine)
"""

from datetime import datetime
from typing import Dict, Any, Optional
import json

from config import PALACE_INFO, ELEMENT_EMOJI


def generate_analysis_prompt(
    chart_datetime: datetime,
    timezone: str,
    structure: str,
    ju_number: int,
    palace_data: Dict[str, Any],
    palace_name: str,
    formation: Optional[Dict[str, Any]],
    bazi_profile: Dict[str, Any],
    purpose: str = "General Forecast"
) -> str:
    """
    Generate a pre-formatted prompt for the Analyst Engine (Project 1)
    """
    palace_num = palace_data.get("palace_number", 0)
    palace_info = PALACE_INFO.get(palace_num, {})
    palace_element = palace_data.get("palace_element", "")
    
    # Get component data
    heaven = palace_data.get("heaven_stem", {})
    earth = palace_data.get("earth_stem", {})
    door = palace_data.get("door", {})
    star = palace_data.get("star", {})
    deity = palace_data.get("deity", {})
    
    # Get BaZi data - handle both old (dict) and new (string/list) formats
    dm = bazi_profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        dm_chinese = dm.get('chinese', '庚')
        dm_pinyin = dm.get('pinyin', 'Geng')
        dm_element = dm.get('element', 'Metal')
        dm_polarity = dm.get('polarity', 'Yang')
    else:
        # New format - day_master is a string
        dm_pinyin = dm
        dm_chinese = bazi_profile.get('chinese', '庚')
        dm_element = bazi_profile.get('element', 'Metal')
        dm_polarity = bazi_profile.get('polarity', 'Yang')
    
    useful = bazi_profile.get("useful_gods", [])
    if isinstance(useful, dict):
        useful_primary = useful.get('primary', '')
        useful_secondary = useful.get('secondary', '')
    elif isinstance(useful, list):
        useful_primary = useful[0] if len(useful) > 0 else ''
        useful_secondary = useful[1] if len(useful) > 1 else ''
    else:
        useful_primary = ''
        useful_secondary = ''
    
    strength = bazi_profile.get("strength", "Unknown")
    profile_name = bazi_profile.get("profile", "")
    ten_god = bazi_profile.get("ten_god_profile", {})
    
    prompt = f"""Analyze this QMDJ chart for {purpose.lower()}:

**CHART DATA**
- Date/Time: {chart_datetime.strftime('%Y-%m-%d %H:%M')} ({timezone})
- Structure: {structure}, Ju {ju_number}
- Method: Chai Bu

**PALACE: {palace_name} {palace_info.get('chinese', '')} ({palace_info.get('direction', '')}, Palace {palace_num}, {palace_element})**

| Component | Value | Element | Strength |
|-----------|-------|---------|----------|
| Heaven Stem | {heaven.get('chinese', '')} | {heaven.get('element', '')} | {heaven.get('strength', '')} ({heaven.get('score', 0):+d}) |
| Earth Stem | {earth.get('chinese', '')} | {earth.get('element', '')} | {earth.get('strength', '')} ({earth.get('score', 0):+d}) |
| Door | {door.get('name', '')} {door.get('chinese', '')} | {door.get('element', '')} | {door.get('strength', '')} ({door.get('score', 0):+d}) |
| Star | {star.get('name', '')} {star.get('chinese', '')} | {star.get('element', '')} | {star.get('strength', '')} ({star.get('score', 0):+d}) |
| Deity | {deity.get('name', '')} {deity.get('chinese', '')} | — | {deity.get('nature', '')} |

"""

    if formation:
        prompt += f"""**FORMATION DETECTED**
- Name: {formation.get('name', '')} ({formation.get('chinese', '')})
- Category: {formation.get('category', '')}
- Source: Book {formation.get('source', '')}

"""
    
    prompt += f"""**MY BAZI PROFILE**
- Day Master: {dm_chinese} {dm_pinyin} {dm_element} ({dm_polarity}) - {strength}
- Useful Gods: {useful_primary} (primary), {useful_secondary} (secondary)
- Profile: {profile_name}

**REQUEST**
Provide complete analysis with:
1. Executive Verdict (1-10 score with interpretation)
2. Formation interpretation (if detected)
3. BaZi alignment assessment
4. 3 Strategic Actions prioritized by impact
5. Optimal timing recommendations
6. Potential obstacles and mitigations
"""

    return prompt


def generate_json_export(
    chart_datetime: datetime,
    timezone: str,
    structure: str,
    ju_number: int,
    palace_data: Dict[str, Any],
    palace_name: str,
    formation: Optional[Dict[str, Any]],
    bazi_profile: Dict[str, Any],
    qmdj_score: float,
    bazi_score: float,
    purpose: str = "Forecasting"
) -> Dict[str, Any]:
    """
    Generate full JSON export following Universal Schema v2.0
    """
    palace_num = palace_data.get("palace_number", 0)
    palace_info = PALACE_INFO.get(palace_num, {})
    
    # Get component data
    heaven = palace_data.get("heaven_stem", {})
    earth = palace_data.get("earth_stem", {})
    door = palace_data.get("door", {})
    star = palace_data.get("star", {})
    deity = palace_data.get("deity", {})
    
    # Get BaZi data - handle both old (dict) and new (string/list) formats
    dm_raw = bazi_profile.get("day_master", "Geng")
    if isinstance(dm_raw, dict):
        dm_pinyin = dm_raw.get('pinyin', 'Geng')
        dm_element = dm_raw.get('element', 'Metal')
        dm_polarity = dm_raw.get('polarity', 'Yang')
    else:
        dm_pinyin = dm_raw
        dm_element = bazi_profile.get('element', 'Metal')
        dm_polarity = bazi_profile.get('polarity', 'Yang')
    
    useful_raw = bazi_profile.get("useful_gods", [])
    if isinstance(useful_raw, dict):
        useful_primary = useful_raw.get('primary', '')
        useful_secondary = useful_raw.get('secondary', '')
    elif isinstance(useful_raw, list):
        useful_primary = useful_raw[0] if len(useful_raw) > 0 else ''
        useful_secondary = useful_raw[1] if len(useful_raw) > 1 else ''
    else:
        useful_primary = ''
        useful_secondary = ''
    
    unfav_raw = bazi_profile.get("unfavorable", bazi_profile.get("unfavorable_elements", []))
    if isinstance(unfav_raw, dict):
        unfav_primary = unfav_raw.get('primary', '')
    elif isinstance(unfav_raw, list):
        unfav_primary = unfav_raw[0] if len(unfav_raw) > 0 else ''
    else:
        unfav_primary = ''
    
    profile_name = bazi_profile.get("profile", "")
    special = bazi_profile.get("special_structures", {})
    
    # Calculate combined score and verdict
    combined_score = round((qmdj_score + bazi_score) / 2, 1)
    
    if combined_score >= 8.5:
        verdict = "HIGHLY AUSPICIOUS"
    elif combined_score >= 7.0:
        verdict = "AUSPICIOUS"
    elif combined_score >= 4.5:
        verdict = "NEUTRAL"
    elif combined_score >= 3.0:
        verdict = "INAUSPICIOUS"
    else:
        verdict = "HIGHLY INAUSPICIOUS"
    
    export_data = {
        "schema_version": "2.0",
        "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
        
        "metadata": {
            "date_time": chart_datetime.strftime("%Y-%m-%d %H:%M"),
            "timezone": timezone,
            "method": "Chai Bu",
            "purpose": purpose,
            "analysis_type": "QMDJ_BAZI_INTEGRATED"
        },
        
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": structure,
            "ju_number": ju_number,
            
            "palace_analyzed": {
                "name": palace_name,
                "number": palace_num,
                "direction": palace_info.get("direction", ""),
                "palace_element": palace_data.get("palace_element", "")
            },
            
            "components": {
                "heaven_stem": {
                    "character": heaven.get("chinese", ""),
                    "element": heaven.get("element", ""),
                    "polarity": heaven.get("polarity", ""),
                    "strength_in_palace": heaven.get("strength", ""),
                    "strength_score": heaven.get("score", 0)
                },
                "earth_stem": {
                    "character": earth.get("chinese", ""),
                    "element": earth.get("element", ""),
                    "polarity": earth.get("polarity", ""),
                    "strength_in_palace": earth.get("strength", ""),
                    "strength_score": earth.get("score", 0)
                },
                "door": {
                    "name": door.get("name", ""),
                    "element": door.get("element", ""),
                    "category": door.get("category", ""),
                    "strength_in_palace": door.get("strength", ""),
                    "strength_score": door.get("score", 0)
                },
                "star": {
                    "name": star.get("name", ""),
                    "element": star.get("element", ""),
                    "category": star.get("category", ""),
                    "strength_in_palace": star.get("strength", ""),
                    "strength_score": star.get("score", 0)
                },
                "deity": {
                    "name": deity.get("name", ""),
                    "nature": deity.get("nature", ""),
                    "function": f"{deity.get('name', '')} deity influence"
                }
            },
            
            "formation": {
                "primary_formation": {
                    "name": formation.get("name", "None detected") if formation else "None detected",
                    "category": formation.get("category", "Neutral") if formation else "Neutral",
                    "source_book": formation.get("source", "") if formation else "",
                    "outcome_pattern": formation.get("description", "") if formation else ""
                },
                "secondary_formations": []
            }
        },
        
        "bazi_data": {
            "chart_source": "User Memory",
            
            "day_master": {
                "stem": dm_pinyin,
                "element": dm_element,
                "polarity": dm_polarity,
                "strength": bazi_profile.get("strength", ""),
                "strength_score": bazi_profile.get("strength_score", 5)
            },
            
            "useful_gods": {
                "primary": useful_primary,
                "secondary": useful_secondary,
                "reasoning": ""
            },
            
            "unfavorable_elements": {
                "primary": unfav_primary,
                "reasoning": ""
            },
            
            "ten_god_profile": {
                "dominant_god": "",
                "profile_name": profile_name,
                "behavioral_traits": []
            },
            
            "special_structures": {
                "wealth_vault": special.get("wealth_vault", False),
                "nobleman_present": special.get("nobleman", False),
                "other_structures": special.get("other", [])
            }
        },
        
        "synthesis": {
            "qmdj_score": {
                "component_total": heaven.get("score", 0) + earth.get("score", 0) + door.get("score", 0) + star.get("score", 0),
                "formation_modifier": 2 if formation and formation.get("category") == "Auspicious" else (-2 if formation and formation.get("category") == "Inauspicious" else 0),
                "final_qmdj_score": qmdj_score
            },
            "bazi_alignment_score": {
                "useful_god_activation": 0,
                "dm_support": 0,
                "profile_alignment": 0,
                "clash_penalty": 0,
                "final_bazi_score": bazi_score
            },
            "combined_verdict_score": combined_score,
            "verdict": verdict,
            "confidence": "HIGH" if abs(combined_score - 5) > 2 else "MEDIUM",
            "primary_action": "",
            "timing_recommendation": {
                "optimal_hour": "",
                "avoid_hour": "",
                "source": "#72"
            }
        },
        
        "tracking": {
            "db_row": f"{chart_datetime.strftime('%Y-%m-%d')},{chart_datetime.strftime('%H:%M')},{palace_name},{formation.get('name', '') if formation else ''},{qmdj_score},{bazi_score},{verdict},,PENDING",
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": ""
        }
    }
    
    return export_data


def generate_csv_row(
    chart_datetime: datetime,
    palace_data: Dict[str, Any],
    palace_name: str,
    formation: Optional[Dict[str, Any]],
    qmdj_score: float,
    bazi_score: float,
    purpose: str = "General"
) -> str:
    """Generate a CSV row for manual database append"""
    combined = round((qmdj_score + bazi_score) / 2, 1)
    
    if combined >= 8.5:
        verdict = "HIGHLY_AUSPICIOUS"
    elif combined >= 7.0:
        verdict = "AUSPICIOUS"
    elif combined >= 4.5:
        verdict = "NEUTRAL"
    elif combined >= 3.0:
        verdict = "INAUSPICIOUS"
    else:
        verdict = "HIGHLY_INAUSPICIOUS"
    
    formation_name = formation.get("name", "") if formation else ""
    
    row_data = [
        chart_datetime.strftime("%Y-%m-%d"),
        chart_datetime.strftime("%H:%M"),
        palace_name,
        formation_name,
        str(qmdj_score),
        str(bazi_score),
        verdict,
        purpose,
        "PENDING"
    ]
    
    return ",".join(row_data)


def format_compact_summary(
    palace_data: Dict[str, Any],
    palace_name: str,
    qmdj_score: float,
    formation: Optional[Dict[str, Any]]
) -> str:
    """Generate a compact one-line summary"""
    formation_str = f" | {formation.get('name', '')}" if formation else ""
    score_emoji = "🌟" if qmdj_score >= 7 else "⚡" if qmdj_score >= 4.5 else "⚠️"
    
    return f"{palace_name} | {palace_data.get('door', {}).get('name', '')} Door | {score_emoji} {qmdj_score}/10{formation_str}"
