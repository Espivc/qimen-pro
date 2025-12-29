"""
Qi Men Pro - Help & Guide Page
Explains how to use the app and QMDJ methodology
"""

import streamlit as st

st.set_page_config(
    page_title="Help & Guide | Qi Men Pro",
    page_icon="📚",
    layout="wide"
)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("📚 Help & Guide 帮助指南")
st.markdown("Learn how to use Qi Men Pro for QMDJ analysis")

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 What is QMDJ?", 
    "📋 How to Use", 
    "🏛️ Palace Guide",
    "📖 Quick Reference"
])

# ============ TAB 1: WHAT IS QMDJ ============
with tab1:
    st.markdown("## 🔮 What is Qi Men Dun Jia? 奇门遁甲")
    
    st.markdown("""
    **Qi Men Dun Jia (奇门遁甲)** is one of the most powerful Chinese metaphysics systems, 
    originally used for military strategy and now applied to:
    
    - ✅ **Business decisions** - When to sign contracts, launch products
    - ✅ **Career choices** - Job changes, negotiations, interviews
    - ✅ **Relationship timing** - Marriage, partnerships
    - ✅ **Travel planning** - Best directions and timing
    - ✅ **Daily forecasting** - Understanding the energy of each day/hour
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔄 How QMDJ Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">1️⃣ Your BaZi</h4>
            <p style="font-size: 2em;">👤</p>
            <p><strong>Who You Are</strong></p>
            <p style="color: #888; font-size: 0.9em;">Your birth chart shows your strengths, 
            weaknesses, and what elements help or harm you.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">2️⃣ QMDJ Chart</h4>
            <p style="font-size: 2em;">🔮</p>
            <p><strong>The Moment</strong></p>
            <p style="color: #888; font-size: 0.9em;">The chart captures cosmic energy at a specific 
            date/time, showing opportunities and obstacles.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">3️⃣ Analysis</h4>
            <p style="font-size: 2em;">📊</p>
            <p><strong>The Answer</strong></p>
            <p style="color: #888; font-size: 0.9em;">Combining your BaZi with the QMDJ chart 
            gives personalized guidance for your question.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 QMDJ Chart Components")
    
    st.markdown("""
    | Component | Chinese | What It Represents |
    |-----------|---------|-------------------|
    | **Heaven Stem** | 天干 | Heaven's energy, intention, what's meant to be |
    | **Earth Stem** | 地干 | Ground reality, current situation |
    | **Star** | 九星 | Timing factor, luck influence |
    | **Door** | 八门 | Type of opportunity, action to take |
    | **Deity** | 八神 | Hidden influence, spiritual guidance |
    | **Formation** | 格局 | Special patterns that modify the reading |
    """)

# ============ TAB 2: HOW TO USE ============
with tab2:
    st.markdown("## 📋 How to Use Qi Men Pro")
    
    st.markdown("### Step-by-Step Workflow")
    
    # Step 1
    st.markdown("#### Step 1: Set Your BaZi Profile (One Time)")
    st.info("""
    📍 **Go to:** Settings → BaZi Calculator
    
    1. Enter your birth date (Solar calendar 阳历, NOT lunar!)
    2. Enter your birth time (as precise as possible)
    3. Click "Calculate BaZi"
    4. Click "Save as My Profile"
    
    ✅ **Done!** Your profile is now saved and will be used for all analyses.
    """)
    
    # Step 2
    st.markdown("#### Step 2: Ask Your Question")
    st.success("""
    📍 **Go to:** Dashboard or Chart Generator
    
    1. **Set the Date** - When is the event/decision?
       - For "should I do X today?" → Use today's date
       - For "is tomorrow good for Y?" → Use tomorrow's date
    
    2. **Set the Time** - What time matters?
       - Current time for immediate decisions
       - Meeting/event time for specific situations
    
    3. **Select the Palace** - What's your question about?
       - See Palace Guide tab for details
    """)
    
    # Step 3
    st.markdown("#### Step 3: Generate & Analyze")
    st.warning("""
    📍 **Go to:** Chart Generator
    
    1. Click "Generate QMDJ Chart"
    2. Review the components (Star, Door, Deity)
    3. Check for any formations
    4. Look at the overall verdict
    
    🔮 **For deeper analysis:** Export JSON → Use with Project 1 (AI Analyst)
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Common Use Cases")
    
    use_cases = [
        ("Should I accept this job offer?", "Set to decision time, Palace #1 (Career)"),
        ("Is today good for signing contract?", "Today + current time, Palace #4 (Wealth)"),
        ("Will my meeting go well?", "Meeting date/time, Palace #6 (Mentor) or #1 (Career)"),
        ("Should I travel this weekend?", "Travel date/time, Palace based on purpose"),
        ("General daily forecast", "Today + morning, Palace #5 (Center/Self)"),
    ]
    
    for question, answer in use_cases:
        with st.expander(f"❓ {question}"):
            st.markdown(f"**Setup:** {answer}")

# ============ TAB 3: PALACE GUIDE ============
with tab3:
    st.markdown("## 🏛️ Palace Selection Guide 宫位指南")
    
    st.markdown("""
    The **9 Palaces** represent different life areas. Select the palace that matches your question.
    """)
    
    # Visual grid
    st.markdown("### 📍 The 9 Palaces Map")
    
    col1, col2, col3 = st.columns(3)
    
    palace_data = [
        [
            ("#4 巽 Xun", "SE 东南", "💰 Wealth", "#228B22", "Money, investments, assets, income"),
            ("#9 离 Li", "S 南", "🌟 Fame", "#DC143C", "Recognition, reputation, visibility"),
            ("#2 坤 Kun", "SW 西南", "💕 Relations", "#DAA520", "Marriage, partnerships, mother"),
        ],
        [
            ("#3 震 Zhen", "E 东", "💪 Health", "#228B22", "Health, family, new beginnings"),
            ("#5 中 Center", "C 中", "🎯 Self", "#DAA520", "Yourself, general matters, overall"),
            ("#7 兑 Dui", "W 西", "👶 Children", "#C0C0C0", "Children, creativity, joy, projects"),
        ],
        [
            ("#8 艮 Gen", "NE 东北", "📚 Knowledge", "#DAA520", "Education, skills, meditation"),
            ("#1 坎 Kan", "N 北", "💼 Career", "#1E90FF", "Career, business, life path"),
            ("#6 乾 Qian", "NW 西北", "🤝 Mentor", "#C0C0C0", "Helpful people, father, travel"),
        ]
    ]
    
    for row in palace_data:
        cols = st.columns(3)
        for col, (name, direction, icon, color, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            padding: 15px; border-radius: 10px; border: 2px solid {color}; 
                            text-align: center; margin-bottom: 10px;">
                    <p style="color: {color}; font-weight: bold; margin: 0;">{name}</p>
                    <p style="color: #888; font-size: 0.8em; margin: 5px 0;">{direction}</p>
                    <p style="font-size: 1.5em; margin: 5px 0;">{icon}</p>
                    <p style="color: #ccc; font-size: 0.85em; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Selection Table")
    
    st.markdown("""
    | Your Question About | Select Palace | Direction |
    |--------------------:|:--------------|:----------|
    | 💼 Career, job, business | **#1 坎 Kan** | North |
    | 💕 Marriage, relationship | **#2 坤 Kun** | Southwest |
    | 💪 Health, family | **#3 震 Zhen** | East |
    | 💰 Money, wealth, investment | **#4 巽 Xun** | Southeast |
    | 🎯 Yourself, general | **#5 中 Center** | Center |
    | 🤝 Helpful people, mentor | **#6 乾 Qian** | Northwest |
    | 👶 Children, creativity | **#7 兑 Dui** | West |
    | 📚 Education, skills | **#8 艮 Gen** | Northeast |
    | 🌟 Fame, recognition | **#9 离 Li** | South |
    """)

# ============ TAB 4: QUICK REFERENCE ============
with tab4:
    st.markdown("## 📖 Quick Reference Card")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Auspicious Indicators 吉")
        
        st.markdown("""
        **Doors 八门 (Best to Good):**
        - 🟢 **开 Open** - Best for starting new things
        - 🟢 **休 Rest** - Good for meetings, negotiations
        - 🟢 **生 Life** - Excellent for wealth, growth
        - 🟡 **景 Scenery** - Good for fame, documents
        
        **Stars 九星 (Auspicious):**
        - ⭐ **天心 Heart** - Wisdom, problem-solving
        - ⭐ **天辅 Assistant** - Help, support available
        - ⭐ **天任 Ren** - Steady progress, reliable
        - ⭐ **天冲 Impulse** - Quick action, momentum
        
        **Deities 八神 (Favorable):**
        - 👑 **值符 Chief** - Authority, blessing
        - 🌙 **太阴 Moon** - Hidden help, secrets revealed
        - ☁️ **九天 Nine Heaven** - Expansion, going public
        - 🤝 **六合 Six Harmony** - Cooperation, partnership
        """)
    
    with col2:
        st.markdown("### ❌ Inauspicious Indicators 凶")
        
        st.markdown("""
        **Doors 八门 (Avoid):**
        - 🔴 **死 Death** - Endings, obstacles, blocked
        - 🔴 **惊 Fear** - Shock, unexpected problems
        - 🔴 **伤 Harm** - Injury, conflict, arguments
        - 🟠 **杜 Delusion** - Hidden, stuck, unclear
        
        **Stars 九星 (Inauspicious):**
        - ⚠️ **天蓬 Canopy** - Deception, hidden dangers
        - ⚠️ **天芮 Grass** - Illness, obstacles
        - ⚠️ **天柱 Pillar** - Gossip, slander
        
        **Deities 八神 (Unfavorable):**
        - 🐍 **腾蛇 Serpent** - Worry, nightmares, deception
        - 🐯 **白虎 Tiger** - Danger, injury, aggression
        - 🌑 **玄武 Emptiness** - Loss, theft, unclear
        - 🪝 **勾陈 Hook** - Obstacles, delays, legal issues
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔥 Five Elements Quick Guide")
    
    element_cols = st.columns(5)
    elements = [
        ("🌳", "Wood 木", "#228B22", "Growth, creativity, kindness"),
        ("🔥", "Fire 火", "#DC143C", "Passion, fame, expansion"),
        ("🏔️", "Earth 土", "#DAA520", "Stability, trust, nurturing"),
        ("⚪", "Metal 金", "#C0C0C0", "Precision, justice, strength"),
        ("💧", "Water 水", "#1E90FF", "Wisdom, flow, communication"),
    ]
    
    for col, (icon, name, color, meaning) in zip(element_cols, elements):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <p style="font-size: 2em; margin: 0;">{icon}</p>
                <p style="color: {color}; font-weight: bold; margin: 5px 0;">{name}</p>
                <p style="color: #888; font-size: 0.8em;">{meaning}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔄 Element Relationships")
    
    st.markdown("""
    **Productive Cycle (相生) - Supporting:**
    ```
    Wood → Fire → Earth → Metal → Water → Wood
    (Wood feeds Fire, Fire creates Earth/ash, etc.)
    ```
    
    **Controlling Cycle (相克) - Weakening:**
    ```
    Wood → Earth → Water → Fire → Metal → Wood
    (Wood breaks Earth, Earth dams Water, etc.)
    ```
    """)

# Footer
st.markdown("---")
st.caption("📚 Qi Men Pro Help & Guide | Joey Yap Methodology")
