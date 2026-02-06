"""
PDF handling utilities
"""

import base64
import os
from pathlib import Path
from typing import List, Optional
from .config import PAPERS_DIR


class PDFHandler:
    """Handle PDF loading and encoding"""
    
    def __init__(self, papers_dir: str = PAPERS_DIR):
        self.papers_dir = Path(papers_dir)
        self._cache = {}  # Cache encoded PDFs
    
    def list_pdfs(self) -> List[Path]:
        """List all PDFs in directory"""
        return list(self.papers_dir.glob("*.pdf"))
    
    def print_pdfs(self):
        """Print available PDFs with sizes"""
        pdfs = self.list_pdfs()
        print(f"\n📚 Found {len(pdfs)} PDFs:")
        
        for i, pdf in enumerate(pdfs, 1):
            size = os.path.getsize(pdf) / 1024 / 1024  # MB
            print(f"  {i}. {pdf.name} ({size:.1f} MB)")
        
        return pdfs
    
    def encode_pdf(self, pdf_path: str) -> str:
        """
        Encode PDF to base64 with caching
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Base64 encoded string
        """
        # Use cache if available
        if pdf_path in self._cache:
            return self._cache[pdf_path]
        
        # Encode and cache
        with open(pdf_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        
        self._cache[pdf_path] = encoded
        return encoded
    
    def get_all_pdfs(self) -> List[str]:
        """Get paths of all PDFs"""
        return [str(p) for p in self.list_pdfs()]
    
    def resolve_pdf_paths(self, pdf_paths: Optional[any]) -> List[str]:
        """
        Resolve PDF paths
        
        Args:
            pdf_paths: "all", None, or list of paths
            
        Returns:
            List of resolved PDF paths
        """
        if pdf_paths == "all":
            return self.get_all_pdfs()
        elif pdf_paths is None:
            return []
        else:
            return pdf_paths
    
    def build_content(self, prompt: str, pdf_paths: List[str]) -> List[dict]:
        """
        Build message content with PDFs
        
        Args:
            prompt: Text prompt
            pdf_paths: List of PDF paths
            
        Returns:
            List of content blocks for Claude API
        """
        content = []
        
        # Add PDFs
        for pdf_path in pdf_paths:
            print(f"  📄 Adding: {Path(pdf_path).name}")
            
            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": self.encode_pdf(pdf_path)
                }
            })
        
        # Add text prompt
        content.append({"type": "text", "text": prompt})
        
        return content
    
    def clear_cache(self):
        """Clear PDF encoding cache"""
        self._cache.clear()
