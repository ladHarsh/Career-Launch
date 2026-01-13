"""
Skill Taxonomy and Knowledge Base.
Curated database of technical skills, tools, and technologies.
"""

from typing import Dict, List, Set
import json


class SkillTaxonomy:
    """
    Manages the skill knowledge base with hierarchical categorization.
    Provides methods for skill lookup, normalization, and expansion.
    """
    
    def __init__(self):
        self.skills_by_category: Dict[str, Set[str]] = {}
        self.skill_to_category: Dict[str, str] = {}
        self.synonyms: Dict[str, str] = {}  # Maps variations to canonical form
        self._load_taxonomy()
    
    def _load_taxonomy(self):
        """Load and initialize the skill taxonomy."""
        from src.core.config import SKILL_CATEGORIES, SKILL_SYNONYMS
        
        # Load categories
        for category, skills in SKILL_CATEGORIES.items():
            self.skills_by_category[category] = set(s.lower() for s in skills)
            for skill in skills:
                self.skill_to_category[skill.lower()] = category
        
        # Load synonyms
        for canonical, variations in SKILL_SYNONYMS.items():
            for variant in variations:
                self.synonyms[variant.lower()] = canonical.lower()
    
    def normalize_skill(self, skill: str) -> str:
        """
        Normalize a skill to its canonical form.
        
        Args:
            skill: Raw skill string
            
        Returns:
            Normalized canonical skill name
        """
        skill_lower = skill.lower().strip()
        
        # Check if it's a known synonym
        if skill_lower in self.synonyms:
            return self.synonyms[skill_lower]
        
        # Return as-is if already in taxonomy
        if skill_lower in self.skill_to_category:
            return skill_lower
        
        # Return cleaned version
        return skill_lower
    
    def is_valid_skill(self, skill: str) -> bool:
        """Check if a skill exists in the taxonomy."""
        normalized = self.normalize_skill(skill)
        return normalized in self.skill_to_category or normalized in self.synonyms.values()
    
    def get_category(self, skill: str) -> str:
        """Get the category for a skill."""
        normalized = self.normalize_skill(skill)
        return self.skill_to_category.get(normalized, "other")
    
    def get_all_skills(self) -> List[str]:
        """Get all skills in the taxonomy."""
        return list(self.skill_to_category.keys())
    
    def get_skills_by_category(self, category: str) -> List[str]:
        """Get all skills in a specific category."""
        return list(self.skills_by_category.get(category, set()))
    
    def expand_query(self, skill: str) -> List[str]:
        """
        Expand a skill to include all its variations.
        Useful for matching against resumes.
        
        Args:
            skill: Skill to expand
            
        Returns:
            List of skill variations including synonyms
        """
        normalized = self.normalize_skill(skill)
        variations = [normalized]
        
        # Add all synonyms that map to this skill
        for variant, canonical in self.synonyms.items():
            if canonical == normalized:
                variations.append(variant)
        
        return list(set(variations))
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Organize a list of skills by category.
        
        Args:
            skills: List of skill strings
            
        Returns:
            Dictionary mapping categories to skills
        """
        categorized = {}
        for skill in skills:
            category = self.get_category(skill)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill)
        
        return categorized


# Global taxonomy instance
_taxonomy_instance = None


def get_taxonomy() -> SkillTaxonomy:
    """Get the global skill taxonomy instance (singleton pattern)."""
    global _taxonomy_instance
    if _taxonomy_instance is None:
        _taxonomy_instance = SkillTaxonomy()
    return _taxonomy_instance
