"""
Core technical analysis functionality
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

from ..config.settings import config

logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Core technical analysis engine following the playbook exactly"""
    
    def __init__(self):
        self.fib_levels = config.analysis.fib_levels
    
    def detect_trendlines(self, data: pd.DataFrame, min_touches: int = None) -> List[Dict]:
        """Detect trendlines using wick-based approach as per playbook"""
        if min_touches is None:
            min_touches = config.analysis.min_trendline_touches
            
        trendlines = []
        
        if len(data) < 20:
            return trendlines
        
        try:
            # Find potential pivot points (highs and lows)
            highs = self._find_pivot_points(data['High'].values, order=3, pivot_type='high')
            lows = self._find_pivot_points(data['Low'].values, order=3, pivot_type='low')
            
            # Create trendlines from highs (resistance/bearish)
            high_points = [(i, data.iloc[i]['High']) for i in highs if i < len(data)]
            trendlines.extend(self._create_trendlines(high_points, data, 'resistance'))
            
            # Create trendlines from lows (support/bullish)  
            low_points = [(i, data.iloc[i]['Low']) for i in lows if i < len(data)]
            trendlines.extend(self._create_trendlines(low_points, data, 'support'))
            
            # Filter trendlines by minimum touches and validity
            valid_trendlines = []
            for tl in trendlines:
                touches = self._count_trendline_touches(data, tl)
                if touches >= min_touches:
                    tl['touches'] = touches
                    tl['strength'] = min(touches / 5.0, 1.0)  # Normalize strength
                    valid_trendlines.append(tl)
            
            return sorted(valid_trendlines, key=lambda x: x['strength'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error detecting trendlines: {e}")
            return []
    
    def _find_pivot_points(self, data: np.array, order: int = 3, pivot_type: str = 'high') -> List[int]:
        """Find pivot highs and lows"""
        pivots = []
        
        try:
            for i in range(order, len(data) - order):
                if pivot_type == 'high':
                    if all(data[i] >= data[i-j] for j in range(1, order+1)) and \
                       all(data[i] >= data[i+j] for j in range(1, order+1)):
                        pivots.append(i)
                else:  # low
                    if all(data[i] <= data[i-j] for j in range(1, order+1)) and \
                       all(data[i] <= data[i+j] for j in range(1, order+1)):
                        pivots.append(i)
        except Exception as e:
            logger.error(f"Error finding pivot points: {e}")
        
        return pivots
    
    def _create_trendlines(self, points: List[Tuple], data: pd.DataFrame, line_type: str) -> List[Dict]:
        """Create trendlines from pivot points"""
        trendlines = []
        
        try:
            for i in range(len(points)):
                for j in range(i+1, len(points)):
                    point1 = points[i]
                    point2 = points[j]
                    
                    # Calculate slope and intercept
                    x1, y1 = point1[0], point1[1]
                    x2, y2 = point2[0], point2[1]
                    
                    if x2 != x1:  # Avoid division by zero
                        slope = (y2 - y1) / (x2 - x1)
                        intercept = y1 - slope * x1
                        
                        # Extend line to current data
                        current_x = len(data) - 1
                        current_y = slope * current_x + intercept
                        
                        # Calculate age in days (handle timezone-naive datetime)
                        try:
                            start_date = data.index[x1]
                            if hasattr(start_date, 'tz') and start_date.tz is not None:
                                start_date = start_date.tz_localize(None)
                            age_days = (datetime.now() - start_date).days
                        except Exception:
                            age_days = 0
                        
                        trendline = {
                            'type': line_type,
                            'slope': slope,
                            'intercept': intercept,
                            'start_point': point1,
                            'end_point': point2,
                            'current_level': current_y,
                            'start_date': data.index[x1],
                            'end_date': data.index[x2],
                            'age_days': age_days,
                            'direction': 'bullish' if slope > 0 else 'bearish'
                        }
                        
                        trendlines.append(trendline)
        except Exception as e:
            logger.error(f"Error creating trendlines: {e}")
        
        return trendlines
    
    def _count_trendline_touches(self, data: pd.DataFrame, trendline: Dict, 
                                tolerance: float = None) -> int:
        """Count how many times price touched the trendline"""
        if tolerance is None:
            tolerance = config.analysis.trendline_tolerance
            
        touches = 0
        slope = trendline['slope']
        intercept = trendline['intercept']
        
        try:
            for i in range(len(data)):
                line_value = slope * i + intercept
                high_val = data.iloc[i]['High']
                low_val = data.iloc[i]['Low']
                
                # Check if price touched the line within tolerance
                high_diff = abs(high_val - line_value) / line_value
                low_diff = abs(low_val - line_value) / line_value
                
                if min(high_diff, low_diff) <= tolerance:
                    touches += 1
        except Exception as e:
            logger.error(f"Error counting trendline touches: {e}")
        
        return touches
    
    def find_support_resistance_levels(self, data: pd.DataFrame, 
                                     lookback: int = None) -> List[Dict]:
        """Find support and resistance levels using multiple methods"""
        if lookback is None:
            lookback = config.analysis.sr_lookback_period
            
        levels = []
        
        if len(data) < lookback:
            return levels
        
        try:
            # Method 1: Pivot-based levels
            levels.extend(self._find_pivot_levels(data, lookback))
            
            # Method 2: Volume-based levels
            levels.extend(self._find_volume_levels(data, lookback))
            
            # Method 3: Psychological levels (round numbers)
            levels.extend(self._find_psychological_levels(data))
            
            # Method 4: Previous high/low levels
            levels.extend(self._find_historical_levels(data, lookback))
            
            # Remove duplicates and sort by strength
            levels = self._consolidate_levels(levels)
            
        except Exception as e:
            logger.error(f"Error finding support/resistance levels: {e}")
        
        return levels
    
    def _find_pivot_levels(self, data: pd.DataFrame, lookback: int) -> List[Dict]:
        """Find levels based on pivot points"""
        levels = []
        
        try:
            recent_data = data.tail(lookback)
            
            # Find pivot highs and lows
            highs = self._find_pivot_points(recent_data['High'].values, order=2, pivot_type='high')
            lows = self._find_pivot_points(recent_data['Low'].values, order=2, pivot_type='low')
            
            # Convert to levels
            for high_idx in highs:
                if high_idx < len(recent_data):
                    level = {
                        'level': recent_data.iloc[high_idx]['High'],
                        'type': 'resistance',
                        'strength': 1,
                        'touches': 1,
                        'date': recent_data.index[high_idx],
                        'source': 'pivot_high'
                    }
                    levels.append(level)
            
            for low_idx in lows:
                if low_idx < len(recent_data):
                    level = {
                        'level': recent_data.iloc[low_idx]['Low'],
                        'type': 'support',
                        'strength': 1,
                        'touches': 1,
                        'date': recent_data.index[low_idx],
                        'source': 'pivot_low'
                    }
                    levels.append(level)
        except Exception as e:
            logger.error(f"Error finding pivot levels: {e}")
        
        return levels
    
    def _find_volume_levels(self, data: pd.DataFrame, lookback: int) -> List[Dict]:
        """Find levels where high volume occurred"""
        levels = []
        
        try:
            recent_data = data.tail(lookback)
            
            # Find high volume periods
            volume_threshold = recent_data['Volume'].quantile(0.8)
            high_vol_data = recent_data[recent_data['Volume'] > volume_threshold]
            
            for idx, row in high_vol_data.iterrows():
                # Create levels at high and low of high volume candles
                levels.extend([
                    {
                        'level': row['High'],
                        'type': 'resistance',
                        'strength': 1,
                        'touches': 1,
                        'date': idx,
                        'source': 'high_volume'
                    },
                    {
                        'level': row['Low'],
                        'type': 'support', 
                        'strength': 1,
                        'touches': 1,
                        'date': idx,
                        'source': 'high_volume'
                    }
                ])
        except Exception as e:
            logger.error(f"Error finding volume levels: {e}")
        
        return levels
    
    def _find_psychological_levels(self, data: pd.DataFrame) -> List[Dict]:
        """Find round number levels"""
        levels = []
        
        try:
            current_price = data['Close'].iloc[-1]
            
            # Find nearest round numbers
            price_range = [current_price * 0.8, current_price * 1.2]
            
            for base in [10, 50, 100, 500, 1000]:
                for multiplier in range(1, 100):
                    level_price = base * multiplier
                    if price_range[0] <= level_price <= price_range[1]:
                        level_type = 'resistance' if level_price > current_price else 'support'
                        levels.append({
                            'level': level_price,
                            'type': level_type,
                            'strength': 1,
                            'touches': 1,
                            'date': data.index[-1],
                            'source': 'psychological'
                        })
        except Exception as e:
            logger.error(f"Error finding psychological levels: {e}")
        
        return levels
    
    def _find_historical_levels(self, data: pd.DataFrame, lookback: int) -> List[Dict]:
        """Find significant historical levels"""
        levels = []
        
        try:
            # All-time high and low
            ath = data['High'].max()
            atl = data['Low'].min()
            
            levels.extend([
                {
                    'level': ath,
                    'type': 'resistance',
                    'strength': 3,
                    'touches': 1,
                    'date': data[data['High'] == ath].index[0],
                    'source': 'all_time_high'
                },
                {
                    'level': atl,
                    'type': 'support',
                    'strength': 3,
                    'touches': 1,
                    'date': data[data['Low'] == atl].index[0],
                    'source': 'all_time_low'
                }
            ])
            
            # Recent highs and lows (52 week)
            recent_data = data.tail(252)  # Approximately 1 year
            if len(recent_data) > 0:
                recent_high = recent_data['High'].max()
                recent_low = recent_data['Low'].min()
                
                levels.extend([
                    {
                        'level': recent_high,
                        'type': 'resistance',
                        'strength': 2,
                        'touches': 1,
                        'date': recent_data[recent_data['High'] == recent_high].index[0],
                        'source': '52week_high'
                    },
                    {
                        'level': recent_low,
                        'type': 'support',
                        'strength': 2,
                        'touches': 1,
                        'date': recent_data[recent_data['Low'] == recent_low].index[0],
                        'source': '52week_low'
                    }
                ])
        except Exception as e:
            logger.error(f"Error finding historical levels: {e}")
        
        return levels
    
    def _consolidate_levels(self, levels: List[Dict], tolerance: float = None) -> List[Dict]:
        """Consolidate similar levels and count touches"""
        if tolerance is None:
            tolerance = config.analysis.sr_consolidation_tolerance
            
        if not levels:
            return []
        
        try:
            consolidated = []
            sorted_levels = sorted(levels, key=lambda x: x['level'])
            
            for level in sorted_levels:
                # Check if this level is close to any existing consolidated level
                merged = False
                for cons_level in consolidated:
                    if abs(level['level'] - cons_level['level']) / cons_level['level'] <= tolerance:
                        # Merge levels
                        cons_level['touches'] += level['touches']
                        cons_level['strength'] += level['strength']
                        cons_level['sources'] = cons_level.get('sources', [cons_level['source']]) + [level['source']]
                        merged = True
                        break
                
                if not merged:
                    level['sources'] = [level['source']]
                    consolidated.append(level)
            
            # Sort by strength
            return sorted(consolidated, key=lambda x: x['strength'] * x['touches'], reverse=True)
        except Exception as e:
            logger.error(f"Error consolidating levels: {e}")
            return levels
    
    def calculate_fibonacci_levels(self, data: pd.DataFrame, trend_type: str = 'auto') -> Dict:
        """Calculate Fibonacci retracement levels"""
        if len(data) < 20:
            return {}
        
        try:
            # Auto-detect trend or use specified
            if trend_type == 'auto':
                trend_type = self._detect_trend(data)
            
            if trend_type == 'bullish':
                # Find swing low to swing high
                swing_low_idx = data['Low'].tail(50).idxmin()
                swing_high_idx = data['High'][swing_low_idx:].idxmax()
                swing_low = data.loc[swing_low_idx, 'Low']
                swing_high = data.loc[swing_high_idx, 'High']
            else:
                # Find swing high to swing low  
                swing_high_idx = data['High'].tail(50).idxmax()
                swing_low_idx = data['Low'][swing_high_idx:].idxmin()
                swing_high = data.loc[swing_high_idx, 'High']
                swing_low = data.loc[swing_low_idx, 'Low']
            
            # Calculate Fibonacci levels
            diff = swing_high - swing_low
            fib_levels = {}
            
            for level in self.fib_levels:
                if trend_type == 'bullish':
                    fib_price = swing_high - (diff * level)
                else:
                    fib_price = swing_low + (diff * level)
                
                fib_levels[f'fib_{level*100:.1f}'] = {
                    'level': fib_price,
                    'percentage': level,
                    'type': 'retracement'
                }
            
            return {
                'trend_type': trend_type,
                'swing_high': swing_high,
                'swing_low': swing_low,
                'swing_high_date': swing_high_idx,
                'swing_low_date': swing_low_idx,
                'levels': fib_levels
            }
        except Exception as e:
            logger.error(f"Error calculating Fibonacci levels: {e}")
            return {}
    
    def _detect_trend(self, data: pd.DataFrame, period: int = 20) -> str:
        """Detect current trend direction"""
        if len(data) < period:
            return 'sideways'
        
        try:
            recent_data = data.tail(period)
            
            # Check if price is making higher highs and higher lows
            highs = recent_data['High'].values
            lows = recent_data['Low'].values
            
            # Linear regression on highs and lows
            x = np.arange(len(highs))
            
            high_slope = np.polyfit(x, highs, 1)[0]
            low_slope = np.polyfit(x, lows, 1)[0]
            
            if high_slope > 0 and low_slope > 0:
                return 'bullish'
            elif high_slope < 0 and low_slope < 0:
                return 'bearish'
            else:
                return 'sideways'
        except Exception as e:
            logger.error(f"Error detecting trend: {e}")
            return 'sideways'
    
    def identify_price_structure(self, data: pd.DataFrame) -> Dict:
        """Identify price structure as per playbook"""
        if len(data) < 20:
            return {}
        
        try:
            structure = {
                'trend': self._detect_trend(data),
                'swing_points': self._identify_swing_points(data),
                'pullbacks': self._identify_pullbacks(data),
                'structure_quality': 'clean'  # clean, choppy, complex
            }
            
            # Analyze structure quality
            swing_points = structure['swing_points']
            if len(swing_points['highs']) < 2 or len(swing_points['lows']) < 2:
                structure['structure_quality'] = 'insufficient_data'
            else:
                # Check for choppy behavior
                recent_volatility = data['High'].tail(20).std() / data['Close'].tail(20).mean()
                if recent_volatility > config.analysis.structure_volatility_threshold:
                    structure['structure_quality'] = 'choppy'
            
            return structure
        except Exception as e:
            logger.error(f"Error identifying price structure: {e}")
            return {'structure_quality': 'error'}
    
    def _identify_swing_points(self, data: pd.DataFrame) -> Dict:
        """Identify swing highs and lows"""
        swing_highs = []
        swing_lows = []
        
        try:
            order = config.analysis.swing_point_order
            high_pivots = self._find_pivot_points(data['High'].values, order=order, pivot_type='high')
            low_pivots = self._find_pivot_points(data['Low'].values, order=order, pivot_type='low')
            
            for idx in high_pivots:
                if idx < len(data):
                    swing_highs.append({
                        'index': idx,
                        'date': data.index[idx],
                        'price': data.iloc[idx]['High']
                    })
            
            for idx in low_pivots:
                if idx < len(data):
                    swing_lows.append({
                        'index': idx,
                        'date': data.index[idx], 
                        'price': data.iloc[idx]['Low']
                    })
        except Exception as e:
            logger.error(f"Error identifying swing points: {e}")
        
        return {
            'highs': swing_highs,
            'lows': swing_lows
        }
    
    def _identify_pullbacks(self, data: pd.DataFrame) -> List[Dict]:
        """Identify pullback patterns"""
        pullbacks = []
        
        try:
            swing_points = self._identify_swing_points(data)
            
            # Combine and sort all swing points
            all_swings = []
            for high in swing_points['highs']:
                all_swings.append({**high, 'type': 'high'})
            for low in swing_points['lows']:
                all_swings.append({**low, 'type': 'low'})
            
            all_swings.sort(key=lambda x: x['index'])
            
            # Identify pullback sequences
            for i in range(len(all_swings) - 2):
                swing1 = all_swings[i]
                swing2 = all_swings[i + 1]
                swing3 = all_swings[i + 2]
                
                # Bullish pullback: High -> Low -> Higher High
                if (swing1['type'] == 'high' and swing2['type'] == 'low' and 
                    swing3['type'] == 'high' and swing3['price'] > swing1['price']):
                    pullbacks.append({
                        'type': 'bullish',
                        'start': swing1,
                        'pullback_low': swing2,
                        'continuation': swing3,
                        'pullback_percentage': (swing1['price'] - swing2['price']) / swing1['price']
                    })
                
                # Bearish pullback: Low -> High -> Lower Low
                elif (swing1['type'] == 'low' and swing2['type'] == 'high' and 
                      swing3['type'] == 'low' and swing3['price'] < swing1['price']):
                    pullbacks.append({
                        'type': 'bearish',
                        'start': swing1,
                        'pullback_high': swing2,
                        'continuation': swing3,
                        'pullback_percentage': (swing2['price'] - swing1['price']) / swing1['price']
                    })
        except Exception as e:
            logger.error(f"Error identifying pullbacks: {e}")
        
        return pullbacks
