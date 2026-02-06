"""
Utility functions for display and formatting
"""

from IPython.display import display, HTML
from typing import Dict, Any


def display_response(result: Dict[str, Any]):
    """
    Display Claude's response with formatting
    
    Args:
        result: Result dict from ClaudeClient.ask()
    """
    if not result["success"]:
        print(f"❌ Error: {result['error']}")
        return
    
    answer = result["answer"]
    model = result["model"]
    
    # Display formatted response
    display(HTML(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3px;
        border-radius: 12px;
        margin: 20px 0;
    ">
        <div style="
            background: white;
            padding: 25px;
            border-radius: 10px;
        ">
            <h3 style="
                color: #667eea;
                margin-top: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            ">
                💬 Claude's Response ({model.upper()})
            </h3>
            <div style="
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                font-family: Georgia, serif;
                line-height: 1.8;
                color: #2c3e50;
                white-space: pre-wrap;
            ">
                {answer}
            </div>
        </div>
    </div>
    """))
    
    # Print stats
    print(f"\n{'='*60}")
    print(f"📊 TOKEN USAGE:")
    print(f"{'='*60}")
    print(f"   Input:  {result['input_tokens']:>8,} tokens")
    print(f"   Output: {result['output_tokens']:>8,} tokens")
    print(f"   Total:  {result['input_tokens'] + result['output_tokens']:>8,} tokens")
    print(f"   💰 Cost: ${result['cost']:.4f}")
    print(f"{'='*60}\n")


def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")
