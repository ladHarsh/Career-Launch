"""
Career Launch - Streamlit UI
Simple, clean interface for resume analysis and job matching.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.resume_parser import get_resume_parser
from src.ml.skill_extractor import get_skill_extractor
from src.ml.matcher import get_job_matcher
from src.analyzers.gap_analyzer import get_gap_analyzer


# ==========================================
# 🎨 UI CONFIGURATION & CSS
# ==========================================

st.set_page_config(
    page_title="Career Launch",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS
st.markdown("""
    <style>
    /* --- MAIN APP BACKGROUND --- */
    .stApp {
        background-color: #0f172a;
    }
    
    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #1e293b;
    }
    
    /* --- SIDEBAR HEADERS --- */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    /* --- TOGGLE SWITCH (RADIO BUTTON) --- */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        background-color: #0f172a;
        padding: 4px;
        border-radius: 10px;
        margin-bottom: 20px;
        gap: 2px;
        width: 100%;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        flex: 1;
        text-align: center;
        background-color: transparent;
        padding: 8px 10px;
        border-radius: 8px;
        border: none;
        transition: all 0.2s ease;
        margin: 0 !important;
        cursor: pointer;
        color: #94a3b8;
        font-weight: 500;
        font-size: 13px;
        white-space: nowrap; /* Keep text in one line */
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #334155;
    }
    
    /* Selected toggle option */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #3b82f6;
        color: #ffffff;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }
    
    /* --- FILE UPLOADER --- */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #0f172a;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 30px 10px;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
        background-color: #1e293b;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background-color: transparent !important;
        border: none;
        padding: 0;
        width: 100%;
        text-align: center; /* Center text */
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    /* Only target the Browse files button, not delete button */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] button[kind="secondary"] {
        background-color: #3b82f6;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }

    /* Style delete button as a clean circular icon */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"] {
        position: absolute !important;
        top: 8px !important;
        right: 8px !important;
        width: 20px !important;
        height: 20px !important;
        padding: 0 !important;
        min-width: 0 !important;
        background-color: transparent !important;
        color: #ef4444 !important;
        border: none !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 100 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"]:hover,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"]:active,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"]:focus {
        background-color: transparent !important;
        color: #ff4b4b !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
        text-align: center;
        width: 100%;
        display: block;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        text-align: center;
        width: 100%;
        display: block;
    }
    
    /* --- TEXT AREA --- */
    [data-testid="stSidebar"] textarea {
        background-color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
        color: #f1f5f9 !important;
        font-size: 14px !important;
    }
    
    [data-testid="stSidebar"] textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    
    [data-testid="stSidebar"] textarea::placeholder {
        color: #64748b !important;
    }
    
    /* --- ANALYZE BUTTON --- */
    [data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] div.stButton > button:active {
        transform: translateY(0);
    }
    
    /* --- DIVIDER --- */
    [data-testid="stSidebar"] hr {
        margin: 20px 0;
        border: none;
        border-top: 1px solid #334155;
    }
    
    /* --- SUCCESS MESSAGE --- */
    [data-testid="stSidebar"] .element-container .stSuccess {
        background-color: #064e3b;
        color: #6ee7b7;
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 3px solid #10b981;
        font-size: 13px;
        margin-top: 8px;
    }
    
    /* --- MAIN CONTENT AREA --- */
    h1, h2, h3 {
        color: #f1f5f9;
    }
    
    /* --- METRICS --- */
    [data-testid="stMetricValue"] {
        color: #3b82f6;
    }
    
    /* --- INFO BOXES --- */
    .element-container .stInfo {
        background-color: #1e3a5f;
        color: #93c5fd;
        border-left: 3px solid #3b82f6;
    }
    
    /* --- SUCCESS BOXES --- */
    .element-container .stSuccess {
        background-color: #064e3b;
        color: #6ee7b7;
        border-left: 3px solid #10b981;
    }
    
    /* --- ERROR BOXES --- */
    .element-container .stError {
        background-color: #7f1d1d;
        color: #fca5a5;
        border-left: 3px solid #ef4444;
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        color: #94a3b8;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 500;
        border: 1px solid #334155;
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0f172a;
        color: #3b82f6;
        border-color: #3b82f6;
        font-weight: 600;
    }
    
    /* --- EXPANDER --- */
    .streamlit-expanderHeader {
        background-color: #1e293b;
        color: #f1f5f9;
        border-radius: 6px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #334155;
    }
    
    /* --- DIVIDER IN MAIN CONTENT --- */
    hr {
        border-color: #334155;
    }
    
    /* --- HERO SECTION --- */
    .hero-container {
        padding: 60px 20px;
        text-align: center;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 20px;
        margin-bottom: 40px;
        border: 1px solid #334155;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 20px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        max-width: 800px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    
    /* --- FEATURE CARDS --- */
    .feature-card {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #334155;
        height: 100%;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        color: #3b82f6;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 12px;
    }
    
    .feature-text {
        color: #94a3b8;
        line-height: 1.5;
        font-size: 1rem;
    }
    
    /* --- ANALYSIS UI COMPONENTS --- */
    .explanation-card {
        background-color: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 20px 25px;
        border-radius: 12px;
        margin-top: 10px;
        line-height: 1.6;
    }
    
    .explanation-header {
        color: #3b82f6;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .explanation-content {
        color: #e2e8f0;
        font-size: 1rem;
    }

    .summary-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 16px;
        height: 100%;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 15px;
        margin-top: 20px;
    }

    .stat-card {
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid transparent;
    }

    .stat-card.matched { background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.2); }
    .stat-card.missing { background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.2); }
    .stat-card.extra { background: rgba(59, 130, 246, 0.08); border-color: rgba(59, 130, 246, 0.2); }

    .stat-value {
        font-size: 1.75rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    
    .matched .stat-value { color: #10b981; }
    .missing .stat-value { color: #ef4444; }
    .extra .stat-value { color: #3b82f6; }

    .stat-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #94a3b8;
    }

    /* --- SKILL BREAKDOWN --- */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 15px;
        margin-top: 10px;
    }

    .skill-category-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }


    .skill-category-title {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 12px;
        border-bottom: 1px solid #334155;
        padding-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .skill-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 4px;
        border: 1px solid transparent;
    }

    .skill-badge.green { background: rgba(16, 185, 129, 0.1); color: #6ee7b7; border-color: rgba(16, 185, 129, 0.2); }
    .skill-badge.red { background: rgba(239, 68, 68, 0.1); color: #fca5a5; border-color: rgba(239, 68, 68, 0.2); }
    .skill-badge.blue { background: rgba(59, 130, 246, 0.1); color: #93c5fd; border-color: rgba(59, 130, 246, 0.2); }

    /* --- INSIGHTS & RECOMMENDATIONS --- */
    .insight-card {
        background-color: rgba(59, 130, 246, 0.05);
        border-left: 4px solid #3b82f6;
        padding: 14px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
        color: #e2e8f0;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .recommendation-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .rec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .rec-category {
        color: #f1f5f9;
        font-weight: 700;
        font-size: 1.1rem;
    }

    .priority-badge {
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
    }

    .priority-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .priority-medium { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .priority-low { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

    .rec-reason {
        color: #94a3b8;
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    .rec-focus {
        background: rgba(15, 23, 42, 0.5);
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 0.85rem;
    }

    .rec-focus-label {
        color: #64748b;
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 5px;
        display: block;
    }

    .rec-skills {
        color: #cbd5e1;
    }

    /* --- REPORT UI ELEMENTS --- */
    .report-header {
        margin-bottom: 25px;
    }
    .report-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #f1f5f9 !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }
    .report-subtitle {
        font-size: 1.1rem !important;
        color: #94a3b8 !important;
        margin-bottom: 0 !important;
    }
    .success-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 20px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .section-title {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        margin-bottom: 15px !important;
    }

    /* --- MATCH INTELLIGENCE DASHBOARD --- */
    .score-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }
    .score-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .score-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .score-card.primary {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-color: rgba(59, 130, 246, 0.3);
    }
    .score-percent {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
        line-height: 1;
    }
    .score-name {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
    }
    .score-bar-bg {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        margin-top: 15px;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
    }
    
    /* Score Colors */
    .color-high { color: #10b981; }
    .color-med { color: #f59e0b; }
    .color-low { color: #ef4444; }
    .bg-high { background: #10b981; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4); }
    .bg-med { background: #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
    .bg-low { background: #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); }

    /* --- MOBILE RESPONSIVENESS --- */
    @media (max-width: 768px) {
        /* Let the design breathe more on mobile */
        .block-container {
            padding-top: 3.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }


        /* Hero Section */
        .hero-container {
            padding: 20px 15px !important;
            margin-bottom: 25px !important;
            margin-top: 5px !important;
        }
        .hero-title {
            font-size: 1.5rem !important;
            margin-bottom: 8px !important;
        }
        .hero-subtitle {
            font-size: 0.85rem !important;
            padding: 0 !important;
            margin-bottom: 15px !important;
        }

        /* Report Header Mobile - More Spaced and Premium */
        .report-header {
            margin-bottom: 20px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 15px !important;
        }
        .report-title {
            font-size: 1.8rem !important;
            margin-bottom: 10px !important;
            background: linear-gradient(90deg, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .report-subtitle {
            font-size: 0.95rem !important;
            margin-bottom: 5px !important;
            opacity: 0.8;
        }
        .section-title {
            font-size: 1.4rem !important;
            margin-top: 10px !important;
        }
        .success-badge {
            padding: 6px 14px !important;
            font-size: 0.8rem !important;
            margin-bottom: 20px !important;
            margin-top: 0 !important;
            border-radius: 10px !important;
            background: rgba(16, 185, 129, 0.15) !important;
        }
        
        /* Comfortable divider space */
        hr {
            margin: 1.25rem 0 !important;
        }

        /* Better vertical rhythm */
        [data-testid="stMain"] [data-testid="stVerticalBlock"] {
            gap: 1.25rem !important;
        }

        /* Redesign Detailed Skill Breakdown for Mobile */
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px !important;
            padding: 0 !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            justify-content: flex-start !important;
            border-bottom: none !important;
        }
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none !important; /* Hide scrollbar for cleaner look */
        }
        .stTabs button {
            padding: 8px 12px !important;
            font-size: 0.75rem !important;
            min-height: 0 !important;
            flex-shrink: 0 !important;
        }
        [data-testid="stMain"] h1, [data-testid="stMain"] h2 {
            font-size: 1.35rem !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.6rem !important;
        }
        [data-testid="stMain"] h3, [data-testid="stMain"] h4, [data-testid="stMain"] h5 {
            font-size: 1.05rem !important;
            margin-top: 0.8rem !important;
            margin-bottom: 0.4rem !important;
        }
        [data-testid="stMain"] .element-container div[data-testid="stMarkdownContainer"] p {
            font-size: 0.82rem !important;
            margin-bottom: 6px !important;
            line-height: 1.4 !important;
        }
        
        /* Metric Score Cards and Grids */
        .score-grid {
            grid-template-columns: 1fr !important;
            gap: 12px !important;
        }
        .score-card {
            padding: 15px 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            text-align: left !important;
        }
        .score-percent {
            font-size: 1.8rem !important;
            margin-bottom: 0 !important;
            order: 2;
        }
        .score-info {
            order: 1;
        }
        .score-bar-bg {
            display: none !important; /* Hide bars on small mobile rows */
        }
        .score-name {
            font-size: 0.75rem !important;
        }


        /* Feature Cards Horizontal Layout */
        [data-testid="column"], [data-testid="stHorizontalBlock"] > div {
            margin-bottom: 20px !important;
        }
        .feature-card {
            display: flex !important;
            flex-direction: row !important;
            align-items: flex-start !important;
            gap: 15px !important;
            padding: 20px !important;
            margin-bottom: 0 !important;
            text-align: left !important;
        }
        .feature-icon {
            font-size: 2rem !important;
            margin-bottom: 0 !important;
            flex-shrink: 0 !important;
            margin-top: 5px !important;
        }
        .feature-title {
            font-size: 1.2rem !important;
            margin-bottom: 5px !important;
        }
        .feature-text {
            font-size: 0.9rem !important;
        }

        /* Metrics Grid */
        .metric-grid {
            grid-template-columns: 1fr !important; /* Stack stats on small screens */
            gap: 20px !important;
        }
        .stat-value {
            font-size: 1.5rem !important;
        }

        /* Category Grid */
        .category-grid {
            grid-template-columns: 1fr !important; /* Stack categories */
        }

        /* Sidebar Mobile Optimizations */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 10px !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0px !important; /* Zero top padding */
            padding-bottom: 5px !important;
        }

        /* Target the very top spacing container in sidebar - Home of the close button */
        [data-testid="stSidebar"] .st-emotion-cache-10p9htt, 
        [data-testid="stSidebar"] .e6f82ta4 {
            min-height: auto !important;
            margin: 0 !important;
            padding: 10px 0 !important;
        }
        
        /* Safely position sidebar content without negative margins to prevent overlap */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
            margin-top: 0 !important;
        }
        
        /* Headers in sidebar */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            font-size: 1.05rem !important;
            margin-bottom: 8px !important;
            margin-top: 5px !important;
        }
        
        /* Taglines and descriptions */
        [data-testid="stSidebar"] .element-container p {
            font-size: 0.85rem !important;
            line-height: 1.4 !important;
            margin-top: 0 !important;
            margin-bottom: 4px !important;
        }

        /* Toggle Button (Radio) */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            padding: 2px !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 4px 8px !important;
            font-size: 10px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            gap: 4px !important;
            margin: 0 !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove internal radio icon margins for perfect centering */
        [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* File Uploader Dropzone - More Compact */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            padding: 10px !important;
            min-height: 80px !important;
        }
        
        /* Hide or drastically shrink sub-labels */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div > small {
            display: none !important; /* Hide the file limit text on mobile */
        }
        
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section > div > div {
            font-size: 0.75rem !important;
            margin-bottom: 2px !important;
        }

        /* Shrink Browse Button */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button[kind="secondary"] {
            padding: 5px 15px !important;
            font-size: 12px !important;
            min-height: 30px !important;
        }

        /* File Uploaded State - Mobile Refinements */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] {
            padding: 8px 10px !important; /* Tighten container padding */
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] div[data-testid="stFileUploaderFileData"] {
            padding: 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] div[data-testid="stFileUploaderFileData"] > div {
            gap: 5px !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] .st-emotion-cache-12w0qpk {
            font-size: 0.8rem !important; /* File name font size */
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] .st-emotion-cache-10p9htt {
            font-size: 0.7rem !important; /* File size font size */
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] svg {
            width: 14px !important;
            height: 14px !important;
        }
        /* Target the close button specifically */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button[title="Remove file"] {
            width: 20px !important;
            height: 20px !important;
            min-height: 20px !important;
        }

        /* Space between sidebar sections */
        [data-testid="stSidebar"] hr {
            margin: 10px 0 !important;
        }

        /* Text Area height reduction */
        [data-testid="stSidebar"] textarea {
            height: 100px !important;
            min-height: 100px !important;
            font-size: 0.8rem !important;
            padding: 8px !important;
        }



        /* Analyze Button */
        [data-testid="stSidebar"] button[kind="primary"] {
            padding: 10px !important;
            font-size: 0.9rem !important;
        }

        /* Analysis Progress & Cards */
        .explanation-card {
            padding: 12px 15px !important;
        }
        .explanation-header {
            font-size: 0.95rem !important;
            margin-bottom: 5px !important;
        }
        .explanation-content {
            font-size: 0.85rem !important;
            line-height: 1.4 !important;
        }
        
        /* Skill Analysis & Insights Mobile Redesign */
        .skill-category-card {
            padding: 12px 15px !important;
            border-radius: 10px !important;
        }
        .skill-category-title {
            font-size: 0.9rem !important;
            margin-bottom: 8px !important;
            padding-bottom: 5px !important;
        }
        .skill-badge {
            padding: 3px 10px !important;
            font-size: 0.75rem !important;
            margin: 3px !important;
        }
        
        .insight-card {
            padding: 10px 15px !important;
            font-size: 0.85rem !important;
            gap: 10px !important;
            margin-bottom: 8px !important;
            border-radius: 0 6px 6px 0 !important;
        }
        
        .recommendation-card {
            padding: 15px !important;
            border-radius: 10px !important;
            margin-bottom: 12px !important;
        }
        .rec-category {
            font-size: 1rem !important;
        }
        .rec-reason {
            font-size: 0.8rem !important;
            margin-bottom: 10px !important;
        }
        .rec-focus {
            padding: 8px 12px !important;
        }
        .rec-focus-label {
            font-size: 0.7rem !important;
        }
        
        .stat-card {
            padding: 12px !important;
        }
        .stat-value {
            font-size: 1.4rem !important;
        }
        .stat-label {
            font-size: 0.65rem !important;
        }

        .summary-card {
            padding: 18px !important;
            border-radius: 12px !important;
        }
        .summary-card div:first-child {
            font-size: 1.1rem !important;
            margin-bottom: 8px !important;
        }
        .summary-card div:nth-child(2) {
            font-size: 0.85rem !important;
            margin-bottom: 12px !important;
        }
        .metric-grid {
            gap: 10px !important;
            margin-top: 15px !important;
        }


        /* Scope specific Streamlit padding containers to avoid bleeding into main content */
        [data-testid="stSidebar"] .stVerticalBlock, 
        [data-testid="stSidebar"] .st-emotion-cache-tn0cau, 
        [data-testid="stSidebar"] .ek2vi383 {
            padding-left: 5px !important;
            padding-right: 5px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            gap: 2px !important; /* Tighten gap between elements */
            font-size: 0.8rem !important; /* Scale down relative fonts */
            width: 100% !important;
            height: auto !important;
            min-height: 0 !important;
        }

        /* Scale down everything inside these blocks for mobile */
        [data-testid="stSidebar"] .st-emotion-cache-tn0cau *, 
        [data-testid="stSidebar"] .ek2vi383 * {
            font-size: 0.8rem !important;
            line-height: 1.2 !important;
        }


        /* Apply full width ONLY when open to allow Streamlit's closing animation to work */
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 100vw !important;
            max-width: 100vw !important;
        }
        
        [data-testid="stSidebar"] {
            overflow-x: hidden !important;
        }


    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📊 VISUALIZATION FUNCTIONS
# ==========================================

def render_score_gauge(score: float, title: str):
    """Render a modern gauge chart for scores."""
    # Determine color based on score
    if score >= 70:
        bar_color = "#10b981" # emerald
    elif score >= 40:
        bar_color = "#f59e0b" # amber
    else:
        bar_color = "#ef4444" # red
        
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#f1f5f9', 'family': 'sans-serif'}},
        number={'font': {'size': 36, 'color': '#f1f5f9', 'family': 'sans-serif'}, 'suffix': "%"},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': bar_color, 'thickness': 0.8},
            'bgcolor': "#1e293b",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.1)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.1)'}
            ],
        }
    ))
    
    fig.update_layout(
        height=240,
        margin=dict(l=30, r=30, t=60, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': "Inter, sans-serif"}
    )
    return fig


def render_skills_chart(matched: int, missing: int, extra: int):
    """Render skills breakdown chart."""
    fig = go.Figure(data=[
        go.Bar(
            x=['Matched', 'Missing', 'Extra'],
            y=[matched, missing, extra],
            marker_color=['#10b981', '#ef4444', '#3b82f6'],
            text=[matched, missing, extra],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Skills Breakdown",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def render_skill_badges(skills: List[str], color: str):
    """Render skill badges with modern custom styling."""
    if not skills:
        st.write("_None_")
        return
    badges_html = "".join([f'<span class="skill-badge {color}">{skill}</span>' for skill in sorted(skills)])
    st.markdown(f'<div style="margin-bottom: 20px;">{badges_html}</div>', unsafe_allow_html=True)


def render_category_breakdown(categorized: Dict[str, List[str]], title: str):
    """Render skills organized by category in a responsive grid of cards."""
    if not categorized:
        st.info(f"No {title.lower()} found.")
        return
    
    cards_html = ""
    for category, skills in sorted(categorized.items()):
        skills_list = ", ".join(sorted(skills))
        cards_html += f'<div class="skill-category-card"><div class="skill-category-title">' \
                      f'<span>{category.replace("_", " ").title()}</span>' \
                      f'<span style="font-size: 0.8rem; color: #64748b;">{len(skills)} skills</span></div>' \
                      f'<div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">{skills_list}</div></div>'
    
    st.markdown(f'<div class="category-grid">{cards_html}</div>', unsafe_allow_html=True)


# ==========================================
# 🚀 MAIN APPLICATION
# ==========================================

def main():
    """Main application logic."""
    
    # Initialize components
    parser = get_resume_parser()
    extractor = get_skill_extractor()
    matcher = get_job_matcher()
    analyzer = get_gap_analyzer()
    
    # ==========================================
    # 🎨 SIDEBAR REDESIGN
    # ==========================================
    with st.sidebar:
        st.header("Configuration")
        st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-top: -15px; margin-bottom: 20px;'>Fine-tune your analysis parameters and inputs</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 1. Resume Input Section
        st.subheader("1. Candidate Resume")
        
        # 1. State Initialization
        if 'input_mode' not in st.session_state:
            st.session_state.input_mode = "Upload PDF"

        # 2. Input Method Selector (Always Visible)
        st.session_state.input_mode = st.radio(
            "Select Input Method",
            ["Upload PDF", "Paste Text"],
            index=0 if st.session_state.input_mode == "Upload PDF" else 1,
            label_visibility="collapsed",
            key="input_method_selector"
        )

        # Container variables
        resume_file = None
        resume_text_input = None

        # 3. Conditional Rendering
        if st.session_state.input_mode == "Upload PDF":
            resume_file = st.file_uploader(
                "Upload resume (PDF)",
                type=['pdf'],
                label_visibility="collapsed",
                key="resume_pdf_uploader"
            )
            
            if resume_file:
                st.markdown("""
                    <style>
                    [data-testid="stFileUploaderDropzone"] { display: none !important; }
                    [data-testid="stFileUploader"] label { display: none !important; }
                    [data-testid="stFileUploader"] {
                        padding: 20px 10px !important;
                        border-style: solid !important;
                        border-color: #10b981 !important;
                        background-color: rgba(16, 185, 129, 0.05) !important;
                        border-radius: 12px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
        else: # Paste Text Mode
            resume_text_input = st.text_area(
                "Paste resume content",
                height=300,
                placeholder="Paste the full text of the resume here...",
                label_visibility="collapsed",
                key="resume_text_area"
            )

        st.markdown("") # Spacer
        
        # 2. Job Description Section
        st.subheader("2. Target Job")
        job_description = st.text_area(
            "Job Description",
            height=250,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 3. Analyze Button
        analyze_button = st.button("Analyze Match", type="primary", width="stretch")
        
        st.markdown(
            "<div style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 20px;'>"
            "Career Intelligence Platform v1.0 • Secure & Private"
            "</div>", 
            unsafe_allow_html=True
        )
    
    # ==========================================
    # MAIN CONTENT AREA
    # ==========================================
    if analyze_button:
        # IMMEDIATELY trigger sidebar collapse on mobile so user sees the loading/results
        st.components.v1.html(
            """
            <script>
            (function() {
                const parentDoc = window.parent.document;
                let attempts = 0;
                const maxAttempts = 100; // 10 seconds total
                
                const interval = setInterval(() => {
                    const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
                    const isMobile = window.parent.innerWidth <= 768;
                    
                    if (sidebar && isMobile) {
                        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                        
                        if (isExpanded) {
                            // Find any button that looks like a collapse button
                            const buttons = Array.from(parentDoc.querySelectorAll('button'));
                            let btn = buttons.find(b => {
                                const label = b.getAttribute('aria-label');
                                return label && (label.includes('Close') || label.includes('Collapse')) && label.includes('sidebar');
                            });
                            
                            // Fallback to data-testid
                            if (!btn) btn = parentDoc.querySelector('[data-testid="stSidebarCollapseButton"]');
                            
                            // Fallback to first icon button in sidebar
                            if (!btn) btn = sidebar.querySelector('button');

                            if (btn) {
                                btn.click();
                                clearInterval(interval);
                            }
                        } else {
                            clearInterval(interval);
                        }
                    }
                    if (++attempts >= maxAttempts) clearInterval(interval);
                }, 100);
            })();
            </script>
            """,
            height=0, width=0,
        )

        st.markdown("""
            <div class="report-header">
                <h1 class="report-title">AI Career Intelligence</h1>
                <p class="report-subtitle">Deep analysis of your professional fit</p>
            </div>
        """, unsafe_allow_html=True)



        # Validation
        if not job_description or len(job_description.strip()) < 50:
            st.error("Please provide a valid job description (at least 50 characters).")
            return
        
        # Logic to handle Resume Source (File vs Text)
        resume_text = ""
        
        # Scenario A: File Upload
        if st.session_state.input_mode == "Upload PDF" and resume_file:
            with st.spinner("Parsing resume PDF..."):
                parse_result = parser.parse_pdf(resume_file)
                
                if not parse_result['success']:
                    st.error(f"Resume parsing failed: {parse_result['error']}")
                    return
                
                resume_text = parse_result['text']
                # Removed redundant success message for cleaner UI
        
        # Scenario B: Text Paste
        elif st.session_state.input_mode == "Paste Text" and resume_text_input:
            resume_text = resume_text_input
        
        # Scenario C: Missing Input
        else:
            st.error("Please provide resume data (Upload a file or paste text).")
            return
        
        # --- Analysis Pipeline ---
        
        # Extract skills
        with st.spinner("Extracting skills using NLP..."):
            resume_skills_data = extractor.extract_skills(resume_text, context="resume")
            job_skills_data = extractor.extract_skills(job_description, context="job_description")
            
            resume_skills = [s['skill'] for s in resume_skills_data]
            job_skills = [s['skill'] for s in job_skills_data]
        
        # Calculate match score
        with st.spinner("Calculating job match score..."):
            match_result = matcher.calculate_match_score(
                resume_text, job_description, resume_skills, job_skills
            )
        
        # Perform gap analysis
        with st.spinner("Analyzing skill gaps..."):
            gap_result = analyzer.analyze_gap(resume_skills, job_skills)
        
        # Display results with custom success badge
        st.markdown('<div class="success-badge">✨ Analysis Complete</div>', unsafe_allow_html=True)
        
        # Overall score section
        st.markdown('<h2 class="section-title">Match Intelligence</h2>', unsafe_allow_html=True)
        
        score_metrics = [
            ("Overall Match", match_result['overall_score'], True),
            ("Skill Match", match_result['skill_match_score'], False),
            ("Content Similarity", match_result['text_similarity_score'], False)
        ]
        
        score_html = '<div class="score-grid">'
        for name, val, is_primary in score_metrics:
            color_class = "high" if val >= 70 else "med" if val >= 40 else "low"
            primary_class = "primary" if is_primary else ""
            score_html += (
                f'<div class="score-card {primary_class}">'
                f'<div class="score-info"><div class="score-name">{name}</div></div>'
                f'<div class="score-percent color-{color_class}">{int(val)}%</div>'
                f'<div class="score-bar-bg"><div class="score-bar-fill bg-{color_class}" style="width: {val}%"></div></div>'
                f'</div>'
            )
        score_html += '</div>'
        st.markdown(score_html, unsafe_allow_html=True)

        
        # Explanation
        st.markdown(f"""
            <div class="explanation-card">
                <div class="explanation-header">
                    <span>🤖</span> AI Analysis Explanation
                </div>
                <div class="explanation-content">
                    {match_result['explanation']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Skills breakdown
        st.header("Skills Analysis")
        
        # Unified Skills Dashboard
        skill_summary_html = f"""
            <div class="summary-card" style="margin-bottom: 20px;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;">Quick Summary</div>
                <div style="color: #94a3b8; line-height: 1.5; font-style: italic; margin-bottom: 0;">
                    {gap_result['summary']}
                </div>
            </div>
        """
        st.markdown(skill_summary_html, unsafe_allow_html=True)

        # Dashboard-style metric cards
        s_matched = gap_result['matched_skills']['count']
        s_missing = gap_result['missing_skills']['count']
        s_extra = gap_result['extra_skills']['count']
        total_s = s_matched + s_missing
        
        m_perc = (s_matched / total_s * 100) if total_s > 0 else 0
        ms_perc = (s_missing / total_s * 100) if total_s > 0 else 0
        
        skill_metrics_html = f"""
            <div class="score-grid">
                <div class="score-card">
                    <div class="score-info"><div class="score-name">Matched</div></div>
                    <div class="score-percent color-high">{s_matched}</div>
                    <div class="score-bar-bg"><div class="score-bar-fill bg-high" style="width: {m_perc}%"></div></div>
                </div>
                <div class="score-card">
                    <div class="score-info"><div class="score-name">Missing</div></div>
                    <div class="score-percent color-low">{s_missing}</div>
                    <div class="score-bar-bg"><div class="score-bar-fill bg-low" style="width: {ms_perc}%"></div></div>
                </div>
                <div class="score-card">
                    <div class="score-info"><div class="score-name">Extra</div></div>
                    <div class="score-percent color-med" style="color: #3b82f6;">{s_extra}</div>
                    <div class="score-bar-bg"><div class="score-bar-fill" style="background: #3b82f6; width: 100%;"></div></div>
                </div>
            </div>
        """
        st.markdown(skill_metrics_html, unsafe_allow_html=True)
        st.divider()

        
        # Detailed skill breakdown
        st.header("Detailed Skill Breakdown")
        
        tab1, tab2, tab3 = st.tabs(["Matched Skills", "Missing Skills", "Extra Skills"])
        
        with tab1:
            st.subheader(f"Matched Skills ({gap_result['matched_skills']['count']})")
            st.write("These skills appear in both your resume and the job description.")
            render_skill_badges(gap_result['matched_skills']['skills'], 'green')
            st.markdown("#### By Category")
            render_category_breakdown(gap_result['matched_skills']['by_category'], "Matched Skills")
        
        with tab2:
            st.subheader(f"Missing Skills ({gap_result['missing_skills']['count']})")
            st.write("These skills are required by the job but not found in your resume.")
            render_skill_badges(gap_result['missing_skills']['skills'], 'red')
            st.markdown("#### By Category")
            render_category_breakdown(gap_result['missing_skills']['by_category'], "Missing Skills")
        
        with tab3:
            st.subheader(f"Extra Skills ({gap_result['extra_skills']['count']})")
            st.write("These skills are in your resume but not explicitly required by the job.")
            render_skill_badges(gap_result['extra_skills']['skills'], 'blue')
            st.markdown("#### By Category")
            render_category_breakdown(gap_result['extra_skills']['by_category'], "Extra Skills")
        
        st.divider()
        
        # Insights and recommendations
        st.header("Insights & Recommendations")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Key Insights")
            for insight in gap_result['insights']:
                st.markdown(f"""
                    <div class="insight-card">
                        <span style="font-size: 1.2rem;">💡</span>
                        <span>{insight}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Recommendations")
            for rec in gap_result['recommendations']:
                priority_class = f"priority-{rec['priority'].lower()}"
                st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="rec-header">
                            <span class="rec-category">{rec['category']}</span>
                            <span class="priority-badge {priority_class}">{rec['priority']} Priority</span>
                        </div>
                        <div class="rec-reason">{rec['reason']}</div>
                        <div class="rec-focus">
                            <span class="rec-focus-label">Focus Areas</span>
                            <span class="rec-skills">{', '.join(rec['skills'])}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # Welcome message (Redesigned Landing Page)
        st.markdown(f"""
            <div class="hero-container">
                <div class="hero-title">Career Launch</div>
                <div class="hero-subtitle">
                    Bridge the gap between your skills and your dream job. 
                    Upload your resume and a job description to get instant, 
                    explainable AI-powered analysis and recommendations.
                </div>
                <p style='color: #3b82f6; font-weight: 600; font-size: 1.1rem;'>
                    Get Started: Choose your resume input method in the sidebar.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights with Cards
        col1, col2, col3 = st.columns(3)
        
        feature_cards = [
            {
                "icon": "📄",
                "title": "Resume Parsing",
                "text": "Robust PDF text extraction with multiple fallback methods for 100% compatibility."
            },
            {
                "icon": "🤖",
                "title": "ML-Powered Analysis",
                "text": "Using TF-IDF and Cosine Similarity to provide mathematically backed, transparent matching."
            },
            {
                "icon": "🎯",
                "title": "Skill Gap Analysis",
                "text": "Instantly identify matched, missing, and extra skills with clear category breakdowns."
            }
        ]
        
        for i, col in enumerate([col1, col2, col3]):
            with col:
                st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{feature_cards[i]['icon']}</div>
                        <div class="feature-content">
                            <div class="feature-title">{feature_cards[i]['title']}</div>
                            <div class="feature-text">{feature_cards[i]['text']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()