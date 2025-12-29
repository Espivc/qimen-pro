"""
Qi Men Pro - Export Page
Phase 3: Enhanced export with Universal Schema v2.0 and CSV
"""

import streamlit as st
from datetime import datetime
import json
import csv
import io

st.set_page_config(
    page_title="Export | Qi Men Pro",
    page_icon="📤",
    layout="wide"
)

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass


def format_universal_schema(chart_data, user_profile=None):
    """
    Format chart data to Universal Schema v2.0
    Compatible with Project 1 (Analyst Engine)
    """
    
    if not chart_data:
        return None
    
    # Get user profile if available
    profile = user_profile or st.session_state.get('user_profile', {})
    
    # Build Universal Schema v2.0 structure
    schema = {
        "schema_version": "2.0",
        "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
        
        "metadata": {
            "date_time": f"{chart_data['metadata']['date']} {chart_data['metadata']['time']}",
            "timezone": "UTC+8",
            "method": "Chai Bu",
            "purpose": "Strategic",
            "analysis_type": "QMDJ_BAZI_INTEGRATED" if profile else "QMDJ_ONLY"
        },
        
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": chart_data['metadata']['structure'],
            "ju_number": chart_data['metadata']['ju_number'],
            
            "palace_analyzed": {
                "name": chart_data['palace']['name'].split()[0],  # Just Chinese
                "name_english": chart_data['palace']['name'].split()[1] if len(chart_data['palace']['name'].split()) > 1 else "",
                "number": chart_data['palace']['number'],
                "direction": chart_data['palace']['direction'],
                "palace_element": chart_data['palace']['element']
            },
            
            "components": {
                "heaven_stem": {
                    "character": chart_data['components']['heaven_stem']['chinese'],
                    "pinyin": chart_data['components']['heaven_stem']['english'],
                    "element": get_stem_element(chart_data['components']['heaven_stem']['full']),
                    "polarity": get_stem_polarity(chart_data['components']['heaven_stem']['full'])
                },
                "earth_stem": {
                    "character": chart_data['components']['earth_stem']['chinese'],
                    "pinyin": chart_data['components']['earth_stem']['english'],
                    "element": get_stem_element(chart_data['components']['earth_stem']['full']),
                    "polarity": get_stem_polarity(chart_data['components']['earth_stem']['full'])
                },
                "door": {
                    "chinese": chart_data['components']['door']['chinese'],
                    "english": chart_data['components']['door']['english'],
                    "element": chart_data['components']['door']['element'],
                    "category": chart_data['components']['door']['nature'],
                    "strength_in_palace": chart_data['components']['door']['strength'][0],
                    "strength_score": chart_data['components']['door']['strength'][1]
                },
                "star": {
                    "chinese": chart_data['components']['star']['chinese'],
                    "english": chart_data['components']['star']['english'],
                    "element": chart_data['components']['star']['element'],
                    "category": chart_data['components']['star']['nature'],
                    "strength_in_palace": chart_data['components']['star']['strength'][0],
                    "strength_score": chart_data['components']['star']['strength'][1]
                },
                "deity": {
                    "chinese": chart_data['components']['deity']['chinese'],
                    "english": chart_data['components']['deity']['english'],
                    "nature": chart_data['components']['deity']['nature']
                }
            },
            
            "formation": None
        },
        
        "bazi_data": None,
        
        "synthesis": {
            "qmdj_score": calculate_qmdj_score(chart_data),
            "bazi_alignment_score": None,
            "combined_verdict_score": None,
            "verdict": chart_data['analysis']['overall_nature'].split()[0].upper(),
            "confidence": "MEDIUM",
            "primary_action": chart_data['analysis']['recommendation']
        },
        
        "tracking": {
            "db_row": generate_db_row(chart_data, profile),
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": None
        }
    }
    
    # Add formation if present
    if chart_data.get('formation'):
        schema['qmdj_data']['formation'] = {
            "primary_formation": {
                "chinese": chart_data['formation']['chinese'],
                "english": chart_data['formation']['english'],
                "category": chart_data['formation']['nature'],
                "meaning": chart_data['formation']['meaning'],
                "source_book": "#64"
            }
        }
    
    # Add BaZi data if user profile exists
    if profile and profile.get('day_master'):
        schema['bazi_data'] = {
            "chart_source": "User Profile",
            "day_master": {
                "stem": profile.get('day_master', ''),
                "element": profile.get('element', '').split()[0] if profile.get('element') else '',
                "polarity": profile.get('polarity', ''),
                "strength": profile.get('strength', '')
            },
            "useful_gods": {
                "primary": profile.get('useful_gods', [''])[0] if profile.get('useful_gods') else '',
                "secondary": profile.get('useful_gods', ['', ''])[1] if len(profile.get('useful_gods', [])) > 1 else ''
            },
            "unfavorable_elements": {
                "primary": profile.get('unfavorable', [''])[0] if profile.get('unfavorable') else ''
            },
            "ten_god_profile": {
                "profile_name": profile.get('profile', '')
            }
        }
        
        # Calculate BaZi alignment score
        bazi_score = calculate_bazi_alignment(chart_data, profile)
        schema['synthesis']['bazi_alignment_score'] = bazi_score
        
        # Calculate combined score
        qmdj_score = schema['synthesis']['qmdj_score']
        combined = round((qmdj_score + bazi_score) / 2, 1)
        schema['synthesis']['combined_verdict_score'] = combined
        schema['metadata']['analysis_type'] = "QMDJ_BAZI_INTEGRATED"
    
    return schema


