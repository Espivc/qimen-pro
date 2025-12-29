"""
Qi Men Pro v2.0 - Dashboard
Phase 3: Fixed profile sync from Settings
"""

import streamlit as st
from datetime import datetime, time
import json

# Page config
st.set_page_config(
    page_title="奇門 Qi Men Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Initialize session state with DEFAULT profile
# This will be overwritten when user saves from Settings
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "day_master": "庚 Geng",
        "element": "Metal 金",
        "polarity": "Yang",
        "strength": "Weak",
        "useful_gods": ["Earth 土", "Metal 金"],
        "unfavorable": ["Fire 火", "Wood 木"],
        "profile": "Pioneer 🎯 (Indirect Wealth 偏财)"
    }

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

if 'language' not in st.session_state:
    st.session_state.language = "mixed"

# ============ HELPER FUNCTIONS ============

def parse_time_input(time_str):
    """Parse time string in HH:MM format, returns (hour, minute) or None if invalid"""
    try:
        # Clean the input
        time_str = time_str.strip().replace("：", ":").replace(".", ":")
        
        # Try parsing HH:MM format
        if ":" in time_str:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
        else:
            # Try parsing as just hour (e.g., "14" → 14:00)
            hour = int(time_str)
            minute = 0
        
        # Validate
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)
        else:
            return None
    except:
        return None

def get_chinese_hour(hour, minute=0):
    """Convert 24h time to Chinese double-hour (时辰)"""
    total_minutes = hour * 60 + minute
    
    chinese_hours = [
        ("子 Zi", "23:00-00:59", "Rat 🐀"),
        ("丑 Chou", "01:00-02:59", "Ox 🐂"),
        ("寅 Yin", "03:00-04:59", "Tiger 🐅"),
        ("卯 Mao", "05:00-06:59", "Rabbit 🐇"),
        ("辰 Chen", "07:00-08:59", "Dragon 🐉"),
        ("巳 Si", "09:00-10:59", "Snake 🐍"),
        ("午 Wu", "11:00-12:59", "Horse 🐴"),
        ("未 Wei", "13:00-14:59", "Goat 🐐"),
        ("申 Shen", "15:00-16:59", "Monkey 🐒"),
        ("酉 You", "17:00-18:59", "Rooster 🐓"),
        ("戌 Xu", "19:00-20:59", "Dog 🐕"),
        ("亥 Hai", "21:00-22:59", "Pig 🐖"),
    ]
    
    # Special handling for 子时 (spans midnight)
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return chinese_hours[0]
    
    # Find the correct hour
    hour_index = (hour + 1) // 2
    if hour_index >= 12:
        hour_index = 0
    
    return chinese_hours[hour_index]

def get_element_color(element):
    """Return color for element"""
    colors = {
        "Wood": "#228B22", "木": "#228B22",
        "Fire": "#DC143C", "火": "#DC143C",
        "Earth": "#DAA520", "土": "#DAA520",
        "Metal": "#C0C0C0", "金": "#C0C0C0",
        "Water": "#1E90FF", "水": "#1E90FF"
    }
    for key, color in colors.items():
        if key.lower() in str(element).lower():
            return color
    return "#FFFFFF"

def format_profile_display(profile):
    """Format profile data for display, handling different data structures from Settings"""
    
    # Handle day_master - could be "庚 Geng" or just "庚" or dict
    day_master = profile.get('day_master', 'Not Set')
    if isinstance(day_master, dict):
        day_master = day_master.get('stem', 'Not Set')
    
    # Handle element
    element = profile.get('element', '')
    if isinstance(element, dict):
        element = element.get('element', '')
    
    # Handle polarity
    polarity = profile.get('polarity', '')
    
    # Handle strength
    strength = profile.get('strength', '')
    
    # Handle useful_gods - could be list of strings or list with element names
    useful_gods = profile.get('useful_gods', [])
    if isinstance(useful_gods, dict):
        useful_gods = [useful_gods.get('primary', ''), useful_gods.get('secondary', '')]
    if not isinstance(useful_gods, list):
        useful_gods = [str(useful_gods)]
    useful_gods = [g for g in useful_gods if g]
    
    # Handle unfavorable
    unfavorable = profile.get('unfavorable', profile.get('unfavorable_elements', []))
    if isinstance(unfavorable, dict):
        unfavorable = [unfavorable.get('primary', '')]
    if not isinstance(unfavorable, list):
        unfavorable = [str(unfavorable)]
    unfavorable = [u for u in unfavorable if u]
    
    # Handle profile name
    profile_name = profile.get('profile', profile.get('ten_god_profile', {}).get('profile_name', 'Not Set'))
    if isinstance(profile_name, dict):
        profile_name = profile_name.get('profile_name', 'Not Set')
    
    return {
        "day_master": day_master,
        "element": element,
        "polarity": polarity,
        "strength": strength,
        "useful_gods": useful_gods,
        "unfavorable": unfavorable,
        "profile": profile_name
    }

# ============ MAIN DASHBOARD ============

