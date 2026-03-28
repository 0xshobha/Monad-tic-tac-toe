"""
MindCheck AI - Core Analyzer Module

This module contains the AI logic for analyzing journal entries:
- Text preprocessing
- Sentiment analysis using TextBlob
- Emotion detection
- Stress level calculation
- Wellness suggestions generation
"""

import re
from textblob import TextBlob
from config import (
    HIGH_STRESS_KEYWORDS,
    MEDIUM_STRESS_KEYWORDS,
    CALM_KEYWORDS,
    EMOTION_CATEGORIES,
    WELLNESS_SUGGESTIONS,
    HIGH_STRESS_RESOURCES,
    SCORING_WEIGHTS,
    STRESS_THRESHOLDS
)
import random


class StressAnalyzer:
    """
    Main analyzer class for processing journal entries and 
    determining stress levels with emotional analysis.
    """
    
    def __init__(self):
        """Initialize the analyzer with keyword sets."""
        self.high_stress_keywords = set(word.lower() for word in HIGH_STRESS_KEYWORDS)
        self.medium_stress_keywords = set(word.lower() for word in MEDIUM_STRESS_KEYWORDS)
        self.calm_keywords = set(word.lower() for word in CALM_KEYWORDS)
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and normalize input text.
        
        Steps:
        1. Convert to lowercase
        2. Remove special characters (keep letters, numbers, spaces)
        3. Normalize whitespace
        4. Strip leading/trailing whitespace
        
        Args:
            text: Raw input text from user
            
        Returns:
            Cleaned and normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep apostrophes for contractions
        text = re.sub(r"[^a-zA-Z0-9\s']", " ", text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip whitespace
        text = text.strip()
        
        return text
    
    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment using TextBlob.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary with polarity and subjectivity scores
        """
        blob = TextBlob(text)
        
        return {
            "polarity": blob.sentiment.polarity,      # -1 (negative) to 1 (positive)
            "subjectivity": blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        }
    
    def detect_emotions(self, text: str) -> dict:
        """
        Detect emotions based on keyword matching.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary with emotion scores and primary emotion
        """
        words = set(text.split())
        emotion_scores = {}
        
        for emotion, data in EMOTION_CATEGORIES.items():
            keywords = set(word.lower() for word in data["keywords"])
            matches = words.intersection(keywords)
            score = len(matches) / max(len(keywords), 1)
            emotion_scores[emotion] = {
                "score": min(score * 3, 1.0),  # Scale up but cap at 1.0
                "matches": list(matches),
                "emoji": data["emoji"],
                "color": data["color"]
            }
        
        # Find primary emotion
        primary_emotion = max(emotion_scores.keys(), 
                            key=lambda x: emotion_scores[x]["score"])
        
        return {
            "emotions": emotion_scores,
            "primary_emotion": primary_emotion,
            "primary_emoji": emotion_scores[primary_emotion]["emoji"]
        }
    
    def calculate_keyword_stress(self, text: str) -> dict:
        """
        Calculate stress score based on keyword analysis.
        
        Args:
            text: Preprocessed text
            
        Returns:
            Dictionary with keyword stress analysis
        """
        words = set(text.split())
        
        high_matches = words.intersection(self.high_stress_keywords)
        medium_matches = words.intersection(self.medium_stress_keywords)
        calm_matches = words.intersection(self.calm_keywords)
        
        # Calculate weighted keyword score
        high_count = len(high_matches)
        medium_count = len(medium_matches)
        calm_count = len(calm_matches)
        
        total_stress_words = high_count + medium_count
        total_calm_words = calm_count
        
        # Keyword stress score (0 to 1)
        if total_stress_words + total_calm_words == 0:
            keyword_score = 0.5  # Neutral if no keywords found
        else:
            stress_weight = (high_count * 1.0 + medium_count * 0.5)
            calm_weight = calm_count * 0.7
            keyword_score = stress_weight / (stress_weight + calm_weight + 1)
        
        return {
            "keyword_score": min(keyword_score, 1.0),
            "high_stress_words": list(high_matches),
            "medium_stress_words": list(medium_matches),
            "calm_words": list(calm_matches)
        }
    
    def calculate_stress_level(self, sentiment: dict, emotions: dict, 
                              keywords: dict) -> dict:
        """
        Calculate overall stress level combining all factors.
        
        Formula:
        stress_score = (
            sentiment_weight * normalized_negative_sentiment +
            keyword_weight * keyword_stress_score +
            emotional_intensity_weight * emotional_intensity
        )
        
        Args:
            sentiment: Sentiment analysis results
            emotions: Emotion detection results
            keywords: Keyword analysis results
            
        Returns:
            Dictionary with stress level and score
        """
        weights = SCORING_WEIGHTS
        
        # Normalize sentiment (convert polarity to stress scale)
        # Polarity: -1 (negative/stressed) to 1 (positive/calm)
        # We want: 0 (calm) to 1 (stressed)
        sentiment_stress = (1 - sentiment["polarity"]) / 2
        
        # Get keyword stress score
        keyword_stress = keywords["keyword_score"]
        
        # Calculate emotional intensity from negative emotions
        negative_emotions = ["anxiety", "sadness", "frustration", "exhaustion"]
        emotional_intensity = sum(
            emotions["emotions"].get(e, {}).get("score", 0) 
            for e in negative_emotions
        ) / len(negative_emotions)
        
        # Combine scores
        stress_score = (
            weights["sentiment_weight"] * sentiment_stress +
            weights["keyword_weight"] * keyword_stress +
            weights["emotional_intensity_weight"] * emotional_intensity
        )
        
        # Clamp to 0-1 range
        stress_score = max(0, min(1, stress_score))
        
        # Determine stress level
        if stress_score < STRESS_THRESHOLDS["low_max"]:
            stress_level = "low"
        elif stress_score < STRESS_THRESHOLDS["medium_max"]:
            stress_level = "medium"
        else:
            stress_level = "high"
        
        return {
            "stress_score": stress_score,
            "stress_level": stress_level,
            "stress_percentage": round(stress_score * 100, 1),
            "components": {
                "sentiment_contribution": sentiment_stress,
                "keyword_contribution": keyword_stress,
                "emotional_contribution": emotional_intensity
            }
        }
    
    def get_wellness_suggestions(self, stress_level: str, 
                                 num_suggestions: int = 3) -> list:
        """
        Get appropriate wellness suggestions based on stress level.
        
        Args:
            stress_level: 'low', 'medium', or 'high'
            num_suggestions: Number of suggestions to return
            
        Returns:
            List of wellness suggestion strings
        """
        suggestions = WELLNESS_SUGGESTIONS.get(stress_level, WELLNESS_SUGGESTIONS["medium"])
        
        # Randomly select suggestions
        selected = random.sample(suggestions, min(num_suggestions, len(suggestions)))
        
        return selected
    
    def get_additional_resources(self, stress_level: str) -> list:
        """
        Get additional resources for high stress levels.
        
        Args:
            stress_level: Current stress level
            
        Returns:
            List of resource strings (empty if not high stress)
        """
        if stress_level == "high":
            return HIGH_STRESS_RESOURCES
        return []
    
    def analyze(self, text: str) -> dict:
        """
        Perform complete analysis on journal entry.
        
        This is the main entry point that combines all analysis steps.
        
        Args:
            text: Raw journal entry text
            
        Returns:
            Complete analysis results dictionary
        """
        # Step 1: Preprocess text
        cleaned_text = self.preprocess_text(text)
        
        # Step 2: Sentiment analysis
        sentiment = self.analyze_sentiment(cleaned_text)
        
        # Step 3: Emotion detection
        emotions = self.detect_emotions(cleaned_text)
        
        # Step 4: Keyword analysis
        keywords = self.calculate_keyword_stress(cleaned_text)
        
        # Step 5: Calculate stress level
        stress = self.calculate_stress_level(sentiment, emotions, keywords)
        
        # Step 6: Get wellness suggestions
        suggestions = self.get_wellness_suggestions(stress["stress_level"])
        
        # Step 7: Get additional resources if needed
        resources = self.get_additional_resources(stress["stress_level"])
        
        return {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "sentiment": sentiment,
            "emotions": emotions,
            "keywords": keywords,
            "stress": stress,
            "suggestions": suggestions,
            "resources": resources,
            "word_count": len(cleaned_text.split())
        }


# Create a singleton instance for easy import
analyzer = StressAnalyzer()


def analyze_journal_entry(text: str) -> dict:
    """
    Convenience function to analyze a journal entry.
    
    Args:
        text: Raw journal entry text
        
    Returns:
        Complete analysis results
    """
    return analyzer.analyze(text)
