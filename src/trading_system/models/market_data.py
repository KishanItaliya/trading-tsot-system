"""
Market data models
"""

from dataclasses import dataclass
from typing import Dict, Optional
import pandas as pd
from datetime import datetime


@dataclass
class TimeframeData:
    """Data for a specific timeframe"""
    timeframe: str
    data: pd.DataFrame
    last_updated: datetime
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    @property
    def current_price(self) -> Optional[float]:
        """Get current price (last close)"""
        if len(self.data) > 0:
            return self.data['Close'].iloc[-1]
        return None
    
    @property
    def is_valid(self) -> bool:
        """Check if data is valid and not empty"""
        return len(self.data) > 0 and not self.data.empty


@dataclass
class MarketData:
    """Container for multi-timeframe market data"""
    symbol: str
    timeframes: Dict[str, TimeframeData]
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    def get_timeframe(self, timeframe: str) -> Optional[TimeframeData]:
        """Get data for specific timeframe"""
        return self.timeframes.get(timeframe)
    
    def get_daily_data(self) -> Optional[pd.DataFrame]:
        """Get daily timeframe data"""
        daily_tf = self.get_timeframe('daily')
        return daily_tf.data if daily_tf and daily_tf.is_valid else None
    
    def get_hourly_data(self) -> Optional[pd.DataFrame]:
        """Get hourly timeframe data"""
        hourly_tf = self.get_timeframe('hourly')
        return hourly_tf.data if hourly_tf and hourly_tf.is_valid else None
    
    @property
    def current_price(self) -> Optional[float]:
        """Get current price from daily data"""
        daily_data = self.get_daily_data()
        if daily_data is not None and len(daily_data) > 0:
            return daily_data['Close'].iloc[-1]
        return None
    
    @property
    def is_valid(self) -> bool:
        """Check if market data is valid"""
        return (len(self.timeframes) > 0 and 
                any(tf.is_valid for tf in self.timeframes.values()))
    
    def has_timeframe(self, timeframe: str) -> bool:
        """Check if timeframe data exists and is valid"""
        tf_data = self.get_timeframe(timeframe)
        return tf_data is not None and tf_data.is_valid
