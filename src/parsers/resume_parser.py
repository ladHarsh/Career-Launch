"""
Resume parser with robust PDF text extraction.
Handles multiple PDF formats with fallback strategies.
"""

import io
from typing import Optional, Dict
import PyPDF2
import pdfplumber
from src.core.config import settings


class ResumeParser:
    """
    Extracts text from PDF resumes using multiple extraction methods.
    Implements fallback strategy for maximum compatibility.
    """
    
    def __init__(self):
        self.max_pages = settings.PDF_MAX_PAGES
    
    def parse_pdf(self, pdf_file) -> Dict[str, any]:
        """
        Parse PDF file and extract text.
        
        Args:
            pdf_file: File object or file path
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            text = self._extract_with_pdfplumber(pdf_file)
            method = "pdfplumber"
            
            # Fallback to PyPDF2 if pdfplumber fails or returns empty
            if not text or len(text.strip()) < 50:
                text = self._extract_with_pypdf2(pdf_file)
                method = "pypdf2"
            
            # Validate extraction
            if not text or len(text.strip()) < 50:
                return {
                    'success': False,
                    'text': '',
                    'error': 'Could not extract meaningful text from PDF',
                    'method': method
                }
            
            return {
                'success': True,
                'text': text,
                'char_count': len(text),
                'word_count': len(text.split()),
                'method': method,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': f'PDF parsing error: {str(e)}',
                'method': None
            }
    
    def _extract_with_pdfplumber(self, pdf_file) -> str:
        """
        Extract text using pdfplumber (better for tables and complex layouts).
        
        Args:
            pdf_file: File object or path
            
        Returns:
            Extracted text
        """
        try:
            # Reset file pointer if it's a file object
            if hasattr(pdf_file, 'seek'):
                pdf_file.seek(0)
            
            text_parts = []
            
            with pdfplumber.open(pdf_file) as pdf:
                # Limit pages to prevent processing huge documents
                pages_to_process = min(len(pdf.pages), self.max_pages)
                
                for page_num in range(pages_to_process):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_parts.append(page_text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            # Return empty string on error (will trigger fallback)
            return ''
    
    def _extract_with_pypdf2(self, pdf_file) -> str:
        """
        Extract text using PyPDF2 (fallback method).
        
        Args:
            pdf_file: File object or path
            
        Returns:
            Extracted text
        """
        try:
            # Reset file pointer if it's a file object
            if hasattr(pdf_file, 'seek'):
                pdf_file.seek(0)
            
            text_parts = []
            
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Limit pages
            pages_to_process = min(len(pdf_reader.pages), self.max_pages)
            
            for page_num in range(pages_to_process):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text_parts.append(page_text)
            
            return '\n'.join(text_parts)
            
        except Exception as e:
            return ''
    
    def parse_text(self, text: str) -> Dict[str, any]:
        """
        Parse plain text (for when user pastes resume text directly).
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with text and metadata
        """
        if not text or len(text.strip()) < 50:
            return {
                'success': False,
                'text': '',
                'error': 'Text is too short or empty',
                'method': 'plain_text'
            }
        
        return {
            'success': True,
            'text': text,
            'char_count': len(text),
            'word_count': len(text.split()),
            'method': 'plain_text',
            'error': None
        }
    
    def validate_resume(self, text: str) -> Dict[str, any]:
        """
        Validate that extracted text looks like a resume.
        
        Args:
            text: Extracted text
            
        Returns:
            Validation result with suggestions
        """
        text_lower = text.lower()
        
        # Common resume indicators
        resume_keywords = [
            'experience', 'education', 'skills', 'work', 'project',
            'university', 'college', 'degree', 'bachelor', 'master',
            'email', 'phone', 'linkedin'
        ]
        
        # Count how many indicators are present
        indicators_found = sum(1 for keyword in resume_keywords if keyword in text_lower)
        
        # Validation
        is_valid = indicators_found >= 3 and len(text.split()) >= 50
        
        return {
            'is_valid': is_valid,
            'indicators_found': indicators_found,
            'word_count': len(text.split()),
            'suggestions': [] if is_valid else [
                'Make sure the PDF contains actual resume content',
                'Check if the PDF is not password protected or corrupted',
                'Ensure the resume has standard sections (Experience, Education, Skills)'
            ]
        }


# Global parser instance
_parser_instance = None


def get_resume_parser() -> ResumeParser:
    """Get the global resume parser instance (singleton pattern)."""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = ResumeParser()
    return _parser_instance
