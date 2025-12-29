"""
Qi Men Pro - Settings Page
Phase 3: Enhanced BaZi Calculator with precise time input
"""

import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="Settings | Qi Men Pro",
    page_icon="⚙️",
    layout="wide"
)

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============ BAZI CALCULATOR FUNCTIONS ============

# Heavenly Stems
STEMS = ["甲 Jia", "乙 Yi", "丙 Bing", "丁 Ding", "戊 Wu", 
         "己 Ji", "庚 Geng", "辛 Xin", "壬 Ren", "癸 Gui"]

STEM_ELEMENTS = {
    "甲 Jia": ("Wood 木", "Yang"),
    "乙 Yi": ("Wood 木", "Yin"),
    "丙 Bing": ("Fire 火", "Yang"),
    "丁 Ding": ("Fire 火", "Yin"),
    "戊 Wu": ("Earth 土", "Yang"),
    "己 Ji": ("Earth 土", "Yin"),
    "庚 Geng": ("Metal 金", "Yang"),
    "辛 Xin": ("Metal 金", "Yin"),
    "壬 Ren": ("Water 水", "Yang"),
    "癸 Gui": ("Water 水", "Yin"),
}

# Earthly Branches
BRANCHES = ["子 Zi", "丑 Chou", "寅 Yin", "卯 Mao", "辰 Chen", "巳 Si",
            "午 Wu", "未 Wei", "申 Shen", "酉 You", "戌 Xu", "亥 Hai"]

BRANCH_ANIMALS = {
    "子 Zi": "Rat 🐀",
    "丑 Chou": "Ox 🐂",
    "寅 Yin": "Tiger 🐅",
    "卯 Mao": "Rabbit 🐇",
    "辰 Chen": "Dragon 🐉",
    "巳 Si": "Snake 🐍",
    "午 Wu": "Horse 🐴",
    "未 Wei": "Goat 🐐",
    "申 Shen": "Monkey 🐒",
    "酉 You": "Rooster 🐓",
    "戌 Xu": "Dog 🐕",
    "亥 Hai": "Pig 🐖",
}

TEN_GODS = {
    "Friend": "比肩 Bi Jian - Competitor, peer, sibling energy",
    "Rob Wealth": "劫财 Jie Cai - Risk-taker, aggressive competitor",
    "Eating God": "食神 Shi Shen - Creative, artistic, easy-going",
    "Hurting Officer": "伤官 Shang Guan - Rebellious, innovative, critical",
    "Direct Wealth": "正财 Zheng Cai - Steady income, practical, hardworking",
    "Indirect Wealth": "偏财 Pian Cai - Windfall, speculative, entrepreneurial",
    "Direct Officer": "正官 Zheng Guan - Authority, status, conventional",
    "7 Killings": "七杀 Qi Sha - Ambitious, competitive, warrior spirit",
    "Direct Resource": "正印 Zheng Yin - Learning, nurturing, traditional knowledge",
    "Indirect Resource": "偏印 Pian Yin - Unconventional wisdom, intuition, esoteric"
}

PROFILES = {
    "Friend": ("Competitor", "💪"),
    "Rob Wealth": ("Risk Taker", "🎲"),
    "Eating God": ("Artist", "🎨"),
    "Hurting Officer": ("Innovator", "💡"),
    "Direct Wealth": ("Worker", "🔧"),
    "Indirect Wealth": ("Pioneer", "🎯"),
    "Direct Officer": ("Manager", "👔"),
    "7 Killings": ("Warrior", "⚔️"),
    "Direct Resource": ("Philosopher", "📚"),
    "Indirect Resource": ("Mystic", "🔮")
}


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


def get_hour_branch(hour, minute=0):
    """Get the Earthly Branch for a given hour (with minute precision)"""
    # Handle late-night 子时 (23:00-00:59)
    total_minutes = hour * 60 + minute
    
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return 0  # 子 Zi
    
    # Each 时辰 is 2 hours
    # 01:00-02:59 = 丑 Chou (index 1)
    # 03:00-04:59 = 寅 Yin (index 2)
    # etc.
    branch_index = (hour + 1) // 2
    if branch_index >= 12:
        branch_index = 0
    
    return branch_index


