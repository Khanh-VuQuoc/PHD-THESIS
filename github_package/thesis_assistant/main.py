"""
Main interface - High-level functions for Colab

Usage:
    from main import *
    initialize()
    quick_ask("Your question here")
"""

from .config import get_api_key
from .claude_client import ClaudeClient
from .pdf_handler import PDFHandler
from .prompts import (
    get_latex_review_prompt,
    get_compare_papers_prompt,
    get_extract_equations_prompt,
    get_gap_analysis_prompt
)
from .utils import display_response, print_header
from .cost_tracker import CostTracker
from .config import get_api_key, DRIVE_ROOT, PAPERS_DIR  # Add DRIVE_ROOT, PAPERS_DIR here

# ============================================
# GLOBAL INSTANCES
# ============================================

_client = None
_pdf_handler = None
_tracker = None


def initialize():
    """Initialize all components"""
    global _client, _pdf_handler, _tracker
    
    print("🔧 Initializing Thesis Assistant...\n")
    
    try:
        api_key = get_api_key()
        _client = ClaudeClient(api_key)
        _pdf_handler = _client.pdf_handler
        _tracker = CostTracker()
        
        print("✅ Initialization complete!")
        print("\n💡 Available functions:")
        print("   • ask_claude(prompt, pdf_paths='all', model='auto')")
        print("   • quick_ask(prompt) - shortcut with all papers")
        print("   • review_latex(latex_text, mode='grammar|rigor|literature')")
        print("   • compare_papers(question)")
        print("   • extract_equations(topic)")
        print("   • find_gaps(research_area)")
        print("   • list_papers() - show available PDFs")
        print("   • show_report() - cost tracking")
        print("   • verify_setup() - check configuration")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


# ============================================
# MAIN FUNCTIONS
# ============================================

def ask_claude(
    prompt: str,
    pdf_paths: any = "all",
    model: str = "auto",
    max_tokens: int = 4096,
    show_response: bool = True
):
    """
    Ask Claude with papers context
    
    Args:
        prompt: Your question
        pdf_paths: "all", None, or list of PDF paths
        model: "auto", "sonnet", or "opus"
        max_tokens: Response length (max 4096)
        show_response: Display formatted response
        
    Returns:
        Response dict with answer, tokens, cost
        
    Example:
        result = ask_claude("Explain Schrödinger Bridge", model="opus")
    """
    if _client is None:
        print("❌ Not initialized. Run initialize() first.")
        return None
    
    # Call API
    result = _client.ask(
        prompt=prompt,
        pdf_paths=pdf_paths,
        model=model,
        max_tokens=max_tokens
    )
    
    # Track if successful
    if result["success"] and _tracker:
        _tracker.add(
            model=result["model"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            cost=result["cost"],
            question_preview=prompt
        )
    
    # Display
    if show_response and result["success"]:
        display_response(result)
    
    return result


def quick_ask(prompt: str, model: str = "auto"):
    """
    Quick ask with all papers (shortcut)
    
    Example:
        quick_ask("Tổng hợp các phương pháp deep hedging")
    """
    return ask_claude(prompt, pdf_paths="all", model=model)


def review_latex(latex_text: str, mode: str = "grammar", model: str = "auto"):
    """
    Review LaTeX section
    
    Args:
        latex_text: LaTeX code to review
        mode: "grammar", "rigor", or "literature"
        model: Which model to use (default: auto)
        
    Example:
        latex = r"\\section{Introduction}\\nThe SB problem..."
        review_latex(latex, mode="rigor", model="opus")
    """
    prompt = get_latex_review_prompt(latex_text, mode)
    return ask_claude(prompt, pdf_paths="all", model=model)


def compare_papers(question: str, model: str = "sonnet"):
    """
    Compare approaches across all papers
    
    Example:
        compare_papers("How to price rainbow options?")
    """
    prompt = get_compare_papers_prompt(question)
    return ask_claude(prompt, pdf_paths="all", model=model)


def extract_equations(topic: str):
    """
    Extract equations from papers
    
    Example:
        extract_equations("Forward-Backward SDE")
    """
    prompt = get_extract_equations_prompt(topic)
    return ask_claude(prompt, pdf_paths="all", model="sonnet")


def find_gaps(research_area: str):
    """
    Find research gaps for thesis
    
    Example:
        find_gaps("Multivariate Schrödinger Bridge for exotic options")
    """
    prompt = get_gap_analysis_prompt(research_area)
    return ask_claude(prompt, pdf_paths="all", model="opus")


# ============================================
# UTILITY FUNCTIONS
# ============================================

def list_papers():
    """List available papers in the directory"""
    if _pdf_handler is None:
        print("❌ Not initialized. Run initialize() first.")
        return
    
    _pdf_handler.print_pdfs()


def show_report():
    """Show session cost and usage report"""
    if _tracker is None:
        print("❌ Tracker not initialized.")
        return
    
    _tracker.report()


def verify_setup():
    """Verify all setup is correct"""
    import os
    from pathlib import Path
    
    print("🔍 Checking setup...\n")
    
    checks = {
        "✓ Google Drive mounted": os.path.exists("/content/drive"),
        "✓ Thesis directory exists": os.path.exists(DRIVE_ROOT),
        "✓ Papers directory exists": os.path.exists(PAPERS_DIR),
        "✓ Client initialized": _client is not None,
    }
    
    all_good = True
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
        if not status:
            all_good = False
    
    print("\n" + "="*60)
    
    if all_good:
        pdfs = list(Path(PAPERS_DIR).glob("*.pdf"))
        print(f"\n🎉 Setup complete! Found {len(pdfs)} PDFs")
        
        if len(pdfs) > 0:
            list_papers()
            print("\n✨ Ready to use! Try:")
            print("   quick_ask('Summarize the papers')")
        else:
            print(f"\n⚠️  No PDFs found. Upload papers to:")
            print(f"    {PAPERS_DIR}")
    else:
        print("\n⚠️  Please fix issues above:")
        if not os.path.exists("/content/drive"):
            print("  1. Mount Drive: from google.colab import drive; drive.mount('/content/drive')")
        if _client is None:
            print("  2. Add ANTHROPIC_API_KEY to Secrets (left panel 🔑)")
        if not os.path.exists(PAPERS_DIR):
            print(f"  3. Create folder: {PAPERS_DIR}")
    
    return all_good


# ============================================
# CONVENIENCE ALIASES
# ============================================

qa = quick_ask  # Shortcut: qa("question")
init = initialize  # Shortcut: init()
verify = verify_setup  # Shortcut: verify()
report = show_report  # Shortcut: report()


if __name__ == "__main__":
    print(__doc__)
