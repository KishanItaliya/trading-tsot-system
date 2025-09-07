"""
Entry model detection for trading opportunities
"""

import pandas as pd
from typing import List, Dict, Optional, Any
import logging

from .technical_analyzer import TechnicalAnalyzer
from .liquidity_detector import LiquidityDetector
from ..models.trading_opportunity import TradingOpportunity
from ..models.market_data import MarketData
from ..config.settings import config

logger = logging.getLogger(__name__)


class EntryModelDetector:
    """Detect Entry Model 1 and Entry Model 2 setups"""
    
    def __init__(self, analyzer: TechnicalAnalyzer, liquidity_detector: LiquidityDetector):
        self.analyzer = analyzer
        self.liquidity_detector = liquidity_detector
    
    def detect_entry_models(self, market_data: MarketData) -> List[TradingOpportunity]:
        """Detect both entry models and return trading opportunities"""
        opportunities = []
        
        try:
            daily_data = market_data.get_daily_data()
            if daily_data is None:
                logger.warning(f"No daily data for {market_data.symbol}")
                return opportunities
            
            # Find liquidity zones first
            liquidity_zones = self.liquidity_detector.find_liquidity_zones(market_data)
            
            if not liquidity_zones:
                logger.debug(f"No liquidity zones found for {market_data.symbol}")
                return opportunities
            
            current_price = market_data.current_price
            if current_price is None:
                logger.warning(f"No current price for {market_data.symbol}")
                return opportunities
            
            # Check each liquidity zone for entry opportunities
            for zone in liquidity_zones:
                # Entry Model 1: Direct Entry
                model1_opp = self._check_entry_model_1(market_data, zone, current_price)
                if model1_opp:
                    opportunities.append(model1_opp)
                
                # Entry Model 2: Confirmation Entry
                model2_opp = self._check_entry_model_2(market_data, zone, current_price)
                if model2_opp:
                    opportunities.append(model2_opp)
            
            # Filter by risk-reward ratio
            valid_opportunities = [
                opp for opp in opportunities 
                if opp.risk_reward_ratio >= config.trading.min_risk_reward_ratio
            ]
            
            return sorted(valid_opportunities, key=lambda x: x.confluence_score, reverse=True)
            
        except Exception as e:
            logger.error(f"Error detecting entry models for {market_data.symbol}: {e}")
            return []
    
    def _check_entry_model_1(self, market_data: MarketData, zone: Dict, 
                            current_price: float) -> Optional[TradingOpportunity]:
        """Check for Entry Model 1: Direct entry at liquidity zone"""
        
        try:
            # Check if price is near the liquidity zone
            distance = abs(current_price - zone['price']) / current_price
            if distance > config.trading.model1_distance_tolerance:
                return None
            
            # Determine trade direction based on trend and zone type
            daily_data = market_data.get_daily_data()
            structure = zone['structure_context']
            
            if structure['trend'] == 'bullish' and zone['type'] == 'support':
                trade_direction = 'long'
            elif structure['trend'] == 'bearish' and zone['type'] == 'resistance':
                trade_direction = 'short'
            else:
                return None  # No clear directional bias
            
            # Calculate entry, stop loss, and target
            entry_price = zone['price']
            
            if trade_direction == 'long':
                target = self._find_next_resistance(daily_data, entry_price)
                stop_loss = self._calculate_stop_loss_long(daily_data, zone, entry_price)
            else:  # short
                target = self._find_next_support(daily_data, entry_price)
                stop_loss = self._calculate_stop_loss_short(daily_data, zone, entry_price)
            
            if not target or not stop_loss:
                return None
            
            # Calculate risk-reward ratio
            if trade_direction == 'long':
                risk = entry_price - stop_loss
                reward = target - entry_price
            else:
                risk = stop_loss - entry_price
                reward = entry_price - target
            
            if risk <= 0 or reward <= 0:
                return None
            
            risk_reward_ratio = reward / risk
            
            if risk_reward_ratio < config.trading.min_risk_reward_ratio:
                return None
            
            return TradingOpportunity(
                symbol=market_data.symbol,
                entry_model="Model1_Direct_Entry",
                entry_price=entry_price,
                stop_loss=stop_loss,
                target=target,
                risk_reward_ratio=risk_reward_ratio,
                confluence_score=zone['confluence_score'],
                confirmations=zone['confirmations'],
                timeframe_analysis=self._create_timeframe_summary(market_data),
                chart_patterns={'liquidity_zone': zone, 'trade_direction': trade_direction},
                notes=f"Direct entry at {zone['type']} with {len(zone['confirmations'])} confirmations"
            )
            
        except Exception as e:
            logger.error(f"Error checking entry model 1: {e}")
            return None
    
    def _check_entry_model_2(self, market_data: MarketData, zone: Dict, 
                            current_price: float) -> Optional[TradingOpportunity]:
        """Check for Entry Model 2: Entry after trendline break + retest"""
        
        try:
            # Check if we have hourly data for trendline break detection
            hourly_data = market_data.get_hourly_data()
            if hourly_data is None:
                return None
            
            daily_data = market_data.get_daily_data()
            
            # Check if price is within reasonable distance of liquidity zone
            distance = abs(current_price - zone['price']) / current_price
            if distance > config.trading.model2_distance_tolerance:
                return None
            
            # Detect recent trendline breaks on hourly timeframe
            recent_trendlines = self.analyzer.detect_trendlines(hourly_data.tail(200))
            
            trendline_broken = False
            broken_trendline = None
            
            # Check for recent trendline breaks (last 5 candles)
            for tl in recent_trendlines:
                if self._is_trendline_recently_broken(hourly_data, tl):
                    trendline_broken = True
                    broken_trendline = tl
                    break
            
            if not trendline_broken:
                return None
            
            # Check if we're in a retest scenario
            if not self._is_retest_scenario(hourly_data, zone, broken_trendline):
                return None
            
            # Determine trade direction
            structure = zone['structure_context']
            if (structure['trend'] == 'bullish' and zone['type'] == 'support' and 
                broken_trendline['direction'] == 'bearish'):
                trade_direction = 'long'
            elif (structure['trend'] == 'bearish' and zone['type'] == 'resistance' and 
                  broken_trendline['direction'] == 'bullish'):
                trade_direction = 'short'
            else:
                return None
            
            # Calculate entry, stop loss, and target
            entry_price = zone['price']
            
            if trade_direction == 'long':
                target = self._find_next_resistance(daily_data, entry_price)
                stop_loss = self._calculate_stop_loss_long(daily_data, zone, entry_price)
            else:
                target = self._find_next_support(daily_data, entry_price)
                stop_loss = self._calculate_stop_loss_short(daily_data, zone, entry_price)
            
            if not target or not stop_loss:
                return None
            
            # Calculate risk-reward ratio
            if trade_direction == 'long':
                risk = entry_price - stop_loss
                reward = target - entry_price
            else:
                risk = stop_loss - entry_price
                reward = entry_price - target
            
            if risk <= 0 or reward <= 0:
                return None
            
            risk_reward_ratio = reward / risk
            
            if risk_reward_ratio < config.trading.min_risk_reward_ratio:
                return None
            
            # Add trendline break to confirmations
            confirmations = zone['confirmations'] + [f"Trendline_Break_{broken_trendline['type']}"]
            
            return TradingOpportunity(
                symbol=market_data.symbol,
                entry_model="Model2_Confirmation_Entry",
                entry_price=entry_price,
                stop_loss=stop_loss,
                target=target,
                risk_reward_ratio=risk_reward_ratio,
                confluence_score=zone['confluence_score'] + 1,  # Bonus for trendline break
                confirmations=confirmations,
                timeframe_analysis=self._create_timeframe_summary(market_data),
                chart_patterns={
                    'liquidity_zone': zone,
                    'broken_trendline': broken_trendline,
                    'trade_direction': trade_direction
                },
                notes=f"Entry after trendline break + retest with {len(confirmations)} confirmations"
            )
            
        except Exception as e:
            logger.error(f"Error checking entry model 2: {e}")
            return None
    
    def _find_next_resistance(self, data: pd.DataFrame, entry_price: float) -> Optional[float]:
        """Find next significant resistance level above entry price"""
        try:
            levels = self.analyzer.find_support_resistance_levels(data)
            
            resistance_levels = [
                level['level'] for level in levels 
                if level['type'] == 'resistance' and level['level'] > entry_price * 1.01
            ]
            
            if not resistance_levels:
                # Use a percentage-based target as fallback
                return entry_price * 1.05  # 5% target
            
            return min(resistance_levels)  # Closest resistance
        except Exception as e:
            logger.error(f"Error finding next resistance: {e}")
            return entry_price * 1.05
    
    def _find_next_support(self, data: pd.DataFrame, entry_price: float) -> Optional[float]:
        """Find next significant support level below entry price"""
        try:
            levels = self.analyzer.find_support_resistance_levels(data)
            
            support_levels = [
                level['level'] for level in levels 
                if level['type'] == 'support' and level['level'] < entry_price * 0.99
            ]
            
            if not support_levels:
                # Use a percentage-based target as fallback
                return entry_price * 0.95  # 5% target
            
            return max(support_levels)  # Closest support
        except Exception as e:
            logger.error(f"Error finding next support: {e}")
            return entry_price * 0.95
    
    def _calculate_stop_loss_long(self, data: pd.DataFrame, zone: Dict, 
                                 entry_price: float) -> Optional[float]:
        """Calculate stop loss for long position"""
        try:
            stop_candidates = []
            
            # Stop loss below the support zone
            stop_candidates.append(zone['price'] * 0.98)
            
            # Stop loss below relevant trendlines
            for tl in zone.get('trendlines', []):
                if tl['type'] == 'support':
                    stop_candidates.append(tl['current_level'] * 0.98)
            
            # Stop loss below recent swing low
            recent_data = data.tail(20)
            recent_low = recent_data['Low'].min()
            stop_candidates.append(recent_low * 0.99)
            
            if not stop_candidates:
                return entry_price * 0.95  # 5% stop loss as fallback
            
            # Use the highest stop loss (most conservative)
            return max(stop_candidates)
        except Exception as e:
            logger.error(f"Error calculating stop loss long: {e}")
            return entry_price * 0.95
    
    def _calculate_stop_loss_short(self, data: pd.DataFrame, zone: Dict, 
                                  entry_price: float) -> Optional[float]:
        """Calculate stop loss for short position"""
        try:
            stop_candidates = []
            
            # Stop loss above the resistance zone
            stop_candidates.append(zone['price'] * 1.02)
            
            # Stop loss above relevant trendlines
            for tl in zone.get('trendlines', []):
                if tl['type'] == 'resistance':
                    stop_candidates.append(tl['current_level'] * 1.02)
            
            # Stop loss above recent swing high
            recent_data = data.tail(20)
            recent_high = recent_data['High'].max()
            stop_candidates.append(recent_high * 1.01)
            
            if not stop_candidates:
                return entry_price * 1.05  # 5% stop loss as fallback
            
            # Use the lowest stop loss (most conservative)
            return min(stop_candidates)
        except Exception as e:
            logger.error(f"Error calculating stop loss short: {e}")
            return entry_price * 1.05
    
    def _is_trendline_recently_broken(self, data: pd.DataFrame, trendline: Dict, 
                                    lookback: int = 5) -> bool:
        """Check if trendline was broken in recent candles"""
        try:
            if len(data) < lookback:
                return False
            
            recent_data = data.tail(lookback)
            slope = trendline['slope']
            intercept = trendline['intercept']
            
            for i, (idx, row) in enumerate(recent_data.iterrows()):
                candle_idx = len(data) - lookback + i
                trendline_value = slope * candle_idx + intercept
                
                # Check for break based on trendline type
                if trendline['type'] == 'support':
                    if row['Low'] < trendline_value * 0.995:  # Broken below with 0.5% buffer
                        return True
                else:  # resistance
                    if row['High'] > trendline_value * 1.005:  # Broken above with 0.5% buffer
                        return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking trendline break: {e}")
            return False
    
    def _is_retest_scenario(self, data: pd.DataFrame, zone: Dict, 
                           broken_trendline: Dict) -> bool:
        """Check if current price action represents a retest"""
        try:
            current_price = data['Close'].iloc[-1]
            
            # Check if price is near the liquidity zone (retest)
            distance_from_zone = abs(current_price - zone['price']) / zone['price']
            
            # For retest, price should be within tolerance of the zone
            if distance_from_zone > config.trading.retest_distance_tolerance:
                return False
            
            # Check if there's rejection at the zone (wick formation)
            recent_candles = data.tail(3)
            
            for _, candle in recent_candles.iterrows():
                if zone['type'] == 'support':
                    # Look for hammer-like patterns (lower wick rejection)
                    body_size = abs(candle['Close'] - candle['Open'])
                    lower_wick = (candle['Open'] - candle['Low'] if candle['Close'] > candle['Open'] 
                                 else candle['Close'] - candle['Low'])
                    if lower_wick > body_size * 1.5:  # Lower wick is 1.5x body size
                        return True
                else:  # resistance
                    # Look for shooting star-like patterns (upper wick rejection)
                    body_size = abs(candle['Close'] - candle['Open'])
                    upper_wick = (candle['High'] - candle['Open'] if candle['Close'] < candle['Open'] 
                                 else candle['High'] - candle['Close'])
                    if upper_wick > body_size * 1.5:  # Upper wick is 1.5x body size
                        return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking retest scenario: {e}")
            return False
    
    def _create_timeframe_summary(self, market_data: MarketData) -> Dict[str, Any]:
        """Create summary of multi-timeframe analysis"""
        summary = {}
        
        try:
            for timeframe, tf_data in market_data.timeframes.items():
                if tf_data.is_valid:
                    trend = self.analyzer._detect_trend(tf_data.data)
                    structure = self.analyzer.identify_price_structure(tf_data.data)
                    
                    summary[timeframe] = {
                        'trend': trend,
                        'structure_quality': structure.get('structure_quality', 'unknown'),
                        'current_price': tf_data.current_price,
                        'volume_trend': self._get_volume_trend(tf_data.data)
                    }
        except Exception as e:
            logger.error(f"Error creating timeframe summary: {e}")
        
        return summary
    
    def _get_volume_trend(self, data: pd.DataFrame) -> str:
        """Determine volume trend"""
        try:
            if len(data) > 20:
                recent_avg = data['Volume'].tail(5).mean()
                longer_avg = data['Volume'].tail(20).mean()
                return 'increasing' if recent_avg > longer_avg else 'decreasing'
            return 'unknown'
        except Exception as e:
            logger.error(f"Error getting volume trend: {e}")
            return 'unknown'
