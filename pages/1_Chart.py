"""
Qi Men Pro - Chart Generator Page
Phase 3: Fixed HTML rendering - using native Streamlit components
"""

import streamlit as st
from datetime import datetime, date
import json

st.set_page_config(
    page_title="Chart Generator | Qi Men Pro",
    page_icon="📈",
    layout="wide"
)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============ CONSTANTS ============

PALACES = {
    1: {"name": "坎 Kan", "direction": "N", "element": "Water", "icon": "💼"},
    2: {"name": "坤 Kun", "direction": "SW", "element": "Earth", "icon": "💕"},
    3: {"name": "震 Zhen", "direction": "E", "element": "Wood", "icon": "💪"},
    4: {"name": "巽 Xun", "direction": "SE", "element": "Wood", "icon": "💰"},
    5: {"name": "中 Center", "direction": "C", "element": "Earth", "icon": "🎯"},
    6: {"name": "乾 Qian", "direction": "NW", "element": "Metal", "icon": "🤝"},
    7: {"name": "兑 Dui", "direction": "W", "element": "Metal", "icon": "👶"},
    8: {"name": "艮 Gen", "direction": "NE", "element": "Earth", "icon": "📚"},
    9: {"name": "离 Li", "direction": "S", "element": "Fire", "icon": "🌟"},
}

STEMS = ["甲 Jia", "乙 Yi", "丙 Bing", "丁 Ding", "戊 Wu", 
         "己 Ji", "庚 Geng", "辛 Xin", "壬 Ren", "癸 Gui"]

BRANCHES = ["子 Zi", "丑 Chou", "寅 Yin", "卯 Mao", "辰 Chen", "巳 Si",
            "午 Wu", "未 Wei", "申 Shen", "酉 You", "戌 Xu", "亥 Hai"]

STARS = {
    "天蓬": {"english": "Canopy", "element": "Water", "nature": "Inauspicious"},
    "天芮": {"english": "Grass", "element": "Earth", "nature": "Inauspicious"},
    "天冲": {"english": "Impulse", "element": "Wood", "nature": "Auspicious"},
    "天辅": {"english": "Assistant", "element": "Wood", "nature": "Auspicious"},
    "天禽": {"english": "Connect", "element": "Earth", "nature": "Neutral"},
    "天心": {"english": "Heart", "element": "Metal", "nature": "Auspicious"},
    "天柱": {"english": "Pillar", "element": "Metal", "nature": "Neutral"},
    "天任": {"english": "Ren", "element": "Earth", "nature": "Auspicious"},
    "天英": {"english": "Hero", "element": "Fire", "nature": "Neutral"},
}

DOORS = {
    "开门": {"english": "Open", "element": "Metal", "nature": "Auspicious"},
    "休门": {"english": "Rest", "element": "Water", "nature": "Auspicious"},
    "生门": {"english": "Life", "element": "Earth", "nature": "Auspicious"},
    "伤门": {"english": "Harm", "element": "Wood", "nature": "Inauspicious"},
    "杜门": {"english": "Delusion", "element": "Wood", "nature": "Neutral"},
    "景门": {"english": "Scenery", "element": "Fire", "nature": "Neutral"},
    "死门": {"english": "Death", "element": "Earth", "nature": "Inauspicious"},
    "惊门": {"english": "Fear", "element": "Metal", "nature": "Inauspicious"},
}

DEITIES = {
    "值符": {"english": "Chief", "nature": "Auspicious"},
    "腾蛇": {"english": "Serpent", "nature": "Inauspicious"},
    "太阴": {"english": "Moon", "nature": "Auspicious"},
    "六合": {"english": "Six Harmony", "nature": "Auspicious"},
    "勾陈": {"english": "Hook", "nature": "Neutral"},
    "白虎": {"english": "Tiger", "nature": "Inauspicious"},
    "玄武": {"english": "Emptiness", "nature": "Inauspicious"},
    "九地": {"english": "Nine Earth", "nature": "Neutral"},
    "九天": {"english": "Nine Heaven", "nature": "Auspicious"},
}

