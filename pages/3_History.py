"""
Qi Men Pro - History & ML Tracking Page
Phase 3: Enhanced with ML feedback loop
"""

import streamlit as st
from datetime import datetime
import json
import pandas as pd

st.set_page_config(
    page_title="History & ML | Qi Men Pro",
    page_icon="📜",
    layout="wide"
)

try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

def get_outcome_emoji(outcome):
    return {"SUCCESS": "✅", "PARTIAL": "🔶", "FAILURE": "❌", 
            "PENDING": "⏳", "NOT_APPLICABLE": "➖"}.get(outcome, "❓")

def calculate_stats(analyses):
    if not analyses:
        return None
    total = len(analyses)
    outcomes = [a.get('outcome', 'PENDING') for a in analyses]
    return {
        "total": total,
        "success": outcomes.count('SUCCESS'),
        "partial": outcomes.count('PARTIAL'),
        "failure": outcomes.count('FAILURE'),
        "pending": outcomes.count('PENDING'),
        "success_rate": (outcomes.count('SUCCESS') / total * 100) if total > 0 else 0
    }

st.title("📜 History & ML Tracking")

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

analyses = st.session_state.analyses

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 History", "🔄 Feedback"])

with tab1:
    st.markdown("### 📊 Analytics Dashboard")
    if analyses:
        stats = calculate_stats(analyses)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", stats['total'])
        c2.metric("Success Rate", f"{stats['success_rate']:.1f}%")
        c3.metric("Pending", stats['pending'])
        c4.metric("Success", stats['success'])
    else:
        st.info("No analyses yet. Generate charts first!")

with tab2:
    st.markdown("### 📋 Analysis History")
    if analyses:
        for i, a in enumerate(reversed(analyses)):
            emoji = get_outcome_emoji(a.get('outcome', 'PENDING'))
            with st.expander(f"{emoji} {a.get('date', 'N/A')} {a.get('time', '')} - Palace #{a.get('palace', 'N/A')}"):
                st.json(a)
    else:
        st.info("No history yet")

with tab3:
    st.markdown("### 🔄 ML Feedback Loop")
    st.markdown("Update outcomes to improve pattern recognition")
    
    if analyses:
        pending = [a for a in analyses if a.get('outcome', 'PENDING') == 'PENDING']
        
        if pending:
            st.markdown(f"**{len(pending)} analyses pending feedback**")
            
            for i, a in enumerate(pending[:5]):
                st.markdown(f"---")
                st.markdown(f"**{a.get('date')} {a.get('time')}** - Palace #{a.get('palace')}")
                st.markdown(f"Verdict: {a.get('verdict', 'N/A')}")
                
                outcome = st.selectbox(
                    "Outcome:",
                    ["PENDING", "SUCCESS", "PARTIAL", "FAILURE", "NOT_APPLICABLE"],
                    key=f"outcome_{i}"
                )
                
                notes = st.text_input("Notes:", key=f"notes_{i}")
                
                if st.button("💾 Save", key=f"save_{i}"):
                    idx = analyses.index(a)
                    st.session_state.analyses[idx]['outcome'] = outcome
                    st.session_state.analyses[idx]['outcome_notes'] = notes
                    st.session_state.analyses[idx]['feedback_date'] = datetime.now().isoformat()
                    st.success("✅ Saved!")
                    st.rerun()
        else:
            st.success("✅ All analyses have been reviewed!")
    else:
        st.info("No analyses to review")

st.markdown("---")
st.caption("📜 Qi Men Pro History | Phase 3 | ML Tracking")
