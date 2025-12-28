"""
🔮 Qi Men Pro v2.0 - Full Version
Comprehensive QMDJ & BaZi Integration System
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from pathlib import Path

# Import configuration
from config import *

# ============================================================================
# INITIALIZATION & SETUP
# ============================================================================

def init_app():
    """Initialize app with page config and session state"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = load_user_profile()
    if 'current_chart' not in st.session_state:
        st.session_state.current_chart = None
    if 'history' not in st.session_state:
        st.session_state.history = load_history()

def apply_custom_css():
    """Apply dark theme with gold accents"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-gold: #FFD700;
        --dark-bg: #1E1E1E;
        --card-bg: #2D2D2D;
    }
    
    /* Streamlit overrides */
    .stApp {
        background-color: var(--dark-bg);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-gold) !important;
    }
    
    /* Cards */
    .element-container {
        background-color: var(--card-bg);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--primary-gold);
        color: black;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            margin: 5px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

def load_user_profile():
    """Load user's BaZi profile"""
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, 'r') as f:
                return json.load(f)
        except:
            return get_default_profile()
    return get_default_profile()

def save_user_profile(profile):
    """Save user's BaZi profile"""
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, 'w') as f:
        json.dump(profile, f, indent=2)
    st.session_state.user_profile = profile

def get_default_profile():
    """Default BaZi profile structure"""
    return {
        "day_master": "Geng",
        "element": "Metal",
        "polarity": "Yang",
        "strength": "Weak",
        "useful_gods": ["Earth", "Metal"],
        "unfavorable": ["Fire"],
        "profile_type": "Pioneer (Indirect Wealth)",
        "special_structures": {
            "wealth_vault": True,
            "nobleman_present": False
        }
    }

def load_history():
    """Load ML tracking database"""
    if os.path.exists(DB_PATH):
        try:
            return pd.read_csv(DB_PATH)
        except:
            return create_empty_history()
    return create_empty_history()

def create_empty_history():
    """Create empty history DataFrame"""
    return pd.DataFrame(columns=[
        'Date', 'Time', 'Palace', 'Formation', 
        'QMDJ_Score', 'BaZi_Score', 'Verdict', 
        'Action', 'Outcome'
    ])