st.title("🔮 奇門遁甲 Qi Men Dun Jia Pro")
st.markdown("**QMDJ + BaZi Integrated Analysis System**")

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    - 📊 **Dashboard** (current)
    - 📈 Chart Generator
    - 📤 Export
    - 📜 History & ML
    - ⚙️ Settings
    """)
    
    st.markdown("---")
    st.markdown("### 📱 Quick Stats")
    total = len(st.session_state.analyses)
    success = len([a for a in st.session_state.analyses if a.get('outcome') == 'SUCCESS'])
    st.metric("Total Analyses", total)
    st.metric("Success Rate", f"{(success/total*100):.0f}%" if total > 0 else "N/A")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚡ Quick Chart 快速起盘")
    
    # Date picker
    selected_date = st.date_input(
        "📅 Select Date 选择日期",
        value=datetime.now().date(),
        help="Choose the date for your QMDJ chart"
    )
    
    # TIME INPUT - Now with text input for precise time!
    st.markdown("#### ⏰ Enter Time 输入时间")
    
    time_col1, time_col2 = st.columns([2, 1])
    
    with time_col1:
        time_input = st.text_input(
            "Time (HH:MM format) 时间",
            value=datetime.now().strftime("%H:%M"),
            placeholder="e.g., 14:30",
            help="Enter time in 24-hour format (HH:MM). Example: 09:15, 14:30, 23:45"
        )
    
    # Parse and validate time
    parsed_time = parse_time_input(time_input)
    
    with time_col2:
        if parsed_time:
            hour, minute = parsed_time
            chinese_hour = get_chinese_hour(hour, minute)
            st.success(f"✅ Valid")
            st.markdown(f"**{chinese_hour[0]}**")
            st.caption(f"{chinese_hour[2]}")
        else:
            st.error("❌ Invalid")
            st.caption("Use HH:MM format")
    
    # Show Chinese hour info
    if parsed_time:
        hour, minute = parsed_time
        chinese_hour = get_chinese_hour(hour, minute)
        st.info(f"🕐 **Chinese Hour 时辰:** {chinese_hour[0]} ({chinese_hour[1]}) - {chinese_hour[2]}")
    
    # Palace selection
    st.markdown("#### 🏛️ Select Palace 选择宫位")
    palace_col1, palace_col2, palace_col3 = st.columns(3)
    
    palaces = [
        [("巽 Xun", 4, "SE"), ("离 Li", 9, "S"), ("坤 Kun", 2, "SW")],
        [("震 Zhen", 3, "E"), ("中 Center", 5, "C"), ("兑 Dui", 7, "W")],
        [("艮 Gen", 8, "NE"), ("坎 Kan", 1, "N"), ("乾 Qian", 6, "NW")]
    ]
    
    selected_palace = st.session_state.get('selected_palace', 5)
    
    for row_idx, row in enumerate(palaces):
        cols = st.columns(3)
        for col_idx, (name, num, direction) in enumerate(row):
            with cols[col_idx]:
                if st.button(f"{name}\n#{num} {direction}", key=f"palace_{num}", use_container_width=True):
                    st.session_state.selected_palace = num
                    selected_palace = num
    
    st.markdown(f"**Selected Palace 选中宫位:** #{selected_palace}")
    
    # Generate button
    if st.button("🔮 Generate Chart 生成盘", type="primary", use_container_width=True):
        if parsed_time:
            hour, minute = parsed_time
            st.session_state.last_chart = {
                "date": selected_date.isoformat(),
                "time": f"{hour:02d}:{minute:02d}",
                "hour": hour,
                "minute": minute,
                "palace": selected_palace,
                "chinese_hour": get_chinese_hour(hour, minute),
                "generated_at": datetime.now().isoformat()
            }
            st.success("✅ Chart generated! Go to **Chart Generator** page for full analysis.")
            st.balloons()
        else:
            st.error("❌ Please enter a valid time in HH:MM format")

with col2:
    # User Profile Card - NOW READS PROPERLY FROM SESSION STATE
    st.markdown("### 👤 Your BaZi Profile")
    
    # Get and format profile data
    raw_profile = st.session_state.user_profile
    profile = format_profile_display(raw_profile)
    
    # Get element color for styling
    elem_color = get_element_color(profile['element'])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                padding: 20px; border-radius: 15px; border: 1px solid #d4af37;">
        <h4 style="color: #d4af37; margin-bottom: 15px;">日主 Day Master</h4>
        <p style="font-size: 2em; margin: 0; color: {elem_color};">{profile['day_master']}</p>
        <p style="color: #888;">{profile['element']} • {profile['polarity']} • {profile['strength']}</p>
        
        <h4 style="color: #d4af37; margin-top: 20px;">用神 Useful Gods</h4>
        <p style="color: #4CAF50;">{' • '.join(profile['useful_gods']) if profile['useful_gods'] else 'Not set'}</p>
        
        <h4 style="color: #d4af37; margin-top: 15px;">忌神 Unfavorable</h4>
        <p style="color: #f44336;">{' • '.join(profile['unfavorable']) if profile['unfavorable'] else 'Not set'}</p>
        
        <h4 style="color: #d4af37; margin-top: 15px;">性格 Profile</h4>
        <p>{profile['profile']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("⚙️ Update Profile", use_container_width=True):
        st.switch_page("pages/4_Settings.py")

# Recent analyses
st.markdown("---")
st.markdown("### 📜 Recent Analyses 最近分析")

if st.session_state.analyses:
    for i, analysis in enumerate(reversed(st.session_state.analyses[-5:])):
        with st.expander(f"📊 {analysis.get('date', 'N/A')} - Palace #{analysis.get('palace', 'N/A')}"):
            st.json(analysis)
else:
    st.info("No analyses yet. Generate your first chart above! 还没有分析记录，请先生成盘局。")

# Footer
st.markdown("---")
st.caption("🔮 Qi Men Pro v2.0 | Phase 3 | Joey Yap Methodology | Universal Schema v2.0")