FORMATIONS = {
    "伏吟": {"english": "Fu Yin (Hidden Voice)", "nature": "Inauspicious", "meaning": "Stagnation, delay"},
    "反吟": {"english": "Fan Yin (Returning Voice)", "nature": "Inauspicious", "meaning": "Reversal, change"},
    "天遁": {"english": "Tian Dun (Heaven Escape)", "nature": "Very Auspicious", "meaning": "Divine help"},
    "地遁": {"english": "Di Dun (Earth Escape)", "nature": "Very Auspicious", "meaning": "Hidden support"},
    "人遁": {"english": "Ren Dun (Human Escape)", "nature": "Auspicious", "meaning": "Help from people"},
    "龙遁": {"english": "Long Dun (Dragon Escape)", "nature": "Auspicious", "meaning": "Power, authority"},
    "虎遁": {"english": "Hu Dun (Tiger Escape)", "nature": "Neutral", "meaning": "Courage needed"},
    "风遁": {"english": "Feng Dun (Wind Escape)", "nature": "Auspicious", "meaning": "Quick success"},
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

def calculate_strength(comp_element, palace_element):
    """Calculate element strength relative to palace"""
    cycle = ["Wood", "Fire", "Earth", "Metal", "Water"]
    if comp_element not in cycle or palace_element not in cycle:
        return ("Unknown", 0)
    
    comp_idx = cycle.index(comp_element)
    palace_idx = cycle.index(palace_element)
    diff = (comp_idx - palace_idx) % 5
    
    if diff == 0:
        return ("Timely", 3)
    elif diff == 1:
        return ("Prosperous", 2)
    elif diff == 2:
        return ("Resting", 0)
    elif diff == 3:
        return ("Confined", -2)
    else:
        return ("Dead", -3)

def get_nature_color(nature):
    if "Auspicious" in str(nature):
        return "green"
    elif "Inauspicious" in str(nature):
        return "red"
    return "orange"

def generate_qmdj_chart(selected_date, hour, minute, palace_number):
    """Generate QMDJ chart data"""
    
    structure = determine_structure(selected_date.month)
    ju_number = calculate_ju_number(selected_date.year, selected_date.month, 
                                     selected_date.day, hour)
    chinese_hour = get_chinese_hour(hour, minute)
    palace = PALACES[palace_number]
    
    # Calculate components (simplified)
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
    
    # Formation detection (simplified)
    formation = None
    formation_keys = list(FORMATIONS.keys())
    if (seed % 7) == 0:
        formation_cn = formation_keys[seed % len(formation_keys)]
        formation = {"chinese": formation_cn, **FORMATIONS[formation_cn]}
    
    chart = {
        "metadata": {
            "date": selected_date.isoformat(),
            "time": f"{hour:02d}:{minute:02d}",
            "chinese_hour": chinese_hour[0],
            "chinese_hour_animal": chinese_hour[1],
            "structure": structure,
            "ju_number": ju_number,
        },
        "palace": {
            "number": palace_number,
            "name": palace["name"],
            "direction": palace["direction"],
            "element": palace_element,
            "icon": palace["icon"]
        },
        "components": {
            "heaven_stem": STEMS[stem_idx],
            "earth_stem": STEMS[earth_stem_idx],
            "star": {
                "chinese": star_cn,
                "english": star["english"],
                "element": star["element"],
                "nature": star["nature"],
                "strength": calculate_strength(star["element"], palace_element)
            },
            "door": {
                "chinese": door_cn,
                "english": door["english"],
                "element": door["element"],
                "nature": door["nature"],
                "strength": calculate_strength(door["element"], palace_element)
            },
            "deity": {
                "chinese": deity_cn,
                "english": deity["english"],
                "nature": deity["nature"]
            }
        },
        "formation": formation
    }
    
    # Calculate verdict
    natures = [star["nature"], door["nature"], deity["nature"]]
    auspicious = sum(1 for n in natures if "Auspicious" in n)
    inauspicious = sum(1 for n in natures if "Inauspicious" in n)
    
    if auspicious >= 2:
        chart["verdict"] = {"text": "Auspicious 吉", "type": "success", "advice": "Favorable for action. Proceed with confidence."}
    elif inauspicious >= 2:
        chart["verdict"] = {"text": "Inauspicious 凶", "type": "error", "advice": "Caution advised. Consider alternative timing."}
    else:
        chart["verdict"] = {"text": "Neutral 平", "type": "warning", "advice": "Mixed signals. Proceed with awareness."}
    
    return chart

# ============ PAGE CONTENT ============

st.title("📈 Chart Generator 奇门起盘")

# Input Section
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_date = st.date_input("📅 Date 日期", value=datetime.now().date())

with col2:
    time_input = st.text_input("⏰ Time (HH:MM)", value=datetime.now().strftime("%H:%M"))
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
        "🏛️ Palace 宫位",
        options=list(PALACES.keys()),
        format_func=lambda x: f"#{x} {PALACES[x]['icon']} {PALACES[x]['name']}",
        index=4
    )

# Generate Button
if st.button("🔮 Generate QMDJ Chart 生成奇门盘", type="primary", use_container_width=True):
    if parsed_time:
        chart = generate_qmdj_chart(selected_date, hour, minute, palace_number)
        st.session_state.current_chart = chart
        st.success("✅ Chart Generated! 盘局已生成!")