def save_to_history(chart_data):
    """Save chart analysis to ML database"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    new_row = pd.DataFrame([{
        'Date': chart_data['date'],
        'Time': chart_data['time'],
        'Palace': chart_data['palace'],
        'Formation': chart_data['formation'],
        'QMDJ_Score': chart_data['qmdj_score'],
        'BaZi_Score': chart_data['bazi_score'],
        'Verdict': chart_data['verdict'],
        'Action': chart_data['action'],
        'Outcome': 'PENDING'
    }])
    
    history = load_history()
    history = pd.concat([history, new_row], ignore_index=True)
    history.to_csv(DB_PATH, index=False)
    st.session_state.history = history

# ============================================================================
# QMDJ CALCULATION ENGINE (Placeholder)
# ============================================================================

def generate_qmdj_chart(date_str, time_str, palace_num):
    """
    Generate QMDJ chart data
    NOTE: This is a placeholder. Replace with actual kinqimen library calls
    """
    
    # Placeholder data matching Universal Schema v2.0
    chart = {
        "schema_version": "2.0",
        "metadata": {
            "date_time": f"{date_str} {time_str}",
            "timezone": DEFAULT_TIMEZONE,
            "method": "Chai Bu",
            "purpose": "Strategic",
            "analysis_type": "QMDJ_BAZI_INTEGRATED"
        },
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": "Yang Dun",
            "ju_number": 5,
            "palace_analyzed": {
                "name": get_palace_name(palace_num),
                "number": palace_num,
                "direction": get_palace_direction(palace_num),
                "palace_element": get_palace_element(palace_num)
            },
            "components": {
                "heaven_stem": {
                    "character": "Geng",
                    "element": "Metal",
                    "polarity": "Yang",
                    "strength_in_palace": "Prosperous",
                    "strength_score": 2
                },
                "earth_stem": {
                    "character": "Wu",
                    "element": "Earth",
                    "polarity": "Yang",
                    "strength_in_palace": "Timely",
                    "strength_score": 3
                },
                "door": {
                    "name": "Life",
                    "element": "Earth",
                    "category": "Auspicious",
                    "strength_in_palace": "Prosperous",
                    "strength_score": 2
                },
                "star": {
                    "name": "Heart",
                    "element": "Metal",
                    "category": "Auspicious",
                    "strength_in_palace": "Timely",
                    "strength_score": 3
                },
                "deity": {
                    "name": "Chief",
                    "nature": "Auspicious",
                    "function": "Leadership and authority"
                }
            },
            "formation": {
                "primary_formation": {
                    "name": "Flying Dragon in Sky",
                    "category": "Auspicious",
                    "source_book": "#64",
                    "outcome_pattern": "Great success with timing"
                }
            }
        },
        "bazi_data": st.session_state.user_profile,
        "synthesis": calculate_synthesis(palace_num)
    }
    
    return chart

def calculate_synthesis(palace_num):
    """Calculate combined QMDJ + BaZi scores"""
    # Placeholder scoring logic
    qmdj_score = min(10, max(1, 5 + (palace_num % 3)))
    bazi_score = min(10, max(1, 6 + (palace_num % 4)))
    combined = int((qmdj_score + bazi_score) / 2)
    
    verdicts = {
        (8, 10): "HIGHLY AUSPICIOUS",
        (6, 7): "AUSPICIOUS",
        (4, 5): "NEUTRAL",
        (2, 3): "INAUSPICIOUS",
        (1, 1): "HIGHLY INAUSPICIOUS"
    }
    
    verdict = "NEUTRAL"
    for (min_s, max_s), v in verdicts.items():
        if min_s <= combined <= max_s:
            verdict = v
            break
    
    return {
        "qmdj_score": qmdj_score,
        "bazi_alignment_score": bazi_score,
        "combined_verdict_score": combined,
        "verdict": verdict,
        "confidence": "MEDIUM",
        "primary_action": "Proceed with careful planning and timing",
        "timing_recommendation": {
            "optimal_hour": "Wu Hour (11am-1pm)",
            "avoid_hour": "Zi Hour (11pm-1am)"
        }
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_palace_name(num):
    """Convert palace number to name"""
    names = {1: "Kan", 2: "Kun", 3: "Zhen", 4: "Xun", 5: "Center",
             6: "Qian", 7: "Dui", 8: "Gen", 9: "Li"}
    return names.get(num, "Center")

def get_palace_direction(num):
    """Get palace direction"""
    directions = {1: "N", 2: "SW", 3: "E", 4: "SE", 5: "Center",
                  6: "NW", 7: "W", 8: "NE", 9: "S"}
    return directions.get(num, "Center")

def get_palace_element(num):
    """Get palace element"""
    elements = {1: "Water", 2: "Earth", 3: "Wood", 4: "Wood", 5: "Earth",
                6: "Metal", 7: "Metal", 8: "Earth", 9: "Fire"}
    return elements.get(num, "Earth")

def format_chart_for_display(chart):
    """Format chart data for UI display"""
    qmdj = chart['qmdj_data']
    synth = chart['synthesis']
    
    return f"""
    ### 📊 Chart Analysis
    
    **Palace:** {qmdj['palace_analyzed']['name']} ({qmdj['palace_analyzed']['direction']})  
    **Formation:** {qmdj['formation']['primary_formation']['name']}
    
    **Components:**
    - Heaven Stem: {qmdj['components']['heaven_stem']['character']} ({qmdj['components']['heaven_stem']['element']})
    - Door: {qmdj['components']['door']['name']}
    - Star: {qmdj['components']['star']['name']}
    - Deity: {qmdj['components']['deity']['name']}
    
    **Scores:**
    - QMDJ Score: {synth['qmdj_score']}/10
    - BaZi Alignment: {synth['bazi_alignment_score']}/10
    - **Combined Verdict: {synth['verdict']}** ({synth['combined_verdict_score']}/10)
    
    **Recommended Action:** {synth['primary_action']}
    """

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def page_dashboard():
    """Main dashboard page"""
    st.title("🔮 Qi Men Pro Dashboard")
    
    profile = st.session_state.user_profile
    
    # User Profile Card
    with st.container():
        st.subheader("👤 Your BaZi Profile")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Day Master", profile['day_master'])
            st.caption(f"{profile['polarity']} {profile['element']}")
        
        with col2:
            st.metric("Strength", profile['strength'])
            emoji = TEN_GOD_PROFILES.get(profile['profile_type'], {}).get('emoji', '🎯')
            st.caption(f"{emoji} {profile['profile_type']}")
        
        with col3:
            st.metric("Useful Gods", ", ".join(profile['useful_gods']))
            st.caption(f"Avoid: {profile['unfavorable'][0]}")
    
    st.divider()
    
    # Recent Activity
    st.subheader("📈 Recent Activity")
    history = st.session_state.history
    
    if len(history) > 0:
        recent = history.tail(5).sort_values('Date', ascending=False)
        st.dataframe(recent[['Date', 'Palace', 'Verdict', 'Action']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No charts generated yet. Go to Chart Generator to create your first analysis!")
    
    # Quick Stats
    if len(history) > 0:
        st.divider()
        st.subheader("📊 Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Charts", len(history))
        with col2:
            auspicious = len(history[history['Verdict'].str.contains('AUSPICIOUS', na=False)])
            st.metric("Auspicious", auspicious)
        with col3:
            avg_qmdj = history['QMDJ_Score'].mean()
            st.metric("Avg QMDJ Score", f"{avg_qmdj:.1f}")
        with col4:
            avg_bazi = history['BaZi_Score'].mean()
            st.metric("Avg BaZi Score", f"{avg_bazi:.1f}")

# ============================================================================
# PAGE: CHART GENERATOR
# ============================================================================

def page_chart_generator():
    """Chart generation page"""
    st.title("🎯 Chart Generator")
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        date_input = st.date_input("📅 Date", datetime.now())
        date_str = date_input.strftime("%Y-%m-%d")
    
    with col2:
        time_input = st.time_input("⏰ Time", datetime.now())
        time_str = time_input.strftime("%H:%M")
    
    # Palace Selection (9-Grid Visual)
    st.subheader("🎲 Select Palace (1-9)")
    
    # Create 3x3 grid
    palace_grid = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]
    
    cols = st.columns(3)
    selected_palace = None
    
    for row_idx, row in enumerate(palace_grid):
        for col_idx, palace_num in enumerate(row):
            with cols[col_idx]:
                if st.button(f"Palace {palace_num}\n{get_palace_name(palace_num)}", 
                            key=f"palace_{palace_num}",
                            use_container_width=True):
                    selected_palace = palace_num
    
    # Manual input as alternative
    st.divider()
    manual_palace = st.number_input("Or enter palace number directly:", 
                                     min_value=1, max_value=9, value=5)
    
    if selected_palace is None:
        selected_palace = manual_palace
    
    st.info(f"Selected: Palace {selected_palace} - {get_palace_name(selected_palace)}")
    
    # Generate Chart Button
    if st.button("🔮 Generate Chart", type="primary", use_container_width=True):
        with st.spinner("Calculating chart..."):
            chart = generate_qmdj_chart(date_str, time_str, selected_palace)
            st.session_state.current_chart = chart
            
            # Display results
            st.success("Chart generated successfully!")
            st.markdown(format_chart_for_display(chart))
            
            # Save to history
            chart_data = {
                'date': date_str,
                'time': time_str,
                'palace': get_palace_name(selected_palace),
                'formation': chart['qmdj_data']['formation']['primary_formation']['name'],
                'qmdj_score': chart['synthesis']['qmdj_score'],
                'bazi_score': chart['synthesis']['bazi_alignment_score'],
                'verdict': chart['synthesis']['verdict'],
                'action': chart['synthesis']['primary_action']
            }
            save_to_history(chart_data)
            
            # Copy prompt button
            st.divider()
            prompt = f"""Analyze this QMDJ chart for strategic decision-making:

