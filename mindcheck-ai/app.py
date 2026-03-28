"""
MindCheck AI - Student Stress Awareness Tool

Main Streamlit Application

⚠️ IMPORTANT DISCLAIMER:
This is an educational self-reflection tool and is NOT a medical 
or mental health diagnostic system.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import custom modules
from analyzer import analyze_journal_entry
from utils import (
    create_history_entry,
    get_trend_data,
    calculate_trend_summary,
    generate_report_content,
    get_emotion_chart_data,
    get_stress_gauge_data,
    format_timestamp
)
from config import (
    APP_CONFIG,
    DISCLAIMER_TEXT,
    FOOTER_TEXT,
    COLORS,
    STRESS_COLORS,
    STRESS_EMOJIS
)

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title=f"{APP_CONFIG['title']} - {APP_CONFIG['subtitle']}",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Disclaimer banner */
    .disclaimer-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        border-left: 5px solid #c0392b;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    /* Stress level indicators */
    .stress-low {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    
    .stress-medium {
        background: linear-gradient(135deg, #ecc94b 0%, #d69e2e 100%);
        color: #1a1a2e;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(236, 201, 75, 0.4);
    }
    
    .stress-high {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.4);
    }
    
    /* Suggestion cards */
    .suggestion-card {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: background 0.3s ease;
    }
    
    .suggestion-card:hover {
        background: rgba(255,255,255,0.1);
    }
    
    /* Resource card for high stress */
    .resource-card {
        background: rgba(245, 101, 101, 0.1);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #f56565;
    }
    
    /* Emotion tag */
    .emotion-tag {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* History entry */
    .history-entry {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
    }
    
    /* Animation keyframes */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "show_disclaimer" not in st.session_state:
    st.session_state.show_disclaimer = True

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_stress_gauge(stress_data):
    """Create a stress level gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_data["value"],
        domain={"x": [0, 1], "y": [0, 1]},
        number={"suffix": "%", "font": {"size": 40, "color": "white"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
            "bar": {"color": stress_data["color"], "thickness": 0.8},
            "bgcolor": "rgba(255,255,255,0.1)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(72, 187, 120, 0.3)"},
                {"range": [40, 65], "color": "rgba(236, 201, 75, 0.3)"},
                {"range": [65, 100], "color": "rgba(245, 101, 101, 0.3)"}
            ],
            "threshold": {
                "line": {"color": "white", "width": 4},
                "thickness": 0.8,
                "value": stress_data["value"]
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=250,
        margin={"l": 20, "r": 20, "t": 30, "b": 20}
    )
    
    return fig


def create_emotion_chart(emotion_data):
    """Create an emotion breakdown bar chart."""
    if not emotion_data["labels"]:
        return None
    
    fig = go.Figure(go.Bar(
        x=emotion_data["values"],
        y=[f"{e} {l}" for e, l in zip(emotion_data["emojis"], emotion_data["labels"])],
        orientation="h",
        marker={"color": emotion_data["colors"], "cornerradius": 10},
        text=[f"{v}%" for v in emotion_data["values"]],
        textposition="outside",
        textfont={"color": "white"}
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=250,
        margin={"l": 10, "r": 50, "t": 20, "b": 20},
        xaxis={"showgrid": False, "showticklabels": False, "range": [0, max(emotion_data["values"]) * 1.3]},
        yaxis={"showgrid": False},
        showlegend=False
    )
    
    return fig


def create_trend_chart(history):
    """Create a stress trend line chart."""
    if len(history) < 2:
        return None
    
    df = get_trend_data(history)
    
    fig = go.Figure()
    
    # Add area under the line
    fig.add_trace(go.Scatter(
        x=df["entry_number"],
        y=df["stress_percentage"],
        fill="tozeroy",
        fillcolor="rgba(102, 126, 234, 0.2)",
        line={"color": "#667eea", "width": 3},
        mode="lines+markers",
        marker={"size": 10, "color": "#667eea"},
        name="Stress Level"
    ))
    
    # Add threshold lines
    fig.add_hline(y=40, line_dash="dash", line_color="rgba(72, 187, 120, 0.5)", 
                  annotation_text="Low/Medium", annotation_position="right")
    fig.add_hline(y=65, line_dash="dash", line_color="rgba(245, 101, 101, 0.5)", 
                  annotation_text="Medium/High", annotation_position="right")
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=250,
        margin={"l": 40, "r": 40, "t": 20, "b": 40},
        xaxis={"title": "Entry #", "showgrid": True, "gridcolor": "rgba(255,255,255,0.1)"},
        yaxis={"title": "Stress %", "showgrid": True, "gridcolor": "rgba(255,255,255,0.1)", "range": [0, 100]},
        showlegend=False
    )
    
    return fig


