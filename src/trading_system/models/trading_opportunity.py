"""
Trading opportunity data model
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class TradingOpportunity:
    """Represents a trading opportunity with all necessary details"""
    symbol: str
    entry_model: str  # "Model1" or "Model2"
    entry_price: float
    stop_loss: float
    target: float
    risk_reward_ratio: float
    confluence_score: int
    confirmations: List[str]
    timeframe_analysis: Dict[str, Any]
    chart_patterns: Dict[str, Any]
    notes: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def risk_percentage(self) -> float:
        """Calculate risk as percentage of entry price"""
        return abs(self.entry_price - self.stop_loss) / self.entry_price * 100
    
    @property
    def reward_percentage(self) -> float:
        """Calculate reward as percentage of entry price"""
        return abs(self.target - self.entry_price) / self.entry_price * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'symbol': self.symbol,
            'entry_model': self.entry_model,
            'entry_price': self.entry_price,
            'stop_loss': self.stop_loss,
            'target': self.target,
            'risk_reward_ratio': self.risk_reward_ratio,
            'confluence_score': self.confluence_score,
            'confirmations': self.confirmations,
            'timeframe_analysis': self.timeframe_analysis,
            'chart_patterns': self.chart_patterns,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'risk_percentage': self.risk_percentage,
            'reward_percentage': self.reward_percentage
        }
