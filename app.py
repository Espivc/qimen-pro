"""
Qi Men Pro v2.1 - Dashboard
Phase 3: Added quick reference card and palace hints
"""

import streamlit as st
from datetime import datetime
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

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        "day_master": "庚 Geng",
        "element": "Metal 金",
        "polarity": "Yang",
        "strength": "Weak",
        "useful_gods": ["Earth", "Metal"],
        "unfavorable": ["Fire", "Wood"],
        "profile": "Pioneer 🎯 (Indirect Wealth 偏财)"
    }

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = 5

# ============ HELPER FUNCTIONS ============

def parse_time_input(time_str):
    """Parse time string in HH:MM format"""
    try:
        time_str = time_str.strip().replace("：", ":").replace(".", ":")
        if ":" in time_str:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
        else:
            hour = int(time_str)
            minute = 0
        
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)
        return None
    except:
        return None

def get_chinese_hour(hour, minute=0):
    """Convert 24h time to Chinese double-hour"""
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
    
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return chinese_hours[0]
    
    hour_index = (hour + 1) // 2
    if hour_index >= 12:
        hour_index = 0
    
    return chinese_hours[hour_index]

# Palace data with hints
PALACE_INFO = {
    1: {"name": "坎 Kan", "direction": "N", "icon": "💼", "topic": "Career", "hint": "Job, business, life path"},
    2: {"name": "坤 Kun", "direction": "SW", "icon": "💕", "topic": "Relations", "hint": "Marriage, partnership"},
    3: {"name": "震 Zhen", "direction": "E", "icon": "💪", "topic": "Health", "hint": "Health, family, new starts"},
    4: {"name": "巽 Xun", "direction": "SE", "icon": "💰", "topic": "Wealth", "hint": "Money, investments"},
    5: {"name": "中 Center", "direction": "C", "icon": "🎯", "topic": "Self", "hint": "General, yourself"},
    6: {"name": "乾 Qian", "direction": "NW", "icon": "🤝", "topic": "Mentor", "hint": "Helpful people, travel"},
    7: {"name": "兑 Dui", "direction": "W", "icon": "👶", "topic": "Children", "hint": "Creativity, joy, projects"},
    8: {"name": "艮 Gen", "direction": "NE", "icon": "📚", "topic": "Knowledge", "hint": "Education, skills"},
    9: {"name": "离 Li", "direction": "S", "icon": "🌟", "topic": "Fame", "hint": "Recognition, reputation"},
}

# ============ MAIN DASHBOARD ============

st.title("🔮 奇門遁甲 Qi Men Dun Jia Pro")
st.markdown("**QMDJ + BaZi Integrated Analysis System**")

