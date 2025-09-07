"""
Liquidity zone detection using confluence analysis
"""

import pandas as pd
from typing import List, Dict
import logging

from .technical_analyzer import TechnicalAnalyzer
from ..models.market_data import MarketData
from ..config.settings import config

logger = logging.getLogger(__name__)


class LiquidityDetector:
    """Detect high liquidity zones using confluence analysis"""
    
    def __init__(self, analyzer: TechnicalAnalyzer):
        self.analyzer = analyzer
    
    def find_liquidity_zones(self, market_data: MarketData) -> List[Dict]:
        """Find high liquidity zones with multiple confirmations"""
        zones = []
        
        try:
            daily_data = market_data.get_daily_data()
            if daily_data is None or len(daily_data) < 50:
                logger.warning(f"Insufficient daily data for {market_data.symbol}")
                return zones
            
            current_price = market_data.current_price
            if current_price is None:
                logger.warning(f"No current price for {market_data.symbol}")
                return zones
            
            # Get technical analysis for daily timeframe
            trendlines = self.analyzer.detect_trendlines(daily_data)
            levels = self.analyzer.find_support_resistance_levels(daily_data)
            fib_data = self.analyzer.calculate_fibonacci_levels(daily_data)
            structure = self.analyzer.identify_price_structure(daily_data)
            
            # Find confluence zones
            potential_zones = self._create_price_zones(current_price)
            
            for zone in potential_zones:
                confirmations = []
                confluence_score = 0
                
                # Check trendline confluence
                for tl in trendlines[:5]:  # Check top 5 trendlines
                    if self._price_near_level(zone['price'], tl['current_level'], tolerance=0.02):
                        confirmations.append(f"Trendline_{tl['type']}_{tl['direction']}")
                        confluence_score += tl['strength'] * 2
                
                # Check support/resistance confluence
                for level in levels[:10]:  # Check top 10 levels
                    if self._price_near_level(zone['price'], level['level'], tolerance=0.015):
                        confirmations.append(f"Level_{level['type']}_{level['source']}")
                        confluence_score += level['strength'] * level['touches']
                
                # Check Fibonacci confluence
                if fib_data and 'levels' in fib_data:
                    for fib_name, fib_info in fib_data['levels'].items():
                        if self._price_near_level(zone['price'], fib_info['level'], tolerance=0.01):
                            confirmations.append(f"Fibonacci_{fib_name}")
                            confluence_score += 2
                
                # Check volume confluence
                volume_confirmation = self._check_volume_confluence(daily_data, zone['price'])
                if volume_confirmation:
                    confirmations.append("High_Volume_Level")
                    confluence_score += 1
                
                # Only consider zones with minimum confirmations
                min_confirmations = config.analysis.min_confluence_confirmations
                if len(confirmations) >= min_confirmations:
                    zones.append({
                        'price': zone['price'],
                        'type': zone['type'],
                        'confirmations': confirmations,
                        'confluence_score': confluence_score,
                        'strength': len(confirmations),
                        'distance_from_price': abs(zone['price'] - current_price) / current_price,
                        'trendlines': [tl for tl in trendlines if self._price_near_level(zone['price'], tl['current_level'], 0.02)],
                        'levels': [l for l in levels if self._price_near_level(zone['price'], l['level'], 0.015)],
                        'fibonacci': fib_data if fib_data else {},
                        'structure_context': structure
                    })
            
            # Sort by confluence score and proximity to current price
            zones.sort(key=lambda x: (x['confluence_score'], -x['distance_from_price']), reverse=True)
            
            return zones[:5]  # Return top 5 zones
            
        except Exception as e:
            logger.error(f"Error finding liquidity zones for {market_data.symbol}: {e}")
            return []
    
    def _create_price_zones(self, current_price: float, range_pct: float = None) -> List[Dict]:
        """Create potential price zones around current price"""
        if range_pct is None:
            range_pct = config.analysis.liquidity_zone_range
            
        zones = []
        
        try:
            # Create zones at different percentages from current price
            percentages = [-0.15, -0.10, -0.08, -0.05, -0.03, -0.02, -0.01, 
                          0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.15]
            
            for pct in percentages:
                zone_price = current_price * (1 + pct)
                zone_type = 'support' if pct < 0 else 'resistance'
                
                zones.append({
                    'price': zone_price,
                    'type': zone_type,
                    'percentage_from_current': pct
                })
        except Exception as e:
            logger.error(f"Error creating price zones: {e}")
        
        return zones
    
    def _price_near_level(self, price1: float, price2: float, tolerance: float = 0.02) -> bool:
        """Check if two prices are near each other within tolerance"""
        try:
            return abs(price1 - price2) / max(price1, price2) <= tolerance
        except (ZeroDivisionError, TypeError):
            return False
    
    def _check_volume_confluence(self, data: pd.DataFrame, target_price: float, 
                               tolerance: float = 0.02) -> bool:
        """Check if there was significant volume near target price"""
        try:
            volume_threshold = data['Volume'].quantile(0.7)
            
            for _, row in data.iterrows():
                if (self._price_near_level(row['High'], target_price, tolerance) or 
                    self._price_near_level(row['Low'], target_price, tolerance)):
                    if row['Volume'] > volume_threshold:
                        return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking volume confluence: {e}")
            return False
