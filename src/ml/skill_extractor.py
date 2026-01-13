"""
Skill extraction engine using NLP and ML techniques.
Combines TF-IDF, taxonomy matching, and pattern recognition.
"""

from typing import List, Dict, Set, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from src.core.config import settings
from src.core.skill_taxonomy import get_taxonomy
from src.ml.text_processor import get_text_processor


class SkillExtractor:
    """
    Extracts skills from text using multiple strategies:
    1. Taxonomy-based matching (exact and fuzzy)
    2. TF-IDF importance scoring
    3. N-gram pattern matching
    """
    
    def __init__(self):
        self.taxonomy = get_taxonomy()
        self.text_processor = get_text_processor()
        self.tfidf_vectorizer = None
        
    def extract_skills(self, text: str, context: str = "resume") -> List[Dict[str, any]]:
        """
        Extract skills from text with confidence scores.
        
        Args:
            text: Input text (resume or job description)
            context: Context type ("resume" or "job_description")
            
        Returns:
            List of dictionaries with skill, confidence, and category
        """
        if not text or not text.strip():
            return []
        
        # Clean text
        cleaned_text = self.text_processor.clean_text(text)
        
        # Extract skills using multiple methods
        taxonomy_skills = self._extract_taxonomy_skills(cleaned_text)
        tfidf_skills = self._extract_tfidf_skills(cleaned_text)
        
        # Merge and score skills
        all_skills = self._merge_skills(taxonomy_skills, tfidf_skills)
        
        # Sort by confidence
        all_skills.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Limit to top skills
        return all_skills[:settings.MAX_SKILLS_EXTRACT]
    
    def _extract_taxonomy_skills(self, text: str) -> Dict[str, float]:
        """
        Extract skills by matching against taxonomy.
        Returns dict of skill -> confidence score.
        """
        skills_found = {}
        
        # Get all possible n-grams from text
        ngrams = self.text_processor.extract_ngrams(text, n=3)
        
        # Check each n-gram against taxonomy
        for ngram in ngrams:
            normalized = self.text_processor.normalize_skill_term(ngram)
            
            # Check if it's a known skill
            if self.taxonomy.is_valid_skill(normalized):
                canonical = self.taxonomy.normalize_skill(normalized)
                
                # Higher confidence for exact matches
                if canonical not in skills_found:
                    skills_found[canonical] = 0.0
                
                # Increase confidence (multiple mentions = higher confidence)
                skills_found[canonical] += 0.3
        
        # Cap confidence at 1.0
        for skill in skills_found:
            skills_found[skill] = min(skills_found[skill], 1.0)
        
        return skills_found
    
    def _extract_tfidf_skills(self, text: str) -> Dict[str, float]:
        """
        Extract important terms using TF-IDF.
        Returns dict of term -> importance score.
        """
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=settings.TFIDF_MAX_FEATURES,
            ngram_range=settings.TFIDF_NGRAM_RANGE,
            stop_words=settings.STOP_WORDS,
            lowercase=True,
            min_df=1
        )
        
        try:
            # Fit on the text (treating it as a single document)
            # For single document, we need at least 2 docs, so duplicate
            tfidf_matrix = vectorizer.fit_transform([text, text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores for first document
            scores = tfidf_matrix[0].toarray()[0]
            
            # Create skill -> score mapping
            tfidf_skills = {}
            for idx, score in enumerate(scores):
                if score >= settings.MIN_SKILL_CONFIDENCE:
                    term = feature_names[idx]
                    normalized = self.text_processor.normalize_skill_term(term)
                    
                    # Only keep if it looks like a skill (not common words)
                    if self._is_likely_skill(normalized):
                        tfidf_skills[normalized] = float(score)
            
            return tfidf_skills
            
        except Exception as e:
            # If TF-IDF fails, return empty dict
            return {}
    
    def _is_likely_skill(self, term: str) -> bool:
        """
        Heuristic to determine if a term is likely a skill.
        Filters out common words and noise.
        """
        # Check against taxonomy first
        if self.taxonomy.is_valid_skill(term):
            return True
        
        # Length checks
        if len(term) < 2 or len(term) > 30:
            return False
        
        # Must contain at least one letter
        if not any(c.isalpha() for c in term):
            return False
        
        # Common non-skill words to filter
        noise_words = {
            'experience', 'work', 'team', 'project', 'company', 'role',
            'position', 'job', 'year', 'month', 'day', 'time', 'good',
            'great', 'excellent', 'strong', 'ability', 'skill', 'knowledge'
        }
        
        if term in noise_words:
            return False
        
        return True
    
    def _merge_skills(
        self, 
        taxonomy_skills: Dict[str, float], 
        tfidf_skills: Dict[str, float]
    ) -> List[Dict[str, any]]:
        """
        Merge skills from different extraction methods.
        Combines confidence scores and adds metadata.
        """
        merged = {}
        
        # Add taxonomy skills (higher weight)
        for skill, confidence in taxonomy_skills.items():
            merged[skill] = {
                'skill': skill,
                'confidence': confidence * 0.7,  # Weight taxonomy matches
                'source': 'taxonomy'
            }
        
        # Add TF-IDF skills
        for skill, score in tfidf_skills.items():
            if skill in merged:
                # Boost confidence if found by both methods
                merged[skill]['confidence'] = min(
                    merged[skill]['confidence'] + score * 0.3,
                    1.0
                )
                merged[skill]['source'] = 'both'
            else:
                merged[skill] = {
                    'skill': skill,
                    'confidence': score * 0.5,  # Lower weight for TF-IDF only
                    'source': 'tfidf'
                }
        
        # Add category information
        result = []
        for skill_data in merged.values():
            skill_data['category'] = self.taxonomy.get_category(skill_data['skill'])
            result.append(skill_data)
        
        return result
    
    def extract_skill_list(self, text: str) -> List[str]:
        """
        Simple method to extract just skill names.
        
        Args:
            text: Input text
            
        Returns:
            List of skill names
        """
        skills = self.extract_skills(text)
        return [s['skill'] for s in skills]


# Global extractor instance
_extractor_instance = None


def get_skill_extractor() -> SkillExtractor:
    """Get the global skill extractor instance (singleton pattern)."""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = SkillExtractor()
    return _extractor_instance
