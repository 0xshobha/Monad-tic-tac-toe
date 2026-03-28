"""
MindCheck AI - Utility Functions

Helper functions for:
- History/trend management
- Report generation
- Data formatting
"""

import pandas as pd
from datetime import datetime
from config import STRESS_COLORS, STRESS_EMOJIS
import json


def format_timestamp(dt: datetime = None) -> str:
    """Format a datetime object or current time as readable string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%B %d, %Y at %I:%M %p")


def get_stress_color(stress_level: str) -> str:
    """Get the color associated with a stress level."""
    return STRESS_COLORS.get(stress_level, STRESS_COLORS["medium"])


def get_stress_emoji(stress_level: str) -> str:
    """Get the emoji associated with a stress level."""
    return STRESS_EMOJIS.get(stress_level, STRESS_EMOJIS["medium"])


def create_history_entry(analysis_result: dict) -> dict:
    """
    Create a history entry from analysis results.
    
    Args:
        analysis_result: Complete analysis result from analyzer
        
    Returns:
        Simplified history entry for storage
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "formatted_time": format_timestamp(),
        "stress_level": analysis_result["stress"]["stress_level"],
        "stress_score": analysis_result["stress"]["stress_score"],
        "stress_percentage": analysis_result["stress"]["stress_percentage"],
        "primary_emotion": analysis_result["emotions"]["primary_emotion"],
        "primary_emoji": analysis_result["emotions"]["primary_emoji"],
        "word_count": analysis_result["word_count"],
        "text_preview": analysis_result["original_text"][:100] + "..." 
                       if len(analysis_result["original_text"]) > 100 
                       else analysis_result["original_text"]
    }


def get_trend_data(history: list) -> pd.DataFrame:
    """
    Convert history entries to a pandas DataFrame for trend visualization.
    
    Args:
        history: List of history entries
        
    Returns:
        DataFrame with trend data
    """
    if not history:
        return pd.DataFrame()
    
    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["entry_number"] = range(1, len(df) + 1)
    
    return df


def calculate_trend_summary(history: list) -> dict:
    """
    Calculate summary statistics from history.
    
    Args:
        history: List of history entries
        
    Returns:
        Summary statistics dictionary
    """
    if not history:
        return {
            "total_entries": 0,
            "average_stress": 0,
            "trend_direction": "neutral",
            "most_common_emotion": None
        }
    
    df = get_trend_data(history)
    
    # Calculate average stress
    avg_stress = df["stress_score"].mean()
    
    # Determine trend direction
    if len(df) >= 2:
        recent_avg = df.tail(2)["stress_score"].mean()
        older_avg = df.head(max(1, len(df) - 2))["stress_score"].mean()
        
        if recent_avg < older_avg - 0.1:
            trend_direction = "improving"
        elif recent_avg > older_avg + 0.1:
            trend_direction = "declining"
        else:
            trend_direction = "stable"
    else:
        trend_direction = "not_enough_data"
    
    # Most common emotion
    most_common_emotion = df["primary_emotion"].mode().iloc[0] if len(df) > 0 else None
    
    return {
        "total_entries": len(history),
        "average_stress": round(avg_stress * 100, 1),
        "trend_direction": trend_direction,
        "most_common_emotion": most_common_emotion
    }


def generate_report_content(history: list, include_entries: bool = True) -> str:
    """
    Generate a text report from history data.
    
    Args:
        history: List of history entries
        include_entries: Whether to include individual entry details
        
    Returns:
        Formatted report string
    """
    report_lines = [
        "=" * 60,
        "MINDCHECK AI - REFLECTION REPORT",
        "=" * 60,
        f"Generated: {format_timestamp()}",
        "",
        "DISCLAIMER: This report is for educational self-reflection only.",
        "It is NOT a medical or psychological assessment.",
        "",
        "-" * 60,
        "SUMMARY",
        "-" * 60,
    ]
    
    summary = calculate_trend_summary(history)
    
    report_lines.extend([
        f"Total Entries Analyzed: {summary['total_entries']}",
        f"Average Stress Level: {summary['average_stress']}%",
        f"Overall Trend: {summary['trend_direction'].replace('_', ' ').title()}",
        f"Most Common Emotion: {summary['most_common_emotion'] or 'N/A'}",
        "",
    ])
    
    if include_entries and history:
        report_lines.extend([
            "-" * 60,
            "ENTRY HISTORY",
            "-" * 60,
            "",
        ])
        
        for i, entry in enumerate(history, 1):
            stress_emoji = get_stress_emoji(entry["stress_level"])
            report_lines.extend([
                f"Entry #{i} - {entry['formatted_time']}",
                f"  Stress Level: {stress_emoji} {entry['stress_level'].upper()} ({entry['stress_percentage']}%)",
                f"  Primary Emotion: {entry['primary_emoji']} {entry['primary_emotion'].title()}",
                f"  Preview: \"{entry['text_preview']}\"",
                "",
            ])
    
    report_lines.extend([
        "-" * 60,
        "RECOMMENDATIONS",
        "-" * 60,
    ])
    
    # Add recommendations based on trend
    if summary["trend_direction"] == "improving":
        report_lines.append("✅ Your stress levels appear to be improving! Keep up the great work.")
    elif summary["trend_direction"] == "declining":
        report_lines.append("⚠️ Your stress levels may be increasing. Consider talking to a trusted adult.")
    else:
        report_lines.append("📊 Continue tracking your entries to identify patterns.")
    
    report_lines.extend([
        "",
        "Remember: If you're feeling overwhelmed, please reach out to:",
        "- A parent or guardian",
        "- A school counselor",
        "- A trusted teacher",
        "",
        "=" * 60,
        "END OF REPORT",
        "=" * 60,
    ])
    
    return "\n".join(report_lines)


def get_emotion_chart_data(emotions: dict) -> dict:
    """
    Prepare emotion data for chart visualization.
    
    Args:
        emotions: Emotion analysis result from analyzer
        
    Returns:
        Dictionary formatted for Plotly charts
    """
    emotion_data = emotions["emotions"]
    
    labels = []
    values = []
    colors = []
    emojis = []
    
    for emotion, data in emotion_data.items():
        if data["score"] > 0:
            labels.append(emotion.title())
            values.append(round(data["score"] * 100, 1))
            colors.append(data["color"])
            emojis.append(data["emoji"])
    
    return {
        "labels": labels,
        "values": values,
        "colors": colors,
        "emojis": emojis
    }


def get_stress_gauge_data(stress_score: float) -> dict:
    """
    Prepare stress score data for gauge visualization.
    
    Args:
        stress_score: Stress score from 0 to 1
        
    Returns:
        Dictionary with gauge configuration
    """
    percentage = round(stress_score * 100, 1)
    
    if percentage < 40:
        color = STRESS_COLORS["low"]
        level = "Low"
    elif percentage < 65:
        color = STRESS_COLORS["medium"]
        level = "Medium"
    else:
        color = STRESS_COLORS["high"]
        level = "High"
    
    return {
        "value": percentage,
        "color": color,
        "level": level,
        "ranges": [
            {"min": 0, "max": 40, "color": STRESS_COLORS["low"], "label": "Low"},
            {"min": 40, "max": 65, "color": STRESS_COLORS["medium"], "label": "Medium"},
            {"min": 65, "max": 100, "color": STRESS_COLORS["high"], "label": "High"}
        ]
    }
