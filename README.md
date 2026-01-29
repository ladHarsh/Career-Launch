# Career Launch

![Python](https://img.shields.io/badge/python-3.9+-blue)
![Scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange)
![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%7C%20Cosine%20Similarity-green)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

Career Launch is an **NLP-based resume-job matching system** that quantifies candidate-role alignment using vector-space similarity and structured skill extraction. The system focuses on **explainability**, showing *why* a resume matches (or doesn't) and what skills to improve.

---

## TL;DR
Career Launch converts resumes and job descriptions into high-dimensional vector representations using TF-IDF and computes semantic similarity via cosine distance. It provides interpretable match scores and actionable skill-gap insights rather than opaque pass/fail decisions.

---

## Links
- **Live Application**: https://career-launch.streamlit.app/
- **Portfolio**: https://harshlad.vercel.app/

---

## Problem Statement
Most hiring pipelines rely on keyword-based filtering or opaque scoring systems, leading to false rejections and poor feedback loops. Candidates rarely understand *why* they were rejected or which skills are missing.

Career Launch addresses this by treating resume screening as a **measurable NLP similarity problem** and exposing intermediate signals instead of hiding them behind black-box decisions.

---

## ML Pipeline

### 1. Text Ingestion
- Resumes and job descriptions uploaded as PDFs or plain text
- Robust parsing using `pdfplumber` with `PyPDF2` as fallback
- Multi-engine extraction handles diverse PDF formats

### 2. Preprocessing
- Text normalization (lowercasing, punctuation handling)
- URL and email removal while preserving content
- Stop-word removal using NLTK's English corpus
- N-gram extraction (unigrams to trigrams) for phrase detection

### 3. Skill Extraction
**Hybrid Approach:**
- **Taxonomy-based matching**: 100+ curated skills across 9 domains
- **TF-IDF scoring**: Statistical importance of terms
- **Confidence weighting**: Combines both methods with 0.7/0.3 split

**Skill Categories:**
- Programming Languages
- Web Frontend/Backend
- Databases
- Cloud & DevOps
- ML & AI
- Data Science
- Tools & Platforms
- Soft Skills

### 4. Vectorization
- TF-IDF vectorization applied to full text (max 500 features)
- N-gram range: (1, 3) to capture multi-word technical terms
- Separate skill vectors maintained for granular analysis

### 5. Similarity Computation
**Weighted Scoring Algorithm:**
```
Overall Score = (Skill Match × 0.6) + (Text Similarity × 0.4)

Where:
- Skill Match = |Resume ∩ Job| / |Job|
- Text Similarity = cosine_similarity(TF-IDF_resume, TF-IDF_job)
```

**Rationale:**
- Skills weighted higher (60%) as they're explicit requirements
- Content similarity (40%) captures contextual alignment
- Produces interpretable 0-100% match score

### 6. Skill Gap Analysis
Skills classified into three sets:
- **Matched**: Resume ∩ Job Description
- **Missing**: Job Description - Resume
- **Extra**: Resume - Job Description

Missing skills prioritized by:
- Category importance (Programming > Soft Skills)
- Existing skill overlap in same category
- Role criticality (High/Medium/Low)

---

## Key Features

### Deterministic Similarity Scoring
- Vector-space model ensures reproducible results
- No black-box neural networks or opaque classifiers
- Full transparency in score computation

### Explainable Skill Gaps
- Explicit identification of matched vs missing skills
- Skills grouped by technical domain
- Contextual recommendations based on existing strengths

### Multi-Engine PDF Parsing
- Primary: `pdfplumber` (handles complex layouts, tables)
- Fallback: `PyPDF2` (broader format compatibility)
- Validation layer ensures minimum text quality

### Synonym Normalization
- Maps variations to canonical forms (e.g., "js" → "javascript")
- Handles common abbreviations (ML, NLP, K8s)
- Reduces false negatives from terminology differences

---

## Evaluation & Design Considerations

Career Launch does not claim "accuracy" in the traditional ML sense, as resume matching is inherently subjective and context-dependent.

**System Evaluation Criteria:**
- **Stability**: Consistent scores across minor text variations
- **Alignment**: Correlation with human judgment on relevance
- **Interpretability**: Users can understand and act on outputs
- **Robustness**: Handles noisy, real-world PDF data

**Design Philosophy:**
- Prioritize **explainability and trust** over aggressive automation
- Expose intermediate signals rather than final binary decisions
- Enable candidates to improve rather than just filter them out

**Known Limitations:**
- TF-IDF captures term frequency but not deep semantics
- No contextual understanding (e.g., "Python" the language vs snake)
- Performance depends on PDF text extraction quality
- Skill taxonomy requires manual curation and updates

---

## Tech Stack

### Core Language
- Python 3.9+

### NLP & ML
- **Scikit-learn** (v1.3.2+) - TF-IDF vectorization, cosine similarity
- **NumPy** (v1.26.2+) - Numerical computations
- **Pandas** (v2.1.3+) - Data manipulation

### Document Processing
- **pdfplumber** (v0.10.3+) - Primary PDF extraction
- **PyPDF2** (v3.0.1+) - Fallback extraction

### Configuration
- **Pydantic** (v2.1.0+) - Settings management with type validation

### UI
- **Streamlit** (v1.28.2+) - Lightweight, stateless UI for rapid iteration
- **Plotly** (v5.18.0+) - Interactive visualizations

---

## Project Structure

```
Career AI/
├── app/
│   └── streamlit_app.py          # UI layer (Streamlit-based interface)
│
├── src/
│   ├── parsers/
│   │   └── resume_parser.py      # Multi-engine PDF extraction
│   │
│   ├── ml/
│   │   ├── text_processor.py     # Text cleaning & normalization
│   │   ├── skill_extractor.py    # Hybrid skill extraction
│   │   └── matcher.py            # Similarity computation
│   │
│   ├── analyzers/
│   │   └── gap_analyzer.py       # Skill gap classification
│   │
│   └── core/
│       ├── config.py              # ML hyperparameters
│       └── skill_taxonomy.py     # Curated skill database
│
├── requirements.txt
└── README.md
```

---

## Setup & Run

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation
```bash
git clone https://github.com/ladHarsh/Career-Launch.git
cd Career-Launch
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Run the Application
```bash
streamlit run app/streamlit_app.py
```

Application will be available at `http://localhost:8501`

---

## Configuration

### ML Hyperparameters (`src/core/config.py`)
```python
# TF-IDF Configuration
TFIDF_MAX_FEATURES = 500        # Maximum vocabulary size
TFIDF_NGRAM_RANGE = (1, 3)      # Unigrams to trigrams
MIN_SKILL_CONFIDENCE = 0.3      # Minimum TF-IDF score threshold

# Skill Extraction
SKILL_MATCH_THRESHOLD = 0.85    # Fuzzy matching threshold
MAX_SKILLS_EXTRACT = 50         # Maximum skills per document

# Scoring Weights
SKILL_WEIGHT = 0.6              # Weight for skill-based matching
CONTENT_WEIGHT = 0.4            # Weight for text similarity
```

### Skill Taxonomy
9 predefined categories with 100+ skills:
- Programming Languages (14 skills)
- Web Frontend (13 skills)
- Web Backend (10 skills)
- Databases (10 skills)
- Cloud & DevOps (11 skills)
- ML & AI (10 skills)
- Data Science (10 skills)
- Tools & Platforms (12 skills)
- Soft Skills (8 skills)

---

## Engineering Learnings

### 1. Vector Space Modeling
- Translating unstructured documents into comparable vector spaces
- Balancing vocabulary size vs computational efficiency
- Handling sparse high-dimensional representations

### 2. Explainability in ML Systems
- Designing systems that favor interpretability over opaque scoring
- Exposing intermediate signals for user trust
- Communicating ML outputs in actionable ways

### 3. Robust Document Processing
- Handling noisy real-world PDF data with multiple extraction strategies
- Validating text quality before processing
- Graceful degradation when extraction fails

### 4. Hybrid Feature Engineering
- Combining rule-based (taxonomy) and statistical (TF-IDF) approaches
- Weighting different signal sources appropriately
- Normalizing heterogeneous skill representations

### 5. Domain Knowledge Integration
- Curating and maintaining skill taxonomies
- Mapping synonyms and abbreviations
- Categorizing skills by technical domain

---

## Limitations

### Current Constraints
1. **Semantic Understanding**: TF-IDF does not capture deep semantic meaning like embeddings
2. **Context Blindness**: Cannot distinguish "Python" (language) from "Python" (snake)
3. **Extraction Dependency**: Performance depends on PDF text extraction quality
4. **Static Taxonomy**: Skill database requires manual updates for new technologies
5. **No Temporal Awareness**: Doesn't account for skill recency or proficiency levels

### Not Implemented
- Contextual language models (BERT, GPT)
- Resume section parsing (Experience, Education, Skills)
- Temporal skill analysis (years of experience)
- Multi-document comparison (ranking multiple candidates)
- Active learning from user feedback

---

## Future Improvements

### Short-term
- Transition to embedding-based similarity (sentence transformers)
- Hybrid scoring combining keyword + embedding signals
- Resume section detection using layout analysis

### Medium-term
- Dataset-driven evaluation with human-labeled relevance pairs
- Active learning pipeline to refine skill taxonomy
- Support for DOCX and other document formats

### Long-term
- Fine-tuned transformer models for domain-specific matching
- Multi-modal analysis (skills + experience + education)
- Temporal skill trend analysis
- Integration with job board APIs

---

## Use Cases

### For Job Seekers
- Understand resume-job fit before applying
- Identify specific skills to learn
- Prioritize upskilling based on role requirements

### For Recruiters
- Pre-screen candidates with transparent scoring
- Provide constructive feedback to applicants
- Reduce bias from keyword-only filtering

### For Career Counselors
- Guide students on skill development paths
- Quantify readiness for specific roles
- Track skill gap closure over time

---

## License

MIT License

Copyright (c) 2024 Harsh Lad

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Author

**Harsh Lad**  
Applied AI Engineer

- Email: harshlad.dev@gmail.com
- GitHub: https://github.com/ladHarsh
- Portfolio: https://harshlad.vercel.app/

---

**Built with a focus on explainability, transparency, and practical ML design.**
