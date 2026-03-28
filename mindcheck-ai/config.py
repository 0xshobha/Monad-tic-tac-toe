"""
MindCheck AI - Configuration Constants

This module contains all configuration constants including:
- Stress-related keywords
- Emotion categories
- Wellness suggestions
- UI styling constants
"""

# ============================================
# STRESS KEYWORDS DATABASE
# ============================================

# Keywords indicating high stress/anxiety
HIGH_STRESS_KEYWORDS = [
    "overwhelmed", "exhausted", "can't cope", "panic", "anxious", "anxiety",
    "terrified", "hopeless", "helpless", "breakdown", "crying", "can't sleep",
    "insomnia", "nightmare", "too much", "failing", "failed", "disaster",
    "impossible", "unbearable", "suffocating", "drowning", "crushed",
    "desperate", "worthless", "terrible", "horrible", "destroyed",
    "breaking down", "falling apart", "can't breathe", "paralyzed",
    "burned out", "burnout", "drained", "depleted"
]

# Keywords indicating moderate stress
MEDIUM_STRESS_KEYWORDS = [
    "worried", "stressed", "nervous", "uncertain", "confused", "frustrated",
    "struggling", "difficult", "challenging", "hard", "tough", "pressure",
    "deadline", "behind", "catching up", "concerned", "uneasy", "tense",
    "restless", "irritated", "annoyed", "impatient", "distracted",
    "scattered", "forgetful", "tired", "busy", "hectic", "rushed"
]

# Keywords indicating low stress/positive state
CALM_KEYWORDS = [
    "happy", "calm", "relaxed", "peaceful", "content", "satisfied",
    "excited", "joyful", "grateful", "thankful", "proud", "accomplished",
    "confident", "optimistic", "hopeful", "balanced", "refreshed",
    "energized", "motivated", "inspired", "cheerful", "wonderful",
    "great", "amazing", "fantastic", "excellent", "good", "fine",
    "okay", "manageable", "comfortable", "easy", "fun", "enjoying"
]

# ============================================
# EMOTION CATEGORIES
# ============================================

EMOTION_CATEGORIES = {
    "anxiety": {
        "keywords": ["anxious", "worried", "nervous", "panic", "fear", "scared", "terrified", "uneasy"],
        "emoji": "😰",
        "color": "#FF6B6B"
    },
    "sadness": {
        "keywords": ["sad", "depressed", "unhappy", "crying", "tears", "lonely", "hopeless", "miserable"],
        "emoji": "😢",
        "color": "#4ECDC4"
    },
    "frustration": {
        "keywords": ["frustrated", "angry", "annoyed", "irritated", "mad", "furious", "upset"],
        "emoji": "😤",
        "color": "#FFE66D"
    },
    "exhaustion": {
        "keywords": ["tired", "exhausted", "drained", "burnout", "fatigue", "sleepy", "worn out"],
        "emoji": "😫",
        "color": "#A8E6CF"
    },
    "calm": {
        "keywords": ["calm", "relaxed", "peaceful", "content", "serene", "tranquil", "at ease"],
        "emoji": "😌",
        "color": "#88D8B0"
    },
    "happiness": {
        "keywords": ["happy", "joyful", "excited", "thrilled", "delighted", "cheerful", "glad"],
        "emoji": "😊",
        "color": "#FFEAA7"
    },
    "confidence": {
        "keywords": ["confident", "proud", "accomplished", "capable", "strong", "determined"],
        "emoji": "💪",
        "color": "#DDA0DD"
    }
}

# ============================================
# WELLNESS SUGGESTIONS DATABASE
# ============================================

