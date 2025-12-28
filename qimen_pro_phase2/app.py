"""
🌟 Qi Men Pro v2.0
QMDJ + BaZi Integrated Analysis System

Main Dashboard
"""

import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import APP_TITLE, COLORS, ELEMENT_EMOJI, PALACE_INFO, LUO_SHU_GRID
from utils.bazi_profile import load_profile, DAY_MASTERS, TEN_GOD_PROFILES
from utils.database import get_recent_records, get_statistics, init_database
from utils.calculations import generate_chart
from utils.language import get_lang

# Page configuration
st.set_page_config(
    page_title="Qi Men Pro v2.0",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Additional inline styles for dark theme
    st.markdown("""
    <style>
        .stApp {
            background-color: #1a1a2e;
        }
        .main .block-container {
            padding-top: 2rem;
        }
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
        [data-testid="stSidebar"] .stRadio label span {
            color: #e0e0e0 !important;
        }
        h1, h2, h3 {
            color: #d4af37 !important;
        }
        .stMetric label {
            color: #b8b8b8 !important;
        }
        .stMetric [data-testid="stMetricValue"] {
            color: #d4af37 !important;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize database
init_database()

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = load_profile()
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None
if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = None
if 'lang_mode' not in st.session_state:
    st.session_state.lang_mode = "mixed"

# Initialize language helper
L = get_lang(st.session_state.lang_mode)

def get_element_color(element: str) -> str:
    """Get color for an element"""
    colors = {
        "Wood": "#4CAF50",
        "Fire": "#F44336",
        "Earth": "#8D6E63",
        "Metal": "#BDBDBD",
        "Water": "#2196F3"
    }
    return colors.get(element, "#ffffff")

def render_profile_card():
    """Render the BaZi profile summary card"""
    profile = st.session_state.profile
    
    # Handle both old (dict) and new (string) day_master formats
    dm = profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        # Old format
        chinese = dm.get("chinese", "庚")
        pinyin = dm.get("pinyin", "Geng")
        element = dm.get("element", "Metal")
        polarity = dm.get("polarity", "Yang")
    else:
        # New format - day_master is a string
        pinyin = dm
        chinese = profile.get("chinese", "庚")
        element = profile.get("element", "Metal")
        polarity = profile.get("polarity", "Yang")
    
    # Handle both old (dict) and new (list) useful_gods formats
    useful = profile.get("useful_gods", ["Earth", "Metal"])
    if isinstance(useful, dict):
        primary_ug = useful.get("primary", "Earth")
        secondary_ug = useful.get("secondary", "Metal")
    elif isinstance(useful, list) and len(useful) >= 2:
        primary_ug = useful[0]
        secondary_ug = useful[1]
    elif isinstance(useful, list) and len(useful) == 1:
        primary_ug = useful[0]
        secondary_ug = useful[0]
    else:
        primary_ug = "Earth"
        secondary_ug = "Metal"
    
    special = profile.get("special_structures", {})
    profile_name = profile.get("profile", "Pioneer (Indirect Wealth)")
    profile_emoji = profile.get("profile_emoji", "🎯")
    strength = profile.get("strength", "Weak")
    
    element_color = get_element_color(element)
    
    # Get mixed language strings
    strength_text = L.get("strength") if st.session_state.lang_mode == "mixed" else "Strength"
    useful_text = L.get("useful_god") if st.session_state.lang_mode == "mixed" else "Useful Gods"
    profile_text = L.get("profile") if st.session_state.lang_mode == "mixed" else "Profile"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.08) 0%, transparent 100%); 
                border: 1px solid rgba(212, 175, 55, 0.25); 
                border-radius: 12px; 
                padding: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2.5rem;">{chinese}</span>
            <div>
                <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600;">
                    {pinyin} {L.element(element)} ({L.get('yang') if polarity == 'Yang' else L.get('yin')})
                </div>
                <div style="color: #b8b8b8; font-size: 0.9rem;">
                    {strength_text}: {L.strength(strength)}
                </div>
            </div>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
            <span style="font-size: 0.85rem; color: #b8b8b8;">{useful_text}:</span>
            <span style="background: {get_element_color(primary_ug)}22; 
                        color: {get_element_color(primary_ug)}; 
                        padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;">
                {ELEMENT_EMOJI.get(primary_ug, '')} {L.element(primary_ug)}
            </span>
            <span style="background: {get_element_color(secondary_ug)}22; 
                        color: {get_element_color(secondary_ug)}; 
                        padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;">
                {ELEMENT_EMOJI.get(secondary_ug, '')} {L.element(secondary_ug)}
            </span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 0.85rem; color: #b8b8b8;">{profile_text}:</span>
            <span style="color: #d4af37; font-weight: 500;">
                {profile_emoji} {profile_name}
            </span>
        </div>
        {"<div style='margin-top: 0.5rem;'><span style='background: rgba(212, 175, 55, 0.2); color: #d4af37; padding: 2px 8px; border-radius: 8px; font-size: 0.75rem;'>💰 " + L.get('wealth_vault') + "</span></div>" if special.get('wealth_vault') else ""}
    </div>
    """, unsafe_allow_html=True)

def render_quick_chart():
    """Render quick chart generation section"""
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.date_input(
            f"📅 {L.get('date')}",
            value=datetime.now().date(),
            key="quick_date"
        )
    
    with col2:
        selected_time = st.time_input(
            f"🕐 {L.get('time')}",
            value=datetime.now().time(),
            key="quick_time"
        )
    
    if st.button(f"🔮 {L.get('generate')}", use_container_width=True, type="primary"):
        chart_dt = datetime.combine(selected_date, selected_time)
        st.session_state.current_chart = generate_chart(chart_dt)
        st.session_state.selected_palace = None
        st.success("Chart generated! Go to Chart page for full view.")
        
def render_recent_analyses():
    """Render recent analyses section"""
    records = get_recent_records(5)
    
    if not records:
        st.info("No analyses yet. Generate your first chart to get started!")
        return
    
    for record in records:
        score = record.get('combined_score', 5.0)
        if score >= 7:
            score_color = "#4CAF50"
            score_emoji = "🌟"
        elif score >= 4.5:
            score_color = "#FFC107"
            score_emoji = "⚡"
        else:
            score_color = "#F44336"
            score_emoji = "⚠️"
        
        outcome = record.get('outcome', 'PENDING')
        outcome_badge = {
            'PENDING': '⏳',
            'SUCCESS': '✅',
            'PARTIAL': '🔶',
            'FAILURE': '❌'
        }.get(outcome, '⏳')
        
        formation = record.get('formation', '')
        formation_text = f" | {formation}" if formation else ""
        
        st.markdown(f"""
        <div style="background-color: #16213e; border: 1px solid #2a3f5f; border-radius: 8px; 
                    padding: 0.75rem 1rem; margin-bottom: 0.5rem; 
                    display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #b8b8b8; font-size: 0.85rem;">
                    {record.get('date', '')} {record.get('time', '')}
                </span>
                <span style="color: #ffffff; margin-left: 0.5rem;">
                    {record.get('palace_name', '')}{formation_text}
                </span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: {score_color}; font-weight: 600;">
                    {score_emoji} {score}
                </span>
                <span>{outcome_badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_stats_overview():
    """Render statistics overview"""
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(L.get("total_analyses"), stats['total_records'])
    
    with col2:
        st.metric(L.get("success_rate"), f"{stats['success_rate']}%")
    
    with col3:
        st.metric(L.get("pending_count"), stats['pending_count'])
    
    with col4:
        completed = stats['success_count'] + stats['partial_count'] + stats['failure_count']
        st.metric(L.get("completed"), completed)

# Main App Layout
def main():
    # Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h1 style="margin: 0; color: #d4af37;">{APP_TITLE}</h1>
        <div style="color: #b8b8b8; font-size: 0.9rem;">
            {datetime.now().strftime('%A, %B %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        # Quick Chart Section
        st.markdown(f"""
        <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
            ⚡ {L.get('quick_chart')}
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            render_quick_chart()
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # BaZi Profile Section
        st.markdown(f"""
        <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
            👤 {L.get('bazi_profile')}
        </div>
        """, unsafe_allow_html=True)
        
        render_profile_card()
        
        if st.button(f"✏️ {L.get('settings')}", key="edit_profile_btn"):
            st.switch_page("pages/4_Settings.py")
    
    with col_right:
        # Stats Overview
        st.markdown(f"""
        <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
            📊 {L.get('stats_overview')}
        </div>
        """, unsafe_allow_html=True)
        
        render_stats_overview()
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Recent Analyses
        st.markdown(f"""
        <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem;">
            📈 {L.get('recent_analyses')}
        </div>
        """, unsafe_allow_html=True)
        
        render_recent_analyses()
        
        if st.button(f"{L.get('history')} →", key="view_history_btn"):
            st.switch_page("pages/3_History.py")
    
    # Footer navigation hint
    st.markdown(f"""
    <div style="margin-top: 2rem; padding: 1rem; background: #16213e; border-radius: 10px; 
                border: 1px solid #2a3f5f; text-align: center;">
        <div style="color: #b8b8b8; font-size: 0.9rem;">
            Use the sidebar to navigate: 
            <span style="color: #d4af37;">📊 {L.get('chart_generator')}</span> • 
            <span style="color: #d4af37;">📤 {L.get('export')}</span> • 
            <span style="color: #d4af37;">📈 {L.get('history')}</span> • 
            <span style="color: #d4af37;">⚙️ {L.get('settings')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
