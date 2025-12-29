"""
Ming Qimen 明奇门 - Help & Guide Page
Clarity for the People
"""

import streamlit as st

st.set_page_config(
    page_title="Help | Ming Qimen",
    page_icon="📚",
    layout="wide"
)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #d4af37;">📚 Help & Guide 帮助指南</h1>
    <p style="color: #888;">Ming Qimen 明奇门 | Ancient Wisdom Made Bright</p>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌟 About Ming", 
    "🔮 What is This?", 
    "📋 How to Use", 
    "🏛️ Topics Guide",
    "📖 Signs Reference"
])

# ============ TAB 1: ABOUT MING ============
with tab1:
    st.markdown("## 🌟 About Ming Qimen 关于明奇门")
    
    st.markdown("""
    ### Our Mission 我们的使命
    
    I created **Ming Qimen** because I believe wisdom shouldn't come with a price tag or a headache.
    
    My name is **Beng (明)**, which means **'Brightness.'** My goal is to use that light to clear 
    the fog of ancient calculations.
    
    Too many apps are built for experts; **this one is built for you.**
    
    ---
    
    ### 💡 What Makes Us Different
    
    | Other Apps | Ming Qimen |
    |------------|------------|
    | Complex jargon | Simple, clear language |
    | Requires expertise | Built for beginners |
    | Paywalls & subscriptions | **Free forever** |
    | Confusing data entry | One tap to clarity |
    | "Dead" and "Confined" | "Rest Energy" and "Low Energy" |
    
    ---
    
    ### 🎯 Our Promise
    
    - **No paywalls** — full access, always free
    - **No confusing jargon** — we explain everything simply
    - **No expertise required** — guidance from your first tap
    - **No judgment** — just helpful direction
    
    ---
    
    > *"Guiding you first, because your peace of mind matters."*
    
    ---
    
    ### The Name "Ming" 明
    
    **明 (Míng)** means **brightness, clarity, understanding**.
    
    It's composed of:
    - ☀️ **日 (Sun)** — the light of day
    - 🌙 **月 (Moon)** — the light of night
    
    Together: **Light that never fades** — guiding you day and night.
    """)

# ============ TAB 2: WHAT IS THIS ============
with tab2:
    st.markdown("## 🔮 What is Qi Men Dun Jia?")
    
    st.markdown("""
    ### Ancient GPS for Life Decisions
    
    Imagine having a GPS that tells you not just *where* to go, but *when* to go.
    
    **Qi Men Dun Jia** (奇门遁甲) is an ancient Chinese system that reads the energy 
    of any moment to help you make better decisions about:
    
    - ✅ **Career** — job changes, business deals
    - ✅ **Money** — investments, purchases
    - ✅ **Relationships** — partnerships, meetings
    - ✅ **Health** — medical appointments, treatments
    - ✅ **Travel** — trips, moving, relocations
    
    ---
    
    ### How Does It Work?
    
    Every moment has its own "energy signature" — like weather, but for decisions.
    
    Just like you'd check the weather before a picnic, you can check the energy 
    before making important choices.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">1️⃣ Your Profile</h4>
            <p style="font-size: 2em;">👤</p>
            <p><strong>Who You Are</strong></p>
            <p style="color: #888; font-size: 0.9em;">Your birth chart shows what elements help or challenge you.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">2️⃣ The Moment</h4>
            <p style="font-size: 2em;">🕐</p>
            <p><strong>Right Now</strong></p>
            <p style="color: #888; font-size: 0.9em;">We read the energy of the current time for your question.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 20px; border-radius: 10px; border: 1px solid #d4af37; text-align: center;">
            <h4 style="color: #d4af37;">3️⃣ Your Guidance</h4>
            <p style="font-size: 2em;">💡</p>
            <p><strong>Clear Advice</strong></p>
            <p style="color: #888; font-size: 0.9em;">Simple guidance: Go ahead, wait, or prepare more.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ---
    
    ### Is This Fortune Telling?
    
    **No.** This is decision support.
    
    We don't predict your future — we help you understand the *current conditions* 
    so you can make better choices. Like checking the weather, not predicting it.
    
    **You always have free will.** This is just another tool in your toolkit.
    """)