def calculate_year_pillar(year):
    """Calculate Year Pillar (年柱) - simplified"""
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return STEMS[stem_index], BRANCHES[branch_index]


def calculate_month_pillar(year, month, day):
    """Calculate Month Pillar (月柱) - simplified using solar terms approximation"""
    # Simplified: using month directly (proper version needs solar terms 节气)
    # This is an approximation - real BaZi uses 24 solar terms
    
    # Adjust for solar terms (approximate - day > 5 uses current month)
    adjusted_month = month if day >= 5 else (month - 1 if month > 1 else 12)
    
    year_stem_index = (year - 4) % 10
    # Month stem calculation (based on year stem)
    month_stem_base = (year_stem_index % 5) * 2
    month_stem_index = (month_stem_base + adjusted_month - 1) % 10
    
    # Month branch is fixed: 寅=1月, 卯=2月, etc. (starts from 寅 Yin for month 1)
    month_branch_index = (adjusted_month + 1) % 12
    
    return STEMS[month_stem_index], BRANCHES[month_branch_index]


def calculate_day_pillar(year, month, day):
    """Calculate Day Pillar (日柱) using a simplified algorithm"""
    # This is a simplified calculation
    # Real BaZi uses the 10,000 year calendar (万年历)
    
    from datetime import date as dt_date
    
    # Reference date: 1900-01-01 was 甲子 (Jia-Zi) day
    ref_date = dt_date(1900, 1, 1)
    target_date = dt_date(year, month, day)
    
    days_diff = (target_date - ref_date).days
    
    # Adjust for the actual reference (1900-01-01 was actually 甲戌)
    # Using 甲子 as base, offset by 10 for stem and 10 for branch
    stem_index = (days_diff + 10) % 10
    branch_index = (days_diff + 10) % 12
    
    return STEMS[stem_index], BRANCHES[branch_index]


def calculate_hour_pillar(day_stem, hour, minute=0):
    """Calculate Hour Pillar (时柱)"""
    hour_branch_index = get_hour_branch(hour, minute)
    
    # Hour stem is based on Day stem
    day_stem_index = STEMS.index(day_stem)
    hour_stem_base = (day_stem_index % 5) * 2
    hour_stem_index = (hour_stem_base + hour_branch_index) % 10
    
    return STEMS[hour_stem_index], BRANCHES[hour_branch_index]


def analyze_day_master(day_stem):
    """Analyze Day Master strength and useful gods"""
    element, polarity = STEM_ELEMENTS[day_stem]
    
    # Simplified strength analysis
    # In real BaZi, this requires analyzing the entire chart
    analysis = {
        "day_master": day_stem,
        "element": element,
        "polarity": polarity,
        "strength": "Moderate",  # Simplified - real analysis is complex
        "useful_gods": [],
        "unfavorable": [],
        "profile": ""
    }
    
    # Determine useful gods based on element (simplified logic)
    element_short = element.split()[0]  # Get just "Wood", "Fire", etc.
    
    element_cycle = ["Wood", "Fire", "Earth", "Metal", "Water"]
    elem_idx = element_cycle.index(element_short)
    
    # For weak Day Master, useful gods are: Resource (produces DM) and Friend (same)
    # For strong Day Master, useful gods are: Wealth, Officer, Output
    
    # Simplified: assume moderate-weak, so support elements are useful
    resource_elem = element_cycle[(elem_idx - 1) % 5]  # Element that produces DM
    same_elem = element_short  # Same element
    
    analysis["useful_gods"] = [f"{resource_elem}", f"{same_elem}"]
    
    # Unfavorable: what DM produces and what controls DM
    output_elem = element_cycle[(elem_idx + 1) % 5]
    controller_elem = element_cycle[(elem_idx + 2) % 5]
    
    analysis["unfavorable"] = [f"{controller_elem}", f"{output_elem}"]
    
    # Profile based on dominant Ten God (simplified - assumes Indirect Wealth for variety)
    analysis["profile"] = "Pioneer 🎯 (Indirect Wealth 偏财)"
    
    return analysis


