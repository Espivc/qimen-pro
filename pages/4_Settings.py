"""
Qi Men Pro - Settings Page
Phase 3: Fixed save with proper session state update
"""

import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="Settings | Qi Men Pro",
    page_icon="⚙️",
    layout="wide"
)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Initialize session state if needed
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

if 'profile_saved' not in st.session_state:
    st.session_state.profile_saved = False

# ============ BAZI CONSTANTS ============

STEMS = ["甲 Jia", "乙 Yi", "丙 Bing", "丁 Ding", "戊 Wu", 
         "己 Ji", "庚 Geng", "辛 Xin", "壬 Ren", "癸 Gui"]

STEM_ELEMENTS = {
    "甲 Jia": ("Wood 木", "Yang"), "乙 Yi": ("Wood 木", "Yin"),
    "丙 Bing": ("Fire 火", "Yang"), "丁 Ding": ("Fire 火", "Yin"),
    "戊 Wu": ("Earth 土", "Yang"), "己 Ji": ("Earth 土", "Yin"),
    "庚 Geng": ("Metal 金", "Yang"), "辛 Xin": ("Metal 金", "Yin"),
    "壬 Ren": ("Water 水", "Yang"), "癸 Gui": ("Water 水", "Yin"),
}

BRANCHES = ["子 Zi", "丑 Chou", "寅 Yin", "卯 Mao", "辰 Chen", "巳 Si",
            "午 Wu", "未 Wei", "申 Shen", "酉 You", "戌 Xu", "亥 Hai"]

BRANCH_ANIMALS = {
    "子 Zi": "Rat 🐀", "丑 Chou": "Ox 🐂", "寅 Yin": "Tiger 🐅",
    "卯 Mao": "Rabbit 🐇", "辰 Chen": "Dragon 🐉", "巳 Si": "Snake 🐍",
    "午 Wu": "Horse 🐴", "未 Wei": "Goat 🐐", "申 Shen": "Monkey 🐒",
    "酉 You": "Rooster 🐓", "戌 Xu": "Dog 🐕", "亥 Hai": "Pig 🐖",
}

# ============ CALCULATION FUNCTIONS ============

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

def get_hour_branch(hour, minute=0):
    total_minutes = hour * 60 + minute
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return 0
    branch_index = (hour + 1) // 2
    return branch_index if branch_index < 12 else 0

def calculate_year_pillar(year):
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return STEMS[stem_index], BRANCHES[branch_index]

def calculate_month_pillar(year, month, day):
    adjusted_month = month if day >= 5 else (month - 1 if month > 1 else 12)
    year_stem_index = (year - 4) % 10
    month_stem_base = (year_stem_index % 5) * 2
    month_stem_index = (month_stem_base + adjusted_month - 1) % 10
    month_branch_index = (adjusted_month + 1) % 12
    return STEMS[month_stem_index], BRANCHES[month_branch_index]

def calculate_day_pillar(year, month, day):
    from datetime import date as dt_date
    ref_date = dt_date(1900, 1, 1)
    target_date = dt_date(year, month, day)
    days_diff = (target_date - ref_date).days
    stem_index = (days_diff + 10) % 10
    branch_index = (days_diff + 10) % 12
    return STEMS[stem_index], BRANCHES[branch_index]

def calculate_hour_pillar(day_stem, hour, minute=0):
    hour_branch_index = get_hour_branch(hour, minute)
    day_stem_index = STEMS.index(day_stem)
    hour_stem_base = (day_stem_index % 5) * 2
    hour_stem_index = (hour_stem_base + hour_branch_index) % 10
    return STEMS[hour_stem_index], BRANCHES[hour_branch_index]

def analyze_day_master(day_stem):
    element, polarity = STEM_ELEMENTS[day_stem]
    element_short = element.split()[0]
    element_cycle = ["Wood", "Fire", "Earth", "Metal", "Water"]
    elem_idx = element_cycle.index(element_short)
    
    resource_elem = element_cycle[(elem_idx - 1) % 5]
    same_elem = element_short
    output_elem = element_cycle[(elem_idx + 1) % 5]
    controller_elem = element_cycle[(elem_idx + 2) % 5]
    
    return {
        "day_master": day_stem,
        "element": element,
        "polarity": polarity,
        "strength": "Moderate",
        "useful_gods": [resource_elem, same_elem],
        "unfavorable": [controller_elem, output_elem],
        "profile": "Pioneer 🎯 (Indirect Wealth 偏财)"
    }

def calculate_full_bazi(year, month, day, hour, minute=0):
    year_stem, year_branch = calculate_year_pillar(year)
    month_stem, month_branch = calculate_month_pillar(year, month, day)
    day_stem, day_branch = calculate_day_pillar(year, month, day)
    hour_stem, hour_branch = calculate_hour_pillar(day_stem, hour, minute)
    
    return {
        "year": {"stem": year_stem, "branch": year_branch, "animal": BRANCH_ANIMALS[year_branch]},
        "month": {"stem": month_stem, "branch": month_branch},
        "day": {"stem": day_stem, "branch": day_branch},
        "hour": {"stem": hour_stem, "branch": hour_branch},
        "day_master_analysis": analyze_day_master(day_stem)
    }

# ============ PAGE CONTENT ============

st.title("⚙️ Settings 设置")

# Check if profile was just saved
if st.session_state.profile_saved:
    st.success("✅ Profile saved successfully! 档案已保存!")
    st.session_state.profile_saved = False

tab1, tab2, tab3 = st.tabs(["🧮 BaZi Calculator", "👤 Profile", "🌐 Preferences"])

