"""
Core configuration for the Career AI platform.
Centralized settings for ML models, parsing, and application behavior.
"""

from typing import Dict, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "Career Launch"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # ML Configuration
    MIN_SKILL_CONFIDENCE: float = 0.3  # Minimum TF-IDF score to consider a skill
    TFIDF_MAX_FEATURES: int = 500
    TFIDF_NGRAM_RANGE: tuple = (1, 3)  # Unigrams to trigrams
    MIN_MATCH_SCORE: float = 0.0  # Minimum cosine similarity (0-1)
    
    # Text Processing
    MIN_WORD_LENGTH: int = 2
    MAX_WORD_LENGTH: int = 50
    STOP_WORDS: str = "english"
    
    # Skill Extraction
    SKILL_MATCH_THRESHOLD: float = 0.85  # Fuzzy matching threshold
    MAX_SKILLS_EXTRACT: int = 50
    
    # PDF Processing
    PDF_MAX_PAGES: int = 10  # Reasonable limit for resumes
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Skill Categories for Organization
SKILL_CATEGORIES: Dict[str, List[str]] = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", 
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r"
    ],
    "web_frontend": [
        "react", "angular", "vue", "html", "css", "sass", "tailwind",
        "bootstrap", "webpack", "vite", "next.js", "nuxt", "svelte"
    ],
    "web_backend": [
        "node.js", "express", "django", "flask", "fastapi", "spring boot",
        "asp.net", "rails", "laravel", "nest.js"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "oracle", "sql server", "sqlite"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "jenkins", "gitlab ci", "github actions", "ansible", "ci/cd"
    ],
    "ml_ai": [
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "keras", "nlp", "computer vision", "transformers",
        "llm", "opencv", "pandas", "numpy", "jupyter"
    ],
    "data_science": [
        "data analysis", "data visualization", "tableau", "power bi",
        "matplotlib", "seaborn", "plotly", "statistics", "sql", "etl"
    ],
    "tools_platforms": [
        "git", "github", "gitlab", "jira", "confluence", "slack",
        "vs code", "intellij", "postman", "figma", "linux", "bash"
    ],
    "soft_skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "agile", "scrum", "project management", "mentoring"
    ]
}


# Common synonyms and variations for skill matching
SKILL_SYNONYMS: Dict[str, List[str]] = {
    "javascript": ["js", "javascript", "ecmascript"],
    "typescript": ["ts", "typescript"],
    "python": ["python", "python3", "py"],
    "machine learning": ["ml", "machine learning", "maching learning"],
    "deep learning": ["dl", "deep learning", "neural networks"],
    "natural language processing": ["nlp", "natural language processing", "text mining"],
    "computer vision": ["cv", "computer vision", "image processing"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node", "nodejs", "node.js"],
    "postgresql": ["postgres", "postgresql", "psql"],
    "mongodb": ["mongo", "mongodb"],
    "kubernetes": ["k8s", "kubernetes"],
    "continuous integration": ["ci", "continuous integration", "ci/cd"],
}


def get_all_skills() -> List[str]:
    """Get flattened list of all skills from taxonomy."""
    skills = []
    for category_skills in SKILL_CATEGORIES.values():
        skills.extend(category_skills)
    return list(set(skills))  # Remove duplicates


def get_skill_category(skill: str) -> str:
    """Get category for a given skill."""
    skill_lower = skill.lower()
    for category, skills in SKILL_CATEGORIES.items():
        if skill_lower in [s.lower() for s in skills]:
            return category
    return "other"
