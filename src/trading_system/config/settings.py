"""
Configuration settings for the trading system
"""

from dataclasses import dataclass
from typing import List, Dict
import os


@dataclass
class MarketConfig:
    """Market-related configuration"""
    # NSE stock list
    nse_stocks: List[str] = None
    
    # Data fetching settings
    default_period: str = "2y"
    hourly_period: str = "60d"
    minute_15_period: str = "30d"
    minute_5_period: str = "10d"
    
    # Market hours (IST)
    market_open_time: str = "09:15"
    market_close_time: str = "15:30"
    
    # Screening time
    screening_time: str = "10:00"
    
    def __post_init__(self):
        if self.nse_stocks is None:
            self.nse_stocks = [
                'RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK', 'HINDUNILVR',
                'INFY', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
                'BAJFINANCE', 'LT', 'ASIANPAINT', 'HCLTECH', 'AXISBANK',
                'MARUTI', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND',
                'WIPRO', 'BAJAJFINSV', 'POWERGRID', 'NTPC', 'ONGC',
                'TECHM', 'M&M', 'TATASTEEL', 'ADANIPORTS', 'COALINDIA',
                'DRREDDY', 'GRASIM', 'BRITANNIA', 'CIPLA', 'EICHERMOT',
                'BPCL', 'TATACONSUM', 'DIVISLAB', 'HEROMOTOCO', 'JSWSTEEL',
                'HINDALCO', 'INDUSINDBK', 'BAJAJ-AUTO', 'APOLLOHOSP',
                'TATAMOTORS', 'UPL', 'SBILIFE', 'HDFCLIFE', 'ADANIENT'
            ]


@dataclass
class AnalysisConfig:
    """Technical analysis configuration"""
    # Fibonacci levels
    fib_levels: List[float] = None
    
    # Trendline detection
    min_trendline_touches: int = 2
    trendline_tolerance: float = 0.005
    
    # Support/resistance detection
    sr_lookback_period: int = 50
    sr_consolidation_tolerance: float = 0.02
    
    # Liquidity zone detection
    liquidity_zone_range: float = 0.15
    min_confluence_confirmations: int = 3
    min_confluence_score: int = 5
    
    # Price structure analysis
    swing_point_order: int = 3
    structure_volatility_threshold: float = 0.05
    
    def __post_init__(self):
        if self.fib_levels is None:
            self.fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]


@dataclass
class TradingConfig:
    """Trading and risk management configuration"""
    # Risk management
    max_risk_per_trade: float = 0.05  # 5%
    min_risk_reward_ratio: float = 2.0
    max_daily_volatility: float = 0.1  # 10%
    
    # Pre-screening filters
    min_price: float = 50.0
    max_price: float = 5000.0
    min_avg_volume: int = 50000
    max_volatility: float = 0.1
    max_avg_daily_change: float = 0.15
    
    # Entry model tolerances
    model1_distance_tolerance: float = 0.02  # 2%
    model2_distance_tolerance: float = 0.05  # 5%
    retest_distance_tolerance: float = 0.02  # 2%
    
    # Market condition checks
    max_market_volatility: float = 0.05  # 5% on Nifty
    
    # Output settings
    max_opportunities: int = 20
    top_charts_count: int = 5
    
    # File paths
    reports_dir: str = "reports"
    charts_dir: str = "charts"
    logs_dir: str = "logs"
    
    def __post_init__(self):
        # Create directories if they don't exist
        for directory in [self.reports_dir, self.charts_dir, self.logs_dir]:
            os.makedirs(directory, exist_ok=True)


@dataclass
class SystemConfig:
    """Overall system configuration"""
    market: MarketConfig = None
    analysis: AnalysisConfig = None
    trading: TradingConfig = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Timezone settings
    timezone: str = "Asia/Kolkata"
    
    def __post_init__(self):
        if self.market is None:
            self.market = MarketConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.trading is None:
            self.trading = TradingConfig()


# Global configuration instance
config = SystemConfig()
