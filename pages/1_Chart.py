"""
Ming Qimen 明奇门 - Chart Generator
Fixed: Singapore timezone (UTC+8)
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json

st.set_page_config(
    page_title="Chart | Ming Qimen",
    page_icon="📈",
    layout="wide"
)

# Singapore timezone (UTC+8)
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    """Get current time in Singapore (UTC+8)"""
    return datetime.now(SGT)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============ CONSTANTS ============

PALACES = {
    1: {"name": "坎 Kan", "direction": "N", "element": "Water", "icon": "💼", "topic": "Career"},
    2: {"name": "坤 Kun", "direction": "SW", "element": "Earth", "icon": "💕", "topic": "Relations"},
    3: {"name": "震 Zhen", "direction": "E", "element": "Wood", "icon": "💪", "topic": "Health"},
    4: {"name": "巽 Xun", "direction": "SE", "element": "Wood", "icon": "💰", "topic": "Wealth"},
    5: {"name": "中 Center", "direction": "C", "element": "Earth", "icon": "🎯", "topic": "Self"},
    6: {"name": "乾 Qian", "direction": "NW", "element": "Metal", "icon": "🤝", "topic": "Mentor"},
    7: {"name": "兑 Dui", "direction": "W", "element": "Metal", "icon": "👶", "topic": "Children"},
    8: {"name": "艮 Gen", "direction": "NE", "element": "Earth", "icon": "📚", "topic": "Knowledge"},
    9: {"name": "离 Li", "direction": "S", "element": "Fire", "icon": "🌟", "topic": "Fame"},
}

STEMS = ["甲 Jia", "乙 Yi", "丙 Bing", "丁 Ding", "戊 Wu", 
         "己 Ji", "庚 Geng", "辛 Xin", "壬 Ren", "癸 Gui"]

STARS = {
    "天蓬": {"english": "Canopy", "element": "Water", "nature": "Challenging", "meaning": "Hidden obstacles"},
    "天芮": {"english": "Grass", "element": "Earth", "nature": "Challenging", "meaning": "Slow progress"},
    "天冲": {"english": "Impulse", "element": "Wood", "nature": "Favorable", "meaning": "Quick action"},
    "天辅": {"english": "Assistant", "element": "Wood", "nature": "Favorable", "meaning": "Help available"},
    "天禽": {"english": "Connect", "element": "Earth", "nature": "Neutral", "meaning": "Connections matter"},
    "天心": {"english": "Heart", "element": "Metal", "nature": "Very Favorable", "meaning": "Wisdom & clarity"},
    "天柱": {"english": "Pillar", "element": "Metal", "nature": "Neutral", "meaning": "Stand firm"},
    "天任": {"english": "Ren", "element": "Earth", "nature": "Favorable", "meaning": "Steady progress"},
    "天英": {"english": "Hero", "element": "Fire", "nature": "Neutral", "meaning": "Recognition possible"},
}

DOORS = {
    "开门": {"english": "Open", "element": "Metal", "nature": "Very Favorable", "meaning": "New opportunities await"},
    "休门": {"english": "Rest", "element": "Water", "nature": "Favorable", "meaning": "Good for meetings"},
    "生门": {"english": "Life", "element": "Earth", "nature": "Very Favorable", "meaning": "Growth & prosperity"},
    "伤门": {"english": "Harm", "element": "Wood", "nature": "Challenging", "meaning": "Caution with words"},
    "杜门": {"english": "Delusion", "element": "Wood", "nature": "Neutral", "meaning": "Things unclear, wait"},
    "景门": {"english": "Scenery", "element": "Fire", "nature": "Neutral", "meaning": "Good for documents"},
    "死门": {"english": "Stillness", "element": "Earth", "nature": "Challenging", "meaning": "Rest & reflect"},
    "惊门": {"english": "Surprise", "element": "Metal", "nature": "Challenging", "meaning": "Expect the unexpected"},
}

DEITIES = {
    "值符": {"english": "Chief", "nature": "Very Favorable", "meaning": "Blessings from above"},
    "腾蛇": {"english": "Serpent", "nature": "Challenging", "meaning": "Worry & anxiety"},
    "太阴": {"english": "Moon", "nature": "Favorable", "meaning": "Hidden help"},
    "六合": {"english": "Harmony", "nature": "Favorable", "meaning": "Cooperation succeeds"},
    "勾陈": {"english": "Hook", "nature": "Neutral", "meaning": "Delays possible"},
    "白虎": {"english": "Tiger", "nature": "Challenging", "meaning": "Be careful"},
    "玄武": {"english": "Void", "nature": "Challenging", "meaning": "Something unclear"},
    "九地": {"english": "Earth", "nature": "Neutral", "meaning": "Stay grounded"},
    "九天": {"english": "Heaven", "nature": "Favorable", "meaning": "Go big, expand"},
}

ENERGY_LEVELS = {
    3: {"label": "🔥 High Energy", "advice": "Take Action!", "color": "green"},
    2: {"label": "✨ Good Energy", "advice": "Favorable", "color": "green"},
    0: {"label": "😐 Balanced", "advice": "Proceed Normally", "color": "orange"},
    -2: {"label": "🌙 Low Energy", "advice": "Be Patient", "color": "orange"},
    -3: {"label": "💤 Rest Energy", "advice": "Wait & Reflect", "color": "red"},
}

# ============ HELPER FUNCTIONS ============

def parse_time_input(time_str):
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
    total_minutes = hour * 60 + minute
    hour_data = [
        ("子 Zi", "Rat 🐀"), ("丑 Chou", "Ox 🐂"), ("寅 Yin", "Tiger 🐅"),
        ("卯 Mao", "Rabbit 🐇"), ("辰 Chen", "Dragon 🐉"), ("巳 Si", "Snake 🐍"),
        ("午 Wu", "Horse 🐴"), ("未 Wei", "Goat 🐐"), ("申 Shen", "Monkey 🐒"),
        ("酉 You", "Rooster 🐓"), ("戌 Xu", "Dog 🐕"), ("亥 Hai", "Pig 🐖"),
    ]
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return hour_data[0]
    idx = (hour + 1) // 2
    return hour_data[idx] if idx < 12 else hour_data[0]

def determine_structure(month):
    if month in [12, 1, 2, 3, 4, 5]:
        return "Yang Dun 阳遁"
    return "Yin Dun 阴遁"

def calculate_ju_number(year, month, day, hour):
    base = (year + month + day + hour) % 9
    return base if base > 0 else 9

def calculate_energy(comp_element, palace_element):
    cycle = ["Wood", "Fire", "Earth", "Metal", "Water"]
    if comp_element not in cycle or palace_element not in cycle:
        return (0, ENERGY_LEVELS[0])
    
    comp_idx = cycle.index(comp_element)
    palace_idx = cycle.index(palace_element)
    diff = (comp_idx - palace_idx) % 5
    
    if diff == 0:
        return (3, ENERGY_LEVELS[3])
    elif diff == 1:
        return (2, ENERGY_LEVELS[2])
    elif diff == 2:
        return (0, ENERGY_LEVELS[0])
    elif diff == 3:
        return (-2, ENERGY_LEVELS[-2])
    else:
        return (-3, ENERGY_LEVELS[-3])

def get_nature_display(nature):
    if "Very Favorable" in str(nature):
        return "🌟", "green", "Excellent!"
    elif "Favorable" in str(nature):
        return "✅", "green", "Good"
    elif "Challenging" in str(nature):
        return "⚠️", "red", "Caution"
    return "😐", "orange", "Neutral"

def generate_qmdj_chart(selected_date, hour, minute, palace_number):
    structure = determine_structure(selected_date.month)
    ju_number = calculate_ju_number(selected_date.year, selected_date.month, 
                                     selected_date.day, hour)
    chinese_hour = get_chinese_hour(hour, minute)
    palace = PALACES[palace_number]
    
    seed = selected_date.year * 10000 + selected_date.month * 100 + selected_date.day + hour + palace_number
    
    stem_idx = seed % 10
    earth_stem_idx = (seed + 3) % 10
    star_idx = seed % len(STARS)
    door_idx = seed % len(DOORS)
    deity_idx = seed % len(DEITIES)
    
    star_keys = list(STARS.keys())
    door_keys = list(DOORS.keys())
    deity_keys = list(DEITIES.keys())
    
    star_cn = star_keys[star_idx]
    door_cn = door_keys[door_idx]
    deity_cn = deity_keys[deity_idx]
    
    star = STARS[star_cn]
    door = DOORS[door_cn]
    deity = DEITIES[deity_cn]
    
    palace_element = palace["element"]
    
    chart = {
        "metadata": {
            "date": selected_date.isoformat(),
            "time": f"{hour:02d}:{minute:02d}",
            "chinese_hour": chinese_hour[0],
            "chinese_hour_animal": chinese_hour[1],
            "structure": structure,
            "ju_number": ju_number,
            "timezone": "SGT (UTC+8)"
        },
        "palace": {
            "number": palace_number,
            "name": palace["name"],
            "direction": palace["direction"],
            "element": palace_element,
            "icon": palace["icon"],
            "topic": palace["topic"]
        },
        "components": {
            "heaven_stem": STEMS[stem_idx],
            "earth_stem": STEMS[earth_stem_idx],
            "star": {
                "chinese": star_cn,
                "english": star["english"],
                "element": star["element"],
                "nature": star["nature"],
                "meaning": star["meaning"],
                "energy": calculate_energy(star["element"], palace_element)
            },
            "door": {
                "chinese": door_cn,
                "english": door["english"],
                "element": door["element"],
                "nature": door["nature"],
                "meaning": door["meaning"],
                "energy": calculate_energy(door["element"], palace_element)
            },
            "deity": {
                "chinese": deity_cn,
                "english": deity["english"],
                "nature": deity["nature"],
                "meaning": deity["meaning"]
            }
        }
    }
    
    natures = [star["nature"], door["nature"], deity["nature"]]
    favorable = sum(1 for n in natures if "Favorable" in n)
    challenging = sum(1 for n in natures if "Challenging" in n)
    
    if favorable >= 2:
        chart["guidance"] = {
            "verdict": "Green Light 🟢",
            "summary": "Favorable conditions for action",
            "advice": f"Good time for {palace['topic'].lower()} matters. Move forward with confidence!",
            "type": "success"
        }
    elif challenging >= 2:
        chart["guidance"] = {
            "verdict": "Yellow Light 🟡",
            "summary": "Proceed with awareness",
            "advice": f"Not ideal for {palace['topic'].lower()} matters. Consider waiting or extra preparation.",
            "type": "warning"
        }
    else:
        chart["guidance"] = {
            "verdict": "Neutral ⚪",
            "summary": "Mixed signals",
            "advice": f"Balanced energy for {palace['topic'].lower()}. Success depends on your effort.",
            "type": "info"
        }
    
    return chart

# ============ PAGE CONTENT ============

st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #d4af37;">📈 Your Reading 您的指引</h1>
    <p style="color: #888;">Ming Qimen 明奇门 | Singapore Time (SGT)</p>
</div>
""", unsafe_allow_html=True)