def get_stem_element(stem_full):
    """Get element from stem"""
    stem_elements = {
        "甲": "Wood", "乙": "Wood",
        "丙": "Fire", "丁": "Fire",
        "戊": "Earth", "己": "Earth",
        "庚": "Metal", "辛": "Metal",
        "壬": "Water", "癸": "Water"
    }
    chinese = stem_full.split()[0]
    return stem_elements.get(chinese, "Unknown")


def get_stem_polarity(stem_full):
    """Get polarity from stem"""
    yang_stems = ["甲", "丙", "戊", "庚", "壬"]
    chinese = stem_full.split()[0]
    return "Yang" if chinese in yang_stems else "Yin"


def calculate_qmdj_score(chart_data):
    """Calculate QMDJ score (1-10)"""
    base_score = 5
    
    # Add/subtract based on component natures
    components = chart_data.get('components', {})
    
    for comp_name in ['star', 'door', 'deity']:
        comp = components.get(comp_name, {})
        nature = comp.get('nature', 'Neutral')
        
        if 'Very Auspicious' in nature:
            base_score += 2
        elif nature == 'Auspicious':
            base_score += 1
        elif nature == 'Inauspicious':
            base_score -= 1
        
        # Add strength modifier for star and door
        if comp_name in ['star', 'door']:
            strength = comp.get('strength', (None, 0))
            if strength and len(strength) > 1:
                base_score += strength[1] * 0.3
    
    # Formation modifier
    if chart_data.get('formation'):
        formation_nature = chart_data['formation'].get('nature', 'Neutral')
        if 'Very Auspicious' in formation_nature:
            base_score += 2
        elif formation_nature == 'Auspicious':
            base_score += 1
        elif formation_nature == 'Inauspicious':
            base_score -= 1.5
    
    # Clamp to 1-10
    return max(1, min(10, round(base_score, 1)))


def calculate_bazi_alignment(chart_data, profile):
    """Calculate BaZi alignment score (1-10)"""
    if not profile or not profile.get('useful_gods'):
        return None
    
    base_score = 5
    useful_gods = [g.split()[0] for g in profile.get('useful_gods', [])]  # Get just element name
    unfavorable = [g.split()[0] for g in profile.get('unfavorable', [])]
    
    # Check palace element
    palace_element = chart_data.get('palace', {}).get('element', '')
    if palace_element in useful_gods:
        base_score += 2
    elif palace_element in unfavorable:
        base_score -= 2
    
    # Check component elements
    components = chart_data.get('components', {})
    for comp_name in ['star', 'door']:
        comp = components.get(comp_name, {})
        comp_element = comp.get('element', '')
        if comp_element in useful_gods:
            base_score += 1
        elif comp_element in unfavorable:
            base_score -= 1
    
    return max(1, min(10, round(base_score, 1)))


def generate_db_row(chart_data, profile):
    """Generate CSV database row"""
    formation = chart_data.get('formation', {})
    formation_name = formation.get('english', 'None') if formation else 'None'
    
    qmdj_score = calculate_qmdj_score(chart_data)
    bazi_score = calculate_bazi_alignment(chart_data, profile) or 0
    
    verdict = chart_data.get('analysis', {}).get('overall_nature', 'Neutral').split()[0]
    action = chart_data.get('analysis', {}).get('recommendation', '')[:50]  # Truncate
    
    row = [
        chart_data['metadata']['date'],
        chart_data['metadata']['time'],
        chart_data['palace']['number'],
        formation_name,
        qmdj_score,
        bazi_score,
        verdict,
        action,
        "PENDING"
    ]
    
    return ",".join(str(x) for x in row)


def generate_csv_export(analyses):
    """Generate CSV file from analyses history"""
    if not analyses:
        return None
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Date", "Time", "Palace", "Formation", 
        "QMDJ_Score", "BaZi_Score", "Verdict", "Action", "Outcome"
    ])
    
    # Data rows
    for analysis in analyses:
        writer.writerow([
            analysis.get('date', ''),
            analysis.get('time', ''),
            analysis.get('palace', ''),
            analysis.get('formation', 'None'),
            analysis.get('qmdj_score', ''),
            analysis.get('bazi_score', ''),
            analysis.get('verdict', ''),
            analysis.get('action', '')[:50],
            analysis.get('outcome', 'PENDING')
        ])
    
    return output.getvalue()


# ============ PAGE CONTENT ============

st.title("📤 Export 导出")
st.markdown("Export your QMDJ analysis data in various formats for Project 1 integration")

# Check for current chart
current_chart = st.session_state.get('current_chart')

tab1, tab2, tab3 = st.tabs(["📄 Current Chart", "📊 Batch Export", "🔧 Format Options"])