# ============================================
# MAIN APPLICATION
# ============================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 MindCheck AI</h1>
    <p>Student Stress Awareness Tool</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer Banner (Always visible)
st.markdown(f"""
<div class="disclaimer-banner">
    ⚠️ <strong>Important:</strong> MindCheck AI is an <strong>educational self-reflection tool</strong> 
    and is <strong>NOT</strong> a medical or mental health diagnostic system. 
    If you're experiencing serious distress, please talk to a trusted adult.
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### 📊 Your History")
    
    if st.session_state.history:
        summary = calculate_trend_summary(st.session_state.history)
        
        st.markdown(f"""
        **{summary['total_entries']}** entries analyzed  
        **{summary['average_stress']}%** average stress  
        **{summary['trend_direction'].replace('_', ' ').title()}** trend
        """)
        
        st.divider()
        
        # Show recent entries
        st.markdown("#### Recent Entries")
        for entry in reversed(st.session_state.history[-3:]):
            emoji = STRESS_EMOJIS.get(entry["stress_level"], "🟡")
            st.markdown(f"""
            <div class="history-entry">
                {emoji} <strong>{entry["stress_level"].title()}</strong> ({entry["stress_percentage"]}%)<br>
                <small>{entry["formatted_time"]}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Download report button
        if st.button("📥 Download Report", use_container_width=True):
            report = generate_report_content(st.session_state.history)
            st.download_button(
                label="💾 Save Report",
                data=report,
                file_name=f"mindcheck_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_analysis = None
            st.rerun()
    else:
        st.info("No entries yet. Start by writing a journal entry!")
    
    st.divider()
    
    # About section
    with st.expander("ℹ️ About MindCheck AI"):
        st.markdown("""
        **MindCheck AI** helps students reflect on their emotional wellbeing 
        by analyzing journal entries.
        
        **How it works:**
        1. Write about your day or feelings
        2. Click "Analyze My Entry"
        3. Review your stress level & emotions
        4. Get personalized wellness tips
        
        **Privacy:**
        - No data is stored permanently
        - All analysis happens locally
        - Your entries are private
        """)

# ============================================
# MAIN CONTENT
# ============================================

# Input Section
st.markdown("### 📝 How are you feeling today?")
st.markdown("Write a short journal entry about your day, studies, or anything on your mind.")

journal_text = st.text_area(
    label="Journal Entry",
    placeholder="Example: Today was pretty stressful. I have three exams next week and I'm feeling overwhelmed with all the studying I need to do. I didn't sleep well last night because I was worrying about my math test...",
    height=150,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze My Entry", use_container_width=True, type="primary")

# Analysis Section
if analyze_button:
    if len(journal_text.strip()) < APP_CONFIG["min_text_length"]:
        st.warning("⚠️ Please write at least a few sentences for accurate analysis.")
    else:
        with st.spinner("🧠 Analyzing your entry..."):
            # Perform analysis
            result = analyze_journal_entry(journal_text)
            st.session_state.last_analysis = result
            
            # Add to history
            history_entry = create_history_entry(result)
            st.session_state.history.append(history_entry)
            
            # Keep only last N entries
            if len(st.session_state.history) > APP_CONFIG["max_history_entries"]:
                st.session_state.history = st.session_state.history[-APP_CONFIG["max_history_entries"]:]

# Display Results
if st.session_state.last_analysis:
    result = st.session_state.last_analysis
    stress_level = result["stress"]["stress_level"]
    stress_emoji = STRESS_EMOJIS.get(stress_level, "🟡")
    
    st.markdown("---")
    st.markdown("### 📊 Analysis Results")
    
    # Main Results Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Stress Level")
        
        # Stress Level Badge
        stress_class = f"stress-{stress_level}"
        st.markdown(f"""
        <div class="{stress_class}">
            {stress_emoji} {stress_level.upper()} STRESS
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Stress Gauge
        stress_data = get_stress_gauge_data(result["stress"]["stress_score"])
        fig = create_stress_gauge(stress_data)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with col2:
        st.markdown("#### 💭 Emotion Breakdown")
        
        # Primary Emotion
        primary = result["emotions"]["primary_emotion"]
        primary_emoji = result["emotions"]["primary_emoji"]
        st.markdown(f"**Primary Emotion:** {primary_emoji} {primary.title()}")
        
        # Emotion Chart
        emotion_data = get_emotion_chart_data(result["emotions"])
        if emotion_data["labels"]:
            fig = create_emotion_chart(emotion_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No strong emotions detected in your entry.")
    
    # Analysis Details
    with st.expander("🔬 Analysis Details"):
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        
        with detail_col1:
            st.markdown("**Sentiment Analysis**")
            polarity = result["sentiment"]["polarity"]
            sentiment_label = "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"
            st.metric("Sentiment", sentiment_label, f"{polarity:.2f}")
        
        with detail_col2:
            st.markdown("**Keywords Detected**")
            high_words = result["keywords"]["high_stress_words"]
            medium_words = result["keywords"]["medium_stress_words"]
            calm_words = result["keywords"]["calm_words"]
            
            if high_words:
                st.markdown(f"🔴 High: {', '.join(high_words[:3])}")
            if medium_words:
                st.markdown(f"🟡 Medium: {', '.join(medium_words[:3])}")
            if calm_words:
                st.markdown(f"🟢 Calm: {', '.join(calm_words[:3])}")
        
        with detail_col3:
            st.markdown("**Score Components**")
            components = result["stress"]["components"]
            st.markdown(f"Sentiment: {components['sentiment_contribution']:.1%}")
            st.markdown(f"Keywords: {components['keyword_contribution']:.1%}")
            st.markdown(f"Emotional: {components['emotional_contribution']:.1%}")
    
    # Wellness Suggestions
    st.markdown("---")
    st.markdown("### 💡 Wellness Suggestions")
    
    for suggestion in result["suggestions"]:
        st.markdown(f"""
        <div class="suggestion-card">
            {suggestion}
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Resources for High Stress
    if result["resources"]:
        st.markdown("### 🆘 Support Resources")
        st.warning("Your stress level appears elevated. Please consider reaching out:")
        
        for resource in result["resources"]:
            st.markdown(f"""
            <div class="resource-card">
                {resource}
            </div>
            """, unsafe_allow_html=True)
    
    # Trend Chart (if enough history)
    if len(st.session_state.history) >= 2:
        st.markdown("---")
        st.markdown("### 📈 Your Stress Trend")
        
        trend_fig = create_trend_chart(st.session_state.history)
        if trend_fig:
            st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})
            
            summary = calculate_trend_summary(st.session_state.history)
            if summary["trend_direction"] == "improving":
                st.success("✨ Great news! Your stress levels appear to be improving.")
            elif summary["trend_direction"] == "declining":
                st.warning("📉 Your stress levels seem to be increasing. Consider talking to someone.")
            else:
                st.info("📊 Your stress levels are relatively stable.")

# Footer
st.markdown(FOOTER_TEXT, unsafe_allow_html=True)

# Full Disclaimer (Collapsible)
with st.expander("📜 Full Disclaimer"):
    st.markdown(DISCLAIMER_TEXT)
