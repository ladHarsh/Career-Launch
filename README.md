# 🎯 Career Launch

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://share.streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Career Launch is an AI-powered career intelligence platform that analyzes resumes against job descriptions to identify skill gaps, calculate matching scores, and provide actionable career insights using NLP and Machine Learning.

---

## 📱 Mobile-First Dashboard
The platform features a **Premium Mobile UI** specifically engineered for high-density information display on small screens. 
- **Match Intelligence**: Interactive score cards replacing traditional heavy gauges.
- **Skill Discovery**: High-density badging system with horizontal scrolling tabs.
- **AI Insights**: Compact, glassmorphic cards for rapid scanning.

---

## 🚀 Key Features

### 🔍 Precision Analysis
- **Automatic PDF Parsing**: Dual-engine parsing (pdfplumber + PyPDF2) with robust fallback mechanisms.
- **Skill Extraction**: Hybrid extraction using TF-IDF importance scoring and a curated skill taxonomy.
- **Similarity Scoring**: Advanced Cosine Similarity calculation across content and skill vectors.

### 📊 Match Intelligence
- **Overall Match Score**: weighted composite score for candidate suitability.
- **Skill Match**: Visual breakdown of shared expertise.
- **Content Similarity**: Deep-text alignment analysis.

### 💡 Career Insights
- **Skill Gap Analysis**: Actionable lists of Matched, Missing, and Extra skills.
- **Prioritized Recommendations**: AI-driven suggestions on which skills to learn first.
- **Category Breakdown**: Skills grouped by domain (ML, Backend, Cloud, etc.) for better context.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (Custom CSS for Mobile Redesign)
- **NLP & ML**: [Scikit-learn](https://scikit-learn.org/), [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/)
- **PDF Processing**: [pdfplumber](https://github.com/jsvine/pdfplumber), [PyPDF2](https://github.com/py-pdf/PyPDF2)
- **Mathematics**: TF-IDF Vectorization, Cosine Similarity

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ladHarsh/AI-Career-Intelligence-Platform.git
cd AI-Career-Intelligence-Platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app/streamlit_app.py
```

---

## 🧬 How it Works

1. **Preprocessing**: The text is cleaned, normalized, and stripped of noise words.
2. **Vectorization**: The engine converts both the resume and job description into high-dimensional TF-IDF vectors.
3. **Similarity Calculation**: Uses **Cosine Similarity** to measure the distance between the two vectors, providing a mathematical "Match Score."
4. **Taxonomy Alignment**: Skills are matched against a structured knowledge base to categorize candidates' strengths.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas to improve the platform.

---

**Developed with ❤️ by [Harsh Lad](https://github.com/ladHarsh)**
