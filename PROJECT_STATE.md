# 🌟 MING QIMEN 明奇门 - PROJECT STATE TRACKER
**Last Updated:** 2025-12-29
**Version:** 3.0 (Ming Qimen Rebrand)
**Status:** 🟢 LIVE AND EVOLVING

---

## 🌟 BRAND IDENTITY

**Name:** Ming Qimen 明奇门  
**Tagline:** "Clarity for the People"  
**Sub-tagline:** "Ancient Wisdom, Made Bright and Simple"  
**Mission Statement:**
> I created Ming Qimen because I believe wisdom shouldn't come with a price tag or a headache.
> My name is Beng (明), which means 'Brightness.' My goal is to use that light to clear the fog 
> of ancient calculations. Too many apps are built for experts; this one is built for you.
> No paywalls, no complex data entry—just clear guidance to help you find your way, for free.
> *Let's help people first, and let the rest follow.*

**Promise:** "Guiding you first, because your peace of mind matters."

---

## 📊 PROJECT OVERVIEW

**Purpose:** Beginner-friendly QMDJ guidance system  
**Target User:** First-timers, non-experts, anyone seeking direction  
**Deployment:** Streamlit Cloud ✅ DEPLOYED  
**Live URL:** https://qimen-pro-qfvejjsappeenzfeuretzw9.streamlit.app/  
**Repository:** https://github.com/Espivc/qimen-pro

---

## ✅ WHAT'S NEW IN V3.0 (Ming Rebrand)

### Brand Changes
- [x] Renamed from "Qi Men Pro" to "Ming Qimen 明奇门"
- [x] Removed all "Joey Yap" references
- [x] Added mission statement and "About Ming" section
- [x] New taglines throughout

### UX Improvements
- [x] **Auto-populated current time** - Value on first load!
- [x] **Time syncs between pages** - Dashboard → Chart keeps your selection
- [x] **Palace recommendation with ⭐** - Shows best topic for current hour
- [x] **Beginner-friendly terms:**
  - "Dead (-3)" → "💤 Rest Energy - Wait & Reflect"
  - "Timely (+3)" → "🔥 High Energy - Take Action!"
  - "Inauspicious" → "Challenging" or "Caution"
  - "Death Door" → "Stillness Door"
  - "Fear Door" → "Surprise Door"

### Help & Guide
- [x] "About Ming" tab with full mission
- [x] "What is This?" for complete beginners
- [x] Visual topic grid
- [x] Simple signs reference
- [x] Energy levels explained

### Profile Section
- [x] "Useful Gods" → "Helpful Elements" with explanation
- [x] Added ℹ️ info captions explaining each field
- [x] Gentle, non-scary language throughout

---

## 📁 FILE STRUCTURE

```
ming-qimen/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── style.css
├── pages/
│   ├── 1_Chart.py          ← 1_Chart_ming.py
│   ├── 2_Export.py
│   ├── 3_History.py
│   ├── 4_Settings.py
│   └── 5_Help.py           ← 5_Help_ming.py
├── app.py                  ← app_ming.py
├── requirements.txt
└── PROJECT_STATE.md
```

---

## 🎯 BEGINNER-FRIENDLY TERMINOLOGY

### Energy Levels (replaces Strength)
| Technical Term | Ming Qimen Term | Advice |
|---------------|-----------------|--------|
| Timely (+3) | 🔥 High Energy | Take Action! |
| Prosperous (+2) | ✨ Good Energy | Favorable |
| Resting (0) | 😐 Balanced | Proceed Normally |
| Confined (-2) | 🌙 Low Energy | Be Patient |
| Dead (-3) | 💤 Rest Energy | Wait & Reflect |

### Door Names (gentler)
| Original | Ming Qimen |
|----------|------------|
| Death 死门 | Stillness |
| Fear 惊门 | Surprise |
| Inauspicious | Challenging |

### Nature Labels
| Original | Ming Qimen |
|----------|------------|
| Inauspicious | Challenging / Caution |
| Very Auspicious | Very Favorable / Excellent |

---

## 🏛️ PALACE TOPICS

| # | Icon | Topic | Description |
|---|------|-------|-------------|
| 1 | 💼 | Career | Job, business, life path |
| 2 | 💕 | Relations | Marriage, partnerships |
| 3 | 💪 | Health | Health, family, new starts |
| 4 | 💰 | Wealth | Money, investments |
| 5 | 🎯 | Self | General, yourself |
| 6 | 🤝 | Mentor | Helpful people, travel |
| 7 | 👶 | Children | Creativity, joy, projects |
| 8 | 📚 | Knowledge | Education, skills |
| 9 | 🌟 | Fame | Recognition, reputation |

---

## 🔧 TECHNICAL FEATURES

### Time Synchronization
```python
# Shared state between pages
st.session_state.shared_time = "HH:MM"
st.session_state.shared_date = date
st.session_state.selected_palace = 1-9
```

### Palace Recommendation Algorithm
```python
def get_recommended_palace(hour, user_profile):
    # Considers:
    # 1. Current hour energy
    # 2. User's helpful elements
    # 3. Palace elements
    # Returns: Best palace number for this moment
```

### Auto-Current Time
```python
current_time = datetime.now()
default_time = current_time.strftime("%H:%M")
# User sees value immediately!
```

---

## 📋 FUTURE PHASES

### Phase 4: Real QMDJ Calculations
- Integrate kinqimen library
- Accurate palace components
- Formation detection

### Phase 5: Enhanced BaZi
- Full strength calculation
- Ten Gods analysis
- Special structures
- Hidden stems

### Phase 6: Advanced Features
- Multiple user profiles
- History analytics
- Export to calendar
- Mobile app wrapper

---

## 🔄 DEPLOYMENT CHECKLIST

### Files to Upload:
| File | Rename To | Location |
|------|-----------|----------|
| `app_ming.py` | `app.py` | Root |
| `1_Chart_ming.py` | `1_Chart.py` | pages/ |
| `5_Help_ming.py` | `5_Help.py` | pages/ |
| `PROJECT_STATE.md` | `PROJECT_STATE.md` | Root |

### After Upload:
1. Wait 2-3 minutes for Streamlit rebuild
2. Test: Current time auto-populates
3. Test: Time syncs to Chart page
4. Test: Palace recommendation shows ⭐
5. Test: Energy levels show (not "Dead")

---

## 🎊 PROJECT STATUS SUMMARY

**Version:** 3.0 Ming Qimen Rebrand  
**Progress:** Core UX complete ✅

**Brand:**
- ✅ Ming Qimen identity
- ✅ Mission statement
- ✅ Beginner-friendly language

**Features:**
- ✅ Auto current time
- ✅ Time sync between pages
- ✅ Palace recommendation
- ✅ Energy levels (not "Dead")
- ✅ Helpful explanations

**Pending:**
- 📋 Real QMDJ calculations
- 📋 Enhanced BaZi
- 📋 Persistent storage

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
"Continue Ming Qimen (明奇门) development. 
Check PROJECT_STATE.md in Espivc/qimen-pro.
I want to [your request here]."
```

---

**END OF PROJECT STATE**  
*Last updated: 2025-12-29*  
*🌟 Ming Qimen 明奇门 | Clarity for the People*