# ============ TAB 1: CURRENT CHART EXPORT ============
with tab1:
    if current_chart:
        st.markdown("### 📊 Current Chart Data")
        
        # Show summary
        st.markdown(f"""
        **Date:** {current_chart['metadata']['date']}  
        **Time:** {current_chart['metadata']['time']}  
        **Palace:** #{current_chart['palace']['number']} {current_chart['palace']['name']}  
        **Verdict:** {current_chart['analysis']['overall_nature']}
        """)
        
        st.markdown("---")
        
        # Export Options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Universal Schema v2.0 (JSON)")
            st.caption("For Project 1 (Analyst Engine)")
            
            user_profile = st.session_state.get('user_profile')
            schema_data = format_universal_schema(current_chart, user_profile)
            
            if schema_data:
                json_str = json.dumps(schema_data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="📥 Download Universal Schema JSON",
                    data=json_str,
                    file_name=f"qmdj_universal_{current_chart['metadata']['date']}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                with st.expander("👁️ Preview JSON"):
                    st.code(json_str, language="json")
        
        with col2:
            st.markdown("#### 📋 Raw Chart Data (JSON)")
            st.caption("Original chart format")
            
            raw_json = json.dumps(current_chart, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Download Raw Chart JSON",
                data=raw_json,
                file_name=f"qmdj_raw_{current_chart['metadata']['date']}.json",
                mime="application/json",
                use_container_width=True
            )
            
            with st.expander("👁️ Preview Raw JSON"):
                st.code(raw_json, language="json")
        
        st.markdown("---")
        
        # Copy for Claude / Project 1
        st.markdown("### 📋 Copy Analysis Prompt")
        st.caption("One-click copy for Project 1 (Claude Analyst)")
        
        prompt_template = f"""Analyze this QMDJ chart using Joey Yap methodology:

```json
{json.dumps(schema_data, indent=2, ensure_ascii=False)}
```

Please provide:
1. Overall assessment of the chart
2. Key formations and their implications
3. Timing recommendations
4. Action advice based on the query purpose
"""
        
        st.text_area(
            "Copy this prompt:",
            value=prompt_template,
            height=300,
            help="Copy and paste this into Project 1 for AI analysis"
        )
        
    else:
        st.info("📊 No current chart to export. Generate a chart first in the **Chart Generator** page!")
        
        if st.button("➡️ Go to Chart Generator"):
            st.switch_page("pages/1_Chart.py")

# ============ TAB 2: BATCH EXPORT ============
with tab2:
    st.markdown("### 📊 Export All Analyses")
    
    analyses = st.session_state.get('analyses', [])
    
    if analyses:
        st.markdown(f"**Total Records:** {len(analyses)}")
        
        # Preview table
        st.markdown("#### Preview")
        st.dataframe(analyses, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            csv_data = generate_csv_export(analyses)
            
            st.download_button(
                label="📥 Download All as CSV",
                data=csv_data,
                file_name=f"qmdj_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON Export (all)
            json_all = json.dumps(analyses, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Download All as JSON",
                data=json_all,
                file_name=f"qmdj_history_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("📊 No analysis history yet. Generate some charts first!")

# ============ TAB 3: FORMAT OPTIONS ============
with tab3:
    st.markdown("### 🔧 Export Format Reference")
    
    st.markdown("""
    #### Universal Schema v2.0
    
    The Universal Schema is designed for compatibility with **Project 1 (Analyst Engine)**.
    
    **Key Sections:**
    - `metadata` - Date, time, method, analysis type
    - `qmdj_data` - Palace, components, formations
    - `bazi_data` - Day Master, useful gods (if profile set)
    - `synthesis` - Scores, verdict, recommendations
    - `tracking` - ML database row, outcome status
    
    **Score Ranges:**
    - QMDJ Score: 1-10 (based on components and formations)
    - BaZi Alignment: 1-10 (based on useful gods match)
    - Combined Score: 1-10 (average of both)
    
    **Verdict Categories:**
    - `HIGHLY_AUSPICIOUS` (8-10)
    - `AUSPICIOUS` (6-7.9)
    - `NEUTRAL` (4-5.9)
    - `INAUSPICIOUS` (2-3.9)
    - `HIGHLY_INAUSPICIOUS` (1-1.9)
    """)
    
    st.markdown("---")
    
    st.markdown("""
    #### CSV Database Format
    
    **Columns:**
    ```
    Date, Time, Palace, Formation, QMDJ_Score, BaZi_Score, Verdict, Action, Outcome
    ```
    
    **Example Row:**
    ```
    2025-01-15,14:30,5,Heaven Escape,8.5,7.0,AUSPICIOUS,Proceed with confidence,PENDING
    ```
    
    **Outcome Values:**
    - `PENDING` - Not yet verified
    - `SUCCESS` - Outcome matched prediction
    - `PARTIAL` - Partially matched
    - `FAILURE` - Did not match
    - `NOT_APPLICABLE` - Cannot be verified
    """)

# Footer
st.markdown("---")
st.caption("📤 Qi Men Pro Export | Phase 3 | Universal Schema v2.0 Compatible")
