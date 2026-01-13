"""
Skill gap analyzer for career intelligence.
Identifies matched, missing, and extra skills with actionable insights.
"""

from typing import List, Dict, Set
from src.core.skill_taxonomy import get_taxonomy
from src.ml.text_processor import get_text_processor


class GapAnalyzer:
    """
    Analyzes skill gaps between resume and job requirements.
    Provides categorized insights and recommendations.
    """
    
    def __init__(self):
        self.taxonomy = get_taxonomy()
        self.text_processor = get_text_processor()
    
    def analyze_gap(
        self,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, any]:
        """
        Perform comprehensive skill gap analysis.
        
        Args:
            resume_skills: Skills extracted from resume
            job_skills: Skills extracted from job description
            
        Returns:
            Dictionary with matched, missing, and extra skills
        """
        # Normalize skills for comparison
        resume_set = self._normalize_skill_set(resume_skills)
        job_set = self._normalize_skill_set(job_skills)
        
        # Calculate skill categories
        matched_skills = resume_set.intersection(job_set)
        missing_skills = job_set - resume_set
        extra_skills = resume_set - job_set
        
        # Categorize skills
        matched_categorized = self._categorize_skills(list(matched_skills))
        missing_categorized = self._categorize_skills(list(missing_skills))
        extra_categorized = self._categorize_skills(list(extra_skills))
        
        # Generate insights
        insights = self._generate_insights(
            matched_skills, missing_skills, extra_skills, job_set
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            missing_categorized, matched_categorized
        )
        
        return {
            'matched_skills': {
                'skills': sorted(list(matched_skills)),
                'count': len(matched_skills),
                'by_category': matched_categorized
            },
            'missing_skills': {
                'skills': sorted(list(missing_skills)),
                'count': len(missing_skills),
                'by_category': missing_categorized
            },
            'extra_skills': {
                'skills': sorted(list(extra_skills)),
                'count': len(extra_skills),
                'by_category': extra_categorized
            },
            'insights': insights,
            'recommendations': recommendations,
            'summary': self._generate_summary(
                len(matched_skills), len(missing_skills), len(job_set)
            )
        }
    
    def _normalize_skill_set(self, skills: List[str]) -> Set[str]:
        """Normalize a list of skills to a set."""
        normalized = set()
        for skill in skills:
            norm_skill = self.text_processor.normalize_skill_term(skill)
            if norm_skill:
                normalized.add(norm_skill)
        return normalized
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize skills by type.
        
        Args:
            skills: List of skills
            
        Returns:
            Dictionary mapping categories to skills
        """
        categorized = {}
        
        for skill in skills:
            category = self.taxonomy.get_category(skill)
            
            if category not in categorized:
                categorized[category] = []
            
            categorized[category].append(skill)
        
        # Sort skills within each category
        for category in categorized:
            categorized[category].sort()
        
        return categorized
    
    def _generate_insights(
        self,
        matched: Set[str],
        missing: Set[str],
        extra: Set[str],
        required: Set[str]
    ) -> List[str]:
        """
        Generate actionable insights from gap analysis.
        
        Args:
            matched: Matched skills
            missing: Missing skills
            extra: Extra skills
            required: All required skills
            
        Returns:
            List of insight strings
        """
        insights = []
        
        # Match rate insight
        if required:
            match_rate = (len(matched) / len(required)) * 100
            insights.append(
                f"You match {match_rate:.1f}% of the required skills for this position."
            )
        
        # Missing skills insight
        if missing:
            if len(missing) <= 3:
                insights.append(
                    f"You're missing {len(missing)} key skill(s): {', '.join(sorted(list(missing))[:3])}."
                )
            else:
                insights.append(
                    f"You're missing {len(missing)} skills. Focus on the most critical ones first."
                )
        else:
            insights.append("Excellent! You have all the required skills for this position.")
        
        # Extra skills insight
        if extra:
            insights.append(
                f"You have {len(extra)} additional skill(s) that could differentiate you from other candidates."
            )
        
        # Strength assessment
        if matched:
            matched_categories = self._categorize_skills(list(matched))
            top_category = max(matched_categories.items(), key=lambda x: len(x[1]))[0]
            insights.append(
                f"Your strongest alignment is in {top_category.replace('_', ' ')} skills."
            )
        
        return insights
    
    def _generate_recommendations(
        self,
        missing_categorized: Dict[str, List[str]],
        matched_categorized: Dict[str, List[str]]
    ) -> List[Dict[str, any]]:
        """
        Generate prioritized recommendations for skill development.
        
        Args:
            missing_categorized: Missing skills by category
            matched_categorized: Matched skills by category
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Prioritize missing skills by category
        priority_categories = [
            'programming_languages',
            'ml_ai',
            'web_frontend',
            'web_backend',
            'databases',
            'cloud_devops'
        ]
        
        for category in priority_categories:
            if category in missing_categorized:
                skills = missing_categorized[category]
                
                # Determine priority level
                if category in matched_categorized:
                    # You have some skills in this category
                    priority = "Medium"
                    reason = f"Build on your existing {category.replace('_', ' ')} knowledge"
                else:
                    # New category for you
                    priority = "High"
                    reason = f"Essential {category.replace('_', ' ')} skills for this role"
                
                recommendations.append({
                    'category': category.replace('_', ' ').title(),
                    'skills': skills[:5],  # Top 5 skills
                    'priority': priority,
                    'reason': reason
                })
        
        # Add recommendations for other categories
        for category, skills in missing_categorized.items():
            if category not in priority_categories:
                recommendations.append({
                    'category': category.replace('_', ' ').title(),
                    'skills': skills[:3],
                    'priority': "Low",
                    'reason': f"Nice-to-have {category.replace('_', ' ')} skills"
                })
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _generate_summary(
        self,
        matched_count: int,
        missing_count: int,
        total_required: int
    ) -> str:
        """
        Generate a summary statement.
        
        Args:
            matched_count: Number of matched skills
            missing_count: Number of missing skills
            total_required: Total required skills
            
        Returns:
            Summary string
        """
        if total_required == 0:
            return "No specific skills were identified in the job description."
        
        match_pct = (matched_count / total_required) * 100
        
        if match_pct >= 80:
            return f"Strong candidate! You have {matched_count}/{total_required} required skills."
        elif match_pct >= 60:
            return f"Good fit with room to grow. You have {matched_count}/{total_required} required skills."
        elif match_pct >= 40:
            return f"Moderate fit. Focus on acquiring {missing_count} missing skills to strengthen your profile."
        else:
            return f"Significant skill gap. Consider upskilling in {missing_count} areas before applying."


# Global analyzer instance
_analyzer_instance = None


def get_gap_analyzer() -> GapAnalyzer:
    """Get the global gap analyzer instance (singleton pattern)."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = GapAnalyzer()
    return _analyzer_instance