# ============ TAB 3: HOW TO USE ============
with tab3:
    st.markdown("## 📋 How to Use Ming Qimen")
    
    st.markdown("### 3 Simple Steps")
    
    # Step 1
    st.success("""
    ### Step 1: Set Up Your Profile (Once)
    
    📍 **Go to:** Settings → BaZi Calculator
    
    1. Enter your birth date (use regular calendar, not lunar)
    2. Enter your birth time (best guess is okay!)
    3. Tap "Calculate"
    4. Tap "Save as My Profile"
    
    ✅ **Done!** This helps personalize your readings.
    """)
    
    # Step 2
    st.info("""
    ### Step 2: Ask Your Question
    
    📍 **On the Home page:**
    
    1. Your current time is already set ⏰
    2. Tap the **topic** that matches your question:
       - 💼 Career, 💰 Wealth, 💕 Relations, etc.
    3. Look for the ⭐ **recommended** topic for best results!
    """)
    
    # Step 3
    st.warning("""
    ### Step 3: Get Your Guidance
    
    📍 **Tap "Get Your Reading"**
    
    You'll see:
    - 🟢 **Green Light** — Go ahead with confidence!
    - 🟡 **Yellow Light** — Proceed carefully or wait
    - ⚪ **Neutral** — Success depends on your effort
    
    **That's it!** Simple guidance in seconds.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Example Questions")
    
    examples = [
        ("Should I apply for this job?", "Tap 💼 Career"),
        ("Is today good for investing?", "Tap 💰 Wealth"),
        ("Will my meeting go well?", "Tap 💼 Career or 🤝 Mentor"),
        ("Should I have this difficult conversation?", "Tap 💕 Relations"),
        ("General outlook for today?", "Tap 🎯 Self"),
    ]
    
    for q, a in examples:
        with st.expander(f"❓ {q}"):
            st.markdown(f"**Action:** {a}")

# ============ TAB 4: TOPICS GUIDE ============
with tab4:
    st.markdown("## 🏛️ Topics Guide 主题指南")
    
    st.markdown("""
    Choose the topic that matches your question. If unsure, pick **🎯 Self** for general guidance.
    """)
    
    # Visual grid
    palace_data = [
        [
            ("💰 Wealth", "#4", "SE", "#228B22", "Money, investments, income, financial decisions"),
            ("🌟 Fame", "#9", "S", "#DC143C", "Recognition, reputation, visibility, promotion"),
            ("💕 Relations", "#2", "SW", "#DAA520", "Marriage, partnerships, mother, cooperation"),
        ],
        [
            ("💪 Health", "#3", "E", "#228B22", "Health, family, new projects, fresh starts"),
            ("🎯 Self", "#5", "C", "#DAA520", "Yourself, general guidance, overall energy"),
            ("👶 Children", "#7", "W", "#C0C0C0", "Children, creativity, joy, passion projects"),
        ],
        [
            ("📚 Knowledge", "#8", "NE", "#DAA520", "Education, skills, self-improvement, study"),
            ("💼 Career", "#1", "N", "#1E90FF", "Career, job, business, life path, purpose"),
            ("🤝 Mentor", "#6", "NW", "#C0C0C0", "Helpful people, mentors, father, travel"),
        ]
    ]
    
    for row in palace_data:
        cols = st.columns(3)
        for col, (name, num, direction, color, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            padding: 15px; border-radius: 10px; border: 2px solid {color}; 
                            text-align: center; margin-bottom: 10px; min-height: 150px;">
                    <p style="font-size: 1.5em; margin: 5px 0;">{name}</p>
                    <p style="color: {color}; font-weight: bold; margin: 0;">{num} • {direction}</p>
                    <p style="color: #ccc; font-size: 0.85em; margin-top: 10px;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# ============ TAB 5: SIGNS REFERENCE ============
with tab5:
    st.markdown("## 📖 Understanding the Signs")
    
    st.markdown("""
    When you get a reading, you'll see **Stars**, **Doors**, and **Spirits**. 
    Here's what they mean in simple terms:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Favorable Signs (Green Light!)")
        
        st.success("""
        **Stars 九星:**
        - 🌟 **Heart** — Wisdom, good decisions
        - 🌟 **Assistant** — Help available
        - 🌟 **Ren** — Steady progress
        - 🌟 **Impulse** — Quick action works
        
        **Doors 八门:**
        - 🚪 **Open** — New opportunities
        - 🚪 **Life** — Growth & prosperity  
        - 🚪 **Rest** — Good for meetings
        
        **Spirits 八神:**
        - ✨ **Chief** — Blessings from above
        - ✨ **Moon** — Hidden help
        - ✨ **Harmony** — Cooperation wins
        - ✨ **Heaven** — Go big!
        """)
    
    with col2:
        st.markdown("### ⚠️ Caution Signs (Slow Down)")
        
        st.error("""
        **Stars 九星:**
        - ⚠️ **Canopy** — Hidden obstacles
        - ⚠️ **Grass** — Slow progress
        
        **Doors 八门:**
        - 🚪 **Stillness** — Rest & reflect
        - 🚪 **Surprise** — Expect unexpected
        - 🚪 **Harm** — Careful with words
        
        **Spirits 八神:**
        - ⚠️ **Serpent** — Worry & anxiety
        - ⚠️ **Tiger** — Be careful
        - ⚠️ **Void** — Something unclear
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔋 Energy Levels")
    
    st.markdown("""
    Each sign also has an **Energy Level** showing how strong it is right now:
    """)
    
    energy_cols = st.columns(5)
    
    energies = [
        ("🔥", "High Energy", "Take Action!", "green"),
        ("✨", "Good Energy", "Favorable", "green"),
        ("😐", "Balanced", "Normal", "orange"),
        ("🌙", "Low Energy", "Be Patient", "orange"),
        ("💤", "Rest Energy", "Wait & Reflect", "red"),
    ]
    
    for col, (icon, label, advice, color) in zip(energy_cols, energies):
        with col:
            if color == "green":
                st.success(f"{icon}\n**{label}**\n{advice}")
            elif color == "red":
                st.error(f"{icon}\n**{label}**\n{advice}")
            else:
                st.warning(f"{icon}\n**{label}**\n{advice}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p style="color: #888;">🌟 Ming Qimen 明奇门 | Clarity for the People</p>
    <p style="color: #666; font-size: 0.9em;"><em>"Guiding you first, because your peace of mind matters."</em></p>
</div>
""", unsafe_allow_html=True)
