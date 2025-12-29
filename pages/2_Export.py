"""
Ming Qimen 明奇门 - Export Page v2.0
Enhanced: Full schema alignment, clipboard copy, validation, strength calculation, DB_ROW generation
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json
import csv
import io

st.set_page_config(
    page_title="Export | Ming Qimen",
    page_icon="📤",
    layout="wide"
)

# Singapore timezone
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# ============ CONSTANTS ============
ELEMENT_PRODUCES = {
    'Water': 'Wood', 'Wood': 'Fire', 'Fire': 'Earth',
    'Earth': 'Metal', 'Metal': 'Water'
}

ELEMENT_CONTROLS = {
    'Water': 'Fire', 'Fire': 'Metal', 'Metal': 'Wood',
    'Wood': 'Earth', 'Earth': 'Water'
}

STEM_ELEMENTS = {
    'Jia': ('Wood', 'Yang'), '甲': ('Wood', 'Yang'),
    'Yi': ('Wood', 'Yin'), '乙': ('Wood', 'Yin'),
    'Bing': ('Fire', 'Yang'), '丙': ('Fire', 'Yang'),
    'Ding': ('Fire', 'Yin'), '丁': ('Fire', 'Yin'),
    'Wu': ('Earth', 'Yang'), '戊': ('Earth', 'Yang'),
    'Ji': ('Earth', 'Yin'), '己': ('Earth', 'Yin'),
    'Geng': ('Metal', 'Yang'), '庚': ('Metal', 'Yang'),
    'Xin': ('Metal', 'Yin'), '辛': ('Metal', 'Yin'),
    'Ren': ('Water', 'Yang'), '壬': ('Water', 'Yang'),
    'Gui': ('Water', 'Yin'), '癸': ('Water', 'Yin')
}

DOOR_ELEMENTS = {
    'Open': 'Metal', 'Rest': 'Water', 'Life': 'Earth',
    'Harm': 'Earth', 'Delusion': 'Fire', 'Fear': 'Water',
    'Death': 'Earth', 'Scenery': 'Fire',
    '开': 'Metal', '休': 'Water', '生': 'Earth',
    '伤': 'Earth', '杜': 'Fire', '景': 'Fire',
    '死': 'Earth', '惊': 'Metal'
}

STAR_ELEMENTS = {
    'Canopy': 'Wood', 'Grass': 'Wood', 'Connect': 'Earth',
    'Assistant': 'Earth', 'Heart': 'Fire', 'Pillar': 'Earth',
    'Impulse': 'Metal', 'Hero': 'Metal', 'Ren': 'Earth',
    '天蓬': 'Water', '天芮': 'Earth', '天冲': 'Wood',
    '天辅': 'Wood', '天禽': 'Earth', '天心': 'Metal',
    '天柱': 'Metal', '天任': 'Earth', '天英': 'Fire'
}

DOOR_NATURE = {
    'Open': 'Auspicious', 'Rest': 'Auspicious', 'Life': 'Auspicious',
    'Harm': 'Inauspicious', 'Delusion': 'Neutral', 'Fear': 'Inauspicious',
    'Death': 'Inauspicious', 'Scenery': 'Neutral',
    '开门': 'Auspicious', '休门': 'Auspicious', '生门': 'Auspicious',
    '伤门': 'Inauspicious', '杜门': 'Neutral', '景门': 'Neutral',
    '死门': 'Inauspicious', '惊门': 'Inauspicious'
}

STAR_NATURE = {
    'Canopy': 'Inauspicious', 'Grass': 'Inauspicious', 'Connect': 'Auspicious',
    'Assistant': 'Auspicious', 'Heart': 'Auspicious', 'Pillar': 'Inauspicious',
    'Impulse': 'Neutral', 'Hero': 'Auspicious', 'Ren': 'Auspicious'
}

DEITY_NATURE = {
    'Chief': 'Auspicious', 'Serpent': 'Inauspicious', 'Moon': 'Auspicious',
    'Six Harmony': 'Auspicious', 'Hook': 'Inauspicious', 'Tiger': 'Inauspicious',
    'Emptiness': 'Neutral', 'Nine Earth': 'Auspicious', 'Nine Heaven': 'Auspicious',
    '值符': 'Auspicious', '腾蛇': 'Inauspicious', '太阴': 'Auspicious',
    '六合': 'Auspicious', '勾陈': 'Inauspicious', '白虎': 'Inauspicious',
    '玄武': 'Neutral', '九地': 'Auspicious', '九天': 'Auspicious'
}


# ============ HELPER FUNCTIONS ============

def calculate_strength(component_element, palace_element):
    """
    Calculate component strength based on palace element relationship.
    Returns (strength_status, strength_score)
    
    Based on Integrated_Metaphysics_Constants_v2.md:
    - Timely: +2 (Same element as Palace)
    - Prosperous: +3 (Produced by Palace element)
    - Resting: 0 (Neutral relationship)
    - Confined: -2 (Controlled by Palace element)
    - Dead: -3 (Controlling Palace = exhausted)
    """
    if not component_element or not palace_element:
        return "Unknown", 0
    
    # Same element
    if component_element == palace_element:
        return "Timely", 2
    
    # Palace produces component (component is prosperous)
    if ELEMENT_PRODUCES.get(palace_element) == component_element:
        return "Prosperous", 3
    
    # Palace controls component (component is confined)
    if ELEMENT_CONTROLS.get(palace_element) == component_element:
        return "Confined", -2
    
    # Component controls palace (component exhausts itself = dead)
    if ELEMENT_CONTROLS.get(component_element) == palace_element:
        return "Dead", -3
    
    # Component produces palace (neutral/resting)
    return "Resting", 0


def get_stem_info(stem_char):
    """Extract element and polarity from stem character"""
    if not stem_char:
        return None, None
    
    # Check direct match
    if stem_char in STEM_ELEMENTS:
        return STEM_ELEMENTS[stem_char]
    
    # Check if it's part of a longer string
    for key, value in STEM_ELEMENTS.items():
        if key in stem_char:
            return value
    
    return None, None


def get_door_element(door_name):
    """Extract element from door name"""
    if not door_name:
        return None
    
    if isinstance(door_name, dict):
        door_name = door_name.get('english', door_name.get('chinese', ''))
    
    for key, element in DOOR_ELEMENTS.items():
        if key.lower() in str(door_name).lower():
            return element
    return None


def get_star_element(star_name):
    """Extract element from star name"""
    if not star_name:
        return None
    
    if isinstance(star_name, dict):
        star_name = star_name.get('english', star_name.get('chinese', ''))
    
    for key, element in STAR_ELEMENTS.items():
        if key.lower() in str(star_name).lower():
            return element
    return None


def validate_chart_data(chart):
    """Validate chart has minimum required fields for export"""
    errors = []
    warnings = []
    
    # Critical fields
    if not chart.get('palace', {}).get('number'):
        errors.append("Missing palace number")
    if not chart.get('palace', {}).get('element'):
        errors.append("Missing palace element")
    if not chart.get('components', {}).get('heaven_stem'):
        errors.append("Missing heaven stem")
    if not chart.get('metadata', {}).get('date'):
        errors.append("Missing date")
    
    # Warning fields (nice to have)
    if not chart.get('components', {}).get('door'):
        warnings.append("Missing door component")
    if not chart.get('components', {}).get('star'):
        warnings.append("Missing star component")
    if not chart.get('components', {}).get('deity'):
        warnings.append("Missing deity component")
    if not chart.get('guidance'):
        warnings.append("Missing guidance/verdict")
    
    return errors, warnings


def calculate_qmdj_score(components_data):
    """Calculate QMDJ component score based on strength values"""
    total = 0
    for comp_name, comp_data in components_data.items():
        if isinstance(comp_data, dict) and 'strength_score' in comp_data:
            total += comp_data['strength_score']
    
    # Normalize to 1-10 scale (raw range is -12 to +12)
    normalized = ((total + 12) / 24) * 9 + 1
    return round(max(1, min(10, normalized)), 1)


def calculate_bazi_alignment(chart, user_profile):
    """Calculate BaZi alignment score based on useful gods presence"""
    score = 5.0  # Start neutral
    
    if not user_profile:
        return score, "No BaZi profile provided"
    
    useful_gods = user_profile.get('useful_gods', [])
    unfavorable = user_profile.get('unfavorable', [])
    palace_element = chart.get('palace', {}).get('element', '')
    
    reasoning = []
    
    # Check if palace element is useful
    if palace_element in useful_gods:
        score += 2
        reasoning.append(f"Palace element ({palace_element}) is a Useful God")
    elif palace_element in unfavorable:
        score -= 1.5
        reasoning.append(f"Palace element ({palace_element}) is unfavorable")
    
    # Check components for useful elements
    components = chart.get('components', {})
    
    # Heaven stem check
    hs = components.get('heaven_stem', '')
    hs_element, _ = get_stem_info(hs)
    if hs_element in useful_gods:
        score += 1
        reasoning.append(f"Heaven Stem ({hs_element}) supports Day Master")
    
    # Door check
    door = components.get('door', {})
    door_element = get_door_element(door)
    if door_element in useful_gods:
        score += 1
        reasoning.append(f"Door element ({door_element}) is favorable")
    
    return round(max(1, min(10, score)), 1), "; ".join(reasoning) if reasoning else "Neutral alignment"


def convert_to_universal_schema(chart):
    """
    Convert Ming Qimen chart to Universal Schema v2.0
    Full alignment with Universal_Data_Schema_v2.json spec
    """
    
    # Get user profile if available
    user_profile = st.session_state.get('user_profile', {})
    palace_element = chart.get('palace', {}).get('element', '')
    
    # === BUILD COMPONENTS WITH STRENGTH CALCULATIONS ===
    components = chart.get('components', {})
    
    # Heaven Stem processing
    hs_char = components.get('heaven_stem', '')
    hs_element, hs_polarity = get_stem_info(hs_char)
    hs_strength, hs_score = calculate_strength(hs_element, palace_element)
    
    heaven_stem_data = {
        "character": hs_char,
        "element": hs_element or "Unknown",
        "polarity": hs_polarity or "Unknown",
        "strength_in_palace": hs_strength,
        "strength_score": hs_score
    }
    
    # Earth Stem processing
    es_char = components.get('earth_stem', '')
    es_element, es_polarity = get_stem_info(es_char)
    es_strength, es_score = calculate_strength(es_element, palace_element)
    
    earth_stem_data = {
        "character": es_char,
        "element": es_element or "Unknown",
        "polarity": es_polarity or "Unknown",
        "strength_in_palace": es_strength,
        "strength_score": es_score
    }
    
    # Door processing
    door_raw = components.get('door', {})
    door_name = door_raw.get('english', door_raw.get('chinese', str(door_raw))) if isinstance(door_raw, dict) else str(door_raw)
    door_element = get_door_element(door_raw)
    door_strength, door_score = calculate_strength(door_element, palace_element)
    
    door_data = {
        "name": door_name,
        "chinese": door_raw.get('chinese', '') if isinstance(door_raw, dict) else '',
        "element": door_element or "Unknown",
        "category": door_raw.get('nature', DOOR_NATURE.get(door_name, 'Unknown')) if isinstance(door_raw, dict) else DOOR_NATURE.get(door_name, 'Unknown'),
        "strength_in_palace": door_strength,
        "strength_score": door_score
    }
    
    # Star processing
    star_raw = components.get('star', {})
    star_name = star_raw.get('english', star_raw.get('chinese', str(star_raw))) if isinstance(star_raw, dict) else str(star_raw)
    star_element = get_star_element(star_raw)
    star_strength, star_score = calculate_strength(star_element, palace_element)
    
    star_data = {
        "name": star_name,
        "chinese": star_raw.get('chinese', '') if isinstance(star_raw, dict) else '',
        "element": star_element or "Unknown",
        "category": star_raw.get('nature', STAR_NATURE.get(star_name, 'Unknown')) if isinstance(star_raw, dict) else STAR_NATURE.get(star_name, 'Unknown'),
        "strength_in_palace": star_strength,
        "strength_score": star_score
    }
    
    # Deity processing
    deity_raw = components.get('deity', {})
    deity_name = deity_raw.get('english', deity_raw.get('chinese', str(deity_raw))) if isinstance(deity_raw, dict) else str(deity_raw)
    
    deity_data = {
        "name": deity_name,
        "chinese": deity_raw.get('chinese', '') if isinstance(deity_raw, dict) else '',
        "nature": deity_raw.get('nature', DEITY_NATURE.get(deity_name, 'Unknown')) if isinstance(deity_raw, dict) else DEITY_NATURE.get(deity_name, 'Unknown'),
        "function": deity_raw.get('function', '') if isinstance(deity_raw, dict) else ''
    }
    
    # === CALCULATE SCORES ===
    components_for_scoring = {
        'heaven_stem': heaven_stem_data,
        'earth_stem': earth_stem_data,
        'door': door_data,
        'star': star_data
    }
    
    qmdj_component_total = hs_score + es_score + door_score + star_score
    qmdj_final_score = calculate_qmdj_score(components_for_scoring)
    
    bazi_score, bazi_reasoning = calculate_bazi_alignment(chart, user_profile)
    
    # Combined verdict
    combined_score = round((qmdj_final_score + bazi_score) / 2, 1)
    
    # Determine verdict text
    if combined_score >= 8:
        verdict_text = "HIGHLY AUSPICIOUS"
    elif combined_score >= 6:
        verdict_text = "AUSPICIOUS"
    elif combined_score >= 4:
        verdict_text = "NEUTRAL"
    elif combined_score >= 2:
        verdict_text = "INAUSPICIOUS"
    else:
        verdict_text = "HIGHLY INAUSPICIOUS"
    
    # Override with chart guidance if available
    guidance = chart.get('guidance', {})
    if guidance.get('verdict'):
        verdict_text = guidance.get('verdict')
    
    # === BUILD UNIVERSAL SCHEMA ===
    universal = {
        "schema_version": "2.0",
        "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
        
        "metadata": {
            "date_time": f"{chart.get('metadata', {}).get('date', '')} {chart.get('metadata', {}).get('time', '')}".strip(),
            "timezone": "SGT (UTC+8)",
            "method": chart.get('metadata', {}).get('method', 'Chai Bu'),
            "purpose": chart.get('palace', {}).get('topic', 'Forecasting'),
            "analysis_type": "QMDJ_BAZI_INTEGRATED" if user_profile else "QMDJ_ONLY",
            "generated_by": "Ming Qimen 明奇门 v2.0",
            "chinese_hour": chart.get('metadata', {}).get('chinese_hour', '')
        },
        
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": chart.get('metadata', {}).get('structure', ''),
            "ju_number": chart.get('metadata', {}).get('ju_number', 0),
            
            "palace_analyzed": {
                "name": chart.get('palace', {}).get('name', ''),
                "number": chart.get('palace', {}).get('number', 0),
                "direction": chart.get('palace', {}).get('direction', ''),
                "palace_element": palace_element,
                "topic": chart.get('palace', {}).get('topic', '')
            },
            
            "components": {
                "heaven_stem": heaven_stem_data,
                "earth_stem": earth_stem_data,
                "door": door_data,
                "star": star_data,
                "deity": deity_data
            },
            
            "formation": {
                "primary_formation": {
                    "name": chart.get('formation', {}).get('name', 'Not Identified'),
                    "category": chart.get('formation', {}).get('category', 'Unknown'),
                    "source_book": chart.get('formation', {}).get('source', ''),
                    "outcome_pattern": chart.get('formation', {}).get('outcome', '')
                },
                "secondary_formations": chart.get('formation', {}).get('secondary', [])
            },
            
            "host_guest_analysis": {
                "host_element": chart.get('host_guest', {}).get('host', ''),
                "guest_element": chart.get('host_guest', {}).get('guest', ''),
                "relationship": chart.get('host_guest', {}).get('relationship', ''),
                "advantage": chart.get('host_guest', {}).get('advantage', ''),
                "source": "#71 Sun Tzu"
            }
        },
        
        "bazi_data": {
            "chart_source": "User Profile" if user_profile else "Not Provided",
            
            "day_master": {
                "stem": user_profile.get('day_master', 'Unknown'),
                "element": user_profile.get('element', 'Unknown'),
                "polarity": user_profile.get('polarity', 'Unknown'),
                "strength": user_profile.get('strength', 'Unknown'),
                "strength_score": user_profile.get('strength_score', 5)
            },
            
            "useful_gods": {
                "primary": user_profile.get('useful_gods', ['Unknown'])[0] if user_profile.get('useful_gods') else 'Unknown',
                "secondary": user_profile.get('useful_gods', ['Unknown', 'Unknown'])[1] if len(user_profile.get('useful_gods', [])) > 1 else 'Unknown',
                "reasoning": user_profile.get('useful_gods_reasoning', '')
            },
            
            "unfavorable_elements": {
                "primary": user_profile.get('unfavorable', ['Unknown'])[0] if user_profile.get('unfavorable') else 'Unknown',
                "reasoning": user_profile.get('unfavorable_reasoning', '')
            },
            
            "ten_god_profile": {
                "dominant_god": user_profile.get('dominant_god', 'Unknown'),
                "profile_name": user_profile.get('profile', 'Unknown'),
                "behavioral_traits": user_profile.get('traits', [])
            },
            
            "special_structures": {
                "wealth_vault": user_profile.get('wealth_vault', False),
                "nobleman_present": user_profile.get('nobleman', False),
                "other_structures": user_profile.get('structures', [])
            }
        },
        
        "synthesis": {
            "qmdj_score": {
                "component_total": qmdj_component_total,
                "formation_modifier": 0,
                "final_qmdj_score": qmdj_final_score
            },
            "bazi_alignment_score": {
                "useful_god_activation": 0,
                "dm_support": 0,
                "profile_alignment": 0,
                "clash_penalty": 0,
                "final_bazi_score": bazi_score,
                "reasoning": bazi_reasoning
            },
            "combined_verdict_score": combined_score,
            "verdict": verdict_text,
            "confidence": "HIGH" if combined_score >= 7 or combined_score <= 3 else "MEDIUM",
            "primary_action": guidance.get('advice', ''),
            "summary": guidance.get('summary', ''),
            "timing_recommendation": {
                "optimal_hour": chart.get('timing', {}).get('optimal', ''),
                "avoid_hour": chart.get('timing', {}).get('avoid', ''),
                "source": "#72"
            }
        },
        
        "tracking": {
            "generated_at": get_singapore_time().isoformat(),
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": ""
        }
    }
    
    return universal


def generate_db_row(chart, universal):
    """Generate single-line CSV for ML tracking feedback loop"""
    metadata = chart.get('metadata', {})
    palace = chart.get('palace', {})
    synthesis = universal.get('synthesis', {})
    formation = universal.get('qmdj_data', {}).get('formation', {}).get('primary_formation', {})
    
    # Clean primary action for CSV (replace quotes with single quotes)
    primary_action = synthesis.get('primary_action', '').replace('"', "'")
    
    row = (
        f"{metadata.get('date', '')},"
        f"{metadata.get('time', '')},"
        f"{palace.get('name', '')},"
        f"{formation.get('name', 'N/A')},"
        f"{synthesis.get('qmdj_score', {}).get('final_qmdj_score', 'N/A')},"
        f"{synthesis.get('bazi_alignment_score', {}).get('final_bazi_score', 'N/A')},"
        f"{synthesis.get('verdict', '')},"
        f'"{primary_action}",'
        f"PENDING"
    )
    return row


def generate_db_row_header():
    """Generate CSV header for tracking"""
    return "Date,Time,Palace,Formation,QMDJ_Score,BaZi_Score,Verdict,Primary_Action,Outcome"


# ============ LOAD CSS ============
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============ PAGE CONTENT ============
st.title("📤 Export 导出")
st.markdown("Export your readings for Project 1 (AI Analyst) integration")

# Initialize export tracking
if 'export_history' not in st.session_state:
    st.session_state.export_history = []

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Current Reading", "📚 History Export", "⚙️ Settings", "❓ How to Use"])

# ============ TAB 1: CURRENT CHART ============
with tab1:
    st.markdown("### 📊 Current Reading Data")
    
    if 'current_chart' in st.session_state and st.session_state.current_chart:
        chart = st.session_state.current_chart
        
        # === VALIDATION ===
        errors, warnings = validate_chart_data(chart)
        
        if errors:
            st.error(f"❌ **Data Issues:** {', '.join(errors)}")
            st.warning("Some required fields are missing. Export may be incomplete.")
        
        if warnings:
            with st.expander("⚠️ Optional fields missing (click to expand)"):
                for w in warnings:
                    st.caption(f"• {w}")
        
        # === DISPLAY SUMMARY ===
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Reading Summary")
            
            if 'palace' in chart:
                palace = chart['palace']
                st.markdown(f"**Topic:** {palace.get('icon', '')} {palace.get('topic', 'N/A')}")
                st.markdown(f"**Palace:** #{palace.get('number', 'N/A')} {palace.get('name', '')}")
                st.markdown(f"**Direction:** {palace.get('direction', 'N/A')}")
                st.markdown(f"**Element:** {palace.get('element', 'N/A')}")
            
            if 'metadata' in chart:
                meta = chart['metadata']
                st.markdown(f"**Date:** {meta.get('date', 'N/A')}")
                st.markdown(f"**Time:** {meta.get('time', 'N/A')} (SGT)")
                st.markdown(f"**Chinese Hour:** {meta.get('chinese_hour', 'N/A')}")
                if meta.get('structure'):
                    st.markdown(f"**Structure:** {meta.get('structure')} Ju {meta.get('ju_number', '')}")
        
        with col2:
            st.markdown("#### Guidance")
            
            if 'guidance' in chart:
                guidance = chart['guidance']
                verdict = guidance.get('verdict', 'N/A')
                summary = guidance.get('summary', '')
                advice = guidance.get('advice', '')
                
                if guidance.get('type') == 'success':
                    st.success(f"**{verdict}**")
                elif guidance.get('type') == 'warning':
                    st.warning(f"**{verdict}**")
                else:
                    st.info(f"**{verdict}**")
                
                st.markdown(f"*{summary}*")
                st.markdown(f"💡 {advice}")
            
            elif 'verdict' in chart:
                verdict = chart['verdict']
                st.markdown(f"**Verdict:** {verdict.get('text', 'N/A')}")
        
        st.markdown("---")
        
        # === COMPONENTS WITH STRENGTH ===
        st.markdown("#### Components & Strength Analysis")
        
        if 'components' in chart:
            comp = chart['components']
            palace_element = chart.get('palace', {}).get('element', '')
            
            comp_cols = st.columns(5)
            
            with comp_cols[0]:
                st.markdown("**Heaven Stem**")
                hs = comp.get('heaven_stem', 'N/A')
                hs_element, _ = get_stem_info(hs)
                hs_strength, hs_score = calculate_strength(hs_element, palace_element)
                st.markdown(f"{hs}")
                if hs_element:
                    color = "#4CAF50" if hs_score > 0 else "#F44336" if hs_score < 0 else "#9E9E9E"
                    st.markdown(f"<span style='color:{color}'>{hs_element} • {hs_strength} ({hs_score:+d})</span>", unsafe_allow_html=True)
            
            with comp_cols[1]:
                st.markdown("**Earth Stem**")
                es = comp.get('earth_stem', 'N/A')
                es_element, _ = get_stem_info(es)
                es_strength, es_score = calculate_strength(es_element, palace_element)
                st.markdown(f"{es}")
                if es_element:
                    color = "#4CAF50" if es_score > 0 else "#F44336" if es_score < 0 else "#9E9E9E"
                    st.markdown(f"<span style='color:{color}'>{es_element} • {es_strength} ({es_score:+d})</span>", unsafe_allow_html=True)
            
            with comp_cols[2]:
                if 'star' in comp:
                    star = comp['star']
                    st.markdown("**Star**")
                    if isinstance(star, dict):
                        star_name = star.get('english', star.get('chinese', ''))
                        st.markdown(f"{star.get('chinese', '')} {star.get('english', '')}")
                        st.caption(star.get('nature', ''))
                    else:
                        star_name = str(star)
                        st.markdown(star_name)
                    
                    star_element = get_star_element(star)
                    if star_element:
                        star_strength, star_score = calculate_strength(star_element, palace_element)
                        color = "#4CAF50" if star_score > 0 else "#F44336" if star_score < 0 else "#9E9E9E"
                        st.markdown(f"<span style='color:{color}'>{star_element} • {star_strength} ({star_score:+d})</span>", unsafe_allow_html=True)
            
            with comp_cols[3]:
                if 'door' in comp:
                    door = comp['door']
                    st.markdown("**Door**")
                    if isinstance(door, dict):
                        door_name = door.get('english', door.get('chinese', ''))
                        st.markdown(f"{door.get('chinese', '')} {door.get('english', '')}")
                        st.caption(door.get('nature', ''))
                    else:
                        door_name = str(door)
                        st.markdown(door_name)
                    
                    door_element = get_door_element(door)
                    if door_element:
                        door_strength, door_score = calculate_strength(door_element, palace_element)
                        color = "#4CAF50" if door_score > 0 else "#F44336" if door_score < 0 else "#9E9E9E"
                        st.markdown(f"<span style='color:{color}'>{door_element} • {door_strength} ({door_score:+d})</span>", unsafe_allow_html=True)
            
            with comp_cols[4]:
                if 'deity' in comp:
                    deity = comp['deity']
                    st.markdown("**Spirit**")
                    if isinstance(deity, dict):
                        st.markdown(f"{deity.get('chinese', '')} {deity.get('english', '')}")
                        nature = deity.get('nature', '')
                        color = "#4CAF50" if 'Auspicious' in nature else "#F44336" if 'Inauspicious' in nature else "#9E9E9E"
                        st.markdown(f"<span style='color:{color}'>{nature}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(str(deity))
        
        st.markdown("---")
        
        # ============ EXPORT FOR PROJECT 1 ============
        st.markdown("### 🚀 Export for Project 1")
        st.markdown("Copy the JSON below and paste it into Project 1 (AI Analyst)")
        
        # Convert to Universal Schema
        universal_data = convert_to_universal_schema(chart)
        universal_json = json.dumps(universal_data, indent=2, ensure_ascii=False, default=str)
        
        # Score summary
        synthesis = universal_data.get('synthesis', {})
        score_cols = st.columns(4)
        
        with score_cols[0]:
            qmdj_score = synthesis.get('qmdj_score', {}).get('final_qmdj_score', 'N/A')
            st.metric("QMDJ Score", f"{qmdj_score}/10")
        
        with score_cols[1]:
            bazi_score = synthesis.get('bazi_alignment_score', {}).get('final_bazi_score', 'N/A')
            st.metric("BaZi Alignment", f"{bazi_score}/10")
        
        with score_cols[2]:
            combined = synthesis.get('combined_verdict_score', 'N/A')
            st.metric("Combined Score", f"{combined}/10")
        
        with score_cols[3]:
            verdict = synthesis.get('verdict', 'N/A')
            st.metric("Verdict", verdict)
        
        st.markdown("---")
        
        # === COPY OPTIONS ===
        st.markdown("#### 📋 Copy to Clipboard")
        
        # Use st.code for built-in copy button
        st.code(universal_json, language="json")
        
        # Alternative: Text area for manual selection
        with st.expander("📝 Alternative: Manual Copy (Select All → Copy)"):
            st.text_area(
                "Universal Schema JSON",
                value=universal_json,
                height=300,
                help="Click inside, press Ctrl+A (or Cmd+A) to select all, then Ctrl+C (or Cmd+C) to copy",
                key="json_textarea"
            )
        
        st.markdown("---")
        
        # === DOWNLOAD OPTIONS ===
        st.markdown("#### 📥 Download Options")
        
        dl_cols = st.columns(3)
        
        with dl_cols[0]:
            st.download_button(
                "📥 Universal Schema (JSON)",
                data=universal_json,
                file_name=f"ming_qimen_universal_{chart.get('metadata', {}).get('date', 'reading').replace('-', '')}.json",
                mime="application/json",
                use_container_width=True,
                type="primary"
            )
        
        with dl_cols[1]:
            # Raw JSON export
            raw_json = json.dumps(chart, indent=2, ensure_ascii=False, default=str)
            st.download_button(
                "📥 Raw Chart (JSON)",
                data=raw_json,
                file_name=f"ming_qimen_raw_{chart.get('metadata', {}).get('date', 'reading').replace('-', '')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with dl_cols[2]:
            # DB Row for ML tracking
            db_row = generate_db_row(chart, universal_data)
            db_content = generate_db_row_header() + "\n" + db_row
            st.download_button(
                "📥 Tracking Row (CSV)",
                data=db_content,
                file_name=f"ming_qimen_tracking_{chart.get('metadata', {}).get('date', 'reading').replace('-', '')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # === DB ROW PREVIEW ===
        with st.expander("🔍 ML Tracking Row Preview"):
            st.markdown("**CSV Header:**")
            st.code(generate_db_row_header())
            st.markdown("**Data Row:**")
            st.code(db_row)
            st.caption("Append this row to your tracking CSV for ML feedback loop")
        
        # Track this export
        if st.button("✅ Mark as Exported", use_container_width=True):
            st.session_state.export_history.append({
                'timestamp': get_singapore_time().isoformat(),
                'palace': chart.get('palace', {}).get('name', 'Unknown'),
                'topic': chart.get('palace', {}).get('topic', 'Unknown'),
                'verdict': synthesis.get('verdict', 'Unknown'),
                'combined_score': synthesis.get('combined_verdict_score', 0)
            })
            st.success("✅ Export logged to history!")
        
        # === ADVANCED OPTIONS ===
        with st.expander("🔧 Advanced Options"):
            st.markdown("**View Raw Data:**")
            
            view_cols = st.columns(2)
            with view_cols[0]:
                if st.button("👁️ View Raw Chart JSON", use_container_width=True):
                    st.json(chart)
            
            with view_cols[1]:
                if st.button("👁️ View Universal Schema", use_container_width=True):
                    st.json(universal_data)
        
    else:
        st.info("📭 No reading available. Generate a reading from the **Home** or **Chart** page first.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Home", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("📈 Go to Chart", use_container_width=True):
                st.switch_page("pages/1_Chart.py")

# ============ TAB 2: HISTORY EXPORT ============
with tab2:
    st.markdown("### 📚 Export History")
    
    if 'analyses' in st.session_state and st.session_state.analyses:
        analyses = st.session_state.analyses
        
        st.markdown(f"**Total Readings:** {len(analyses)}")
        
        # Show recent history
        st.markdown("#### Recent Readings")
        
        for i, analysis in enumerate(reversed(analyses[-10:])):
            with st.expander(f"📊 {analysis.get('date', 'N/A')} {analysis.get('time', '')} - {analysis.get('topic', analysis.get('palace', 'N/A'))}"):
                st.json(analysis)
        
        st.markdown("---")
        
        # Export all history
        st.markdown("#### Export All History")
        
        export_cols = st.columns(3)
        
        with export_cols[0]:
            # JSON export
            json_str = json.dumps(analyses, indent=2, ensure_ascii=False, default=str)
            st.download_button(
                "📥 History (JSON)",
                data=json_str,
                file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with export_cols[1]:
            # CSV export
            if analyses:
                csv_buffer = io.StringIO()
                
                all_keys = set()
                for a in analyses:
                    all_keys.update(a.keys())
                
                fieldnames = sorted(list(all_keys))
                
                writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
                writer.writeheader()
                for a in analyses:
                    writer.writerow(a)
                
                st.download_button(
                    "📥 History (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with export_cols[2]:
            # Universal Schema batch export
            universal_batch = []
            for a in analyses:
                try:
                    # Attempt to convert each analysis
                    if 'palace' in a or 'components' in a:
                        universal_batch.append(convert_to_universal_schema(a))
                except:
                    pass
            
            if universal_batch:
                batch_json = json.dumps(universal_batch, indent=2, ensure_ascii=False, default=str)
                st.download_button(
                    "📥 History (Universal)",
                    data=batch_json,
                    file_name=f"ming_qimen_universal_batch_{get_singapore_time().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    else:
        st.info("📭 No history available yet. Your readings will appear here after you generate them.")
    
    # Export tracking history
    if st.session_state.export_history:
        st.markdown("---")
        st.markdown("#### Export Tracking Log")
        st.dataframe(st.session_state.export_history, use_container_width=True)

# ============ TAB 3: SETTINGS ============
with tab3:
    st.markdown("### ⚙️ BaZi Profile Settings")
    st.markdown("Configure your personal BaZi profile for integrated analysis")
    
    # Initialize user profile if not exists
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    profile = st.session_state.user_profile
    
    with st.form("bazi_profile_form"):
        st.markdown("#### Day Master Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            day_master = st.selectbox(
                "Day Master Stem",
                options=['', 'Jia 甲', 'Yi 乙', 'Bing 丙', 'Ding 丁', 'Wu 戊', 
                        'Ji 己', 'Geng 庚', 'Xin 辛', 'Ren 壬', 'Gui 癸'],
                index=0 if not profile.get('day_master') else 
                      ['', 'Jia 甲', 'Yi 乙', 'Bing 丙', 'Ding 丁', 'Wu 戊', 
                       'Ji 己', 'Geng 庚', 'Xin 辛', 'Ren 壬', 'Gui 癸'].index(profile.get('day_master', ''))
                      if profile.get('day_master') in ['', 'Jia 甲', 'Yi 乙', 'Bing 丙', 'Ding 丁', 'Wu 戊', 
                       'Ji 己', 'Geng 庚', 'Xin 辛', 'Ren 壬', 'Gui 癸'] else 0
            )
        
        with col2:
            strength = st.selectbox(
                "Day Master Strength",
                options=['', 'Strong', 'Weak', 'Extremely Strong', 'Extremely Weak', 'Balanced'],
                index=0 if not profile.get('strength') else 
                      ['', 'Strong', 'Weak', 'Extremely Strong', 'Extremely Weak', 'Balanced'].index(profile.get('strength', ''))
                      if profile.get('strength') in ['', 'Strong', 'Weak', 'Extremely Strong', 'Extremely Weak', 'Balanced'] else 0
            )
        
        with col3:
            profile_type = st.selectbox(
                "10 God Profile",
                options=['', 'Pioneer (Indirect Wealth)', 'Philosopher (Eating God)', 
                        'Director (Direct Officer)', 'Warrior (7 Killings)', 
                        'Leader (Direct Wealth)', 'Diplomat (Direct Resource)',
                        'Artist (Hurting Officer)', 'Networker (Friend)',
                        'Strategist (Indirect Resource)', 'Competitor (Rob Wealth)'],
                index=0
            )
        
        st.markdown("#### Useful Gods")
        
        ug_col1, ug_col2 = st.columns(2)
        
        with ug_col1:
            useful_gods = st.multiselect(
                "Favorable Elements (Useful Gods)",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('useful_gods', [])
            )
        
        with ug_col2:
            unfavorable = st.multiselect(
                "Unfavorable Elements",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('unfavorable', [])
            )
        
        st.markdown("#### Special Structures")
        
        struct_col1, struct_col2 = st.columns(2)
        
        with struct_col1:
            wealth_vault = st.checkbox("Wealth Vault Present", value=profile.get('wealth_vault', False))
        
        with struct_col2:
            nobleman = st.checkbox("Nobleman Present", value=profile.get('nobleman', False))
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            # Extract element from day master selection
            dm_element = ''
            if day_master:
                dm_parts = day_master.split()
                if dm_parts:
                    dm_name = dm_parts[0]
                    element_info = get_stem_info(dm_name)
                    if element_info[0]:
                        dm_element = element_info[0]
            
            st.session_state.user_profile = {
                'day_master': day_master,
                'element': dm_element,
                'polarity': 'Yang' if day_master and day_master.split()[0] in ['Jia', 'Bing', 'Wu', 'Geng', 'Ren'] else 'Yin',
                'strength': strength,
                'profile': profile_type,
                'useful_gods': useful_gods,
                'unfavorable': unfavorable,
                'wealth_vault': wealth_vault,
                'nobleman': nobleman
            }
            st.success("✅ Profile saved! BaZi data will be included in exports.")
    
    # Display current profile
    if st.session_state.user_profile and st.session_state.user_profile.get('day_master'):
        st.markdown("---")
        st.markdown("#### Current Profile Summary")
        st.json(st.session_state.user_profile)
    
    # Quick preset for Ben's profile
    st.markdown("---")
    with st.expander("🎯 Quick Presets"):
        if st.button("Load Geng Metal Pioneer Profile", use_container_width=True):
            st.session_state.user_profile = {
                'day_master': 'Geng 庚',
                'element': 'Metal',
                'polarity': 'Yang',
                'strength': 'Weak',
                'strength_score': 4,
                'profile': 'Pioneer (Indirect Wealth)',
                'dominant_god': 'Indirect Wealth',
                'useful_gods': ['Earth', 'Metal'],
                'useful_gods_reasoning': 'Earth produces Metal (Resource), Metal supports (Companion)',
                'unfavorable': ['Fire'],
                'unfavorable_reasoning': 'Fire controls Metal excessively for weak DM',
                'wealth_vault': True,
                'nobleman': False,
                'traits': ['Risk-tolerant', 'Opportunity-focused', 'Quick decision-making']
            }
            st.success("✅ Geng Metal Pioneer profile loaded!")
            st.rerun()

# ============ TAB 4: HOW TO USE ============
with tab4:
    st.markdown("### ❓ How to Copy to Project 1")
    
    st.markdown("""
    #### Step-by-Step Guide
    
    **1️⃣ Generate a Reading**
    - Go to Home or Chart page
    - Select your topic and time
    - Click "Get Your Reading"
    
    **2️⃣ Come to Export Page**
    - Click on Export in the sidebar
    - Your reading will be shown here
    
    **3️⃣ Copy the JSON**
    - Find the code block with the Universal Schema JSON
    - Click the **copy icon** in the top-right corner of the code block
    - Or use the text area: Click inside → **Ctrl+A** → **Ctrl+C**
    
    **4️⃣ Paste to Project 1**
    - Open Project 1 (AI Analyst)
    - Paste the JSON data
    - Project 1 will analyze your reading with full QMDJ + BaZi integration!
    
    ---
    
    #### 📋 What Gets Exported? (Universal Schema v2.0)
    
    | Section | Data |
    |---------|------|
    | **Metadata** | Date, time, timezone, method, Chinese hour |
    | **QMDJ Data** | Palace, components with **strength scores**, formations |
    | **BaZi Data** | Day Master, useful gods, profile, special structures |
    | **Synthesis** | QMDJ score, BaZi alignment, combined verdict |
    | **Tracking** | Timestamps for ML feedback loop |
    
    ---
    
    #### 🆕 New in v2.0
    
    - ✅ **Full Schema Alignment** - Matches Universal_Data_Schema_v2.json spec
    - ✅ **Strength Calculations** - Automatic Timely/Prosperous/Confined/Dead scoring
    - ✅ **Component Scores** - Individual strength scores for each component
    - ✅ **BaZi Integration** - Your Day Master profile affects alignment scores
    - ✅ **One-Click Copy** - Use the copy button on the code block
    - ✅ **ML Tracking Row** - CSV format for feedback loop
    - ✅ **Validation** - Warns about missing required fields
    
    ---
    
    #### 💡 Pro Tips
    
    - **Set your BaZi profile** in the Settings tab for integrated scoring
    - **Download** the JSON if you want to save it for later
    - **Tracking Row** CSV is perfect for building your ML dataset
    - **History Export** lets you batch export all past readings
    """)

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Export v2.0 | Singapore Time (UTC+8)")
