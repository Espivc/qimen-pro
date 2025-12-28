"""
📈 History & ML Tracking Page
Analysis history and pattern insights
"""

import streamlit as st
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import (
    get_all_records, get_recent_records, get_pending_records,
    update_outcome, get_statistics, export_to_csv_string, clear_database
)
from utils.language import get_lang

# Initialize session state for language
if 'lang_mode' not in st.session_state:
    st.session_state.lang_mode = "mixed"

# Initialize language helper
L = get_lang(st.session_state.lang_mode)

st.set_page_config(
    page_title="History - Qi Men Pro",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    [data-testid="stSidebar"] { background-color: #16213e; }
    h1, h2, h3 { color: #d4af37 !important; }
    .metric-card {
        background: #16213e;
        border: 1px solid #2a3f5f;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #d4af37;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #b8b8b8;
    }
</style>
""", unsafe_allow_html=True)

def render_stats_cards():
    """Render statistics overview cards"""
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_records']}</div>
            <div class="metric-label">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        rate_color = "#4CAF50" if stats['success_rate'] >= 60 else "#FFC107" if stats['success_rate'] >= 40 else "#F44336"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {rate_color};">{stats['success_rate']}%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #FFC107;">{stats['pending_count']}</div>
            <div class="metric-label">Pending</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        completed = stats['success_count'] + stats['partial_count'] + stats['failure_count']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #4CAF50;">{completed}</div>
            <div class="metric-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)

def render_history_table(records: list):
    """Render history table"""
    if not records:
        st.info("No records found.")
        return
    
    for record in records:
        score = float(record.get('combined_score', 5.0))
        if score >= 7:
            score_color = "#4CAF50"
            score_emoji = "🌟"
        elif score >= 4.5:
            score_color = "#FFC107"
            score_emoji = "⚡"
        else:
            score_color = "#F44336"
            score_emoji = "⚠️"
        
        outcome = record.get('outcome', 'PENDING')
        outcome_badge = {
            'PENDING': ('⏳', '#FFC107', L.outcome('PENDING')),
            'SUCCESS': ('✅', '#4CAF50', L.outcome('SUCCESS')),
            'PARTIAL': ('🔶', '#FFC107', L.outcome('PARTIAL')),
            'FAILURE': ('❌', '#F44336', L.outcome('FAILURE')),
            'NOT_APPLICABLE': ('➖', '#b8b8b8', L.outcome('NOT_APPLICABLE'))
        }.get(outcome, ('⏳', '#FFC107', L.outcome('PENDING')))
        
        formation = record.get('formation', '')
        formation_text = f" | {L.formation(formation)}" if formation else ""
        
        palace_display = L.palace(record.get('palace_name', ''))
        verdict_display = L.verdict(record.get('verdict', '')) if record.get('verdict') else 'N/A'
        
        st.markdown(f"""
        <div style="background-color: #16213e; border: 1px solid #2a3f5f; border-radius: 8px; 
                    padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #d4af37; font-weight: 500;">
                        {record.get('date', '')} {record.get('time', '')}
                    </span>
                    <span style="color: #ffffff; margin-left: 0.75rem;">
                        {palace_display}{formation_text}
                    </span>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="color: {score_color}; font-weight: 600;">
                        {score_emoji} {score}
                    </span>
                    <span style="background: {outcome_badge[1]}22; color: {outcome_badge[1]}; 
                                padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;">
                        {outcome_badge[0]} {outcome_badge[2]}
                    </span>
                </div>
            </div>
            <div style="margin-top: 0.5rem; display: flex; gap: 1rem; font-size: 0.8rem; color: #b8b8b8;">
                <span>Purpose: {record.get('purpose', 'General')}</span>
                <span>Verdict: {verdict_display}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_pattern_insights():
    """Render ML pattern insights"""
    stats = get_statistics()
    
    # Success rate by formation
    st.markdown("#### Success Rate by Formation")
    
    if not stats['by_formation']:
        st.info("Not enough data yet. Complete more analyses to see patterns.")
        return
    
    for formation, data in sorted(stats['by_formation'].items(), 
                                   key=lambda x: x[1]['success'] / x[1]['total'] if x[1]['total'] > 0 else 0,
                                   reverse=True):
        if formation == '':
            formation_display = 'No Formation 无格局'
        else:
            formation_display = L.formation(formation)
        
        total = data['total']
        success = data['success']
        rate = round((success / total * 100) if total > 0 else 0, 0)
        
        if rate >= 60:
            bar_color = "#4CAF50"
        elif rate >= 40:
            bar_color = "#FFC107"
        else:
            bar_color = "#F44336"
        
        st.markdown(f"""
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="color: #ffffff;">{formation_display}</span>
                <span style="color: {bar_color}; font-weight: 500;">{rate}% ({success}/{total})</span>
            </div>
            <div style="background: #2a3f5f; border-radius: 4px; height: 8px;">
                <div style="background: {bar_color}; width: {rate}%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Success rate by palace
    st.markdown("#### Best Performing Palaces")
    
    if stats['by_palace']:
        palace_rates = []
        for palace, data in stats['by_palace'].items():
            rate = (data['success'] / data['total'] * 100) if data['total'] > 0 else 0
            palace_rates.append((palace, rate, data['success'], data['total']))
        
        palace_rates.sort(key=lambda x: x[1], reverse=True)
        
        for i, (palace, rate, success, total) in enumerate(palace_rates[:3], 1):
            medal = ["🥇", "🥈", "🥉"][i-1]
            rate_color = "#4CAF50" if rate >= 60 else "#FFC107" if rate >= 40 else "#F44336"
            palace_display = L.palace(palace)
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;
                        background: #16213e; padding: 0.5rem 1rem; border-radius: 8px;">
                <span style="font-size: 1.2rem;">{medal}</span>
                <span style="color: #ffffff; flex: 1;">{palace_display}</span>
                <span style="color: {rate_color}; font-weight: 500;">{round(rate)}% success</span>
            </div>
            """, unsafe_allow_html=True)

def main():
    st.title("📈 Analysis History & ML Tracking")
    
    # Stats Overview
    render_stats_cards()
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All History", "⏳ Update Outcomes", "🔮 Pattern Insights"])
    
    with tab1:
        # Filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_option = st.selectbox(
                "Filter",
                ["All Records", "This Week", "This Month", "Pending Only", "Completed Only"],
                key="history_filter"
            )
        with col2:
            sort_order = st.selectbox(
                "Sort",
                ["Newest First", "Oldest First", "Highest Score", "Lowest Score"],
                key="history_sort"
            )
        
        # Get records based on filter
        all_records = get_all_records()
        
        if filter_option == "Pending Only":
            records = [r for r in all_records if r.get('outcome') == 'PENDING']
        elif filter_option == "Completed Only":
            records = [r for r in all_records if r.get('outcome') != 'PENDING']
        elif filter_option == "This Week":
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            records = [r for r in all_records if r.get('date', '') >= week_ago]
        elif filter_option == "This Month":
            month_start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            records = [r for r in all_records if r.get('date', '') >= month_start]
        else:
            records = all_records
        
        # Sort records
        if sort_order == "Newest First":
            records.sort(key=lambda x: f"{x.get('date', '')} {x.get('time', '')}", reverse=True)
        elif sort_order == "Oldest First":
            records.sort(key=lambda x: f"{x.get('date', '')} {x.get('time', '')}")
        elif sort_order == "Highest Score":
            records.sort(key=lambda x: float(x.get('combined_score', 0)), reverse=True)
        elif sort_order == "Lowest Score":
            records.sort(key=lambda x: float(x.get('combined_score', 0)))
        
        st.markdown(f"<div style='color: #b8b8b8; margin-bottom: 0.5rem;'>Showing {len(records)} records</div>", 
                    unsafe_allow_html=True)
        
        render_history_table(records)
        
        # Export options
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = export_to_csv_string()
            st.download_button(
                label="📥 Export Full Database",
                data=csv_data,
                file_name=f"qmdj_database_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                st.session_state.confirm_clear = True
        
        if st.session_state.get('confirm_clear', False):
            st.warning("⚠️ This will delete all analysis records. This action cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Clear Everything", type="primary"):
                    clear_database()
                    st.session_state.confirm_clear = False
                    st.success("Database cleared.")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_clear = False
                    st.rerun()
    
    with tab2:
        st.markdown("### ⏳ Update Outcome")
        st.markdown("<small style='color: #b8b8b8;'>Track your predictions to improve future accuracy</small>", 
                    unsafe_allow_html=True)
        
        pending_records = get_pending_records()
        
        if not pending_records:
            st.info("🎉 No pending outcomes to update!")
        else:
            # Select record to update
            record_options = {
                f"{r.get('date', '')} {r.get('time', '')} | {r.get('palace_name', '')} | Score: {r.get('combined_score', 0)}": r.get('id', '')
                for r in pending_records
            }
            
            selected_record_label = st.selectbox(
                "Select Record",
                options=list(record_options.keys()),
                key="update_record_select"
            )
            
            selected_id = record_options[selected_record_label]
            
            # Find the selected record
            selected_record = next((r for r in pending_records if r.get('id') == selected_id), None)
            
            if selected_record:
                st.markdown(f"""
                <div style="background: #16213e; border: 1px solid #2a3f5f; border-radius: 10px; 
                            padding: 1rem; margin: 1rem 0;">
                    <div style="color: #d4af37; font-weight: 600; margin-bottom: 0.5rem;">
                        {selected_record.get('palace_name', '')} Palace Analysis
                    </div>
                    <div style="color: #b8b8b8; font-size: 0.9rem;">
                        <div>Date: {selected_record.get('date', '')} {selected_record.get('time', '')}</div>
                        <div>Formation: {selected_record.get('formation', 'None')}</div>
                        <div>Purpose: {selected_record.get('purpose', 'General')}</div>
                        <div>Predicted Verdict: {selected_record.get('verdict', 'N/A')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    outcome = st.radio(
                        "Outcome",
                        ["SUCCESS", "PARTIAL", "FAILURE", "NOT_APPLICABLE"],
                        key="outcome_select",
                        horizontal=True
                    )
                
                with col2:
                    notes = st.text_area(
                        "Notes (optional)",
                        placeholder="What happened? Any insights?",
                        key="outcome_notes"
                    )
                
                if st.button("💾 Save Outcome", type="primary"):
                    if update_outcome(selected_id, outcome, notes):
                        st.success("✅ Outcome saved successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save outcome.")
    
    with tab3:
        st.markdown("### 🔮 Pattern Insights")
        st.markdown("<small style='color: #b8b8b8;'>ML-powered analysis of your prediction accuracy</small>", 
                    unsafe_allow_html=True)
        
        stats = get_statistics()
        
        if stats['total_records'] < 5:
            st.info(f"""
            📊 Need more data for pattern analysis.
            
            Current records: {stats['total_records']}/5 minimum
            
            Keep generating charts and tracking outcomes to unlock insights!
            """)
        else:
            render_pattern_insights()
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # Success by door
            st.markdown("#### Success Rate by Door")
            
            if stats['by_door']:
                for door, data in sorted(stats['by_door'].items(), 
                                         key=lambda x: x[1]['success'] / x[1]['total'] if x[1]['total'] > 0 else 0,
                                         reverse=True):
                    total = data['total']
                    success = data['success']
                    rate = round((success / total * 100) if total > 0 else 0, 0)
                    
                    if rate >= 60:
                        bar_color = "#4CAF50"
                    elif rate >= 40:
                        bar_color = "#FFC107"
                    else:
                        bar_color = "#F44336"
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span style="color: #ffffff;">{door} Door</span>
                            <span style="color: {bar_color}; font-weight: 500;">{rate}% ({success}/{total})</span>
                        </div>
                        <div style="background: #2a3f5f; border-radius: 4px; height: 6px;">
                            <div style="background: {bar_color}; width: {rate}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