# Get Singapore time and shared state
sg_now = get_singapore_time()
default_date = st.session_state.get('shared_date', sg_now.date())
default_time = st.session_state.get('shared_time', sg_now.strftime("%H:%M"))
default_palace = st.session_state.get('selected_palace', 5)

# Input Section
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_date = st.date_input("📅 Date 日期", value=default_date)

with col2:
    time_input = st.text_input("⏰ Time (HH:MM)", value=default_time)
    parsed_time = parse_time_input(time_input)
    if parsed_time:
        hour, minute = parsed_time
        chinese_hour = get_chinese_hour(hour, minute)
        st.success(f"✅ {chinese_hour[0]} ({chinese_hour[1]})")
    else:
        st.error("❌ Invalid")
        hour, minute = 12, 0

with col3:
    palace_number = st.selectbox(
        "🏛️ Topic 主题",
        options=list(PALACES.keys()),
        format_func=lambda x: f"#{x} {PALACES[x]['icon']} {PALACES[x]['topic']}",
        index=default_palace - 1
    )

# Generate Button
if st.button("🔮 Get Guidance 获取指引", type="primary", use_container_width=True):
    if parsed_time:
        chart = generate_qmdj_chart(selected_date, hour, minute, palace_number)
        st.session_state.current_chart = chart
        st.success("✅ Your guidance is ready!")

