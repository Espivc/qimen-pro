"""
Ming Qimen 明奇门 - Dashboard
Clarity for the People | Ancient Wisdom Made Bright
Fixed: Singapore timezone (UTC+8)
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json

# Page config
st.set_page_config(
    page_title="明 Ming Qimen",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Singapore timezone (UTC+8)
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    """Get current time in Singapore (UTC+8)"""
    return datetime.now(SGT)

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

# Get SINGAPORE time
sg_now = get_singapore_time()

# Sync time input with chart page
if 'shared_time' not in st.session_state:
    st.session_state.shared_time = sg_now.strftime("%H:%M")

if 'shared_date' not in st.session_state:
    st.session_state.shared_date = sg_now.date()

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
        ("子 Zi", "23:00-00:59", "Rat 🐀", 0),
        ("丑 Chou", "01:00-02:59", "Ox 🐂", 1),
        ("寅 Yin", "03:00-04:59", "Tiger 🐅", 2),
        ("卯 Mao", "05:00-06:59", "Rabbit 🐇", 3),
        ("辰 Chen", "07:00-08:59", "Dragon 🐉", 4),
        ("巳 Si", "09:00-10:59", "Snake 🐍", 5),
        ("午 Wu", "11:00-12:59", "Horse 🐴", 6),
        ("未 Wei", "13:00-14:59", "Goat 🐐", 7),
        ("申 Shen", "15:00-16:59", "Monkey 🐒", 8),
        ("酉 You", "17:00-18:59", "Rooster 🐓", 9),
        ("戌 Xu", "19:00-20:59", "Dog 🐕", 10),
        ("亥 Hai", "21:00-22:59", "Pig 🐖", 11),
    ]
    
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return chinese_hours[0]
    
    hour_index = (hour + 1) // 2
    if hour_index >= 12:
        hour_index = 0
    
    return chinese_hours[hour_index]

def get_recommended_palace(hour, user_profile):
    """Get recommended palace based on current hour and user's useful gods"""
    useful = user_profile.get('useful_gods', [])
    
    palace_elements = {
        1: "Water", 2: "Earth", 3: "Wood", 4: "Wood",
        5: "Earth", 6: "Metal", 7: "Metal", 8: "Earth", 9: "Fire"
    }
    
    good_palaces = []
    for num, elem in palace_elements.items():
        if elem in useful:
            good_palaces.append(num)
    
    hour_recommendations = {
        (23, 0, 1): [1, 6],
        (1, 2, 3): [8, 1],
        (3, 4, 5): [3, 4],
        (5, 6, 7): [3, 4],
        (7, 8, 9): [4, 9],
        (9, 10, 11): [9, 4],
        (11, 12, 13): [9, 2],
        (13, 14, 15): [2, 7],
        (15, 16, 17): [6, 7],
        (17, 18, 19): [6, 7],
        (19, 20, 21): [1, 8],
        (21, 22, 23): [1, 6],
    }
    
    for hours, palaces in hour_recommendations.items():
        if hour in hours or (hours[0] <= hour < hours[2]):
            for p in palaces:
                if p in good_palaces:
                    return p
            return palaces[0]
    
    return 5

# Palace data
PALACE_INFO = {
    1: {"name": "坎 Kan", "direction": "N", "icon": "💼", "topic": "Career", "hint": "Job, business, life path", "element": "Water"},
    2: {"name": "坤 Kun", "direction": "SW", "icon": "💕", "topic": "Relations", "hint": "Marriage, partnership", "element": "Earth"},
    3: {"name": "震 Zhen", "direction": "E", "icon": "💪", "topic": "Health", "hint": "Health, family, new starts", "element": "Wood"},
    4: {"name": "巽 Xun", "direction": "SE", "icon": "💰", "topic": "Wealth", "hint": "Money, investments", "element": "Wood"},
    5: {"name": "中 Center", "direction": "C", "icon": "🎯", "topic": "Self", "hint": "General, yourself", "element": "Earth"},
    6: {"name": "乾 Qian", "direction": "NW", "icon": "🤝", "topic": "Mentor", "hint": "Helpful people, travel", "element": "Metal"},
    7: {"name": "兑 Dui", "direction": "W", "icon": "👶", "topic": "Children", "hint": "Creativity, joy, projects", "element": "Metal"},
    8: {"name": "艮 Gen", "direction": "NE", "icon": "📚", "topic": "Knowledge", "hint": "Education, skills", "element": "Earth"},
    9: {"name": "离 Li", "direction": "S", "icon": "🌟", "topic": "Fame", "hint": "Recognition, reputation", "element": "Fire"},
}