def calculate_full_bazi(year, month, day, hour, minute=0):
    """Calculate complete Four Pillars"""
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

tab1, tab2, tab3 = st.tabs(["🧮 BaZi Calculator 八字计算器", "👤 Profile 个人档案", "🌐 Preferences 偏好设置"])

# ============ TAB 1: BAZI CALCULATOR ============
with tab1:
    st.markdown("### 🎂 Birthday Calculator 生日计算器")
    st.markdown("Enter your birth details to calculate your Four Pillars (四柱八字)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Birth Date 出生日期")
        birth_date = st.date_input(
            "Select your birth date",
            value=date(1985, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Use the SOLAR calendar (阳历), not lunar calendar"
        )
        
        st.info("💡 **Important:** BaZi uses the **Solar Calendar (阳历)**, NOT the Lunar Calendar (农历)!")
    
    with col2:
        st.markdown("#### ⏰ Birth Time 出生时间")
        
        # TEXT INPUT for time (Phase 3 enhancement!)
        time_input = st.text_input(
            "Enter exact birth time (HH:MM) 输入出生时间",
            value="12:00",
            placeholder="e.g., 09:30, 14:45, 23:15",
            help="24-hour format. Example: 09:30 for 9:30 AM, 14:45 for 2:45 PM"
        )
        
        parsed_time = parse_time_input(time_input)
        
        if parsed_time:
            hour, minute = parsed_time
            branch_idx = get_hour_branch(hour, minute)
            chinese_hour = BRANCHES[branch_idx]
            animal = BRANCH_ANIMALS[chinese_hour]
            
            st.success(f"✅ **{chinese_hour}时** ({animal})")
            
            # Show the time range for this 时辰
            hour_ranges = [
                "23:00-00:59", "01:00-02:59", "03:00-04:59", "05:00-06:59",
                "07:00-08:59", "09:00-10:59", "11:00-12:59", "13:00-14:59",
                "15:00-16:59", "17:00-18:59", "19:00-20:59", "21:00-22:59"
            ]
            st.caption(f"时辰 range: {hour_ranges[branch_idx]}")
        else:
            st.error("❌ Invalid time format. Please use HH:MM (e.g., 14:30)")
        
        st.markdown("")
        st.markdown("**💡 Tip for boundary times:**")
        st.caption("If born near hour boundaries (e.g., 00:58, 02:59), the exact minute matters for accuracy!")
    
    # Calculate button
    st.markdown("---")
    
    if st.button("🔮 Calculate BaZi 计算八字", type="primary", use_container_width=True):
        if parsed_time:
            hour, minute = parsed_time
            
            with st.spinner("Calculating your Four Pillars... 正在计算四柱..."):
                bazi = calculate_full_bazi(
                    birth_date.year,
                    birth_date.month,
                    birth_date.day,
                    hour,
                    minute
                )
            
            st.success("✅ Calculation Complete! 计算完成!")
            
            # Display Four Pillars
            st.markdown("### 📊 Your Four Pillars 四柱八字")
            
            # Create visual display
            pillar_cols = st.columns(4)
            pillar_names = [
                ("Hour 时柱", bazi["hour"]),
                ("Day 日柱", bazi["day"]),
                ("Month 月柱", bazi["month"]),
                ("Year 年柱", bazi["year"])
            ]
            
            for col, (name, pillar) in zip(pillar_cols, pillar_names):
                with col:
                    stem_elem, stem_pol = STEM_ELEMENTS[pillar["stem"]]
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                                padding: 15px; border-radius: 10px; text-align: center;
                                border: 1px solid #d4af37;">
                        <p style="color: #d4af37; margin-bottom: 5px; font-size: 0.9em;">{name}</p>
                        <p style="font-size: 1.8em; margin: 5px 0;">{pillar['stem'].split()[0]}</p>
                        <p style="font-size: 1.8em; margin: 5px 0;">{pillar['branch'].split()[0]}</p>
                        <p style="color: #888; font-size: 0.8em; margin-top: 10px;">{stem_elem}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if "animal" in pillar:
                        st.caption(f"{pillar['animal']}")
            
            # Day Master Analysis
            st.markdown("---")
            st.markdown("### 🌟 Day Master Analysis 日主分析")
            
            analysis = bazi["day_master_analysis"]
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                st.markdown(f"""
                **日主 Day Master:** {analysis['day_master']}  
                **五行 Element:** {analysis['element']}  
                **阴阳 Polarity:** {analysis['polarity']}  
                **强弱 Strength:** {analysis['strength']}
                """)
            
            with analysis_col2:
                st.markdown(f"""
                **用神 Useful Gods:** {', '.join(analysis['useful_gods'])}  
                **忌神 Unfavorable:** {', '.join(analysis['unfavorable'])}  
                **性格 Profile:** {analysis['profile']}
                """)
            
            # Save to profile button
            st.markdown("---")
            if st.button("💾 Save as My Profile 保存为我的档案", use_container_width=True):
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
                st.success("✅ Profile saved! 档案已保存!")
                st.balloons()
                st.info("👉 **Go to Dashboard** to see your updated profile!")
                
                # Add button to go to dashboard
                if st.button("🏠 Go to Dashboard 返回首页"):
                    st.switch_page("app.py")
        else:
            st.error("❌ Please enter a valid birth time in HH:MM format")

# ============ TAB 2: PROFILE ============
with tab2:
    st.markdown("### 👤 Your Current Profile 您的当前档案")
    
    if 'user_profile' in st.session_state and st.session_state.user_profile:
        profile = st.session_state.user_profile
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid #d4af37;">
            <h3 style="color: #d4af37; text-align: center;">📜 BaZi Profile Card</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div>
                    <p style="color: #d4af37;">日主 Day Master</p>
                    <p style="font-size: 1.5em;">{profile.get('day_master', 'Not set')}</p>
                </div>
                <div>
                    <p style="color: #d4af37;">五行 Element</p>
                    <p style="font-size: 1.2em;">{profile.get('element', 'Not set')} • {profile.get('polarity', '')}</p>
                </div>
                <div>
                    <p style="color: #d4af37;">强弱 Strength</p>
                    <p style="font-size: 1.2em;">{profile.get('strength', 'Not set')}</p>
                </div>
                <div>
                    <p style="color: #d4af37;">性格 Profile</p>
                    <p style="font-size: 1.2em;">{profile.get('profile', 'Not set')}</p>
                </div>
            </div>
            
            <hr style="border-color: #d4af37; margin: 20px 0;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p style="color: #4CAF50;">✅ 用神 Useful Gods</p>
                    <p>{', '.join(profile.get('useful_gods', ['Not set']))}</p>
                </div>
                <div>
                    <p style="color: #f44336;">❌ 忌神 Unfavorable</p>
                    <p>{', '.join(profile.get('unfavorable', ['Not set']))}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show birth details if available
        if 'birth_date' in profile:
            st.markdown("---")
            st.markdown(f"**Birth Date:** {profile.get('birth_date', 'N/A')}")
            st.markdown(f"**Birth Time:** {profile.get('birth_time', 'N/A')}")
    else:
        st.info("No profile saved yet. Use the BaZi Calculator to create your profile!")

# ============ TAB 3: PREFERENCES ============
with tab3:
    st.markdown("### 🌐 Language & Display 语言与显示")
    
    language = st.selectbox(
        "Language Mode 语言模式",
        options=["mixed", "english", "chinese"],
        index=0,
        format_func=lambda x: {
            "mixed": "🌏 Mixed (English + 中文)",
            "english": "🇬🇧 English Only",
            "chinese": "🇨🇳 中文 Only"
        }[x]
    )
    
    if st.button("Save Language Preference"):
        st.session_state.language = language
        st.success(f"✅ Language set to: {language}")
    
    st.markdown("---")
    st.markdown("### 🗑️ Data Management 数据管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Analyses", type="secondary"):
            st.session_state.analyses = []
            st.success("✅ All analyses cleared!")
    
    with col2:
        if st.button("🔄 Reset Profile", type="secondary"):
            st.session_state.user_profile = {}
            st.success("✅ Profile reset!")

# Footer
st.markdown("---")
st.caption("⚙️ Qi Men Pro Settings | Phase 3 | v2.0")
