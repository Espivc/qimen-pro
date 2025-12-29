"""
Qi Men Pro - Chart Generator Page
Phase 3: Enhanced with precise time input and improved calculations
"""

import streamlit as st
from datetime import datetime, date
import json

st.set_page_config(
    page_title="Chart Generator | Qi Men Pro",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============ CONSTANTS ============

PALACES = {
    1: {"name": "坎 Kan", "direction": "N", "element": "Water", "color": "#1E90FF"},
    2: {"name": "坤 Kun", "direction": "SW", "element": "Earth", "color": "#DAA520"},
    3: {"name": "震 Zhen", "direction": "E", "element": "Wood", "color": "#228B22"},
    4: {"name": "巽 Xun", "direction": "SE", "element": "Wood", "color": "#228B22"},
    5: {"name": "中 Center", "direction": "C", "element": "Earth", "color": "#DAA520"},
    6: {"name": "乾 Qian", "direction": "NW", "element": "Metal", "color": "#C0C0C0"},
    7: {"name": "兑 Dui", "direction": "W", "element": "Metal", "color": "#C0C0C0"},
    8: {"name": "艮 Gen", "direction": "NE", "element": "Earth", "color": "#DAA520"},
    9: {"name": "离 Li", "direction": "S", "element": "Fire", "color": "#DC143C"},
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

# Formations from Joey Yap Book #64
FORMATIONS = {
    "伏吟": {"english": "Fu Yin (Hidden Voice)", "nature": "Inauspicious", "meaning": "Stagnation, delay, things hidden"},
    "反吟": {"english": "Fan Yin (Returning Voice)", "nature": "Inauspicious", "meaning": "Reversal, going back, change of mind"},
    "天遁": {"english": "Tian Dun (Heaven Escape)", "nature": "Very Auspicious", "meaning": "Divine help, prayers answered"},
    "地遁": {"english": "Di Dun (Earth Escape)", "nature": "Very Auspicious", "meaning": "Hidden support, secret assistance"},
    "人遁": {"english": "Ren Dun (Human Escape)", "nature": "Auspicious", "meaning": "Help from people, networking success"},
    "神遁": {"english": "Shen Dun (Spirit Escape)", "nature": "Very Auspicious", "meaning": "Spiritual protection, intuition guides"},
    "鬼遁": {"english": "Gui Dun (Ghost Escape)", "nature": "Inauspicious", "meaning": "Deception, hidden enemies"},
    "龙遁": {"english": "Long Dun (Dragon Escape)", "nature": "Auspicious", "meaning": "Power, authority, career success"},
    "虎遁": {"english": "Hu Dun (Tiger Escape)", "nature": "Neutral", "meaning": "Courage needed, calculated risks"},
    "风遁": {"english": "Feng Dun (Wind Escape)", "nature": "Auspicious", "meaning": "Quick success, swift changes"},
    "云遁": {"english": "Yun Dun (Cloud Escape)", "nature": "Neutral", "meaning": "Uncertainty, wait and see"},
}


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
    """Get Chinese double-hour (时辰) for given time"""
    total_minutes = hour * 60 + minute
    
    hour_data = [
        ("子 Zi", 0, "Rat 🐀", "23:00-00:59"),
        ("丑 Chou", 1, "Ox 🐂", "01:00-02:59"),
        ("寅 Yin", 2, "Tiger 🐅", "03:00-04:59"),
        ("卯 Mao", 3, "Rabbit 🐇", "05:00-06:59"),
        ("辰 Chen", 4, "Dragon 🐉", "07:00-08:59"),
        ("巳 Si", 5, "Snake 🐍", "09:00-10:59"),
        ("午 Wu", 6, "Horse 🐴", "11:00-12:59"),
        ("未 Wei", 7, "Goat 🐐", "13:00-14:59"),
        ("申 Shen", 8, "Monkey 🐒", "15:00-16:59"),
        ("酉 You", 9, "Rooster 🐓", "17:00-18:59"),
        ("戌 Xu", 10, "Dog 🐕", "19:00-20:59"),
        ("亥 Hai", 11, "Pig 🐖", "21:00-22:59"),
    ]
    
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return hour_data[0]
    
    idx = (hour + 1) // 2
    if idx >= 12:
        idx = 0
    
    return hour_data[idx]


def determine_structure(month):
    """Determine Yin Dun or Yang Dun based on month"""
    # Yang Dun: Winter Solstice to Summer Solstice (roughly months 12, 1-5)
    # Yin Dun: Summer Solstice to Winter Solstice (roughly months 6-11)
    if month in [12, 1, 2, 3, 4, 5]:
        return "Yang Dun 阳遁"
    else:
        return "Yin Dun 阴遁"


def calculate_ju_number(year, month, day, hour):
    """Calculate Ju number (1-9) - simplified"""
    # This is a simplified calculation
    # Real QMDJ uses solar terms and specific rules
    base = (year + month + day + hour) % 9
    return base if base > 0 else 9


def generate_qmdj_chart(selected_date, hour, minute, palace_number):
    """Generate QMDJ chart data - enhanced calculation"""
    
    # Calculate basic parameters
    structure = determine_structure(selected_date.month)
    ju_number = calculate_ju_number(selected_date.year, selected_date.month, 
                                     selected_date.day, hour)
    chinese_hour = get_chinese_hour(hour, minute)
    
    # Get palace info
    palace = PALACES[palace_number]
    
    # Calculate components (simplified - real version uses kinqimen)
    # Using deterministic calculation based on date/time/palace
    seed = selected_date.year * 10000 + selected_date.month * 100 + selected_date.day + hour + palace_number
    
    stem_idx = seed % 10
    earth_stem_idx = (seed + 3) % 10
    star_idx = seed % 9
    door_idx = seed % 8
    deity_idx = seed % 9
    
    star_keys = list(STARS.keys())
    door_keys = list(DOORS.keys())
    deity_keys = list(DEITIES.keys())
    
    star_cn = star_keys[star_idx]
    door_cn = door_keys[door_idx]
    deity_cn = deity_keys[deity_idx]
    
    star = STARS[star_cn]
    door = DOORS[door_cn]
    deity = DEITIES[deity_cn]
    
    # Calculate element strengths relative to palace element
    palace_element = palace["element"]
    
    def calculate_strength(component_element, palace_element):
        """Calculate strength based on Five Element relationships"""
        cycle = ["Wood", "Fire", "Earth", "Metal", "Water"]
        comp_idx = cycle.index(component_element)
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
    
    # Formation detection (simplified)
    formation = None
    formation_keys = list(FORMATIONS.keys())
    if (seed % 7) == 0:  # Randomly assign formation for demo
        formation_cn = formation_keys[seed % len(formation_keys)]
        formation = {
            "chinese": formation_cn,
            **FORMATIONS[formation_cn]
        }
    
    # Build chart data
    chart = {
        "metadata": {
            "date": selected_date.isoformat(),
            "time": f"{hour:02d}:{minute:02d}",
            "chinese_hour": chinese_hour[0],
            "chinese_hour_animal": chinese_hour[2],
            "structure": structure,
            "ju_number": ju_number,
            "method": "Chai Bu 拆补"
        },
        "palace": {
            "number": palace_number,
            "name": palace["name"],
            "direction": palace["direction"],
            "element": palace["element"]
        },
        "components": {
            "heaven_stem": {
                "chinese": STEMS[stem_idx].split()[0],
                "english": STEMS[stem_idx].split()[1],
                "full": STEMS[stem_idx]
            },
            "earth_stem": {
                "chinese": STEMS[earth_stem_idx].split()[0],
                "english": STEMS[earth_stem_idx].split()[1],
                "full": STEMS[earth_stem_idx]
            },
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
        "formation": formation,
        "analysis": {
            "overall_nature": "Calculating...",
            "recommendation": ""
        }
    }
    
    # Calculate overall nature
    natures = [
        chart["components"]["star"]["nature"],
        chart["components"]["door"]["nature"],
        chart["components"]["deity"]["nature"]
    ]
    
    auspicious_count = natures.count("Auspicious") + natures.count("Very Auspicious")
    inauspicious_count = natures.count("Inauspicious")
    
    if auspicious_count >= 2:
        chart["analysis"]["overall_nature"] = "Auspicious 吉"
        chart["analysis"]["recommendation"] = "Favorable for action. Proceed with confidence."
    elif inauspicious_count >= 2:
        chart["analysis"]["overall_nature"] = "Inauspicious 凶"
        chart["analysis"]["recommendation"] = "Caution advised. Consider postponing or alternative approach."
    else:
        chart["analysis"]["overall_nature"] = "Neutral 平"
        chart["analysis"]["recommendation"] = "Mixed signals. Proceed with awareness and flexibility."
    
    if formation:
        chart["analysis"]["formation_impact"] = formation["meaning"]
    
    return chart


def get_nature_color(nature):
    """Get color based on nature"""
    if "Auspicious" in nature:
        return "#4CAF50"
    elif "Inauspicious" in nature:
        return "#f44336"
    else:
        return "#FFA500"


# ============ PAGE CONTENT ============

st.title("📈 Chart Generator 奇门起盘")

# Input Section
st.markdown("### 📅 Select Date & Time 选择日期时间")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_date = st.date_input(
        "Date 日期",
        value=datetime.now().date(),
        help="Select the date for your QMDJ chart"
    )

with col2:
    # TIME TEXT INPUT (Phase 3 enhancement!)
    time_input = st.text_input(
        "Time (HH:MM) 时间",
        value=datetime.now().strftime("%H:%M"),
        placeholder="e.g., 14:30",
        help="Enter time in 24-hour format (HH:MM)"
    )
    
    parsed_time = parse_time_input(time_input)
    
    if parsed_time:
        hour, minute = parsed_time
        chinese_hour = get_chinese_hour(hour, minute)
        st.success(f"✅ {chinese_hour[0]} ({chinese_hour[2]})")
    else:
        st.error("❌ Invalid format")
        hour, minute = 12, 0

with col3:
    palace_number = st.selectbox(
        "Palace 宫位",
        options=list(PALACES.keys()),
        format_func=lambda x: f"#{x} {PALACES[x]['name']} ({PALACES[x]['direction']})",
        index=4  # Default to Center (5)
    )

# Generate Button
if st.button("🔮 Generate QMDJ Chart 生成奇门盘", type="primary", use_container_width=True):
    if parsed_time:
        with st.spinner("Calculating QMDJ chart... 正在计算奇门盘..."):
            chart = generate_qmdj_chart(selected_date, hour, minute, palace_number)
        
        st.success("✅ Chart Generated! 盘局已生成!")
        
        # Store in session state
        st.session_state.current_chart = chart
        
        # Display Results
        st.markdown("---")
        st.markdown("## 📊 Chart Results 盘局结果")
        
        # Metadata
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        
        with meta_col1:
            st.markdown(f"""
            **📅 Date 日期:** {chart['metadata']['date']}  
            **⏰ Time 时间:** {chart['metadata']['time']}
            """)
        
        with meta_col2:
            st.markdown(f"""
            **🕐 时辰:** {chart['metadata']['chinese_hour']} ({chart['metadata']['chinese_hour_animal']})  
            **Structure 局:** {chart['metadata']['structure']}
            """)
        
        with meta_col3:
            st.markdown(f"""
            **Ju Number 局数:** {chart['metadata']['ju_number']}  
            **Method 方法:** {chart['metadata']['method']}
            """)
        
        st.markdown("---")
        
        # Palace Info
        palace = chart['palace']
        st.markdown(f"""
        ### 🏛️ Palace #{palace['number']} - {palace['name']}
        **Direction 方位:** {palace['direction']} | **Element 五行:** {palace['element']}
        """)
        
        # Components Display
        st.markdown("### 📋 Components 组件")
        
        comp_cols = st.columns(5)
        
        components = [
            ("Heaven Stem\n天干", chart['components']['heaven_stem']['full'], None, None),
            ("Earth Stem\n地干", chart['components']['earth_stem']['full'], None, None),
            ("Star\n九星", f"{chart['components']['star']['chinese']}\n{chart['components']['star']['english']}", 
             chart['components']['star']['nature'], chart['components']['star']['strength']),
            ("Door\n八门", f"{chart['components']['door']['chinese']}\n{chart['components']['door']['english']}", 
             chart['components']['door']['nature'], chart['components']['door']['strength']),
            ("Deity\n八神", f"{chart['components']['deity']['chinese']}\n{chart['components']['deity']['english']}", 
             chart['components']['deity']['nature'], None),
        ]
        
        for col, (label, value, nature, strength) in zip(comp_cols, components):
            with col:
                nature_color = get_nature_color(nature) if nature else "#d4af37"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            padding: 15px; border-radius: 10px; text-align: center;
                            border: 2px solid {nature_color}; min-height: 150px;">
                    <p style="color: #888; font-size: 0.8em; margin-bottom: 10px;">{label}</p>
                    <p style="font-size: 1.2em; color: white;">{value}</p>
                    {f'<p style="color: {nature_color}; font-size: 0.9em; margin-top: 10px;">{nature}</p>' if nature else ''}
                    {f'<p style="color: #888; font-size: 0.8em;">{strength[0]} ({strength[1]:+d})</p>' if strength else ''}
                </div>
                """, unsafe_allow_html=True)
        
        # Formation
        if chart['formation']:
            st.markdown("---")
            formation = chart['formation']
            nature_color = get_nature_color(formation['nature'])
            
            st.markdown(f"""
            ### 🌟 Formation Detected! 格局发现!
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                        padding: 20px; border-radius: 10px; border: 2px solid {nature_color};">
                <h4 style="color: {nature_color};">{formation['chinese']} - {formation['english']}</h4>
                <p><strong>Nature:</strong> {formation['nature']}</p>
                <p><strong>Meaning:</strong> {formation['meaning']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Analysis Summary
        st.markdown("---")
        st.markdown("### 📝 Analysis Summary 分析总结")
        
        analysis = chart['analysis']
        nature_color = get_nature_color(analysis['overall_nature'])
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 25px; border-radius: 15px; border: 3px solid {nature_color};">
            <h3 style="color: {nature_color}; text-align: center;">{analysis['overall_nature']}</h3>
            <p style="text-align: center; font-size: 1.1em;">{analysis['recommendation']}</p>
            {f"<p style='text-align: center; color: #888; margin-top: 15px;'><em>Formation Impact: {analysis.get('formation_impact', 'N/A')}</em></p>" if chart['formation'] else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Export Options
        st.markdown("---")
        st.markdown("### 📤 Export Options")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            json_str = json.dumps(chart, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"qmdj_chart_{selected_date}_{hour:02d}{minute:02d}.json",
                mime="application/json"
            )
        
        with export_col2:
            if st.button("📋 Copy to Clipboard"):
                st.code(json_str, language="json")
                st.info("Copy the JSON above manually (Ctrl+C / Cmd+C)")
        
        # Save to history
        if 'analyses' not in st.session_state:
            st.session_state.analyses = []
        
        st.session_state.analyses.append({
            "date": selected_date.isoformat(),
            "time": f"{hour:02d}:{minute:02d}",
            "palace": palace_number,
            "verdict": analysis['overall_nature'],
            "formation": chart['formation']['english'] if chart['formation'] else None,
            "generated_at": datetime.now().isoformat()
        })
        
    else:
        st.error("❌ Please enter a valid time in HH:MM format")

# Footer
st.markdown("---")
st.caption("📈 Qi Men Pro Chart Generator | Phase 3 | Joey Yap Methodology")
