"""
📤 Export to Analyst Page
Seamless integration with Project 1 (Analyst Engine)
"""

import streamlit as st
from datetime import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PALACE_INFO, ELEMENT_EMOJI
from utils.calculations import generate_chart
from utils.bazi_profile import load_profile, calculate_bazi_alignment
from utils.export_formatter import generate_analysis_prompt, generate_json_export, generate_csv_row
from utils.language import get_lang

st.set_page_config(
    page_title="Export - Qi Men Pro",
    page_icon="📤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    [data-testid="stSidebar"] { background-color: #16213e; }
    h1, h2, h3 { color: #d4af37 !important; }
    .copy-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.85rem;
        color: #c9d1d9;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = load_profile()
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None
if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = None
if 'export_palace' not in st.session_state:
    st.session_state.export_palace = None
if 'chart_purpose' not in st.session_state:
    st.session_state.chart_purpose = "General Forecast"
if 'lang_mode' not in st.session_state:
    st.session_state.lang_mode = "mixed"

# Initialize language helper
L = get_lang(st.session_state.lang_mode)

def main():
    st.title("📤 Export to Analyst Engine")
    
    # Check if we have a chart
    if st.session_state.current_chart is None:
        st.warning("⚠️ No chart generated yet. Please generate a chart first.")
        
        if st.button("Go to Chart Generator →", type="primary"):
            st.switch_page("pages/1_Chart.py")
        
        st.markdown("""
        <div style="margin-top: 2rem; padding: 2rem; background: #16213e; border-radius: 12px; 
                    border: 1px solid #2a3f5f; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔮</div>
            <div style="color: #b8b8b8; font-size: 1rem;">
                Generate a QMDJ chart and select a palace to export
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    chart = st.session_state.current_chart
    profile = st.session_state.profile
    
    # Use export_palace if set, otherwise use selected_palace
    selected_palace = st.session_state.export_palace or st.session_state.selected_palace
    
    # Sidebar - Palace Selection
    with st.sidebar:
        st.markdown("### 📍 Select Palace")
        
        palace_options = {
            f"{PALACE_INFO[i]['name']} ({PALACE_INFO[i]['direction']})": i 
            for i in range(1, 10)
        }
        
        default_idx = list(palace_options.values()).index(selected_palace) if selected_palace in palace_options.values() else 0
        
        selected_name = st.selectbox(
            "Palace",
            options=list(palace_options.keys()),
            index=default_idx,
            key="export_palace_select"
        )
        selected_palace = palace_options[selected_name]
        
        st.markdown("### 🎯 Purpose")
        purpose = st.selectbox(
            "Analysis Purpose",
            ["General Forecast", "Wealth / Business", "Relationship", "Strategic Decision", "Date Selection"],
            index=["General Forecast", "Wealth / Business", "Relationship", "Strategic Decision", "Date Selection"].index(st.session_state.chart_purpose),
            key="export_purpose"
        )
        
        st.markdown("### ℹ️ Chart Info")
        st.markdown(f"""
        <div style="background: #1a1a2e; padding: 0.75rem; border-radius: 8px; border: 1px solid #2a3f5f;">
            <div style="color: #b8b8b8; font-size: 0.85rem;">Date/Time</div>
            <div style="color: #ffffff;">{chart.datetime.strftime('%Y-%m-%d %H:%M')}</div>
            <div style="color: #b8b8b8; font-size: 0.85rem; margin-top: 0.5rem;">Structure</div>
            <div style="color: #ffffff;">{chart.structure} · Ju {chart.ju_number}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Get palace data
    palace_data = chart.palaces.get(selected_palace, {})
    palace_info = PALACE_INFO[selected_palace]
    formation = chart.detect_formation(selected_palace)
    qmdj_score = chart.calculate_palace_score(selected_palace)
    alignment = calculate_bazi_alignment(profile, palace_data)
    bazi_score = alignment['score']
    
    # Main content
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, transparent 100%);
                border: 1px solid rgba(212, 175, 55, 0.3);
                border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #d4af37; font-size: 1.3rem; font-weight: 600;">
                    🎯 Selected Palace Analysis
                </div>
                <div style="color: #ffffff; font-size: 1.1rem; margin-top: 0.25rem;">
                    {palace_info['name']} {palace_info['chinese']} ({palace_info['direction']})
                </div>
                <div style="color: #b8b8b8; font-size: 0.9rem;">
                    Purpose: {purpose}
                </div>
            </div>
            <div style="display: flex; gap: 1.5rem;">
                <div style="text-align: center;">
                    <div style="color: #b8b8b8; font-size: 0.75rem;">QMDJ</div>
                    <div style="color: {'#4CAF50' if qmdj_score >= 7 else '#FFC107' if qmdj_score >= 4.5 else '#F44336'}; 
                                font-size: 1.8rem; font-weight: 600;">{qmdj_score}</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #b8b8b8; font-size: 0.75rem;">BaZi</div>
                    <div style="color: {'#4CAF50' if bazi_score >= 7 else '#FFC107' if bazi_score >= 4.5 else '#F44336'}; 
                                font-size: 1.8rem; font-weight: 600;">{bazi_score}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate the analysis prompt
    analysis_prompt = generate_analysis_prompt(
        chart_datetime=chart.datetime,
        timezone=chart.timezone,
        structure=chart.structure,
        ju_number=chart.ju_number,
        palace_data=palace_data,
        palace_name=palace_info['name'],
        formation=formation,
        bazi_profile=profile,
        purpose=purpose
    )
    
    # Main Export Section
    st.markdown("### 📋 Analysis Prompt for Project 1")
    st.markdown("<small style='color: #b8b8b8;'>Copy this prompt and paste directly into the Analyst Engine</small>", unsafe_allow_html=True)
    
    # Copy button with prominent styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Using text_area for copy functionality
        st.text_area(
            "Analysis Prompt",
            value=analysis_prompt,
            height=350,
            key="prompt_text",
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <div style="text-align: center; margin-top: 0.5rem;">
            <small style="color: #b8b8b8;">
                💡 Select all (Ctrl+A) and copy (Ctrl+C) the text above, then paste into Project 1
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Other Export Formats
    st.markdown("### 📄 Other Export Formats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #16213e; border: 1px solid #2a3f5f; border-radius: 10px; 
                    padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📄</div>
            <div style="color: #d4af37; font-weight: 600;">Full JSON Schema</div>
            <div style="color: #b8b8b8; font-size: 0.8rem; margin-top: 0.25rem;">
                Universal Schema v2.0 format
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate JSON
        json_export = generate_json_export(
            chart_datetime=chart.datetime,
            timezone=chart.timezone,
            structure=chart.structure,
            ju_number=chart.ju_number,
            palace_data=palace_data,
            palace_name=palace_info['name'],
            formation=formation,
            bazi_profile=profile,
            qmdj_score=qmdj_score,
            bazi_score=bazi_score,
            purpose=purpose
        )
        
        json_str = json.dumps(json_export, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"qmdj_export_{chart.datetime.strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.markdown("""
        <div style="background: #16213e; border: 1px solid #2a3f5f; border-radius: 10px; 
                    padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
            <div style="color: #d4af37; font-weight: 600;">CSV Row</div>
            <div style="color: #b8b8b8; font-size: 0.8rem; margin-top: 0.25rem;">
                For database append
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        csv_row = generate_csv_row(
            chart_datetime=chart.datetime,
            palace_data=palace_data,
            palace_name=palace_info['name'],
            formation=formation,
            qmdj_score=qmdj_score,
            bazi_score=bazi_score,
            purpose=purpose
        )
        
        st.download_button(
            label="Download CSV Row",
            data=csv_row,
            file_name=f"qmdj_row_{chart.datetime.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.markdown("""
        <div style="background: #16213e; border: 1px solid #2a3f5f; border-radius: 10px; 
                    padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📝</div>
            <div style="color: #d4af37; font-weight: 600;">Summary Text</div>
            <div style="color: #b8b8b8; font-size: 0.8rem; margin-top: 0.25rem;">
                Quick reference format
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        summary = f"""QMDJ Analysis Summary
Date: {chart.datetime.strftime('%Y-%m-%d %H:%M')} ({chart.timezone})
Structure: {chart.structure}, Ju {chart.ju_number}

Palace: {palace_info['name']} ({palace_info['direction']})
Element: {palace_info['element']}

Components:
- Heaven Stem: {palace_data.get('heaven_stem', {}).get('chinese', '')} ({palace_data.get('heaven_stem', {}).get('element', '')})
- Door: {palace_data.get('door', {}).get('name', '')}
- Star: {palace_data.get('star', {}).get('name', '')}
- Deity: {palace_data.get('deity', {}).get('name', '')}

Formation: {formation.get('name', 'None') if formation else 'None'}

Scores:
- QMDJ: {qmdj_score}/10
- BaZi Alignment: {bazi_score}/10
- Combined: {round((qmdj_score + bazi_score) / 2, 1)}/10

Verdict: {chart.get_verdict(qmdj_score)}
"""
        
        st.download_button(
            label="Download Summary",
            data=summary,
            file_name=f"qmdj_summary_{chart.datetime.strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Workflow reminder
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1.5rem; background: #16213e; border-radius: 12px; 
                border: 1px solid #2a3f5f;">
        <div style="color: #d4af37; font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;">
            🔄 Workflow: Project 2 → Project 1
        </div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; padding: 0.75rem; background: #1a1a2e; border-radius: 8px;">
                <div style="color: #d4af37; font-weight: 500;">1. Generate</div>
                <div style="color: #b8b8b8; font-size: 0.85rem;">Create chart & select palace ✓</div>
            </div>
            <div style="flex: 1; min-width: 200px; padding: 0.75rem; background: #1a1a2e; border-radius: 8px;">
                <div style="color: #d4af37; font-weight: 500;">2. Export</div>
                <div style="color: #b8b8b8; font-size: 0.85rem;">Copy analysis prompt ✓</div>
            </div>
            <div style="flex: 1; min-width: 200px; padding: 0.75rem; background: #1a1a2e; border-radius: 8px;">
                <div style="color: #d4af37; font-weight: 500;">3. Analyze</div>
                <div style="color: #b8b8b8; font-size: 0.85rem;">Paste into Project 1 →</div>
            </div>
            <div style="flex: 1; min-width: 200px; padding: 0.75rem; background: #1a1a2e; border-radius: 8px;">
                <div style="color: #d4af37; font-weight: 500;">4. Track</div>
                <div style="color: #b8b8b8; font-size: 0.85rem;">Update outcome in History</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expander for JSON preview
    with st.expander("📄 View Full JSON Schema"):
        st.json(json_export)

if __name__ == "__main__":
    main()
