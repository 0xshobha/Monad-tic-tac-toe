# 🧠 MindCheck AI

## Student Stress Awareness Tool

> ⚠️ **Important Disclaimer**: MindCheck AI is an **educational self-reflection tool** and is **NOT** a medical or mental health diagnostic system. It is designed for educational awareness only.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [AI Methodology](#-ai-methodology)
- [Installation](#-installation)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [Ethical Considerations](#-ethical-considerations)
- [Future Plans](#-future-plans)
- [Demo](#-demo)

---

## 🎯 Problem Statement

Students in grades 6-12 often experience:

- **Academic stress** from homework, tests, and assignments
- **Exam pressure** during test seasons
- **Burnout** from balancing school and activities

However, many students:

- ❌ Don't recognize early signs of stress
- ❌ Lack accessible, judgment-free tools for self-reflection
- ❌ Don't know when to seek help

---

## 💡 Solution

**MindCheck AI** is an AI-powered self-reflection tool that helps students:

1. 📝 **Write** short journal entries about their day or studies
2. 🧠 **Analyze** their text using AI to detect stress patterns
3. 📊 **Visualize** their stress levels and emotional state
4. 💡 **Receive** gentle, appropriate wellness suggestions
5. 📈 **Track** their wellbeing over time

**Key Principle**: This is a tool for **awareness and reflection**, not diagnosis or treatment.

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| 📝 Journal Input | Write about your day, feelings, or concerns |
| 🎯 Stress Level Detection | AI analyzes and shows Low/Medium/High stress |
| 💭 Emotion Breakdown | Visual breakdown of detected emotions |
| 💡 Wellness Tips | Personalized, stress-level-appropriate suggestions |
| ⚠️ Ethical Disclaimers | Clear messaging that this is educational only |

### Bonus Features

| Feature | Description |
|---------|-------------|
| 📈 Trend Tracking | View your stress patterns over last 5 entries |
| 📥 Report Download | Export your reflection history as a text report |
| 🔬 Analysis Details | See sentiment scores, keywords, and components |

---

## 🧠 AI Methodology

MindCheck AI uses a multi-step analysis approach:

### Step 1: Text Preprocessing

```python
# Clean and normalize input text
- Convert to lowercase
- Remove special characters
- Normalize whitespace
```

### Step 2: Sentiment Analysis

Using **TextBlob** NLP library:

- **Polarity**: -1 (negative) to +1 (positive)
- **Subjectivity**: 0 (objective) to 1 (subjective)

### Step 3: Emotion Detection

Keyword-based analysis for emotions:

| Emotion | Keywords (Examples) |
|---------|---------------------|
| 😰 Anxiety | anxious, worried, nervous, panic |
| 😢 Sadness | sad, lonely, hopeless, crying |
| 😤 Frustration | frustrated, angry, annoyed |
| 😫 Exhaustion | tired, drained, burnout |
| 😌 Calm | relaxed, peaceful, content |
| 😊 Happiness | happy, joyful, excited |

### Step 4: Stress Scoring Algorithm

```
stress_score = (
    0.35 × sentiment_stress +
    0.40 × keyword_stress +
    0.25 × emotional_intensity
)

Stress Level:
- 🟢 Low: score < 40%
- 🟡 Medium: 40% ≤ score < 65%
- 🔴 High: score ≥ 65%
```

This combines multiple signals for more accurate stress detection than any single metric alone.

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**

```bash
cd mindcheck-ai
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Download TextBlob corpora** (first time only)

```bash
python -m textblob.download_corpora
```

5. **Run the application**

```bash
streamlit run app.py
```

6. **Open in browser**

The app will open automatically at `http://localhost:8501`

---

## 📖 Usage

### Basic Usage

1. **Open the app** in your web browser
2. **Read the disclaimer** - understand this is for self-reflection only
3. **Write a journal entry** describing how you're feeling
4. **Click "Analyze My Entry"** 
5. **Review your results**:
   - Stress level (Low/Medium/High)
   - Emotion breakdown chart
   - Personalized wellness suggestions
6. **Track your progress** over multiple entries

### Sample Entries to Try

**Low Stress Example:**
> "Today was a great day! I finished my homework early and got to play video games with my friends. I feel pretty happy and relaxed."

**Medium Stress Example:**
> "I have exams coming up next week and I'm a bit nervous about them. I've been studying but there's still a lot to cover. Feeling a bit overwhelmed but manageable."

**High Stress Example:**
> "I'm so stressed out. I have three tests tomorrow and I haven't slept well in days. Everything feels like too much. I can't focus and I'm really anxious about failing."

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | Streamlit |
| **NLP Engine** | TextBlob |
| **Visualization** | Plotly |
| **Data Handling** | Pandas |
| **Language** | Python 3.8+ |

---

## ⚖️ Ethical Considerations

MindCheck AI is built with careful attention to ethics:

### ✅ What This Tool Does

- Provides educational awareness about stress
- Offers self-reflection opportunities
- Gives general wellness suggestions
- Encourages talking to trusted adults

### ❌ What This Tool Does NOT Do

- Diagnose mental health conditions
- Provide medical or psychological advice
- Replace professional mental health support
- Store personal data permanently
- Identify individuals or require personal info

### Safety Measures

1. **Clear Disclaimers**: Prominent messaging about educational-only purpose
2. **No Permanent Storage**: Entries are session-only, not saved to any database
3. **Professional Referrals**: High stress results include recommendations to talk to adults
4. **No Labels**: We avoid clinical terminology or diagnostic labels
5. **Positive Framing**: Suggestions focus on healthy habits, not treatment

---

## 🔮 Future Plans

- [ ] **Multi-language Support** - Analyze entries in multiple languages
- [ ] **Improved Emotion Models** - Fine-tuned transformer models for better accuracy
- [ ] **Mobile App Version** - Native iOS/Android apps
- [ ] **Privacy-Safe Sharing** - Option to share anonymized summaries with counselors
- [ ] **Voice Input** - Speak your journal entries
- [ ] **Mindfulness Exercises** - Built-in guided breathing and meditation

---

## 🎬 Demo

### Video Script (2 minutes)

**0:00-0:15** - Introduction
> "Hi, I'm [Name], a student in grade [X]. This project is called MindCheck AI."

**0:15-0:35** - Problem
> "Many students experience academic stress but don't recognize the early signs. They need accessible, judgment-free ways to reflect on their wellbeing."

**0:35-1:30** - Live Demo
> - Show the app interface
> - Paste a sample journal entry
> - Click analyze
> - Walk through stress level, emotions, and suggestions

**1:30-2:00** - Conclusion
> "This is NOT a medical tool - it's an educational self-reflection assistant. In the future, we plan to add better emotion detection and multi-language support."

---

## 📄 Devpost Write-Up

### Problem

Students often experience academic stress but lack accessible tools to reflect on their emotional wellbeing early. Early awareness can help prevent burnout and encourage seeking support when needed.

### Solution

MindCheck AI is an AI-powered self-reflection tool that analyzes student journal entries to detect stress levels and emotional tone, helping students become more aware of their wellbeing through a judgment-free interface.

### Tools Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **TextBlob** - NLP sentiment analysis
- **Plotly** - Interactive visualizations
- **Pandas** - Data processing

### What Makes It Special

- **Real AI Analysis**: Combines sentiment analysis, keyword detection, and emotional classification
- **Beautiful UI**: Modern, accessible interface designed for students
- **Ethical Design**: Clear disclaimers, no data storage, professional referrals for high stress
- **Actionable Insights**: Personalized wellness suggestions based on stress level

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- TextBlob for NLP capabilities
- Streamlit for the amazing web framework
- Plotly for beautiful visualizations

---

**Made with 💚 for student wellbeing**

*Remember: It's okay to not be okay. Reaching out for help is a sign of strength.*
