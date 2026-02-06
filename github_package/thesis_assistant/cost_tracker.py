"""
Cost and usage tracking
"""

import datetime
from typing import List, Dict, Any


class CostTracker:
    """Track API usage and costs across session"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.session_start = None
    
    def add(
        self, 
        model: str, 
        input_tokens: int, 
        output_tokens: int, 
        cost: float,
        question_preview: str
    ):
        """Add a query to history"""
        if self.session_start is None:
            self.session_start = datetime.datetime.now()
        
        self.history.append({
            "timestamp": datetime.datetime.now(),
            "model": model.upper(),
            "input": input_tokens,
            "output": output_tokens,
            "cost": cost,
            "question": (question_preview[:50] + "...") 
                       if len(question_preview) > 50 
                       else question_preview
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary statistics"""
        if not self.history:
            return None
        
        total_cost = sum(h['cost'] for h in self.history)
        total_queries = len(self.history)
        
        sonnet_queries = sum(1 for h in self.history if 'SONNET' in h['model'])
        opus_queries = sum(1 for h in self.history if 'OPUS' in h['model'])
        
        sonnet_cost = sum(h['cost'] for h in self.history if 'SONNET' in h['model'])
        opus_cost = sum(h['cost'] for h in self.history if 'OPUS' in h['model'])
        
        total_input = sum(h['input'] for h in self.history)
        total_output = sum(h['output'] for h in self.history)
        
        return {
            "total_cost": total_cost,
            "total_queries": total_queries,
            "sonnet_queries": sonnet_queries,
            "opus_queries": opus_queries,
            "sonnet_cost": sonnet_cost,
            "opus_cost": opus_cost,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output
        }
    
    def report(self):
        """Print session report"""
        summary = self.get_summary()
        
        if summary is None:
            print("📊 No queries yet in this session")
            return
        
        print("\n" + "="*70)
        print("📊 SESSION REPORT")
        print("="*70)
        print(f"\n💰 Total Cost: ${summary['total_cost']:.4f}")
        print(f"📈 Total Queries: {summary['total_queries']}")
        print(f"\n   🟢 Sonnet: {summary['sonnet_queries']} queries, ${summary['sonnet_cost']:.4f}")
        print(f"   🔴 Opus: {summary['opus_queries']} queries, ${summary['opus_cost']:.4f}")
        
        print(f"\n📊 Token Usage:")
        print(f"   Input:  {summary['total_input_tokens']:,} tokens")
        print(f"   Output: {summary['total_output_tokens']:,} tokens")
        print(f"   Total:  {summary['total_input_tokens'] + summary['total_output_tokens']:,} tokens")
        
        print("\n" + "="*70)
        print("📋 Recent Queries:")
        print("="*70)
        
        for i, h in enumerate(self.history[-10:], 1):  # Last 10
            ts = h['timestamp'].strftime('%H:%M:%S')
            print(f"{i:2d}. [{ts}] {h['model']:6s} | ${h['cost']:.4f} | {h['question']}")
        
        print("="*70)
