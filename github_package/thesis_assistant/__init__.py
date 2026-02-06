"""
Thesis Assistant - Claude AI for Academic Research

A modular package for thesis research assistance using Claude API.
Supports paper analysis, LaTeX review, and research gap identification.
"""

__version__ = "1.0.0"
__author__ = "Khanh Vu Quoc"

from .main import (
    initialize,
    ask_claude,
    quick_ask,
    review_latex,
    compare_papers,
    extract_equations,
    find_gaps,
    list_papers,
    show_report,
    verify_setup,
    # Shortcuts
    qa,
    init,
    verify,
    report
)

__all__ = [
    "initialize",
    "ask_claude",
    "quick_ask",
    "review_latex",
    "compare_papers",
    "extract_equations",
    "find_gaps",
    "list_papers",
    "show_report",
    "verify_setup",
    "qa",
    "init",
    "verify",
    "report"
]