# Display Chart Results
if 'current_chart' in st.session_state and st.session_state.current_chart:
    chart = st.session_state.current_chart
    
    st.markdown("---")
    
    # Metadata
    st.markdown(f"### 🏛️ Palace #{chart['palace']['number']} - {chart['palace']['name']}")
    st.markdown(f"**Direction 方位:** {chart['palace']['direction']} | **Element 五行:** {chart['palace']['element']}")
    
    meta_cols = st.columns(4)
    meta_cols[0].metric("📅 Date", chart['metadata']['date'])
    meta_cols[1].metric("⏰ Time", chart['metadata']['time'])
    meta_cols[2].metric("🕐 时辰", chart['metadata']['chinese_hour'])
    meta_cols[3].metric("局", f"{chart['metadata']['structure']} #{chart['metadata']['ju_number']}")
    
    # Components - Using NATIVE Streamlit (no complex HTML!)
    st.markdown("### 📋 Components 组件")
    
    comp_cols = st.columns(5)
    
    # Heaven Stem
    with comp_cols[0]:
        st.markdown("**Heaven Stem 天干**")
        st.markdown(f"### {chart['components']['heaven_stem']}")
    
    # Earth Stem
    with comp_cols[1]:
        st.markdown("**Earth Stem 地干**")
        st.markdown(f"### {chart['components']['earth_stem']}")
    
    # Star
    with comp_cols[2]:
        star = chart['components']['star']
        st.markdown("**Star 九星**")
        st.markdown(f"### {star['chinese']} {star['english']}")
        nature_color = get_nature_color(star['nature'])
        if nature_color == "green":
            st.success(f"{star['nature']}")
        elif nature_color == "red":
            st.error(f"{star['nature']}")
        else:
            st.warning(f"{star['nature']}")
        st.caption(f"{star['strength'][0]} ({star['strength'][1]:+d})")
    
    # Door
    with comp_cols[3]:
        door = chart['components']['door']
        st.markdown("**Door 八门**")
        st.markdown(f"### {door['chinese']} {door['english']}")
        nature_color = get_nature_color(door['nature'])
        if nature_color == "green":
            st.success(f"{door['nature']}")
        elif nature_color == "red":
            st.error(f"{door['nature']}")
        else:
            st.warning(f"{door['nature']}")
        st.caption(f"{door['strength'][0]} ({door['strength'][1]:+d})")
    
    # Deity
    with comp_cols[4]:
        deity = chart['components']['deity']
        st.markdown("**Deity 八神**")
        st.markdown(f"### {deity['chinese']} {deity['english']}")
        nature_color = get_nature_color(deity['nature'])
        if nature_color == "green":
            st.success(f"{deity['nature']}")
        elif nature_color == "red":
            st.error(f"{deity['nature']}")
        else:
            st.warning(f"{deity['nature']}")
    
    # Formation
    if chart.get('formation'):
        st.markdown("---")
        st.markdown("### 🌟 Formation Detected! 格局发现!")
        formation = chart['formation']
        nature_color = get_nature_color(formation['nature'])
        
        if nature_color == "green":
            st.success(f"**{formation['chinese']}** - {formation['english']}")
        elif nature_color == "red":
            st.error(f"**{formation['chinese']}** - {formation['english']}")
        else:
            st.warning(f"**{formation['chinese']}** - {formation['english']}")
        
        st.markdown(f"**Nature:** {formation['nature']} | **Meaning:** {formation['meaning']}")
    
    # Verdict
    st.markdown("---")
    st.markdown("### 📝 Verdict 判断")
    
    verdict = chart['verdict']
    if verdict['type'] == 'success':
        st.success(f"## {verdict['text']}")
    elif verdict['type'] == 'error':
        st.error(f"## {verdict['text']}")
    else:
        st.warning(f"## {verdict['text']}")
    
    st.markdown(f"**Advice:** {verdict['advice']}")
    
    # Export Options
    st.markdown("---")
    st.markdown("### 📤 Export")
    
    export_cols = st.columns(2)
    
    with export_cols[0]:
        json_str = json.dumps(chart, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Download JSON",
            data=json_str,
            file_name=f"qmdj_{chart['metadata']['date']}_{chart['metadata']['time'].replace(':', '')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with export_cols[1]:
        if st.button("📋 Show JSON", use_container_width=True):
            st.json(chart)
    
    # Save to history
    if 'analyses' not in st.session_state:
        st.session_state.analyses = []
    
    # Check if already saved
    existing = [a for a in st.session_state.analyses 
                if a.get('date') == chart['metadata']['date'] 
                and a.get('time') == chart['metadata']['time']
                and a.get('palace') == chart['palace']['number']]
    
    if not existing:
        st.session_state.analyses.append({
            "date": chart['metadata']['date'],
            "time": chart['metadata']['time'],
            "palace": chart['palace']['number'],
            "verdict": verdict['text'],
            "formation": chart['formation']['english'] if chart.get('formation') else None,
            "generated_at": datetime.now().isoformat()
        })

# Footer
st.markdown("---")
st.caption("📈 Qi Men Pro Chart Generator | Phase 3 | Joey Yap Methodology")