{json.dumps(chart, indent=2)}

Please provide:
1. Detailed interpretation based on Joey Yap methodology
2. Strategic recommendations
3. Timing considerations
4. Risk factors to consider"""
            
            st.text_area("📋 Analysis Prompt (Copy to use with Claude)", 
                        prompt, height=200)

# ============================================================================
# PAGE: EXPORT
# ============================================================================

def page_export():
    """Export page"""
    st.title("📤 Export Data")
    
    if st.session_state.current_chart is None:
        st.warning("⚠️ No chart available. Generate a chart first!")
        return
    
    st.subheader("Current Chart")
    
    # JSON Export
    st.markdown("### 📄 Universal Schema JSON")
    json_str = json.dumps(st.session_state.current_chart, indent=2)
    st.code(json_str, language='json')
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download JSON",
            json_str,
            file_name=f"qmdj_chart_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        if st.button("📋 Copy JSON", use_container_width=True):
            st.code(json_str, language='json')
            st.success("JSON displayed above - select and copy!")
    
    # CSV Export of History
    st.divider()
    st.markdown("### 📊 History Database (CSV)")
    
    if len(st.session_state.history) > 0:
        csv = st.session_state.history.to_csv(index=False)
        st.download_button(
            "⬇️ Download History CSV",
            csv,
            file_name=f"qmdj_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.dataframe(st.session_state.history, use_container_width=True)
    else:
        st.info("No history data yet")

# ============================================================================
# PAGE: HISTORY & ML TRACKING
# ============================================================================

def page_history():
    """History and ML tracking page"""
    st.title("📈 History & ML Tracking")
    
    history = st.session_state.history
    
    if len(history) == 0:
        st.info("No history data yet. Generate some charts to see tracking!")
        return
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        verdict_filter = st.multiselect(
            "Verdict",
            options=history['Verdict'].unique(),
            default=history['Verdict'].unique()
        )
    
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(history['Date'].min(), history['Date'].max())
        )
    
    with col3:
        palace_filter = st.multiselect(
            "Palace",
            options=history['Palace'].unique(),
            default=history['Palace'].unique()
        )
    
    # Apply filters
    filtered = history[
        (history['Verdict'].isin(verdict_filter)) &
        (history['Palace'].isin(palace_filter))
    ]
    
    # Display filtered data
    st.subheader("📋 Records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    
    # Analytics
    st.divider()
    st.subheader("📊 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Verdict Distribution**")
        verdict_counts = filtered['Verdict'].value_counts()
        st.bar_chart(verdict_counts)
    
    with col2:
        st.markdown("**Palace Usage**")
        palace_counts = filtered['Palace'].value_counts()
        st.bar_chart(palace_counts)

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

def page_settings():
    """Settings page for BaZi profile management"""
    st.title("⚙️ Settings")
    
    st.subheader("👤 BaZi Profile Configuration")
    
    profile = st.session_state.user_profile.copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        profile['day_master'] = st.selectbox(
            "Day Master Stem",
            ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"],
            index=["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(profile['day_master'])
        )
        
        profile['element'] = st.selectbox(
            "Element",
            ["Wood", "Fire", "Earth", "Metal", "Water"],
            index=["Wood", "Fire", "Earth", "Metal", "Water"].index(profile['element'])
        )
        
        profile['polarity'] = st.radio("Polarity", ["Yang", "Yin"], 
                                       index=0 if profile['polarity'] == "Yang" else 1)
    
    with col2:
        profile['strength'] = st.selectbox(
            "Strength",
            ["Strong", "Weak", "Extremely Strong", "Extremely Weak", "Balanced"],
            index=["Strong", "Weak", "Extremely Strong", "Extremely Weak", "Balanced"].index(profile['strength'])
        )
        
        profile['useful_gods'] = st.multiselect(
            "Useful Gods",
            ["Wood", "Fire", "Earth", "Metal", "Water"],
            default=profile['useful_gods']
        )
        
        profile['unfavorable'] = st.multiselect(
            "Unfavorable Elements",
            ["Wood", "Fire", "Earth", "Metal", "Water"],
            default=profile['unfavorable']
        )
    
    # Ten God Profile
    st.divider()
    profile['profile_type'] = st.selectbox(
        "Ten God Profile",
        list(TEN_GOD_PROFILES.keys()),
        index=list(TEN_GOD_PROFILES.keys()).index(profile['profile_type']) 
            if profile['profile_type'] in TEN_GOD_PROFILES else 0
    )
    
    emoji = TEN_GOD_PROFILES[profile['profile_type']]['emoji']
    st.info(f"{emoji} {profile['profile_type']}")
    
    # Special Structures
    st.divider()
    st.subheader("Special Structures")
    
    profile['special_structures']['wealth_vault'] = st.checkbox(
        "Wealth Vault Present",
        value=profile['special_structures']['wealth_vault']
    )
    
    profile['special_structures']['nobleman_present'] = st.checkbox(
        "Nobleman Present",
        value=profile['special_structures']['nobleman_present']
    )
    
    # Save Button
    st.divider()
    if st.button("💾 Save Profile", type="primary", use_container_width=True):
        save_user_profile(profile)
        st.success("✅ Profile saved successfully!")
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point"""
    init_app()
    apply_custom_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🔮 Qi Men Pro v2.0")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🎯 Chart Generator", "📤 Export", 
             "📈 History & ML", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.caption(f"Version {APP_VERSION}")
        st.caption(f"Location: {DEFAULT_LOCATION}")
        st.caption(f"Timezone: {DEFAULT_TIMEZONE}")
    
    # Route to selected page
    if page == "📊 Dashboard":
        page_dashboard()
    elif page == "🎯 Chart Generator":
        page_chart_generator()
    elif page == "📤 Export":
        page_export()
    elif page == "📈 History & ML":
        page_history()
    elif page == "⚙️ Settings":
        page_settings()

if __name__ == "__main__":
    main()