# Display Results
if 'current_chart' in st.session_state and st.session_state.current_chart:
    chart = st.session_state.current_chart
    
    st.markdown("---")
    
    palace = chart['palace']
    st.markdown(f"### {palace['icon']} Your {palace['topic']} Reading")
    st.markdown(f"**Palace:** #{palace['number']} {palace['name']} | **Element:** {palace['element']}")
    
    meta_cols = st.columns(4)
    meta_cols[0].metric("📅 Date", chart['metadata']['date'])
    meta_cols[1].metric("⏰ Time (SGT)", chart['metadata']['time'])
    meta_cols[2].metric("🕐 时辰", chart['metadata']['chinese_hour'])
    meta_cols[3].metric("Structure", f"#{chart['metadata']['ju_number']}")
    
    st.markdown("---")
    guidance = chart['guidance']
    
    if guidance['type'] == 'success':
        st.success(f"## {guidance['verdict']}")
        st.success(f"**{guidance['summary']}**")
    elif guidance['type'] == 'warning':
        st.warning(f"## {guidance['verdict']}")
        st.warning(f"**{guidance['summary']}**")
    else:
        st.info(f"## {guidance['verdict']}")
        st.info(f"**{guidance['summary']}**")
    
    st.markdown(f"### 💡 Advice: {guidance['advice']}")
    
    st.markdown("---")
    st.markdown("### 📋 What the Signs Say 详细信息")
    
    comp_cols = st.columns(3)
    
    with comp_cols[0]:
        star = chart['components']['star']
        emoji, color, label = get_nature_display(star['nature'])
        st.markdown(f"**Star 九星** {emoji}")
        st.markdown(f"### {star['chinese']} {star['english']}")
        if "Favorable" in star['nature']:
            st.success(f"{star['meaning']}")
        elif "Challenging" in star['nature']:
            st.error(f"{star['meaning']}")
        else:
            st.warning(f"{star['meaning']}")
        energy_score, energy_info = star['energy']
        st.caption(f"{energy_info['label']} - {energy_info['advice']}")
    
    with comp_cols[1]:
        door = chart['components']['door']
        emoji, color, label = get_nature_display(door['nature'])
        st.markdown(f"**Door 八门** {emoji}")
        st.markdown(f"### {door['chinese']} {door['english']}")
        if "Favorable" in door['nature']:
            st.success(f"{door['meaning']}")
        elif "Challenging" in door['nature']:
            st.error(f"{door['meaning']}")
        else:
            st.warning(f"{door['meaning']}")
        energy_score, energy_info = door['energy']
        st.caption(f"{energy_info['label']} - {energy_info['advice']}")
    
    with comp_cols[2]:
        deity = chart['components']['deity']
        emoji, color, label = get_nature_display(deity['nature'])
        st.markdown(f"**Spirit 八神** {emoji}")
        st.markdown(f"### {deity['chinese']} {deity['english']}")
        if "Favorable" in deity['nature']:
            st.success(f"{deity['meaning']}")
        elif "Challenging" in deity['nature']:
            st.error(f"{deity['meaning']}")
        else:
            st.warning(f"{deity['meaning']}")
    
    with st.expander("🔍 More Details 更多详情", expanded=False):
        stem_cols = st.columns(2)
        with stem_cols[0]:
            st.markdown(f"**Heaven Stem 天干:** {chart['components']['heaven_stem']}")
        with stem_cols[1]:
            st.markdown(f"**Earth Stem 地干:** {chart['components']['earth_stem']}")
        st.json(chart)
    
    # Save to history
    if 'analyses' not in st.session_state:
        st.session_state.analyses = []
    
    existing = [a for a in st.session_state.analyses 
                if a.get('date') == chart['metadata']['date'] 
                and a.get('time') == chart['metadata']['time']
                and a.get('palace') == chart['palace']['number']]
    
    if not existing:
        st.session_state.analyses.append({
            "date": chart['metadata']['date'],
            "time": chart['metadata']['time'],
            "palace": chart['palace']['number'],
            "topic": chart['palace']['topic'],
            "verdict": guidance['verdict'],
            "generated_at": get_singapore_time().isoformat()
        })

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Clarity for the People | Singapore Time (UTC+8)")
