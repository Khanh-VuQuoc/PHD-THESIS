# Thesis Assistant - Quick Start Example

This notebook demonstrates how to use the Thesis Assistant package.

## Setup

```python
# Install dependencies
!pip install anthropic -q

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Clone repository
!git clone https://github.com/Khanh-VuQuoc/PHD-THESIS.git

# Add to path
import sys
sys.path.append('/content/PHD-THESIS')
```

## Configure API Key

**Important**: Add your API key to Colab Secrets:
1. Click 🔑 Secrets in left sidebar
2. Add name: `ANTHROPIC_API_KEY`
3. Add value: `sk-ant-xxxxx`
4. Toggle "Notebook access" ON

## Initialize

```python
from thesis_assistant import *

# Initialize all components
initialize()

# Verify setup
verify_setup()
```

## Example 1: Quick Question

```python
# Ask about your papers
quick_ask("What are the main methodologies discussed in these papers?")
```

## Example 2: LaTeX Review

```python
# Your LaTeX section
my_latex = r"""
\section{Introduction}

The Schrödinger Bridge problem seeks to find the most likely
path between two probability distributions $\mu_0$ and $\mu_T$.

\begin{equation}
    dX_t = b(X_t, t)dt + \sigma dW_t
\end{equation}

where $b$ represents the drift term and $\sigma$ is the diffusion coefficient.
"""

# Review for mathematical rigor
review_latex(my_latex, mode="rigor", model="opus")
```

## Example 3: Compare Papers

```python
# Compare approaches across your papers
compare_papers("""
How do different papers approach the pricing of rainbow options?
What are the key differences in their methodologies?
""")
```

## Example 4: Extract Equations

```python
# Extract specific equations
extract_equations("Schrödinger Bridge formulation")
```

## Example 5: Find Research Gaps

```python
# Identify opportunities for your thesis
find_gaps("""
Multivariate Schrödinger Bridge applications to exotic options,
specifically rainbow and basket options
""")
```

## Check Costs

```python
# View your session costs
show_report()
```

## Advanced: Specific Papers Only

```python
# Use specific papers for focused analysis
ask_claude(
    "Compare the SB formulations in these two papers",
    pdf_paths=[
        "/content/drive/MyDrive/PHD_SBTS/paper1.pdf",
        "/content/drive/MyDrive/PHD_SBTS/paper2.pdf"
    ],
    model="opus"
)
```

## Tips

1. **Start with Sonnet** (auto-mode) for exploration
2. **Use Opus** for critical mathematical reviews
3. **Check costs** regularly with `show_report()`
4. **Be specific** in your questions for better results
5. **Batch similar queries** to save time

## Save Your Work

```python
# The results are displayed in the notebook
# You can copy important responses to your thesis documents
```

---

**Need help?** Check the [full documentation](https://github.com/Khanh-VuQuoc/PHD-THESIS)
