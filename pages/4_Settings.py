"""
Settings Page - Qi Men Pro v2.0
Profile configuration and database management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import ELEMENT_EMOJI
from utils.bazi_profile import (
    load_profile, save_profile, get_default_profile,
    DAY_MASTER_OPTIONS, TEN_GOD_PROFILE_OPTIONS
)
from utils.database import get_all_records, get_statistics, clear_database, export_to_csv_string
from utils.bazi_calculator import calculate_full_profile, get_hour_branch_name, EARTHLY_BRANCHES

st.set_page_config(
    page_title="Settings 设置 - Qi Men Pro",
    page_icon="⚙️",
    layout="wide"
)

# Element colors
ELEMENT_COLORS = {
    "Wood": "#4CAF50",
    "Fire": "#F44336",
    "Earth": "#CD853F",
    "Metal": "#C0C0C0",
    "Water": "#4169E1"
}

ELEMENT_CHINESE = {
    "Wood": "木",
    "Fire": "火",
    "Earth": "土",
    "Metal": "金",
    "Water": "水"
}

# Custom CSS for better visibility
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    [data-testid="stSidebar"] { background-color: #16213e; }
    h1, h2, h3, h4, h5 { color: #d4af37 !important; }
    p, span, label, .stMarkdown { color: #e0e0e0 !important; }
    .stRadio label span, .stCheckbox label span { color: #e0e0e0 !important; }
    .stSelectbox label, .stTextInput label { color: #e0e0e0 !important; }
    .preview-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .chinese-big {
        font-size: 5rem;
        color: #d4af37;
        font-weight: bold;
    }
    .profile-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #2a3f5f;
    }
    .profile-label { color: #888 !important; }
    .profile-value { color: #fff !important; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = load_profile()

# Helper functions
def get_profile_value(profile, key, default=""):
    value = profile.get(key, default)
    if key == "day_master" and isinstance(value, dict):
        return value.get("pinyin", default)
    return value

def get_profile_chinese(profile):
    dm = profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        return dm.get("chinese", "庚")
    return DAY_MASTER_OPTIONS.get(dm, {}).get("chinese", "庚")

def get_profile_element(profile):
    dm = profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        return dm.get("element", "Metal")
    if profile.get("element"):
        return profile.get("element")
    return DAY_MASTER_OPTIONS.get(dm, {}).get("element", "Metal")

def get_profile_polarity(profile):
    dm = profile.get("day_master", "Geng")
    if isinstance(dm, dict):
        return dm.get("polarity", "Yang")
    if profile.get("polarity"):
        return profile.get("polarity")
    return DAY_MASTER_OPTIONS.get(dm, {}).get("polarity", "Yang")

# ==================== PAGE HEADER ====================
st.title("⚙️ Settings 设置")
st.caption("Configure your BaZi profile, preferences, and manage data | 配置八字档案、偏好设置和数据管理")

# Initialize birthday session state
if 'saved_birth_date' not in st.session_state:
    # Try to get from saved profile
    profile = st.session_state.profile
    if profile.get('birth_date'):
        try:
            st.session_state.saved_birth_date = date.fromisoformat(profile['birth_date'])
        except:
            st.session_state.saved_birth_date = date(1985, 1, 1)
    else:
        st.session_state.saved_birth_date = date(1985, 1, 1)

if 'saved_birth_hour' not in st.session_state:
    profile = st.session_state.profile
    st.session_state.saved_birth_hour = profile.get('birth_hour', 12)

# Two columns layout
col1, col2 = st.columns([3, 2])

with col1:
    # ==================== BIRTHDAY CALCULATOR ====================
    st.header("🎂 Birthday Calculator 生日计算器")
    st.caption("Enter birth date and time to auto-calculate your BaZi profile")
    st.caption("输入出生日期和时间，自动计算八字档案")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        birth_date = st.date_input(
            "Birth Date 出生日期",
            value=st.session_state.saved_birth_date,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key="birth_date_input"
        )
    
    with calc_col2:
        # Hour selection with Chinese hour names
        hour_options = list(range(0, 24))
        hour_labels = {h: f"{h:02d}:00 - {get_hour_branch_name(h)}" for h in hour_options}
        
        birth_hour = st.selectbox(
            "Birth Hour 出生时辰",
            options=hour_options,
            format_func=lambda h: hour_labels[h],
            index=st.session_state.saved_birth_hour,
            key="birth_hour_input"
        )
    
    if st.button("🔮 Calculate BaZi 计算八字", use_container_width=True, type="secondary"):
        try:
            # Save the birthday to session state
            st.session_state.saved_birth_date = birth_date
            st.session_state.saved_birth_hour = birth_hour
            
            # Calculate BaZi
            birth_datetime = datetime.combine(birth_date, datetime.min.time())
            result = calculate_full_profile(birth_datetime, birth_hour)
            
            # Store in session state
            st.session_state.calculated_bazi = result
            
            st.success("✅ BaZi calculated successfully! 八字计算成功！")
        except Exception as e:
            st.error(f"Calculation error: {e}")
    
    # Show calculated result if available
    if 'calculated_bazi' in st.session_state and st.session_state.calculated_bazi:
        result = st.session_state.calculated_bazi
        bazi = result['bazi']
        analysis = result['analysis']
        
        st.markdown("---")
        st.subheader("📊 Calculated Result 计算结果")
        
        # Four Pillars Display
        st.markdown("**Four Pillars 四柱:**")
        pillar_cols = st.columns(4)
        
        with pillar_cols[0]:
            st.markdown(f"""
            <div style="text-align:center; background:#16213e; padding:10px; border-radius:8px; border:1px solid #2a3f5f;">
                <div style="color:#888; font-size:0.8rem;">Year 年柱</div>
                <div style="color:#d4af37; font-size:1.5rem; font-weight:bold;">{bazi['year_pillar']['display']}</div>
                <div style="color:#aaa; font-size:0.7rem;">{bazi['animal_sign']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with pillar_cols[1]:
            st.markdown(f"""
            <div style="text-align:center; background:#16213e; padding:10px; border-radius:8px; border:1px solid #2a3f5f;">
                <div style="color:#888; font-size:0.8rem;">Month 月柱</div>
                <div style="color:#d4af37; font-size:1.5rem; font-weight:bold;">{bazi['month_pillar']['display']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with pillar_cols[2]:
            dm = bazi['day_master']
            elem_color = ELEMENT_COLORS.get(dm['element'], '#C0C0C0')
            st.markdown(f"""
            <div style="text-align:center; background:#1e3a5f; padding:10px; border-radius:8px; border:2px solid #d4af37;">
                <div style="color:#d4af37; font-size:0.8rem;">Day 日柱 ⭐</div>
                <div style="color:{elem_color}; font-size:1.5rem; font-weight:bold;">{bazi['day_pillar']['display']}</div>
                <div style="color:#fff; font-size:0.7rem;">{dm['pinyin']} {dm['element']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with pillar_cols[3]:
            st.markdown(f"""
            <div style="text-align:center; background:#16213e; padding:10px; border-radius:8px; border:1px solid #2a3f5f;">
                <div style="color:#888; font-size:0.8rem;">Hour 时柱</div>
                <div style="color:#d4af37; font-size:1.5rem; font-weight:bold;">{bazi['hour_pillar']['display']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Analysis summary
        st.markdown(f"""
        **Day Master 日主:** {bazi['day_master']['chinese']} {bazi['day_master']['pinyin']} ({bazi['day_master']['element']} {ELEMENT_CHINESE.get(bazi['day_master']['element'], '')} - {bazi['day_master']['polarity']})
        
        **Strength 强弱:** {analysis['strength']}
        
        **Useful Gods 用神:** {', '.join([f"{ELEMENT_EMOJI.get(e, '')} {e} {ELEMENT_CHINESE.get(e, '')}" for e in analysis['useful_gods']])}
        
        **Unfavorable 忌神:** {', '.join([f"{ELEMENT_EMOJI.get(e, '')} {e} {ELEMENT_CHINESE.get(e, '')}" for e in analysis['unfavorable']])}
        
        **Suggested Profile 建议性格:** {result['profile_suggestion']['emoji']} {result['profile_suggestion']['profile']}
        """)
        
        # Apply to profile button
        if st.button("📥 Apply to Profile 应用到档案", use_container_width=True, type="primary"):
            new_profile = result['settings_profile']
            # Add birth info for persistence
            new_profile['birth_date'] = st.session_state.saved_birth_date.isoformat()
            new_profile['birth_hour'] = st.session_state.saved_birth_hour
            save_profile(new_profile)
            st.session_state.profile = new_profile
            st.session_state.calculated_bazi = None  # Clear calculated result
            st.success("✅ Profile updated from BaZi calculation! 档案已从八字计算更新！")
            st.rerun()
    
    st.markdown("---")
    st.markdown("---")
    
    # ==================== BAZI PROFILE SECTION ====================
    st.header("👤 Analysis Target Profile 分析目标档案")
    st.caption("Default: Your BaZi profile. Change to analyze charts for clients, family, or friends.")
    st.caption("默认：您的八字档案。可更改为客户、家人或朋友的资料进行分析。")
    
    # Always reload profile from session state to get latest
    profile = st.session_state.profile
    
    st.markdown("---")
    
    # Day Master Selection
    st.subheader("Day Master 日主")
    
    dm_options = list(DAY_MASTER_OPTIONS.keys())
    current_dm = get_profile_value(profile, 'day_master', 'Geng')
    
    # Use index based on profile, not widget state
    try:
        current_dm_index = dm_options.index(current_dm)
    except ValueError:
        current_dm_index = 6  # Default to Geng
    
    # Clear widget key if profile was just updated
    dm_key = f"dm_select_{current_dm}"  # Key includes current value to force refresh
    
    selected_dm = st.selectbox(
        "Select Day Master 选择日主",
        options=dm_options,
        format_func=lambda x: f"{x} {DAY_MASTER_OPTIONS[x]['chinese']} - {DAY_MASTER_OPTIONS[x]['element']} {ELEMENT_CHINESE.get(DAY_MASTER_OPTIONS[x]['element'], '')} ({DAY_MASTER_OPTIONS[x]['polarity']})",
        index=current_dm_index,
        key=dm_key
    )
    
    dm_info = DAY_MASTER_OPTIONS[selected_dm]
    
    # Element and Polarity display
    col_elem, col_pol = st.columns(2)
    with col_elem:
        elem = dm_info['element']
        st.info(f"**Element 五行:** {ELEMENT_EMOJI.get(elem, '')} {elem} {ELEMENT_CHINESE.get(elem, '')}")
    with col_pol:
        pol = dm_info['polarity']
        pol_zh = "阳" if pol == "Yang" else "阴"
        st.info(f"**Polarity 阴阳:** {'☀️' if pol == 'Yang' else '🌙'} {pol} {pol_zh}")
    
    st.markdown("---")
    
    # Strength Assessment
    st.subheader("Strength Assessment 日主强弱")
    strength_options = ["Weak 弱", "Strong 强", "Extremely Weak 极弱", "Extremely Strong 极强", "Balanced 中和"]
    strength_values = ["Weak", "Strong", "Extremely Weak", "Extremely Strong", "Balanced"]
    current_strength = profile.get('strength', 'Weak')
    current_strength_index = 0
    for i, v in enumerate(strength_values):
        if v == current_strength:
            current_strength_index = i
            break
    
    strength_key = f"strength_{current_strength}"  # Dynamic key
    selected_strength_display = st.radio(
        "How strong is your Day Master? 日主强度如何？",
        strength_options,
        index=current_strength_index,
        horizontal=True,
        key=strength_key
    )
    selected_strength = strength_values[strength_options.index(selected_strength_display)]
    
    st.markdown("---")
    
    # Useful Gods
    st.subheader("Useful Gods 用神")
    st.caption("Select elements that support your chart 选择对您命盘有利的五行")
    
    current_useful = profile.get('useful_gods', ['Earth', 'Metal'])
    if isinstance(current_useful, dict):
        current_useful = [current_useful.get('primary', 'Earth'), current_useful.get('secondary', 'Metal')]
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    useful_cols = st.columns(5)
    useful_selected = []
    
    # Create unique key suffix based on current useful gods
    useful_key_suffix = "_".join(sorted(current_useful)) if current_useful else "none"
    
    for i, elem in enumerate(elements):
        with useful_cols[i]:
            if st.checkbox(
                f"{ELEMENT_EMOJI.get(elem, '')} {elem} {ELEMENT_CHINESE.get(elem, '')}",
                value=elem in current_useful,
                key=f"useful_{elem}_{useful_key_suffix}"
            ):
                useful_selected.append(elem)
    
    st.markdown("---")
    
    # Unfavorable Elements
    st.subheader("Unfavorable Elements 忌神")
    st.caption("Select elements that weaken your chart 选择对您命盘不利的五行")
    
    current_unfav = profile.get('unfavorable', ['Fire'])
    if isinstance(current_unfav, dict):
        current_unfav = [current_unfav.get('primary', 'Fire')]
    
    # Create unique key suffix
    unfav_key_suffix = "_".join(sorted(current_unfav)) if current_unfav else "none"
    unfav_cols = st.columns(5)
    unfav_selected = []
    
    for i, elem in enumerate(elements):
        with unfav_cols[i]:
            if st.checkbox(
                f"{ELEMENT_EMOJI.get(elem, '')} {elem} {ELEMENT_CHINESE.get(elem, '')}",
                value=elem in current_unfav,
                key=f"unfav_{elem}_{unfav_key_suffix}"
            ):
                unfav_selected.append(elem)
    
    st.markdown("---")
    
    # Ten God Profile
    st.subheader("Ten God Profile 十神性格")
    
    profile_options = list(TEN_GOD_PROFILE_OPTIONS.keys())
    current_profile_name = profile.get('profile', 'Pioneer (Indirect Wealth)')
    try:
        current_profile_index = profile_options.index(current_profile_name)
    except ValueError:
        current_profile_index = 5
    
    profile_key = f"profile_select_{current_profile_name.replace(' ', '_')[:10]}"
    selected_profile = st.selectbox(
        "Select your dominant Ten God profile 选择主导十神性格",
        options=profile_options,
        format_func=lambda x: f"{TEN_GOD_PROFILE_OPTIONS[x]['emoji']} {x}",
        index=current_profile_index,
        key=profile_key
    )
    
    profile_info = TEN_GOD_PROFILE_OPTIONS[selected_profile]
    st.caption(f"**Traits 特征:** {', '.join(profile_info.get('traits', []))}")
    
    st.markdown("---")
    
    # Special Structures
    st.subheader("Special Structures 特殊格局")
    
    current_structs = profile.get('special_structures', {})
    struct_key_suffix = f"{current_structs.get('wealth_vault', False)}_{current_structs.get('nobleman', False)}"
    struct_cols = st.columns(3)
    
    with struct_cols[0]:
        wealth_vault = st.checkbox("💰 Wealth Vault 财库", value=current_structs.get('wealth_vault', True), key=f"struct_wealth_{struct_key_suffix}")
    with struct_cols[1]:
        nobleman = st.checkbox("👑 Nobleman 贵人", value=current_structs.get('nobleman', False), key=f"struct_noble_{struct_key_suffix}")
    with struct_cols[2]:
        horse = st.checkbox("🐴 Traveling Horse 驿马", value=current_structs.get('traveling_horse', False), key=f"struct_horse_{struct_key_suffix}")
    
    st.markdown("")
    st.markdown("")
    
    # Save Button
    if st.button("💾 Save Profile 保存档案", use_container_width=True, type="primary"):
        new_profile = {
            "day_master": selected_dm,
            "chinese": dm_info['chinese'],
            "element": dm_info['element'],
            "polarity": dm_info['polarity'],
            "strength": selected_strength,
            "useful_gods": useful_selected if useful_selected else ['Earth', 'Metal'],
            "unfavorable": unfav_selected if unfav_selected else ['Fire'],
            "profile": selected_profile,
            "profile_emoji": profile_info['emoji'],
            "special_structures": {
                "wealth_vault": wealth_vault,
                "nobleman": nobleman,
                "traveling_horse": horse,
                "other": []
            }
        }
        save_profile(new_profile)
        st.session_state.profile = new_profile
        st.success("✅ Profile saved successfully! 档案保存成功！")
        st.rerun()

with col2:
    # ==================== PROFILE PREVIEW ====================
    st.header("👁️ Profile Preview 档案预览")
    
    # Check if we have a calculated BaZi to preview, otherwise show saved profile
    if 'calculated_bazi' in st.session_state and st.session_state.calculated_bazi:
        # Show calculated result
        calc = st.session_state.calculated_bazi
        bazi = calc['bazi']
        analysis = calc['analysis']
        
        dm_name = bazi['day_master']['pinyin']
        chinese = bazi['day_master']['chinese']
        element = bazi['day_master']['element']
        polarity = bazi['day_master']['polarity']
        strength = analysis['strength']
        useful = analysis['useful_gods']
        unfav = analysis['unfavorable']
        prof = calc['profile_suggestion']['profile']
        prof_emoji = calc['profile_suggestion']['emoji']
        structs = {}  # Calculated doesn't have special structures yet
        
        st.caption("📊 Showing calculated result (not yet saved)")
    else:
        # Show saved profile
        current = st.session_state.profile
        
        dm_name = get_profile_value(current, 'day_master', 'Geng')
        chinese = get_profile_chinese(current)
        element = get_profile_element(current)
        polarity = get_profile_polarity(current)
        strength = current.get('strength', 'Weak')
        useful = current.get('useful_gods', ['Earth', 'Metal'])
        unfav = current.get('unfavorable', ['Fire'])
        prof = current.get('profile', 'Pioneer (Indirect Wealth)')
        prof_emoji = current.get('profile_emoji', '🎯')
        structs = current.get('special_structures', {})
        
        st.caption("💾 Showing saved profile")
    
    elem_color = ELEMENT_COLORS.get(element, '#C0C0C0')
    
    # Preview Card using Streamlit components
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
                    border: 2px solid #d4af37; border-radius: 15px; padding: 25px; text-align: center;">
            <div style="font-size: 5rem; color: #d4af37; margin-bottom: 10px;">{chinese}</div>
            <div style="font-size: 1.5rem; color: {elem_color}; font-weight: 600;">{dm_name} {element} {ELEMENT_CHINESE.get(element, '')}</div>
            <div style="color: #aaa; font-size: 1rem;">({polarity} {'阳' if polarity == 'Yang' else '阴'} · {strength})</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Profile details using st.write for reliability
    st.markdown("**Profile 性格:**")
    st.write(f"{prof_emoji} {prof}")
    
    st.markdown("**Useful Gods 用神:**")
    useful_display = " ".join([f"{ELEMENT_EMOJI.get(e, '')} {e} {ELEMENT_CHINESE.get(e, '')}" for e in useful]) if useful else "None"
    st.write(useful_display)
    
    st.markdown("**Unfavorable 忌神:**")
    unfav_display = " ".join([f"{ELEMENT_EMOJI.get(e, '')} {e} {ELEMENT_CHINESE.get(e, '')}" for e in unfav]) if unfav else "None"
    st.write(unfav_display)
    
    st.markdown("**Special Structures 特殊格局:**")
    special_list = []
    if structs.get('wealth_vault'):
        special_list.append("💰 Wealth Vault 财库")
    if structs.get('nobleman'):
        special_list.append("👑 Nobleman 贵人")
    if structs.get('traveling_horse'):
        special_list.append("🐴 Traveling Horse 驿马")
    st.write(", ".join(special_list) if special_list else "None")
    
    st.markdown("---")
    
    # ==================== DISPLAY SETTINGS ====================
    st.header("🎨 Display 显示设置")
    
    lang_options = ["English", "中文", "Mixed 混合"]
    current_lang = st.session_state.get('lang_mode', 'mixed')
    lang_index = {"en": 0, "zh": 1, "mixed": 2}.get(current_lang, 2)
    
    selected_lang = st.radio("Language 语言", lang_options, index=lang_index, horizontal=True, key="lang_radio")
    
    lang_map = {"English": "en", "中文": "zh", "Mixed 混合": "mixed"}
    new_lang = lang_map.get(selected_lang, "mixed")
    if new_lang != current_lang:
        st.session_state.lang_mode = new_lang
    
    st.markdown("---")
    
    # ==================== DATABASE MANAGEMENT ====================
    st.header("📊 Database 数据库")
    
    stats = get_statistics()
    
    stat_cols = st.columns(2)
    with stat_cols[0]:
        st.metric("Total Analyses 总分析", stats.get('total', 0))
    with stat_cols[1]:
        rate = stats.get('success_rate', 0)
        st.metric("Success Rate 成功率", f"{rate:.0%}" if isinstance(rate, float) else "0%")
    
    st.markdown("")
    
    # Export button
    records = get_all_records()
    if records:
        csv_data = export_to_csv_string()
        st.download_button(
            "📥 Export CSV 导出数据",
            data=csv_data,
            file_name="qmdj_analyses.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("")
    
    # Clear database
    with st.expander("⚠️ Danger Zone 危险区域"):
        st.warning("This will delete all analysis history! 这将删除所有分析历史！")
        if st.button("🗑️ Clear All Data 清除所有数据", use_container_width=True):
            clear_database()
            st.success("Database cleared! 数据库已清除！")
            st.rerun()
    
    st.markdown("")
    
    # Reset to defaults
    if st.button("🔄 Reset Profile to Defaults 重置为默认", use_container_width=True):
        default = get_default_profile()
        save_profile(default)
        st.session_state.profile = default
        st.success("Profile reset to defaults! 档案已重置！")
        st.rerun()
