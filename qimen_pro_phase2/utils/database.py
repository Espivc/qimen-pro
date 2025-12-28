"""
Database Management Module
Handles CSV database for ML tracking and analysis history
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid

# Database paths
DATA_DIR = Path("data")
DB_FILE = DATA_DIR / "qmdj_bazi_patterns.csv"

# CSV columns
CSV_COLUMNS = [
    "id",
    "date",
    "time",
    "timezone",
    "palace_name",
    "palace_number",
    "palace_element",
    "heaven_stem",
    "earth_stem",
    "door",
    "star",
    "deity",
    "formation",
    "qmdj_score",
    "bazi_score",
    "combined_score",
    "verdict",
    "purpose",
    "primary_action",
    "outcome",
    "outcome_notes",
    "feedback_date"
]


def ensure_data_dir():
    """Ensure the data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def init_database():
    """Initialize the database file with headers if it doesn't exist"""
    ensure_data_dir()
    
    if not DB_FILE.exists():
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        return True
    return False


def add_analysis(
    chart_datetime: datetime,
    timezone: str,
    palace_data: Dict[str, Any],
    palace_name: str,
    formation: Optional[str],
    qmdj_score: float,
    bazi_score: float,
    verdict: str,
    purpose: str = "General Forecast",
    primary_action: str = ""
) -> str:
    """
    Add a new analysis record to the database
    Returns the record ID
    """
    init_database()
    
    record_id = str(uuid.uuid4())[:8]
    
    record = {
        "id": record_id,
        "date": chart_datetime.strftime("%Y-%m-%d"),
        "time": chart_datetime.strftime("%H:%M"),
        "timezone": timezone,
        "palace_name": palace_name,
        "palace_number": palace_data.get("palace_number", 0),
        "palace_element": palace_data.get("palace_element", ""),
        "heaven_stem": palace_data.get("heaven_stem", {}).get("chinese", ""),
        "earth_stem": palace_data.get("earth_stem", {}).get("chinese", ""),
        "door": palace_data.get("door", {}).get("name", ""),
        "star": palace_data.get("star", {}).get("name", ""),
        "deity": palace_data.get("deity", {}).get("name", ""),
        "formation": formation or "",
        "qmdj_score": qmdj_score,
        "bazi_score": bazi_score,
        "combined_score": round((qmdj_score + bazi_score) / 2, 1),
        "verdict": verdict,
        "purpose": purpose,
        "primary_action": primary_action,
        "outcome": "PENDING",
        "outcome_notes": "",
        "feedback_date": ""
    }
    
    with open(DB_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writerow(record)
    
    return record_id


def get_all_records() -> List[Dict[str, Any]]:
    """Get all records from the database"""
    init_database()
    
    records = []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                try:
                    row['qmdj_score'] = float(row.get('qmdj_score', 0))
                    row['bazi_score'] = float(row.get('bazi_score', 0))
                    row['combined_score'] = float(row.get('combined_score', 0))
                    row['palace_number'] = int(row.get('palace_number', 0))
                except (ValueError, TypeError):
                    pass
                records.append(row)
    except FileNotFoundError:
        pass
    
    return records


def get_recent_records(n: int = 10) -> List[Dict[str, Any]]:
    """Get the n most recent records"""
    records = get_all_records()
    # Sort by date and time (newest first)
    records.sort(key=lambda x: f"{x.get('date', '')} {x.get('time', '')}", reverse=True)
    return records[:n]


def get_pending_records() -> List[Dict[str, Any]]:
    """Get all records with pending outcomes"""
    records = get_all_records()
    return [r for r in records if r.get('outcome', '') == 'PENDING']


def update_outcome(record_id: str, outcome: str, notes: str = "") -> bool:
    """Update the outcome for a record"""
    records = get_all_records()
    updated = False
    
    for record in records:
        if record.get('id') == record_id:
            record['outcome'] = outcome
            record['outcome_notes'] = notes
            record['feedback_date'] = datetime.now().strftime("%Y-%m-%d")
            updated = True
            break
    
    if updated:
        # Rewrite the entire file
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(records)
    
    return updated


def get_statistics() -> Dict[str, Any]:
    """Get analysis statistics for ML insights"""
    records = get_all_records()
    
    stats = {
        "total_records": len(records),
        "pending_count": 0,
        "success_count": 0,
        "partial_count": 0,
        "failure_count": 0,
        "success_rate": 0.0,
        "by_formation": {},
        "by_palace": {},
        "by_door": {},
    }
    
    completed_records = []
    
    for record in records:
        outcome = record.get('outcome', 'PENDING')
        
        if outcome == 'PENDING':
            stats['pending_count'] += 1
        elif outcome == 'SUCCESS':
            stats['success_count'] += 1
            completed_records.append(record)
        elif outcome == 'PARTIAL':
            stats['partial_count'] += 1
            completed_records.append(record)
        elif outcome == 'FAILURE':
            stats['failure_count'] += 1
            completed_records.append(record)
    
    # Calculate success rate
    total_completed = len(completed_records)
    if total_completed > 0:
        stats['success_rate'] = round(
            (stats['success_count'] + stats['partial_count'] * 0.5) / total_completed * 100, 
            1
        )
    
    # Group by formation
    for record in completed_records:
        formation = record.get('formation', 'None')
        if formation not in stats['by_formation']:
            stats['by_formation'][formation] = {'total': 0, 'success': 0}
        stats['by_formation'][formation]['total'] += 1
        if record.get('outcome') == 'SUCCESS':
            stats['by_formation'][formation]['success'] += 1
    
    # Group by palace
    for record in completed_records:
        palace = record.get('palace_name', 'Unknown')
        if palace not in stats['by_palace']:
            stats['by_palace'][palace] = {'total': 0, 'success': 0}
        stats['by_palace'][palace]['total'] += 1
        if record.get('outcome') == 'SUCCESS':
            stats['by_palace'][palace]['success'] += 1
    
    # Group by door
    for record in completed_records:
        door = record.get('door', 'Unknown')
        if door not in stats['by_door']:
            stats['by_door'][door] = {'total': 0, 'success': 0}
        stats['by_door'][door]['total'] += 1
        if record.get('outcome') == 'SUCCESS':
            stats['by_door'][door]['success'] += 1
    
    return stats


def export_to_csv_string() -> str:
    """Export database to CSV string for download"""
    init_database()
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def clear_database() -> bool:
    """Clear all records from the database (keep headers)"""
    try:
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        return True
    except IOError:
        return False


def get_db_row_format(
    chart_datetime: datetime,
    palace_name: str,
    formation: str,
    qmdj_score: float,
    bazi_score: float,
    verdict: str,
    action: str
) -> str:
    """Generate DB_ROW format string for schema compliance"""
    return f"{chart_datetime.strftime('%Y-%m-%d')},{chart_datetime.strftime('%H:%M')},{palace_name},{formation},{qmdj_score},{bazi_score},{verdict},{action},PENDING"