# Sidebar with Quick Reference
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    - 📊 **Dashboard** (current)
    - 📈 Chart Generator
    - 📤 Export
    - 📜 History & ML
    - ⚙️ Settings
    - 📚 Help & Guide
    """)
    
    st.markdown("---")
    
    # Quick Reference Card
    st.markdown("### 📖 Quick Reference")
    
    with st.expander("✅ Auspicious 吉", expanded=False):
        st.markdown("""
        **Doors:** Open 开, Rest 休, Life 生
        
        **Stars:** Heart 心, Assistant 辅, Ren 任
        
        **Deities:** Chief 值符, Moon 太阴
        """)
    
    with st.expander("❌ Inauspicious 凶", expanded=False):
        st.markdown("""
        **Doors:** Death 死, Fear 惊, Harm 伤
        
        **Stars:** Canopy 蓬, Grass 芮
        
        **Deities:** Serpent 蛇, Tiger 虎
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
    
    # Date and Time row
    date_col, time_col = st.columns(2)
    
    with date_col:
        selected_date = st.date_input(
            "📅 Select Date 选择日期",
            value=datetime.now().date(),
            help="Choose the date for your QMDJ chart"
        )
    
    with time_col:
        time_input = st.text_input(
            "⏰ Time (HH:MM) 时间",
            value=datetime.now().strftime("%H:%M"),
            placeholder="e.g., 14:30",
            help="Enter time in 24-hour format"
        )
        
        parsed_time = parse_time_input(time_input)
        if parsed_time:
            hour, minute = parsed_time
            chinese_hour = get_chinese_hour(hour, minute)
            st.success(f"✅ {chinese_hour[0]} ({chinese_hour[2]})")
        else:
            st.error("❌ Invalid time format")
    
    # Palace Selection with hints
    st.markdown("#### 🏛️ Select Palace 选择宫位")
    st.caption("💡 Choose based on your question topic:")
    
    # Palace grid with topic hints
    palace_grid = [
        [4, 9, 2],  # Top row: SE, S, SW
        [3, 5, 7],  # Middle row: E, Center, W
        [8, 1, 6],  # Bottom row: NE, N, NW
    ]
    
    for row in palace_grid:
        cols = st.columns(3)
        for col, palace_num in zip(cols, row):
            with col:
                info = PALACE_INFO[palace_num]
                is_selected = st.session_state.selected_palace == palace_num
                
                # Button with topic hint
                button_label = f"{info['icon']} {info['name']}\n#{palace_num} {info['direction']}\n{info['topic']}"
                
                if st.button(
                    button_label, 
                    key=f"palace_{palace_num}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_palace = palace_num
    
    # Show selected palace info
    selected = PALACE_INFO[st.session_state.selected_palace]
    st.info(f"**Selected:** #{st.session_state.selected_palace} {selected['name']} - {selected['icon']} {selected['topic']} ({selected['hint']})")
    
    # Generate button
    if st.button("🔮 Generate Chart 生成盘", type="primary", use_container_width=True):
        if parsed_time:
            hour, minute = parsed_time
            st.session_state.last_chart = {
                "date": selected_date.isoformat(),
                "time": f"{hour:02d}:{minute:02d}",
                "hour": hour,
                "minute": minute,
                "palace": st.session_state.selected_palace,
                "palace_info": PALACE_INFO[st.session_state.selected_palace],
                "chinese_hour": get_chinese_hour(hour, minute),
                "generated_at": datetime.now().isoformat()
            }
            st.success("✅ Chart generated! Go to **Chart Generator** page for full analysis.")
            st.balloons()
        else:
            st.error("❌ Please enter a valid time in HH:MM format")

with col2:
    # User Profile Card
    st.markdown("### 👤 Your BaZi Profile")
    
    profile = st.session_state.user_profile
    
    # Day Master
    st.markdown("#### 日主 Day Master")
    st.markdown(f"## {profile.get('day_master', 'Not set')}")
    st.caption(f"{profile.get('element', '')} • {profile.get('polarity', '')} • {profile.get('strength', '')}")
    
    st.markdown("---")
    
    # Useful Gods
    st.markdown("#### 用神 Useful Gods")
    useful = profile.get('useful_gods', [])
    if useful:
        st.success(' • '.join(str(g) for g in useful))
    else:
        st.info("Not set")
    
    # Unfavorable
    st.markdown("#### 忌神 Unfavorable")
    unfav = profile.get('unfavorable', [])
    if unfav:
        st.error(' • '.join(str(u) for u in unfav))
    else:
        st.info("Not set")
    
    # Profile
    st.markdown("#### 性格 Profile")
    st.info(profile.get('profile', 'Not set'))
    
    st.markdown("")
    if st.button("⚙️ Update Profile", use_container_width=True):
        st.switch_page("pages/4_Settings.py")
    
    # Birth info
    if profile.get('birth_date'):
        st.caption(f"📅 {profile.get('birth_date')} {profile.get('birth_time', '')}")

# Quick Palace Reference (collapsible)
st.markdown("---")
with st.expander("🏛️ Palace Quick Reference 宫位速查", expanded=False):
    ref_cols = st.columns(3)
    
    for i, col in enumerate(ref_cols):
        with col:
            for palace_num in [i*3 + 1, i*3 + 2, i*3 + 3]:
                if palace_num <= 9:
                    info = PALACE_INFO[palace_num]
                    st.markdown(f"**#{palace_num} {info['name']}** {info['icon']}")
                    st.caption(f"{info['topic']}: {info['hint']}")

# Recent analyses
st.markdown("---")
st.markdown("### 📜 Recent Analyses 最近分析")

if st.session_state.analyses:
    for i, analysis in enumerate(reversed(st.session_state.analyses[-5:])):
        palace_num = analysis.get('palace', 5)
        palace_info = PALACE_INFO.get(palace_num, {})
        with st.expander(f"📊 {analysis.get('date', 'N/A')} - {palace_info.get('icon', '')} Palace #{palace_num}"):
            st.json(analysis)
else:
    st.info("No analyses yet. Generate your first chart above! 还没有分析记录。")

# Footer
st.markdown("---")
col_foot1, col_foot2 = st.columns([3, 1])
with col_foot1:
    st.caption("🔮 Qi Men Pro v2.1 | Phase 3 | Joey Yap Methodology")
with col_foot2:
    if st.button("📚 Help & Guide"):
        st.switch_page("pages/5_Help.py")
