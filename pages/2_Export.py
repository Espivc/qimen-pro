"""
Ming Qimen 明奇门 - Export Page
Fixed: Function order, added copy to clipboard
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json
import csv
import io

st.set_page_config(
    page_title="Export | Ming Qimen",
    page_icon="📤",
    layout="wide"
)

# Singapore timezone
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# ============ HELPER FUNCTION - DEFINED FIRST! ============
def convert_to_universal_schema(chart):
    """Convert Ming Qimen chart to Universal Schema v2.0"""
    
    # Get user profile if available
    user_profile = st.session_state.get('user_profile', {})
    
    universal = {
        "schema_version": "2.0",
        "schema_name": "Ming_Qimen_Universal_Schema",
        
        "metadata": {
            "date_time": f"{chart.get('metadata', {}).get('date', '')} {chart.get('metadata', {}).get('time', '')}",
            "timezone": "SGT (UTC+8)",
            "method": "Chai Bu",
            "purpose": "Forecasting",
            "analysis_type": "QMDJ_BAZI_INTEGRATED",
            "generated_by": "Ming Qimen 明奇门"
        },
        
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": chart.get('metadata', {}).get('structure', ''),
            "ju_number": chart.get('metadata', {}).get('ju_number', 0),
            
            "palace_analyzed": {
                "name": chart.get('palace', {}).get('name', ''),
                "number": chart.get('palace', {}).get('number', 0),
                "direction": chart.get('palace', {}).get('direction', ''),
                "palace_element": chart.get('palace', {}).get('element', ''),
                "topic": chart.get('palace', {}).get('topic', '')
            },
            
            "components": {
                "heaven_stem": chart.get('components', {}).get('heaven_stem', ''),
                "earth_stem": chart.get('components', {}).get('earth_stem', ''),
                "star": chart.get('components', {}).get('star', {}),
                "door": chart.get('components', {}).get('door', {}),
                "deity": chart.get('components', {}).get('deity', {})
            }
        },
        
        "bazi_data": {
            "chart_source": "User Profile" if user_profile else "Not Provided",
            "day_master": {
                "stem": user_profile.get('day_master', 'Unknown'),
                "element": user_profile.get('element', 'Unknown'),
                "strength": user_profile.get('strength', 'Unknown')
            },
            "useful_gods": user_profile.get('useful_gods', []),
            "unfavorable_elements": user_profile.get('unfavorable', []),
            "profile": user_profile.get('profile', 'Unknown')
        },
        
        "synthesis": {
            "verdict": chart.get('guidance', {}).get('verdict', ''),
            "summary": chart.get('guidance', {}).get('summary', ''),
            "advice": chart.get('guidance', {}).get('advice', ''),
            "guidance_type": chart.get('guidance', {}).get('type', '')
        },
        
        "tracking": {
            "generated_at": get_singapore_time().isoformat(),
            "outcome_status": "PENDING",
            "outcome_notes": ""
        }
    }
    
    return universal

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("📤 Export 导出")
st.markdown("Export your readings for Project 1 integration")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Current Reading", "📚 History Export", "❓ How to Use"])

# ============ TAB 1: CURRENT CHART ============
with tab1:
    st.markdown("### 📊 Current Reading Data")
    
    if 'current_chart' in st.session_state and st.session_state.current_chart:
        chart = st.session_state.current_chart
        
        # Display summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Reading Summary")
            
            if 'palace' in chart:
                palace = chart['palace']
                st.markdown(f"**Topic:** {palace.get('icon', '')} {palace.get('topic', 'N/A')}")
                st.markdown(f"**Palace:** #{palace.get('number', 'N/A')} {palace.get('name', '')}")
                st.markdown(f"**Element:** {palace.get('element', 'N/A')}")
            
            if 'metadata' in chart:
                meta = chart['metadata']
                st.markdown(f"**Date:** {meta.get('date', 'N/A')}")
                st.markdown(f"**Time:** {meta.get('time', 'N/A')} (SGT)")
                st.markdown(f"**Chinese Hour:** {meta.get('chinese_hour', 'N/A')}")
        
        with col2:
            st.markdown("#### Guidance")
            
            if 'guidance' in chart:
                guidance = chart['guidance']
                verdict = guidance.get('verdict', 'N/A')
                summary = guidance.get('summary', '')
                advice = guidance.get('advice', '')
                
                if guidance.get('type') == 'success':
                    st.success(f"**{verdict}**")
                elif guidance.get('type') == 'warning':
                    st.warning(f"**{verdict}**")
                else:
                    st.info(f"**{verdict}**")
                
                st.markdown(f"*{summary}*")
                st.markdown(f"💡 {advice}")
            
            elif 'verdict' in chart:
                verdict = chart['verdict']
                st.markdown(f"**Verdict:** {verdict.get('text', 'N/A')}")
        
        st.markdown("---")
        
        # Components display
        st.markdown("#### Components")
        
        if 'components' in chart:
            comp = chart['components']
            comp_cols = st.columns(5)
            
            with comp_cols[0]:
                st.markdown("**Heaven Stem**")
                st.markdown(comp.get('heaven_stem', 'N/A'))
            
            with comp_cols[1]:
                st.markdown("**Earth Stem**")
                st.markdown(comp.get('earth_stem', 'N/A'))
            
            with comp_cols[2]:
                if 'star' in comp:
                    star = comp['star']
                    st.markdown("**Star**")
                    if isinstance(star, dict):
                        st.markdown(f"{star.get('chinese', '')} {star.get('english', '')}")
                        st.caption(star.get('nature', ''))
                    else:
                        st.markdown(str(star))
            
            with comp_cols[3]:
                if 'door' in comp:
                    door = comp['door']
                    st.markdown("**Door**")
                    if isinstance(door, dict):
                        st.markdown(f"{door.get('chinese', '')} {door.get('english', '')}")
                        st.caption(door.get('nature', ''))
                    else:
                        st.markdown(str(door))
            
            with comp_cols[4]:
                if 'deity' in comp:
                    deity = comp['deity']
                    st.markdown("**Spirit**")
                    if isinstance(deity, dict):
                        st.markdown(f"{deity.get('chinese', '')} {deity.get('english', '')}")
                        st.caption(deity.get('nature', ''))
                    else:
                        st.markdown(str(deity))
        
        st.markdown("---")
        
        # ============ EXPORT FOR PROJECT 1 ============
        st.markdown("### 🚀 Export for Project 1")
        st.markdown("Copy the JSON below and paste it into Project 1 (AI Analyst)")
        
        # Convert to Universal Schema
        universal_data = convert_to_universal_schema(chart)
        universal_json = json.dumps(universal_data, indent=2, ensure_ascii=False, default=str)
        
        # Text area for easy copy
        st.text_area(
            "📋 Universal Schema JSON (Select All → Copy)",
            value=universal_json,
            height=300,
            help="Click inside, press Ctrl+A (or Cmd+A) to select all, then Ctrl+C (or Cmd+C) to copy"
        )
        
        # Download button
        st.download_button(
            "📥 Download Universal Schema JSON",
            data=universal_json,
            file_name=f"ming_qimen_universal_{chart.get('metadata', {}).get('date', 'reading')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Additional export options
        with st.expander("📂 More Export Options"):
            export_cols = st.columns(2)
            
            with export_cols[0]:
                # Raw JSON export
                raw_json = json.dumps(chart, indent=2, ensure_ascii=False, default=str)
                st.download_button(
                    "📥 Download Raw Chart JSON",
                    data=raw_json,
                    file_name=f"ming_qimen_raw_{chart.get('metadata', {}).get('date', 'reading')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with export_cols[1]:
                if st.button("👁️ View Raw JSON", use_container_width=True):
                    st.json(chart)
        
    else:
        st.info("📭 No reading available. Generate a reading from the **Home** or **Chart** page first.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Home", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("📈 Go to Chart", use_container_width=True):
                st.switch_page("pages/1_Chart.py")

# ============ TAB 2: HISTORY EXPORT ============
with tab2:
    st.markdown("### 📚 Export History")
    
    if 'analyses' in st.session_state and st.session_state.analyses:
        analyses = st.session_state.analyses
        
        st.markdown(f"**Total Readings:** {len(analyses)}")
        
        # Show recent history
        st.markdown("#### Recent Readings")
        
        for i, analysis in enumerate(reversed(analyses[-10:])):
            with st.expander(f"📊 {analysis.get('date', 'N/A')} {analysis.get('time', '')} - {analysis.get('topic', analysis.get('palace', 'N/A'))}"):
                st.json(analysis)
        
        st.markdown("---")
        
        # Export all history
        st.markdown("#### Export All History")
        
        export_cols = st.columns(2)
        
        with export_cols[0]:
            # JSON export
            json_str = json.dumps(analyses, indent=2, ensure_ascii=False, default=str)
            st.download_button(
                "📥 Download History (JSON)",
                data=json_str,
                file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with export_cols[1]:
            # CSV export
            if analyses:
                csv_buffer = io.StringIO()
                
                all_keys = set()
                for a in analyses:
                    all_keys.update(a.keys())
                
                fieldnames = sorted(list(all_keys))
                
                writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
                writer.writeheader()
                for a in analyses:
                    writer.writerow(a)
                
                st.download_button(
                    "📥 Download History (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.info("📭 No history available yet. Your readings will appear here after you generate them.")

# ============ TAB 3: HOW TO USE ============
with tab3:
    st.markdown("### ❓ How to Copy to Project 1")
    
    st.markdown("""
    #### Step-by-Step Guide
    
    **1️⃣ Generate a Reading**
    - Go to Home or Chart page
    - Select your topic and time
    - Click "Get Your Reading"
    
    **2️⃣ Come to Export Page**
    - Click on Export in the sidebar
    - Your reading will be shown here
    
    **3️⃣ Copy the JSON**
    - Find the text box with "Universal Schema JSON"
    - Click inside the text box
    - Press **Ctrl+A** (Windows) or **Cmd+A** (Mac) to select all
    - Press **Ctrl+C** (Windows) or **Cmd+C** (Mac) to copy
    
    **4️⃣ Paste to Project 1**
    - Open Project 1 (AI Analyst)
    - Paste the JSON data
    - Project 1 will analyze your reading!
    
    ---
    
    #### 📋 What Gets Exported?
    
    The Universal Schema includes:
    
    | Section | Data |
    |---------|------|
    | **Metadata** | Date, time, timezone, method |
    | **QMDJ Data** | Palace, components (Star, Door, Spirit) |
    | **BaZi Data** | Your Day Master, helpful elements |
    | **Synthesis** | Verdict, summary, advice |
    | **Tracking** | For ML feedback loop |
    
    ---
    
    #### 💡 Pro Tips
    
    - **Download** the JSON if you want to save it for later
    - **History Export** lets you download all your past readings
    - **CSV format** is great for spreadsheets and ML training
    """)

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Export | Singapore Time (UTC+8)")
