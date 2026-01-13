"""
Job matching engine using cosine similarity and skill-based scoring.
Provides explainable match scores with detailed breakdowns.
"""

from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.core.config import settings
from src.ml.text_processor import get_text_processor


class JobMatcher:
    """
    Calculates job match scores using multiple signals:
    1. Overall text similarity (TF-IDF + cosine similarity)
    2. Skill-level matching
    3. Weighted scoring with explainability
    """
    
    def __init__(self):
        self.text_processor = get_text_processor()
    
    def calculate_match_score(
        self,
        resume_text: str,
        job_description: str,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, any]:
        """
        Calculate comprehensive match score with explainability.
        
        Args:
            resume_text: Full resume text
            job_description: Full job description text
            resume_skills: Extracted resume skills
            job_skills: Extracted job description skills
            
        Returns:
            Dictionary with overall score and detailed breakdown
        """
        # Calculate text similarity score
        text_similarity = self._calculate_text_similarity(resume_text, job_description)
        
        # Calculate skill match score
        skill_match = self._calculate_skill_match(resume_skills, job_skills)
        
        # Weighted overall score (60% skills, 40% text similarity)
        overall_score = (skill_match['score'] * 0.6) + (text_similarity * 0.4)
        
        return {
            'overall_score': round(overall_score * 100, 2),  # Convert to percentage
            'text_similarity_score': round(text_similarity * 100, 2),
            'skill_match_score': round(skill_match['score'] * 100, 2),
            'matched_skills_count': skill_match['matched_count'],
            'total_required_skills': skill_match['total_required'],
            'skill_coverage': round(skill_match['coverage'] * 100, 2),
            'explanation': self._generate_explanation(
                overall_score, text_similarity, skill_match
            )
        }
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts using TF-IDF.
        
        Args:
            text1: First text (resume)
            text2: Second text (job description)
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Clean texts
            text1_clean = self.text_processor.clean_text(text1)
            text2_clean = self.text_processor.clean_text(text2)
            
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                max_features=settings.TFIDF_MAX_FEATURES,
                ngram_range=settings.TFIDF_NGRAM_RANGE,
                stop_words=settings.STOP_WORDS,
                lowercase=True
            )
            
            # Fit and transform both texts
            tfidf_matrix = vectorizer.fit_transform([text1_clean, text2_clean])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return max(0.0, min(1.0, float(similarity)))  # Clamp to [0, 1]
            
        except Exception as e:
            # If calculation fails, return 0
            return 0.0
    
    def _calculate_skill_match(
        self,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, any]:
        """
        Calculate skill-based matching score.
        
        Args:
            resume_skills: Skills from resume
            job_skills: Skills from job description
            
        Returns:
            Dictionary with match statistics
        """
        if not job_skills:
            return {
                'score': 0.0,
                'matched_count': 0,
                'total_required': 0,
                'coverage': 0.0
            }
        
        # Normalize skills for comparison
        resume_skills_normalized = set(
            self.text_processor.normalize_skill_term(s) for s in resume_skills
        )
        job_skills_normalized = set(
            self.text_processor.normalize_skill_term(s) for s in job_skills
        )
        
        # Find matches
        matched_skills = resume_skills_normalized.intersection(job_skills_normalized)
        matched_count = len(matched_skills)
        total_required = len(job_skills_normalized)
        
        # Calculate coverage (what % of required skills are matched)
        coverage = matched_count / total_required if total_required > 0 else 0.0
        
        # Score calculation (with diminishing returns for extra skills)
        # Perfect match = 1.0, partial match scales with coverage
        score = coverage
        
        return {
            'score': score,
            'matched_count': matched_count,
            'total_required': total_required,
            'coverage': coverage
        }
    
    def _generate_explanation(
        self,
        overall_score: float,
        text_similarity: float,
        skill_match: Dict[str, any]
    ) -> str:
        """
        Generate human-readable explanation of the match score.
        
        Args:
            overall_score: Overall match score (0-1)
            text_similarity: Text similarity score (0-1)
            skill_match: Skill match statistics
            
        Returns:
            Explanation string
        """
        score_pct = overall_score * 100
        
        # Determine match level
        if score_pct >= 80:
            level = "Excellent"
        elif score_pct >= 60:
            level = "Good"
        elif score_pct >= 40:
            level = "Moderate"
        else:
            level = "Low"
        
        explanation = f"{level} match ({score_pct:.1f}%). "
        
        # Add skill coverage context
        coverage_pct = skill_match['coverage'] * 100
        explanation += f"You have {skill_match['matched_count']} out of "
        explanation += f"{skill_match['total_required']} required skills ({coverage_pct:.1f}% coverage). "
        
        # Add text similarity context
        text_sim_pct = text_similarity * 100
        explanation += f"Overall content alignment is {text_sim_pct:.1f}%."
        
        return explanation
    
    def get_match_level(self, score: float) -> str:
        """
        Get categorical match level from score.
        
        Args:
            score: Match score (0-100)
            
        Returns:
            Match level string
        """
        if score >= 80:
            return "Excellent Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Moderate Match"
        elif score >= 20:
            return "Low Match"
        else:
            return "Poor Match"


# Global matcher instance
_matcher_instance = None


def get_job_matcher() -> JobMatcher:
    """Get the global job matcher instance (singleton pattern)."""
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = JobMatcher()
    return _matcher_instance