# ============ MAIN DASHBOARD ============

# Header with Mission
st.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <h1 style="color: #d4af37; margin-bottom: 5px;">🌟 明 Ming Qimen</h1>
    <p style="color: #888; font-style: italic; font-size: 1.1em;">Ancient Wisdom, Made Bright and Simple</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Get SINGAPORE current time
current_time = get_singapore_time()
current_hour = current_time.hour
current_minute = current_time.minute

# Recommended palace for THIS moment
recommended_palace = get_recommended_palace(current_hour, st.session_state.user_profile)

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    - 🏠 **Home** (current)
    - 📈 Chart Generator
    - 📤 Export
    - 📜 History
    - ⚙️ Settings
    - 📚 Help & Guide
    """)
    
    st.markdown("---")
    
    # Quick Reference
    st.markdown("### 📖 Quick Guide")
    
    with st.expander("✅ Good Signs 吉", expanded=False):
        st.markdown("""
        **Doors:** Open 开, Rest 休, Life 生
        
        **Stars:** Heart 心, Assistant 辅
        
        **Energy:** High Energy = Take Action!
        """)
    
    with st.expander("⚠️ Caution Signs 凶", expanded=False):
        st.markdown("""
        **Doors:** Stillness 死, Surprise 惊
        
        **Stars:** Canopy 蓬, Grass 芮
        
        **Energy:** Low Energy = Rest & Wait
        """)
    
    st.markdown("---")
    st.markdown("### 📱 Your Stats")
    total = len(st.session_state.analyses)
    success = len([a for a in st.session_state.analyses if a.get('outcome') == 'SUCCESS'])
    st.metric("Total Readings", total)
    st.metric("Success Rate", f"{(success/total*100):.0f}%" if total > 0 else "N/A")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚡ Your Reading 您的盘局")
    
    # CURRENT TIME - Singapore timezone!
    st.markdown(f"**🕐 Singapore Time (SGT):** {current_time.strftime('%Y-%m-%d %H:%M')}")
    
    chinese_hour_info = get_chinese_hour(current_hour, current_minute)
    st.success(f"**时辰:** {chinese_hour_info[0]} ({chinese_hour_info[1]}) - {chinese_hour_info[2]}")
    
    # Date and Time inputs
    date_col, time_col = st.columns(2)
    
    with date_col:
        selected_date = st.date_input(
            "📅 Select Date 选择日期",
            value=current_time.date(),
            help="Default is today (Singapore time)"
        )
        st.session_state.shared_date = selected_date
    
    with time_col:
        default_time = current_time.strftime("%H:%M")
        time_input = st.text_input(
            "⏰ Time (HH:MM) 时间",
            value=default_time,
            placeholder="e.g., 14:30",
            help="Default is now (Singapore time)"
        )
        
        parsed_time = parse_time_input(time_input)
        if parsed_time:
            hour, minute = parsed_time
            st.session_state.shared_time = f"{hour:02d}:{minute:02d}"
            if f"{hour:02d}:{minute:02d}" != default_time:
                ch_hour = get_chinese_hour(hour, minute)
                st.info(f"📅 Selected: {ch_hour[0]} ({ch_hour[2]})")
        else:
            st.error("❌ Invalid time format")
            hour, minute = current_hour, current_minute
    
    # Palace Selection
    st.markdown("#### 🏛️ What's Your Question About? 选择宫位")
    st.caption("💡 Tap the topic that matches your question:")
    
    # Show recommendation
    rec_info = PALACE_INFO[recommended_palace]
    st.markdown(f"⭐ **Recommended for now:** #{recommended_palace} {rec_info['icon']} **{rec_info['topic']}** - {rec_info['hint']}")
    
    # Palace grid
    palace_grid = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6],
    ]
    
    for row in palace_grid:
        cols = st.columns(3)
        for col, palace_num in zip(cols, row):
            with col:
                info = PALACE_INFO[palace_num]
                is_selected = st.session_state.selected_palace == palace_num
                is_recommended = palace_num == recommended_palace
                
                star = "⭐ " if is_recommended else ""
                button_label = f"{star}{info['icon']} {info['topic']}\n#{palace_num} {info['direction']}"
                
                if st.button(
                    button_label, 
                    key=f"palace_{palace_num}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_palace = palace_num
    
    # Selected palace info
    selected = PALACE_INFO[st.session_state.selected_palace]
    st.info(f"**Selected:** #{st.session_state.selected_palace} {selected['name']} - {selected['icon']} **{selected['topic']}** ({selected['hint']})")
    
    # Generate button
    if st.button("🔮 Get Your Reading 获取指引", type="primary", use_container_width=True):
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
                "generated_at": get_singapore_time().isoformat()
            }
            st.session_state.shared_time = f"{hour:02d}:{minute:02d}"
            st.session_state.shared_date = selected_date
            st.success("✅ Reading prepared! Go to **Chart** page to see your guidance.")
            st.balloons()
        else:
            st.error("❌ Please enter a valid time in HH:MM format")

with col2:
    # User Profile Card
    st.markdown("### 👤 Your Profile")
    
    profile = st.session_state.user_profile
    
    st.markdown("#### 日主 Day Master")
    st.markdown(f"## {profile.get('day_master', 'Not set')}")
    st.caption(f"{profile.get('element', '')} • {profile.get('polarity', '')} • {profile.get('strength', '')}")
    
    st.markdown("---")
    
    st.markdown("#### 用神 Helpful Elements")
    useful = profile.get('useful_gods', [])
    if useful:
        st.success(' • '.join(str(g) for g in useful))
        st.caption("ℹ️ These elements bring you balance. Seeing them is a good sign!")
    else:
        st.info("Not set - Go to Settings")
    
    st.markdown("#### 忌神 Challenging Elements")
    unfav = profile.get('unfavorable', [])
    if unfav:
        st.error(' • '.join(str(u) for u in unfav))
        st.caption("ℹ️ Be mindful when these appear.")
    else:
        st.info("Not set")
    
    st.markdown("#### 性格 Your Nature")
    st.info(profile.get('profile', 'Not set'))
    
    st.markdown("")
    if st.button("⚙️ Update Profile", use_container_width=True):
        st.switch_page("pages/4_Settings.py")
    
    if profile.get('birth_date'):
        st.caption(f"📅 {profile.get('birth_date')} {profile.get('birth_time', '')}")

# Mission Statement
st.markdown("---")
with st.expander("🌟 About Ming Qimen 关于明奇门", expanded=False):
    st.markdown("""
    ### Our Mission 我们的使命
    
    I created **Ming Qimen** because I believe wisdom shouldn't come with a price tag or a headache.
    
    My name is **Beng (明)**, which means **'Brightness.'** My goal is to use that light to clear 
    the fog of ancient calculations.
    
    Too many apps are built for experts; **this one is built for you.**
    
    **No paywalls, no complex data entry** — just clear guidance to help you find your way, for free.
    
    *Let's help people first, and let the rest follow.*
    
    ---
    
    **"Guiding you first, because your peace of mind matters."**
    """)

# Palace Reference
with st.expander("🏛️ Topic Quick Reference 宫位速查", expanded=False):
    ref_cols = st.columns(3)
    for i, col in enumerate(ref_cols):
        with col:
            for palace_num in [i*3 + 1, i*3 + 2, i*3 + 3]:
                if palace_num <= 9:
                    info = PALACE_INFO[palace_num]
                    st.markdown(f"**#{palace_num} {info['name']}** {info['icon']}")
                    st.caption(f"{info['topic']}: {info['hint']}")

# Footer
st.markdown("---")
col_foot1, col_foot2 = st.columns([3, 1])
with col_foot1:
    st.caption("🌟 Ming Qimen 明奇门 | Clarity for the People | Singapore Time (UTC+8)")
with col_foot2:
    if st.button("📚 Help & Guide"):
        st.switch_page("pages/5_Help.py")
