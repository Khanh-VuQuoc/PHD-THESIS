# 🎓 PhD Thesis Assistant

> Claude AI-powered research assistant for thesis writing, paper analysis, and LaTeX review

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Anthropic Claude](https://img.shields.io/badge/Claude-API-purple.svg)](https://www.anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **📚 Multi-Paper Analysis**: Ask questions across multiple research papers simultaneously
- **✍️ LaTeX Review**: Grammar, mathematical rigor, and literature alignment checks
- **🔍 Research Gap Analysis**: Identify opportunities for thesis contributions
- **🤖 Smart Routing**: Automatically selects Sonnet (fast) or Opus (thorough) based on query
- **💰 Cost Tracking**: Monitor API usage and expenses in real-time
- **🎯 Specialized Prompts**: Pre-built templates for common thesis tasks

## 🚀 Quick Start

### For Google Colab (Recommended)

```python
# Install
!pip install anthropic

# Clone this repo
!git clone https://github.com/Khanh-VuQuoc/PHD-THESIS.git

# Add to path
import sys
sys.path.append('/content/PHD-THESIS')

# Import and use
from thesis_assistant import *

initialize()
quick_ask("Summarize the main approaches in my papers")
```

### Local Installation

```bash
# Clone repository
git clone https://github.com/Khanh-VuQuoc/PHD-THESIS.git
cd PHD-THESIS

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY='sk-ant-xxxxx'
```

## 📖 Usage Examples

### Basic Queries

```python
from thesis_assistant import *

# Initialize
initialize()

# Quick question with all papers
quick_ask("What is Schrödinger Bridge problem?")

# Detailed analysis with specific model
ask_claude(
    "Verify the proof in Section 3.2 step by step",
    model="opus"
)
```

### LaTeX Review

```python
latex_section = r"""
\section{Methodology}
The Schrödinger Bridge formulation...
"""

# Grammar and style check
review_latex(latex_section, mode="grammar")

# Mathematical rigor check
review_latex(latex_section, mode="rigor", model="opus")
```

### Research Tasks

```python
# Compare approaches across papers
compare_papers("How do papers handle rainbow options pricing?")

# Extract relevant equations
extract_equations("Forward-Backward SDE")

# Identify research gaps
find_gaps("Multivariate Schrödinger Bridge for exotic options")
```

## ⚙️ Configuration

### Google Colab Setup

1. **Add API Key to Secrets**:
   - Click 🔑 in left sidebar
   - Add `ANTHROPIC_API_KEY`
   - Toggle "Notebook access" ON

2. **Configure Paths** in `thesis_assistant/config.py`:
   ```python
   DRIVE_ROOT = "/content/drive/MyDrive/PHD_SBTS"
   PAPERS_DIR = DRIVE_ROOT
   ```

3. **Upload PDFs** to your Drive folder

### Local Setup

Create `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Or set environment variable:
```bash
export ANTHROPIC_API_KEY='sk-ant-xxxxx'
```

## 📁 Project Structure

```
PHD-THESIS/
├── thesis_assistant/        # Main package
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration
│   ├── claude_client.py    # API wrapper
│   ├── pdf_handler.py      # PDF operations
│   ├── prompts.py          # Prompt templates
│   ├── utils.py            # Utilities
│   ├── cost_tracker.py     # Cost tracking
│   └── main.py             # Main interface
├── examples/               # Example notebooks
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🎯 Model Selection

### Automatic Routing

The system automatically chooses the best model:

| Task Type | Model | Cost | Speed |
|-----------|-------|------|-------|
| Literature review | Sonnet 4.5 | 💰 Low | ⚡ Fast |
| Equation extraction | Sonnet 4.5 | 💰 Low | ⚡ Fast |
| Grammar check | Sonnet 4.5 | 💰 Low | ⚡ Fast |
| Proof verification | Opus 4.5 | 💰💰 High | 🐢 Thorough |
| Mathematical critique | Opus 4.5 | 💰💰 High | 🐢 Thorough |
| Gap analysis | Opus 4.5 | 💰💰 High | 🐢 Thorough |

### Manual Override

```python
# Force specific model
ask_claude("Question", model="sonnet")  # Fast
ask_claude("Question", model="opus")    # Thorough
```

## 💰 Cost Estimates

Typical thesis usage:

| Task | Model | Approximate Cost |
|------|-------|-----------------|
| Literature review (4 papers) | Sonnet | $0.01 - $0.03 |
| LaTeX grammar review | Sonnet | $0.005 - $0.01 |
| Mathematical proof verification | Opus | $0.02 - $0.05 |
| Research gap analysis | Opus | $0.03 - $0.08 |

**Full thesis support**: ~$10-30 total

Track your usage:
```python
show_report()
```

## 📚 Available Functions

### Main Functions
- `initialize()` - Setup the assistant
- `ask_claude()` - Main query function
- `quick_ask()` - Quick query with all papers

### Specialized Functions
- `review_latex()` - Review LaTeX sections
- `compare_papers()` - Compare paper approaches
- `extract_equations()` - Extract equations
- `find_gaps()` - Find research gaps

### Utilities
- `list_papers()` - Show available PDFs
- `show_report()` - Display cost report
- `verify_setup()` - Check configuration

## 🔧 Advanced Usage

### Custom Prompts

```python
result = ask_claude(
    prompt="Your custom prompt here",
    pdf_paths=["path/to/specific/paper.pdf"],
    model="auto",
    max_tokens=4096,
    show_response=True
)

# Access raw results
print(result["answer"])
print(result["cost"])
```

### Batch Processing

```python
questions = [
    "What are the main contributions?",
    "List key equations",
    "Identify limitations"
]

for q in questions:
    result = ask_claude(q, show_response=False)
    print(f"Q: {q}\nA: {result['answer'][:200]}...\n")
```

## 🐛 Troubleshooting

### "API Key not found"
- For Colab: Add to Secrets (🔑 in sidebar)
- For local: Set `ANTHROPIC_API_KEY` environment variable

### "No PDFs found"
- Check `PAPERS_DIR` path in `config.py`
- Run `verify_setup()` to diagnose

### "Module not found"
- Add package to Python path:
  ```python
  import sys
  sys.path.append('/path/to/PHD-THESIS')
  ```

## 🤝 Contributing

This is a personal thesis project, but suggestions are welcome:

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

MIT License - Free for academic use

## 🙏 Acknowledgments

- Built with [Claude 4.5](https://www.anthropic.com/claude) by Anthropic
- Designed for thesis research at UEH (University of Economics Ho Chi Minh City)

## 📧 Contact

**Khanh Vu Quoc**
- GitHub: [@Khanh-VuQuoc](https://github.com/Khanh-VuQuoc)
- Research: Mathematical Economics, Quantitative Finance

---

⭐ Star this repo if it helps with your thesis!
