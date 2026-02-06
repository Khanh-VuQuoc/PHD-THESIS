"""
Prompt templates for common tasks
"""

LATEX_REVIEW_PROMPTS = {
    "grammar": """
Review this LaTeX section for:
1. Grammar and clarity
2. Logical flow between sentences and paragraphs
3. Academic tone and style
4. Suggest improvements

Provide corrections in LaTeX format.
    """,
    
    "rigor": """
Critique this mathematical exposition:
1. Are definitions precise and complete?
2. Are theorems/propositions stated correctly?
3. Any logical gaps in the argument?
4. Are assumptions explicitly stated?
5. Compare with standard formulations in the papers

Point out any issues with mathematical rigor.
    """,
    
    "literature": """
Compare this section with the provided papers:
1. Am I citing relevant work correctly?
2. Are there missing key references I should include?
3. Does my approach align with established literature?
4. Are there contradictions with existing work?

Suggest improvements to better position this work.
    """
}


def get_compare_papers_prompt(question: str) -> str:
    """Generate prompt for comparing papers"""
    return f"""
Compare and contrast how different papers in my collection approach this question:

{question}

Provide a structured comparison:
1. Summary of each paper's approach (be specific)
2. Key similarities across papers
3. Key differences and unique contributions
4. Gaps or opportunities for my thesis

Reference specific sections/equations from papers when relevant.
    """


def get_extract_equations_prompt(topic: str) -> str:
    """Generate prompt for extracting equations"""
    return f"""
Extract all equations related to: {topic}

For each equation:
1. Provide the equation in LaTeX format
2. Note which paper it's from
3. Brief explanation of the notation
4. Context of when it's used

Format ready to paste into my thesis.
    """


def get_gap_analysis_prompt(research_area: str) -> str:
    """Generate prompt for gap analysis"""
    return f"""
Analyze the literature in my collection regarding: {research_area}

Identify:
1. What has been thoroughly covered?
2. What are the open questions or limitations?
3. Where do papers disagree or provide conflicting results?
4. What extensions or applications are missing?
5. Potential contributions for my thesis

Be specific and reference papers.
    """


def get_latex_review_prompt(latex_text: str, mode: str = "grammar") -> str:
    """Generate prompt for LaTeX review"""
    base_prompt = LATEX_REVIEW_PROMPTS.get(mode, LATEX_REVIEW_PROMPTS["grammar"])
    
    return f"{base_prompt}\n\nLaTeX Section:\n```latex\n{latex_text}\n```"