# ============ TAB 1: CALCULATOR ============
with tab1:
    st.markdown("### 🎂 Birthday Calculator 生日计算器")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Birth Date 出生日期")
        birth_date = st.date_input(
            "Select your birth date",
            value=date(1985, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
        st.info("💡 BaZi uses **Solar Calendar (阳历)**, NOT Lunar!")
    
    with col2:
        st.markdown("#### ⏰ Birth Time 出生时间")
        time_input = st.text_input(
            "Enter birth time (HH:MM)",
            value="12:00",
            placeholder="e.g., 09:30, 14:45"
        )
        
        parsed_time = parse_time_input(time_input)
        if parsed_time:
            hour, minute = parsed_time
            branch_idx = get_hour_branch(hour, minute)
            chinese_hour = BRANCHES[branch_idx]
            animal = BRANCH_ANIMALS[chinese_hour]
            st.success(f"✅ {chinese_hour}时 ({animal})")
        else:
            st.error("❌ Invalid format")
            hour, minute = 12, 0
    
    st.markdown("---")
    
    if st.button("🔮 Calculate BaZi 计算八字", type="primary", use_container_width=True):
        if parsed_time:
            hour, minute = parsed_time
            bazi = calculate_full_bazi(birth_date.year, birth_date.month, birth_date.day, hour, minute)
            
            st.success("✅ Calculation Complete! 计算完成!")
            
            # Display Four Pillars
            st.markdown("### 📊 Your Four Pillars 四柱八字")
            
            pillar_cols = st.columns(4)
            pillars = [
                ("Hour 时柱", bazi["hour"]),
                ("Day 日柱", bazi["day"]),
                ("Month 月柱", bazi["month"]),
                ("Year 年柱", bazi["year"])
            ]
            
            for col, (name, pillar) in zip(pillar_cols, pillars):
                with col:
                    stem_elem, _ = STEM_ELEMENTS[pillar["stem"]]
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                                padding: 15px; border-radius: 10px; text-align: center;
                                border: 1px solid #d4af37;">
                        <p style="color: #d4af37; margin-bottom: 5px;">{name}</p>
                        <p style="font-size: 1.8em; margin: 5px 0;">{pillar['stem'].split()[0]}</p>
                        <p style="font-size: 1.8em; margin: 5px 0;">{pillar['branch'].split()[0]}</p>
                        <p style="color: #888; font-size: 0.8em;">{stem_elem}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if "animal" in pillar:
                        st.caption(pillar['animal'])
            
            # Analysis
            st.markdown("---")
            st.markdown("### 🌟 Day Master Analysis 日主分析")
            
            analysis = bazi["day_master_analysis"]
            
            a_col1, a_col2 = st.columns(2)
            with a_col1:
                st.markdown(f"""
                **日主 Day Master:** {analysis['day_master']}  
                **五行 Element:** {analysis['element']}  
                **阴阳 Polarity:** {analysis['polarity']}  
                **强弱 Strength:** {analysis['strength']}
                """)
            with a_col2:
                st.markdown(f"""
                **用神 Useful Gods:** {', '.join(analysis['useful_gods'])}  
                **忌神 Unfavorable:** {', '.join(analysis['unfavorable'])}  
                **性格 Profile:** {analysis['profile']}
                """)
            
            # Store calculated data for save button
            st.session_state.calculated_bazi = {
                "bazi": bazi,
                "analysis": analysis,
                "birth_date": birth_date.isoformat(),
                "birth_time": f"{hour:02d}:{minute:02d}"
            }
            
            # Save button
            st.markdown("---")
            if st.button("💾 Save as My Profile 保存为我的档案", type="primary", use_container_width=True):
                # Update session state with new profile
                st.session_state.user_profile = {
                    "day_master": analysis['day_master'],
                    "element": analysis['element'],
                    "polarity": analysis['polarity'],
                    "strength": analysis['strength'],
                    "useful_gods": analysis['useful_gods'],
                    "unfavorable": analysis['unfavorable'],
                    "profile": analysis['profile'],
                    "birth_date": birth_date.isoformat(),
                    "birth_time": f"{hour:02d}:{minute:02d}",
                    "four_pillars": bazi
                }
                st.session_state.profile_saved = True
                st.rerun()  # Force refresh to show success message

# ============ TAB 2: PROFILE ============
with tab2:
    st.markdown("### 👤 Your Current Profile")
    
    profile = st.session_state.user_profile
    
    if profile and profile.get('day_master'):
        st.markdown("#### 日主 Day Master")
        st.markdown(f"## {profile.get('day_master', 'Not set')}")
        st.caption(f"{profile.get('element', '')} • {profile.get('polarity', '')} • {profile.get('strength', '')}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 用神 Useful Gods")
            useful = profile.get('useful_gods', [])
            if useful:
                st.success(' • '.join(str(g) for g in useful))
            else:
                st.info("Not set")
        
        with col2:
            st.markdown("#### 忌神 Unfavorable")
            unfav = profile.get('unfavorable', [])
            if unfav:
                st.error(' • '.join(str(u) for u in unfav))
            else:
                st.info("Not set")
        
        st.markdown("#### 性格 Profile")
        st.info(profile.get('profile', 'Not set'))
        
        if profile.get('birth_date'):
            st.markdown("---")
            st.caption(f"📅 Birth: {profile.get('birth_date')} {profile.get('birth_time', '')}")
    else:
        st.info("No profile saved. Use the BaZi Calculator to create your profile!")

# ============ TAB 3: PREFERENCES ============
with tab3:
    st.markdown("### 🌐 Preferences")
    
    st.markdown("#### 🗑️ Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear All Analyses"):
            st.session_state.analyses = []
            st.success("✅ Cleared!")
    with col2:
        if st.button("🔄 Reset Profile"):
            st.session_state.user_profile = {}
            st.success("✅ Reset!")
            st.rerun()

st.markdown("---")
st.caption("⚙️ Qi Men Pro Settings | Phase 3")
