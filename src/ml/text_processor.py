"""
Text preprocessing and cleaning utilities.
Handles normalization, tokenization, and cleaning for NLP tasks.
"""

import re
from typing import List, Set
from src.core.config import settings


class TextProcessor:
    """
    Handles text preprocessing for resume and job description analysis.
    Implements cleaning, normalization, and tokenization.
    """
    
    def __init__(self):
        self.min_word_length = settings.MIN_WORD_LENGTH
        self.max_word_length = settings.MAX_WORD_LENGTH
        
        # Common resume/job description noise patterns
        self.noise_patterns = [
            r'\b\d+\s*(years?|months?|yrs?)\b',  # Keep experience mentions
            r'http[s]?://\S+',  # URLs
            r'\S+@\S+',  # Emails
            r'\d{10,}',  # Long numbers (phone, etc.)
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text while preserving important information.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs and emails (keep other content)
        for pattern in self.noise_patterns[1:]:  # Skip experience pattern
            text = re.sub(pattern, '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric, spaces, and common separators
        text = re.sub(r'[^a-z0-9\s\.\+\#\-]', ' ', text)
        
        # Clean up multiple spaces again
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_ngrams(self, text: str, n: int = 3) -> List[str]:
        """
        Extract n-grams from text for skill matching.
        
        Args:
            text: Input text
            n: Maximum n-gram size
            
        Returns:
            List of n-grams
        """
        words = text.split()
        ngrams = []
        
        for i in range(1, n + 1):
            for j in range(len(words) - i + 1):
                ngram = ' '.join(words[j:j + i])
                if self._is_valid_ngram(ngram):
                    ngrams.append(ngram)
        
        return ngrams
    
    def _is_valid_ngram(self, ngram: str) -> bool:
        """Check if an n-gram is valid (not too short/long, not all numbers)."""
        if not ngram or len(ngram) < self.min_word_length:
            return False
        if len(ngram) > self.max_word_length:
            return False
        if ngram.isdigit():
            return False
        return True
    
    def tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization for skill extraction.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Clean first
        text = self.clean_text(text)
        
        # Split on whitespace
        tokens = text.split()
        
        # Filter valid tokens
        tokens = [t for t in tokens if self._is_valid_ngram(t)]
        
        return tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text.
        Useful for context-aware skill extraction.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?\n]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def normalize_skill_term(self, term: str) -> str:
        """
        Normalize a skill term for matching.
        
        Args:
            term: Skill term
            
        Returns:
            Normalized term
        """
        # Convert to lowercase
        term = term.lower().strip()
        
        # Remove extra whitespace
        term = re.sub(r'\s+', ' ', term)
        
        # Remove trailing version numbers (e.g., "python 3" -> "python")
        term = re.sub(r'\s+\d+(\.\d+)*$', '', term)
        
        # Remove common prefixes/suffixes
        term = re.sub(r'^(expert|proficient|advanced|intermediate|beginner)\s+', '', term)
        term = re.sub(r'\s+(expert|proficient|advanced|intermediate|beginner)$', '', term)
        
        return term


# Global processor instance
_processor_instance = None


def get_text_processor() -> TextProcessor:
    """Get the global text processor instance (singleton pattern)."""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = TextProcessor()
    return _processor_instance
