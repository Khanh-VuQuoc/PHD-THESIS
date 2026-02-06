"""
Claude API client wrapper
"""

import anthropic
from typing import Optional, List, Dict, Any
from .config import MODELS, PRICING, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE
from .pdf_handler import PDFHandler


class ClaudeClient:
    """Wrapper for Claude API with smart routing"""
    
    # Keywords for auto model detection
    OPUS_KEYWORDS = [
        "prove", "verify", "critique", "rigor", "review my",
        "analyze deeply", "step by step", "mathematical",
        "chứng minh", "kiểm tra", "đánh giá chi tiết",
        "xem xét kỹ", "phân tích sâu"
    ]
    
    def __init__(self, api_key: str):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.pdf_handler = PDFHandler()
    
    def auto_detect_model(self, prompt: str) -> str:
        """
        Auto-detect which model to use
        
        Args:
            prompt: User prompt
            
        Returns:
            "sonnet" or "opus"
        """
        prompt_lower = prompt.lower()
        
        # Check keywords
        if any(kw in prompt_lower for kw in self.OPUS_KEYWORDS):
            return "opus"
        
        # Long complex queries
        if len(prompt) > 500:
            return "opus"
        
        return "sonnet"
    
    def calculate_cost(
        self, 
        model: str, 
        input_tokens: int, 
        output_tokens: int
    ) -> float:
        """Calculate API call cost"""
        model_key = "sonnet" if "sonnet" in model else "opus"
        pricing = PRICING[model_key]
        
        cost = (
            input_tokens * pricing["input"] / 1_000_000 +
            output_tokens * pricing["output"] / 1_000_000
        )
        
        return cost
    
    def ask(
        self,
        prompt: str,
        pdf_paths: Optional[any] = None,
        model: str = "auto",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> Dict[str, Any]:
        """
        Ask Claude with papers context
        
        Args:
            prompt: Your question
            pdf_paths: List of PDF paths or "all"
            model: "auto", "sonnet", or "opus"
            max_tokens: Response length
            temperature: Creativity (0-1)
            
        Returns:
            Dict with response, tokens, cost, model used
        """
        # Resolve PDF paths
        resolved_paths = self.pdf_handler.resolve_pdf_paths(pdf_paths)
        
        # Auto-detect model
        if model == "auto":
            model = self.auto_detect_model(prompt)
            print(f"🤖 Auto-selected: {model.upper()}")
        
        model_name = MODELS[model]
        
        # Print info
        print(f"\n{'='*60}")
        print(f"🔵 Model: {model.upper()}")
        print(f"📚 Papers: {len(resolved_paths)}")
        print(f"💬 Prompt length: {len(prompt)} chars")
        print(f"{'='*60}\n")
        
        # Build content
        content = self.pdf_handler.build_content(prompt, resolved_paths)
        
        # Call API
        print("⏳ Calling Claude API...\n")
        
        try:
            response = self.client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": content}]
            )
            
            # Extract data
            answer = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = self.calculate_cost(model_name, input_tokens, output_tokens)
            
            return {
                "answer": answer,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "answer": None,
                "error": str(e),
                "success": False
            }
