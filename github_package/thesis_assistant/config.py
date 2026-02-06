"""
Configuration and constants for Thesis Assistant
"""

import os
from pathlib import Path

# ============================================
# API CONFIGURATION
# ============================================

def get_api_key():
    """Get API key from Colab Secrets"""
    try:
        from google.colab import userdata
        return userdata.get('ANTHROPIC_API_KEY')
    except:
        raise ValueError(
            "API Key not found! "
            "Add ANTHROPIC_API_KEY to Colab Secrets (left panel 🔑)"
        )

# ============================================
# PATHS
# ============================================

DRIVE_ROOT = "/content/drive/MyDrive/PHD_SBTS"
PAPERS_DIR = DRIVE_ROOT

# ============================================
# MODELS
# ============================================

MODELS = {
    "sonnet": "claude-sonnet-4-5-20250929",
    "opus": "claude-opus-4-5-20251101"
}

# Model pricing (per million tokens)
PRICING = {
    "sonnet": {"input": 3.00, "output": 15.00},
    "opus": {"input": 15.00, "output": 75.00}
}

# ============================================
# DEFAULTS
# ============================================

DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 1.0
DEFAULT_MODEL = "auto"