WELLNESS_SUGGESTIONS = {
    "low": [
        "🌟 Keep up the great work! Your positive mindset is wonderful.",
        "📝 Consider journaling about what's going well - it helps maintain positivity.",
        "🎯 You're doing great! Set a small goal to challenge yourself.",
        "🤝 Share your positive energy with a friend or classmate.",
        "🎨 This is a great time to explore a new hobby or interest.",
        "📚 Your calm state is perfect for learning something new!",
        "💪 Keep building on these good habits - they're working for you."
    ],
    "medium": [
        "🧘 Try taking 5 deep breaths - inhale for 4 counts, hold for 4, exhale for 4.",
        "🚶 A short 10-minute walk can help clear your mind.",
        "📋 Break down your tasks into smaller, manageable steps.",
        "⏰ Try the Pomodoro technique: 25 minutes work, 5 minutes break.",
        "💬 Talk to someone you trust about how you're feeling.",
        "🎵 Listen to your favorite calming music for a few minutes.",
        "✍️ Write down 3 things you're grateful for today.",
        "🌿 Step outside and get some fresh air for a few minutes.",
        "💤 Make sure you're getting enough sleep tonight.",
        "🥤 Stay hydrated - drink a glass of water right now!"
    ],
    "high": [
        "🛑 PAUSE. Take 10 slow, deep breaths right now. You've got this.",
        "💬 Please talk to a trusted adult (parent, teacher, counselor) about how you're feeling.",
        "🚶 Step away from your work for at least 15 minutes.",
        "📞 Reach out to a friend or family member - you don't have to handle this alone.",
        "📝 Write down everything you're worried about, then circle what you can control.",
        "🎯 Focus on just ONE small task you can complete right now.",
        "🌙 If it's late, stop working and get some rest. Tomorrow is a new day.",
        "🧊 Try the 5-4-3-2-1 technique: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste.",
        "💪 Remember: Your worth is NOT defined by grades or achievements.",
        "❤️ Be kind to yourself - everyone struggles sometimes, and that's okay."
    ]
}

# High stress specific resources (displayed as additional help)
HIGH_STRESS_RESOURCES = [
    "📚 **School Counselor**: Your school counselor is trained to help with academic stress.",
    "👨‍👩‍👧 **Talk to Family**: A parent or guardian can help you manage your workload.",
    "👥 **Peer Support**: Sometimes friends going through similar experiences can help.",
]

# ============================================
# UI STYLING CONSTANTS
# ============================================

# Color scheme
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#48bb78",
    "warning": "#ecc94b",
    "danger": "#f56565",
    "info": "#4299e1",
    "background": "#1a1a2e",
    "card": "#16213e",
    "text": "#ffffff",
    "text_secondary": "#a0aec0"
}

# Stress level colors
STRESS_COLORS = {
    "low": "#48bb78",      # Green
    "medium": "#ecc94b",   # Yellow
    "high": "#f56565"      # Red
}

# Stress level emojis
STRESS_EMOJIS = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🔴"
}

# ============================================
# SCORING WEIGHTS
# ============================================

SCORING_WEIGHTS = {
    "sentiment_weight": 0.35,
    "keyword_weight": 0.40,
    "emotional_intensity_weight": 0.25
}

# Stress level thresholds
STRESS_THRESHOLDS = {
    "low_max": 0.40,
    "medium_max": 0.65
}

# ============================================
# APP CONFIGURATION
# ============================================

APP_CONFIG = {
    "title": "MindCheck AI",
    "subtitle": "Student Stress Awareness Tool",
    "version": "1.0.0",
    "max_history_entries": 5,
    "min_text_length": 10
}

# Disclaimer text
DISCLAIMER_TEXT = """
⚠️ **Important Disclaimer**

MindCheck AI is an **educational self-reflection tool** and is **NOT** a medical 
or mental health diagnostic system. This tool:

- Does NOT provide medical advice or diagnosis
- Does NOT replace professional mental health support
- Does NOT store your data permanently
- Is designed for educational awareness only

If you're experiencing serious distress, please talk to a trusted adult, 
school counselor, or mental health professional.
"""

FOOTER_TEXT = """
---
**MindCheck AI** - Helping students reflect on their wellbeing 💚

*Remember: It's okay to not be okay. Reaching out for help is a sign of strength.*
"""
