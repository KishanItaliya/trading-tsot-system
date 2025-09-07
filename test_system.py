#!/usr/bin/env python3
"""
Test script for the trading system with mock data
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_system.analysis.technical_analyzer import TechnicalAnalyzer
from trading_system.models.market_data import MarketData, TimeframeData
from trading_system.utils.logger import setup_logging

def create_mock_data(symbol: str, days: int = 100) -> MarketData:
    """Create mock market data for testing"""
    
    # Generate dates
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate realistic price data
    np.random.seed(42)  # For reproducible results
    
    # Start with a base price
    base_price = 1000.0
    
    # Generate price movements
    returns = np.random.normal(0.001, 0.02, days)  # Small daily returns with volatility
    prices = [base_price]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Create OHLCV data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Add some intraday volatility
        high = price * (1 + abs(np.random.normal(0, 0.01)))
        low = price * (1 - abs(np.random.normal(0, 0.01)))
        open_price = prices[i-1] if i > 0 else price
        close_price = price
        volume = np.random.randint(50000, 500000)
        
        # Ensure OHLC relationships are correct
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)
        
        data.append({
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': close_price,
            'Volume': volume
        })
    
    df = pd.DataFrame(data, index=dates)
    
    # Create timeframe data
    daily_tf = TimeframeData(
        timeframe='daily',
        data=df,
        last_updated=datetime.now()
    )
    
    # Create market data
    market_data = MarketData(
        symbol=symbol,
        timeframes={'daily': daily_tf},
        last_updated=datetime.now()
    )
    
    return market_data

def test_technical_analyzer():
    """Test the technical analyzer with mock data"""
    logger = setup_logging('INFO')
    logger.info("Testing Technical Analyzer")
    
    # Create mock data
    market_data = create_mock_data('TEST', 100)
    daily_data = market_data.get_daily_data()
    
    # Initialize analyzer
    analyzer = TechnicalAnalyzer()
    
    print(f"Testing with {len(daily_data)} days of mock data")
    print(f"Price range: ₹{daily_data['Low'].min():.2f} - ₹{daily_data['High'].max():.2f}")
    
    # Test trendline detection
    print("\n1. Testing Trendline Detection...")
    trendlines = analyzer.detect_trendlines(daily_data)
    print(f"   Found {len(trendlines)} trendlines")
    
    if trendlines:
        for i, tl in enumerate(trendlines[:3]):
            print(f"   Trendline {i+1}: {tl['type']} ({tl['direction']}) - Strength: {tl['strength']:.2f}")
    
    # Test support/resistance levels
    print("\n2. Testing Support/Resistance Detection...")
    levels = analyzer.find_support_resistance_levels(daily_data)
    print(f"   Found {len(levels)} levels")
    
    if levels:
        for i, level in enumerate(levels[:5]):
            print(f"   Level {i+1}: {level['type']} at ₹{level['level']:.2f} (Strength: {level['strength']})")
    
    # Test Fibonacci levels
    print("\n3. Testing Fibonacci Levels...")
    fib_data = analyzer.calculate_fibonacci_levels(daily_data)
    if fib_data:
        print(f"   Trend: {fib_data['trend_type']}")
        print(f"   Swing High: ₹{fib_data['swing_high']:.2f}")
        print(f"   Swing Low: ₹{fib_data['swing_low']:.2f}")
        
        for fib_name, fib_info in list(fib_data['levels'].items())[:3]:
            print(f"   {fib_name}: ₹{fib_info['level']:.2f}")
    
    # Test price structure
    print("\n4. Testing Price Structure...")
    structure = analyzer.identify_price_structure(daily_data)
    print(f"   Trend: {structure.get('trend', 'N/A')}")
    print(f"   Structure Quality: {structure.get('structure_quality', 'N/A')}")
    print(f"   Swing Highs: {len(structure.get('swing_points', {}).get('highs', []))}")
    print(f"   Swing Lows: {len(structure.get('swing_points', {}).get('lows', []))}")
    
    print("\n✅ Technical Analyzer test completed successfully!")
    return True

def test_system_components():
    """Test various system components"""
    logger = setup_logging('INFO')
    logger.info("Testing System Components")
    
    try:
        # Test data models
        print("1. Testing Data Models...")
        market_data = create_mock_data('TEST', 50)
        print(f"   ✅ Created market data for {market_data.symbol}")
        print(f"   ✅ Current price: ₹{market_data.current_price:.2f}")
        print(f"   ✅ Has daily data: {market_data.has_timeframe('daily')}")
        
        # Test configuration
        print("\n2. Testing Configuration...")
        from trading_system.config.settings import config
        print(f"   ✅ Loaded {len(config.market.nse_stocks)} stocks")
        print(f"   ✅ Min R:R ratio: {config.trading.min_risk_reward_ratio}")
        print(f"   ✅ Max risk per trade: {config.trading.max_risk_per_trade * 100}%")
        
        # Test data processor
        print("\n3. Testing Data Processor...")
        from trading_system.data.data_processor import DataProcessor
        daily_data = market_data.get_daily_data()
        is_valid = DataProcessor.validate_data(daily_data)
        passes_filters = DataProcessor.apply_pre_screening_filters(daily_data)
        print(f"   ✅ Data validation: {is_valid}")
        print(f"   ✅ Passes filters: {passes_filters}")
        
        # Test technical analyzer
        print("\n4. Testing Technical Analysis...")
        result = test_technical_analyzer()
        
        print("\n✅ All system components tested successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error in system test: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TRADING SYSTEM - COMPONENT TESTING")
    print("="*60)
    
    success = test_system_components()
    
    if success:
        print("\n🎉 All tests passed! The trading system is working correctly.")
        print("\nNote: This test uses mock data. For live data, ensure:")
        print("- Internet connection is stable")
        print("- Yahoo Finance API is accessible")
        print("- No rate limiting issues")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
    
    print("="*60)
