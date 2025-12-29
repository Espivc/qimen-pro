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

- [x] Dark theme with gold accents
- [x] Professional CSS styling
- [x] Mobile responsive design
- [x] Streamlit Cloud deployment

---

### **Phase 2: Modular Architecture** ✅ COMPLETE
**Completed:** 2025-12-29

- [x] 5-page structure (Dashboard, Chart, Export, History, Settings)
- [x] Utility modules (calculations, database, mappings)
- [x] BaZi Calculator integration
- [x] Mixed language support (English + Chinese)
- [x] Universal Schema v2.0 JSON export

---

### **Phase 3: Enhanced Features** 🔄 IN PROGRESS
**Started:** 2025-12-29

#### ✅ Completed:
- [x] **Time text input (HH:MM)** - Replaced dropdown with precise time input
- [x] **Profile sync fix** - Settings → Dashboard sync now working
- [x] **Callback pattern** - Using `on_click` callback for reliable saves
- [x] **Session state management** - Proper state handling across pages
- [x] **Chinese hour display** - Shows 时辰 with animal zodiac

#### 📋 Pending:
- [ ] Real QMDJ calculations (kinqimen library integration)
- [ ] Formation detection (Joey Yap #64/#73)
- [ ] Improved export formatting
- [ ] Enhanced BaZi Day Master analysis
- [ ] ML feedback loop for outcome tracking
- [ ] Persistent storage (save profile to file)

---

## 📁 CURRENT FILE STRUCTURE

```
qimen-pro/
├── .streamlit/
│   └── config.toml          ✅ Dark theme config
├── assets/
│   └── style.css            ✅ Professional styling
├── pages/
│   ├── 1_Chart.py           ✅ Chart Generator
│   ├── 2_Export.py          ✅ Export page
│   ├── 3_History.py         ✅ History & ML tracking
│   └── 4_Settings.py        ✅ Settings (v4 - with callback fix)
├── utils/
│   ├── __init__.py
│   ├── bazi_calculator.py   ✅ Pure Python BaZi
│   ├── bazi_profile.py
│   ├── calculations.py      ✅ QMDJ calculations
│   ├── database.py          ✅ ML tracking
│   ├── export_formatter.py  ✅ JSON export
│   ├── language.py          ✅ Mixed language
│   └── mappings.py          ✅ Joey Yap terms
├── data/
│   └── .gitkeep
├── app.py                   ✅ Dashboard (v3 - with profile display fix)
├── config.py                ✅ Configuration
├── requirements.txt         ✅ Dependencies
└── PROJECT_STATE.md         ← This file
```

---

## 🎯 CURRENT FEATURES

### **Dashboard (app.py)** ✅
- Quick chart generator with date/time input
- **Time text input (HH:MM)** - NEW in Phase 3!
- Chinese hour (时辰) display with zodiac animal
- Palace selection (9-palace grid)
- BaZi profile card (synced from Settings)
- Recent analyses display

### **Settings (4_Settings.py)** ✅
- **Birthday Calculator** with precise time input
- Four Pillars (四柱) calculation and display
- Day Master analysis with useful gods
- **Save profile with callback** - Fixed in Phase 3!
- Profile tab showing saved data
- Debug expander for troubleshooting

### **Chart Generator (1_Chart.py)** ✅
- Date/time selection
- Palace selection
- Basic QMDJ calculations
- Element color coding

### **Export (2_Export.py)** ✅
- Universal Schema v2.0 JSON format
- Copy to clipboard
- Download functionality

### **History (3_History.py)** ✅
- Analysis tracking
- Outcome recording
- Basic statistics

---

## 🔧 TECHNICAL DECISIONS (Phase 3)

### **Why Callback Pattern for Save?**
```python
st.button("Save", on_click=save_profile_callback)
```
- Streamlit reruns page on every button click
- Data calculated before click was lost on rerun
- `on_click` callback runs BEFORE rerun, ensuring data is saved
- This is the recommended Streamlit pattern for form submissions

### **Why Session State for Profile?**
- `st.session_state.user_profile` persists across page navigation
- Shared between Dashboard and Settings
- Must initialize with `if 'key' not in st.session_state`

### **Why Text Input for Time?**
- Dropdown limited to preset values
- Text input allows exact minute precision (e.g., 02:37)
- Important for boundary times between 时辰
- Better UX for users who know exact birth time

---

## 🐛 ISSUES RESOLVED (Phase 3)

### **Issue: Profile Not Syncing** ❌ → ✅ FIXED
**Problem:** Saving profile in Settings didn't update Dashboard  
**Cause:** Streamlit rerun pattern losing calculated data  
**Solution:** Used `on_click=callback` pattern to save before rerun  
**Files Changed:** `pages/4_Settings.py` (v4)

### **Issue: HTML Not Rendering** ❌ → ✅ FIXED
**Problem:** Raw HTML code showing in profile card  
**Cause:** Complex f-string with HTML breaking markdown  
**Solution:** Replaced with native Streamlit components (`st.success`, `st.error`, etc.)  
**Files Changed:** `app.py` (v3)

### **Issue: Time Dropdown Limited** ❌ → ✅ FIXED
**Problem:** Could only select preset hour values  
**Solution:** Changed to text input with HH:MM parsing  
**Files Changed:** `app.py`, `pages/4_Settings.py`

---

## 🎓 USER PROFILE (Ben's BaZi)

**Day Master 日主:** 庚 Geng (Metal 金 - Yang)  
**Strength 强弱:** Weak  
**Useful Gods 用神:** Earth 土, Metal 金  
**Unfavorable 忌神:** Fire 火, Wood 木  
**Profile 性格:** Pioneer 🎯 (Indirect Wealth 偏财)

---

## 📱 DEPLOYMENT INFO

| Item | Value |
|------|-------|
| Platform | Streamlit Cloud |
| Repository | github.com/Espivc/qimen-pro |
| Branch | main |
| Main File | app.py |
| Live URL | qimen-pro-qfvejjsappeenzfeuretzw9.streamlit.app |

---

## 📝 NEXT STEPS (Priority Order)

1. **Real QMDJ Calculations** - Integrate kinqimen library
2. **Formation Detection** - Joey Yap books #64/#73
3. **Improved Export** - Better JSON/CSV for Project 1
4. **Persistent Storage** - Save profile to file (survives refresh)
5. **ML Feedback Loop** - Outcome tracking system
6. **Enhanced BaZi Analysis** - More detailed Day Master insights

---

## 🔄 CONTINUITY INSTRUCTIONS

### **Starting New Chat:**
```
"Continue Qi Men Pro (Project 2) development - 
check PROJECT_STATE.md in Espivc/qimen-pro repository.
Phase 3 in progress. I want to [your request here]."
```

### **Key Files to Reference:**
- `app.py` - Dashboard (v3 with native Streamlit components)
- `pages/4_Settings.py` - Settings (v4 with callback pattern)
- `PROJECT_STATE.md` - This file

### **Update This File When:**
- ✅ Complete a feature
- ✅ Fix a bug
- ✅ Make architecture decisions
- ✅ Change file versions

---

## 📖 REFERENCE

### **Joey Yap Books:**
- #64: QMDJ Formations
- #71: Sun Tzu Host/Guest Analysis
- #72: Timing and Hour Selection
- #73: Advanced Formations

### **Technical Stack:**
- Python 3.10+
- Streamlit (Web UI)
- kinqimen (QMDJ calculations - pending full integration)
- Pandas (data handling)

---

## 🎊 PROJECT STATUS SUMMARY

**Phase 3 Progress:** 40% complete

**What Works:**
- ✅ Time text input (HH:MM precision)
- ✅ Profile sync between pages
- ✅ BaZi Calculator with callback save
- ✅ Chinese hour display
- ✅ Session state management

**What's Next:**
- 📋 Real QMDJ calculations
- 📋 Formation detection
- 📋 Export improvements

---

**END OF PROJECT STATE**  
*Last updated: 2025-12-29*  
*Status: 🟢 Phase 3 IN PROGRESS - Core fixes complete*
