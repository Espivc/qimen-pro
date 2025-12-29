# 🔮 QI MEN PRO - PROJECT STATE TRACKER
**Last Updated:** 2025-12-29
**Version:** 2.1 (Phase 3 - IN PROGRESS)
**Status:** 🟢 LIVE AND WORKING

---

## 📊 PROJECT OVERVIEW

**Purpose:** QMDJ + BaZi Integrated Analysis System  
**Deployment:** Streamlit Cloud ✅ DEPLOYED  
**Access:** Desktop (home) + iPhone (travel)  
**Integration:** Feeds data to Project 1 (Analyst Engine)  
**Live URL:** https://qimen-pro-qfvejjsappeenzfeuretzw9.streamlit.app/  
**Repository:** https://github.com/Espivc/qimen-pro

---

## ✅ COMPLETED PHASES

### **Phase 1: Professional Styling** ✅ COMPLETE
**Completed:** 2025-12-28
- Dark theme with gold accents
- Professional CSS styling
- Mobile responsive design

---

### **Phase 2: Modular Architecture** ✅ COMPLETE
**Completed:** 2025-12-29
- 5-page structure
- Utility modules
- Basic BaZi Calculator
- Universal Schema v2.0 export

---

### **Phase 3: Enhanced UX & Features** 🔄 IN PROGRESS
**Started:** 2025-12-29

#### ✅ Completed:
- [x] Time text input (HH:MM precision)
- [x] Profile sync fix (Settings → Dashboard)
- [x] Callback pattern for saves
- [x] **Help & Guide page** (NEW!)
- [x] **Quick Reference card in sidebar** (NEW!)
- [x] **Palace selection with topic hints** (NEW!)
- [x] **Palace Quick Reference expander** (NEW!)

#### 📋 Pending:
- [ ] Real QMDJ calculations (kinqimen library)
- [ ] Formation detection (Joey Yap #64/#73)
- [ ] Improved export formatting
- [ ] ML feedback loop
- [ ] Persistent storage

---

## 📁 CURRENT FILE STRUCTURE

```
qimen-pro/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── style.css
├── pages/
│   ├── 1_Chart.py
│   ├── 2_Export.py
│   ├── 3_History.py
│   ├── 4_Settings.py      ✅ v4 with callback
│   └── 5_Help.py          ✅ NEW! Help & Guide
├── utils/
│   └── [modules]
├── app.py                 ✅ v4 with palace hints
├── config.py
├── requirements.txt
└── PROJECT_STATE.md
```

---

## 🎯 CURRENT FEATURES

### **Dashboard (app.py v4)** ✅
- Quick chart with date/time input
- **Palace grid with topic icons & hints** (NEW!)
- **Quick Reference in sidebar** (NEW!)
- BaZi profile card
- Recent analyses

### **Help & Guide (5_Help.py)** ✅ NEW!
- What is QMDJ explanation
- Step-by-step workflow
- **Palace selection guide with visual grid**
- **Quick reference card** (auspicious/inauspicious)
- Five elements guide

### **Settings (4_Settings.py v4)** ✅
- BaZi Calculator with callback save
- Profile management
- Debug expander

---

## 🏛️ PALACE REFERENCE (Built into App)

| # | Name | Direction | Topic | Use For |
|---|------|-----------|-------|---------|
| 1 | 坎 Kan | N | 💼 Career | Job, business, life path |
| 2 | 坤 Kun | SW | 💕 Relations | Marriage, partnership |
| 3 | 震 Zhen | E | 💪 Health | Health, family, new starts |
| 4 | 巽 Xun | SE | 💰 Wealth | Money, investments |
| 5 | 中 Center | C | 🎯 Self | General, yourself |
| 6 | 乾 Qian | NW | 🤝 Mentor | Helpful people, travel |
| 7 | 兑 Dui | W | 👶 Children | Creativity, joy, projects |
| 8 | 艮 Gen | NE | 📚 Knowledge | Education, skills |
| 9 | 离 Li | S | 🌟 Fame | Recognition, reputation |

---

## 📋 FUTURE PHASES

### **Phase 4: Real QMDJ Calculations** 📋 PLANNED
- Integrate kinqimen library
- Chai Bu (拆补) method
- Full 9-palace chart generation
- Formation detection from Joey Yap #64/#73
- Host-Guest analysis (#71)

### **Phase 5: Enhanced BaZi Analysis** 📋 PLANNED
**Full BaZi module with:**

#### 5.1 Complete Four Pillars
- Hidden Stems (藏干) for each Branch
- Proper stem/branch combinations

#### 5.2 Day Master Strength Calculation
- Month season analysis (most important)
- Element counting from all pillars
- Hidden stems contribution
- Strength score (1-10)
- Accurate Weak/Strong determination

#### 5.3 Ten Gods Analysis
- Calculate Ten Gods for ALL positions
- Identify DOMINANT Ten God
- Accurate personality profile based on chart

#### 5.4 Element Balance
- Count all elements (stems + hidden)
- Show element distribution chart
- Identify missing/excess elements

#### 5.5 Special Structures Detection
- 财库 Wealth Vault
- 贵人 Nobleman (天乙, 月德, etc.)
- 桃花 Peach Blossom
- 驿马 Traveling Horse
- 羊刃 Blade
- 华盖 Canopy
- Self-punishment, destructions

#### 5.6 Combinations & Clashes
- 三合 Three Combinations (Fire/Water/Metal/Wood frames)
- 六合 Six Combinations
- 六冲 Six Clashes
- 相刑 Punishments
- 相害 Harms

#### 5.7 Advanced Features (Optional)
- 大运 Major Luck Pillars (10-year periods)
- 流年 Annual Pillars
- Compatibility analysis

---

## 🔧 TECHNICAL NOTES

### Callback Pattern (Phase 3 Fix)
```python
# This runs BEFORE page rerenders
st.button("Save", on_click=save_callback)

def save_callback():
    st.session_state.user_profile = data
```

### Session State Keys
- `user_profile` - BaZi profile data
- `selected_palace` - Currently selected palace (1-9)
- `calculated_bazi` - Temp storage for BaZi calculation
- `analyses` - History of analyses
- `last_chart` - Most recent generated chart

---

## 🔄 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
"Continue Qi Men Pro development - check PROJECT_STATE.md.
Phase 3 in progress, Help page added.
I want to [your request here]."
```

### Key Files for Phase 3:
- `app.py` → `app_v4.py` (with palace hints)
- `pages/4_Settings.py` → `4_Settings_v4.py` (with callback)
- `pages/5_Help.py` → NEW Help & Guide page

---

## 📖 REFERENCE BOOKS

**Joey Yap QMDJ:**
- #64: Formations (Auspicious/Inauspicious)
- #71: Sun Tzu Host/Guest Analysis
- #72: Timing and Hour Selection
- #73: Advanced Formations

**BaZi References (for Phase 5):**
- Hidden Stems tables
- Ten Gods calculation
- Special structures rules
- Combination/clash tables

---

## 🎊 PROJECT STATUS SUMMARY

**Phase 3 Progress:** 60% complete

**What's New:**
- ✅ Help & Guide page with full QMDJ explanation
- ✅ Palace selection with topic hints
- ✅ Quick Reference card in sidebar
- ✅ Palace Quick Reference expander

**What's Next:**
- 📋 Real QMDJ calculations (Phase 4)
- 📋 Enhanced BaZi (Phase 5 - documented above)

---

**END OF PROJECT STATE**  
*Last updated: 2025-12-29*  
*Status: 🟢 Phase 3 - Help & UI enhancements complete*
