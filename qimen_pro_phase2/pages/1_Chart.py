"""
📊 Chart Generator Page
Interactive 9-Palace QMDJ Grid
"""

import streamlit as st
from datetime import datetime, time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PALACE_INFO, LUO_SHU_GRID, ELEMENT_EMOJI, COLORS
from utils.calculations import generate_chart, QMDJChart
from utils.mappings import DOOR_EMOJI, STAR_EMOJI, DEITY_EMOJI
from utils.bazi_profile import load_profile, calculate_bazi_alignment
from utils.database import add_analysis
from utils.language import get_lang

st.set_page_config(
    page_title="Chart Generator - Qi Men Pro",
    page_icon="📊",
    layout="wide"
)

# Custom CSS - Fixed sidebar visibility
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    [data-testid="stSidebar"] { 
        background-color: #16213e; 
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #d4af37 !important;
    }
    [data-testid="stSidebar"] label {
        color: #b8b8b8 !important;
    }
    h1, h2, h3 { color: #d4af37 !important; }
    .palace-card {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border: 2px solid #2a3f5f;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
    .palace-card:hover {
        border-color: #d4af37;
    }
    .palace-selected {
        border-color: #d4af37 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }
    .gold-text { color: #d4af37; }
    .white-text { color: #ffffff; }
    .gray-text { color: #b8b8b8; }
    .score-good { color: #4CAF50; }
    .score-warn { color: #FFC107; }
    .score-bad { color: #F44336; }
    .element-wood { color: #4CAF50; }
    .element-fire { color: #F44336; }
    .element-earth { color: #8D6E63; }
    .element-metal { color: #BDBDBD; }
    .element-water { color: #2196F3; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = load_profile()
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None
if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = None
if 'chart_purpose' not in st.session_state:
    st.session_state.chart_purpose = "General Forecast"
if 'lang_mode' not in st.session_state:
    st.session_state.lang_mode = "mixed"

# Initialize language helper
L = get_lang(st.session_state.lang_mode)

ELEMENT_COLORS = {
    "Wood": "#4CAF50",
    "Fire": "#F44336", 
    "Earth": "#8D6E63",
    "Metal": "#BDBDBD",
    "Water": "#2196F3"
}

def get_score_color(score):
    if score >= 7:
        return "#4CAF50"
    elif score >= 4.5:
        return "#FFC107"
    else:
        return "#F44336"

def render_palace_card(palace_num: int, palace_data: dict, chart: QMDJChart, is_selected: bool = False):
    """Render a palace card using Streamlit components"""
    info = PALACE_INFO[palace_num]
    element = info["element"]
    direction = info["direction"]
    
    heaven = palace_data.get("heaven_stem", {})
    door = palace_data.get("door", {})
    star = palace_data.get("star", {})
    deity = palace_data.get("deity", {})
    
    score = chart.calculate_palace_score(palace_num)
    formation = chart.detect_formation(palace_num)
    
    score_color = get_score_color(score)
    element_color = ELEMENT_COLORS.get(element, "#ffffff")
    border_class = "palace-selected" if is_selected else ""
    
    # Build the palace card content
    direction_display = L.direction(direction)
    element_display = L.element(element)
    
    # Heaven stem
    heaven_chinese = heaven.get('chinese', '')
    heaven_element = heaven.get('element', '')
    
    # Door
    door_name = door.get('name', '')
    door_display = L.door(door_name) if door_name else ''
    door_emoji = DOOR_EMOJI.get(door_name, '')
    
    # Star
    star_name = star.get('name', '')
    star_display = L.star(star_name) if star_name else ''
    star_emoji = STAR_EMOJI.get(star_name, '')
    
    # Deity
    deity_name = deity.get('name', '')
    deity_display = L.deity(deity_name) if deity_name else ''
    deity_emoji = DEITY_EMOJI.get(deity_name, '')
    
    # Formation badge
    formation_html = ""
    if formation:
        f_name = L.formation(formation.get('name', ''))
        f_cat = formation.get('category', 'Neutral')
        f_color = "#4CAF50" if f_cat == "Auspicious" else "#F44336" if f_cat == "Inauspicious" else "#FFC107"
        formation_html = f'<div style="background:{f_color}22; color:{f_color}; padding:2px 8px; border-radius:10px; font-size:0.7rem; margin-top:6px; display:inline-block;">{f_name[:18]}</div>'
    
    st.markdown(f"""
<div class="palace-card {border_class}">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span style="color:#d4af37; font-weight:600;">{direction_display} ({palace_num})</span>
        <span style="color:{element_color};">{ELEMENT_EMOJI.get(element, '')}</span>
        <span style="color:{score_color}; font-weight:600;">⭐ {score}</span>
    </div>
    <div style="color:#fff; font-size:0.8rem; line-height:1.6;">
        <div>{heaven_chinese} {L.element(heaven_element) if heaven_element else ''}</div>
        <div>{door_emoji} {door_display}</div>
        <div>{star_emoji} {star_display}</div>
        <div>{deity_emoji} {deity_display}</div>
    </div>
    {formation_html}
</div>
""", unsafe_allow_html=True)


def render_palace_detail(palace_num: int, palace_data: dict, chart: QMDJChart):
    """Render detailed view of selected palace"""
    info = PALACE_INFO[palace_num]
    profile = st.session_state.profile
    
    score = chart.calculate_palace_score(palace_num)
    formation = chart.detect_formation(palace_num)
    alignment = calculate_bazi_alignment(profile, palace_data)
    
    element = info["element"]
    element_color = ELEMENT_COLORS.get(element, "#ffffff")
    score_color = get_score_color(score)
    
    # Header
    st.markdown(f"### 📍 {L.palace(palace_num)} - {L.direction(info['direction'])}")
    
    # Score metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("QMDJ Score", f"{score}/10")
    with col2:
        st.metric("BaZi Score", f"{alignment['score']}/10")
    with col3:
        combined = round((score + alignment['score']) / 2, 1)
        st.metric("Combined", f"{combined}/10")
    
    # Palace Element
    st.markdown(f"""
<div style="background:#16213e; border:1px solid #2a3f5f; border-radius:8px; padding:12px; margin:12px 0;">
    <span style="color:#b8b8b8;">Palace Element:</span>
    <span style="color:{element_color}; font-weight:600; margin-left:8px;">{ELEMENT_EMOJI.get(element,'')} {L.element(element)}</span>
</div>
""", unsafe_allow_html=True)
    
    # Components table
    st.markdown("#### Components")
    
    components = [
        ("Heaven Stem", palace_data.get("heaven_stem", {})),
        ("Earth Stem", palace_data.get("earth_stem", {})),
        ("Door", palace_data.get("door", {})),
        ("Star", palace_data.get("star", {})),
    ]
    
    for comp_name, comp in components:
        name = comp.get("name", "")
        chinese = comp.get("chinese", "")
        comp_element = comp.get("element", "")
        strength = comp.get("strength", "")
        comp_score = comp.get("strength_score", 0)
        
        if comp_name == "Heaven Stem":
            display = L.stem(name) if name else chinese
        elif comp_name == "Door":
            display = f"{DOOR_EMOJI.get(name, '')} {L.door(name)}" if name else ""
        elif comp_name == "Star":
            display = f"{STAR_EMOJI.get(name, '')} {L.star(name)}" if name else ""
        else:
            display = f"{name} {chinese}"
        
        el_color = ELEMENT_COLORS.get(comp_element, "#ffffff")
        sc_color = "#4CAF50" if comp_score > 0 else "#F44336" if comp_score < 0 else "#FFC107"
        
        st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; background:#16213e; padding:8px 12px; border-radius:6px; margin-bottom:6px; border:1px solid #2a3f5f;">
    <span style="color:#b8b8b8; width:25%;">{comp_name}</span>
    <span style="color:#fff; width:30%;">{display}</span>
    <span style="color:{el_color}; width:20%;">{L.element(comp_element) if comp_element else ''}</span>
    <span style="color:#b8b8b8; width:15%;">{L.strength(strength) if strength else ''}</span>
    <span style="color:{sc_color}; width:10%; text-align:right;">{comp_score:+d}</span>
</div>
""", unsafe_allow_html=True)
    
    # Deity
    deity = palace_data.get("deity", {})
    deity_name = deity.get("name", "")
    deity_nature = deity.get("nature", "Neutral")
    nature_color = "#4CAF50" if deity_nature == "Auspicious" else "#F44336" if deity_nature == "Inauspicious" else "#FFC107"
    
    st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; background:#16213e; padding:8px 12px; border-radius:6px; margin-bottom:12px; border:1px solid #2a3f5f;">
    <span style="color:#b8b8b8; width:25%;">Deity</span>
    <span style="color:#fff; width:50%;">{DEITY_EMOJI.get(deity_name, '')} {L.deity(deity_name)}</span>
    <span style="color:{nature_color}; width:25%; text-align:right;">{deity_nature}</span>
</div>
""", unsafe_allow_html=True)
    
    # Formation
    if formation:
        f_name = L.formation(formation.get('name', ''))
        f_cat = formation.get('category', 'Neutral')
        f_color = "#4CAF50" if f_cat == "Auspicious" else "#F44336" if f_cat == "Inauspicious" else "#FFC107"
        
        st.markdown(f"""
<div style="background:linear-gradient(135deg, rgba(212,175,55,0.1) 0%, rgba(212,175,55,0.05) 100%); border:1px solid rgba(212,175,55,0.3); border-radius:10px; padding:12px; margin:12px 0;">
    <div style="color:#d4af37; font-weight:600; margin-bottom:6px;">🐉 Formation: {f_name}</div>
    <span style="background:{f_color}22; color:{f_color}; padding:2px 10px; border-radius:12px; font-size:0.8rem;">{f_cat}</span>
    <div style="color:#fff; font-size:0.9rem; margin-top:8px;">{formation.get('description', '')}</div>
</div>
""", unsafe_allow_html=True)
    
    # BaZi Alignment
    st.markdown("#### BaZi Alignment")
    dm = profile.get("day_master", "Geng")
    strength = profile.get("strength", "Weak")
    
    st.markdown(f"""
<div style="background:#16213e; border:1px solid #2a3f5f; border-radius:10px; padding:12px;">
    <div style="color:#b8b8b8; margin-bottom:8px;">For {dm} ({strength})</div>
    <div style="color:#4CAF50;">Alignment Score: {alignment['score']}/10</div>
</div>
""", unsafe_allow_html=True)
    
    for detail in alignment.get("details", []):
        st.markdown(f"- {detail}")
    
    # Save button
    st.markdown("---")
    if st.button("💾 Save This Analysis", use_container_width=True):
        record_id = add_analysis(
            chart_datetime=chart.datetime,
            timezone=chart.timezone,
            palace_data=palace_data,
            palace_name=info['name'],
            formation=formation.get('name') if formation else None,
            qmdj_score=score,
            bazi_score=alignment['score'],
            verdict=chart.get_verdict(score),
            purpose=st.session_state.chart_purpose
        )
        st.success(f"✅ Saved! Record ID: {record_id}")


def main():
    st.title("📊 Chart Generator")
    
    # Initialize default values
    if 'default_date' not in st.session_state:
        st.session_state.default_date = datetime.now().date()
    if 'default_time' not in st.session_state:
        st.session_state.default_time = datetime.now().time()
    
    # Sidebar - Input Panel
    with st.sidebar:
        st.markdown("### 📅 Date & Time")
        
        # Quick Select buttons BEFORE widgets
        st.markdown("### ⚡ Quick Select")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Now", use_container_width=True, key="btn_now"):
                st.session_state.default_date = datetime.now().date()
                st.session_state.default_time = datetime.now().time()
                st.rerun()
        with col2:
            if st.button("8 AM", use_container_width=True, key="btn_8am"):
                st.session_state.default_time = time(8, 0)
                st.rerun()
        
        st.markdown("---")
        
        selected_date = st.date_input(
            "Date",
            value=st.session_state.default_date,
            key="input_date"
        )
        
        selected_time = st.time_input(
            "Time",
            value=st.session_state.default_time,
            key="input_time"
        )
        
        timezone = st.selectbox(
            "Timezone",
            ["UTC+8", "UTC+0", "UTC-5", "UTC-8"],
            index=0,
            key="input_tz"
        )
        
        st.markdown("### 🎯 Purpose")
        purpose_options = [
            "General Forecast",
            "Wealth/Business",
            "Relationship",
            "Strategic Decision",
            "Date Selection 择日"
        ]
        purpose = st.radio(
            "Purpose",
            purpose_options,
            key="purpose_select",
            label_visibility="collapsed"
        )
        st.session_state.chart_purpose = purpose
        
        st.markdown("")
        
        if st.button("🔮 GENERATE", use_container_width=True, type="primary"):
            chart_dt = datetime.combine(selected_date, selected_time)
            st.session_state.current_chart = generate_chart(chart_dt, timezone)
            st.session_state.selected_palace = None
            st.rerun()
    
    # Main Area
    if st.session_state.current_chart is None:
        st.info("👈 Configure date/time and click **GENERATE** to begin")
        
        st.markdown("""
<div style="text-align:center; padding:3rem; background:#16213e; border-radius:12px; border:1px dashed #2a3f5f; margin-top:2rem;">
    <div style="font-size:4rem; margin-bottom:1rem;">🔮</div>
    <div style="color:#b8b8b8; font-size:1.1rem;">Your QMDJ Chart will appear here</div>
</div>
""", unsafe_allow_html=True)
        return
    
    chart = st.session_state.current_chart
    
    # Chart Header
    st.markdown(f"""
<div style="background:#16213e; border:1px solid #2a3f5f; border-radius:10px; padding:1rem; margin-bottom:1rem; text-align:center;">
    <div style="color:#d4af37; font-size:1.2rem; font-weight:600;">
        {chart.datetime.strftime('%Y-%m-%d %H:%M')} ({chart.timezone})
    </div>
    <div style="color:#b8b8b8; font-size:0.9rem;">
        {chart.structure} · Ju {chart.ju_number} · Chai Bu Method
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Two column layout: Grid + Detail
    col_grid, col_detail = st.columns([1.2, 1])
    
    with col_grid:
        st.markdown("### 9-Palace Grid")
        st.caption("Click a palace to view details")
        
        # Render grid using Luo Shu order
        for row_idx, row in enumerate(LUO_SHU_GRID):
            cols = st.columns(3)
            for col_idx, palace_num in enumerate(row):
                with cols[col_idx]:
                    palace_data = chart.palaces.get(palace_num, {})
                    is_selected = st.session_state.selected_palace == palace_num
                    
                    render_palace_card(palace_num, palace_data, chart, is_selected)
                    
                    if st.button(
                        "Select", 
                        key=f"palace_{palace_num}",
                        use_container_width=True
                    ):
                        st.session_state.selected_palace = palace_num
                        st.rerun()
    
    with col_detail:
        if st.session_state.selected_palace:
            palace_num = st.session_state.selected_palace
            palace_data = chart.palaces.get(palace_num, {})
            render_palace_detail(palace_num, palace_data, chart)
        else:
            st.markdown("""
<div style="background:#16213e; border:1px dashed #2a3f5f; border-radius:10px; padding:3rem; text-align:center;">
    <div style="font-size:2rem; margin-bottom:0.5rem;">👆</div>
    <div style="color:#b8b8b8;">Select a palace to view detailed breakdown</div>
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
