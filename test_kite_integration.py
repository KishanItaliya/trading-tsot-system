#!/usr/bin/env python3
"""
Test script for Kite API integration
"""

import sys
import os
from datetime import datetime

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_system.data.kite_data_fetcher import KiteDataFetcher
from trading_system.data.market_data_fetcher import MarketDataFetcher
from trading_system.config.settings import config
from trading_system.utils.logger import setup_logging

def test_kite_configuration():
    """Test Kite API configuration"""
    print("="*60)
    print("KITE API CONFIGURATION TEST")
    print("="*60)
    
    print(f"API Key: {'✅ Set' if config.kite.api_key else '❌ Not Set'}")
    print(f"API Secret: {'✅ Set' if config.kite.api_secret else '❌ Not Set'}")
    print(f"Access Token: {'✅ Set' if config.kite.access_token else '❌ Not Set'}")
    print(f"Is Configured: {'✅ Yes' if config.kite.is_configured() else '❌ No'}")
    print(f"Use Kite Primary: {'✅ Yes' if config.kite.use_kite_primary else '❌ No'}")
    print(f"Fallback to Yahoo: {'✅ Yes' if config.kite.fallback_to_yahoo else '❌ No'}")
    
    return config.kite.is_configured()

def test_kite_connection():
    """Test Kite API connection"""
    print("\n" + "="*60)
    print("KITE API CONNECTION TEST")
    print("="*60)
    
    try:
        kite_fetcher = KiteDataFetcher()
        
        if not kite_fetcher.kite:
            print("❌ Kite API not initialized")
            return False
        
        print("✅ Kite API initialized successfully")
        
        # Test market status
        market_status = kite_fetcher.get_market_status()
        print(f"Market Status: {market_status}")
        
        # Test instrument loading
        instrument_count = len(kite_fetcher.instruments)
        print(f"Instruments Loaded: {instrument_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Kite API connection failed: {e}")
        return False

def test_current_price(symbol: str = "INFY"):
    """Test current price fetching"""
    print(f"\n" + "="*60)
    print(f"CURRENT PRICE TEST - {symbol}")
    print("="*60)
    
    try:
        kite_fetcher = KiteDataFetcher()
        
        if not kite_fetcher.kite:
            print("❌ Kite API not available")
            return None
        
        # Get current price
        current_price = kite_fetcher.get_current_price(symbol)
        
        if current_price:
            print(f"✅ {symbol} Current Price: ₹{current_price}")
            return current_price
        else:
            print(f"❌ Could not fetch current price for {symbol}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching current price: {e}")
        return None

def test_historical_data(symbol: str = "INFY"):
    """Test historical data fetching"""
    print(f"\n" + "="*60)
    print(f"HISTORICAL DATA TEST - {symbol}")
    print("="*60)
    
    try:
        kite_fetcher = KiteDataFetcher()
        
        if not kite_fetcher.kite:
            print("❌ Kite API not available")
            return False
        
        # Test multi-timeframe data
        market_data = kite_fetcher.get_multi_timeframe_data(symbol)
        
        if market_data and market_data.is_valid:
            print(f"✅ Multi-timeframe data fetched successfully")
            print(f"   Current Price: ₹{market_data.current_price}")
            print(f"   Timeframes Available:")
            
            for tf_name, tf_data in market_data.timeframes.items():
                print(f"     {tf_name}: {len(tf_data.data)} records")
            
            return True
        else:
            print(f"❌ Could not fetch historical data for {symbol}")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching historical data: {e}")
        return False

def test_integrated_system(symbol: str = "INFY"):
    """Test the integrated system with Kite API"""
    print(f"\n" + "="*60)
    print(f"INTEGRATED SYSTEM TEST - {symbol}")
    print("="*60)
    
    try:
        # Use the main MarketDataFetcher which should use Kite API
        fetcher = MarketDataFetcher()
        
        print(f"Fetching data for {symbol} using integrated system...")
        market_data = fetcher.get_multi_timeframe_data(symbol)
        
        if market_data and market_data.is_valid:
            print(f"✅ Integrated system working successfully")
            print(f"   Symbol: {market_data.symbol}")
            print(f"   Current Price: ₹{market_data.current_price}")
            print(f"   Last Updated: {market_data.last_updated}")
            print(f"   Timeframes: {list(market_data.timeframes.keys())}")
            
            # Show sample data
            daily_data = market_data.get_daily_data()
            if daily_data is not None and len(daily_data) > 0:
                latest = daily_data.tail(1).iloc[0]
                print(f"   Latest Daily Data:")
                print(f"     Date: {daily_data.index[-1]}")
                print(f"     Open: ₹{latest['Open']:.2f}")
                print(f"     High: ₹{latest['High']:.2f}")
                print(f"     Low: ₹{latest['Low']:.2f}")
                print(f"     Close: ₹{latest['Close']:.2f}")
                print(f"     Volume: {latest['Volume']:,}")
            
            return True
        else:
            print(f"❌ Integrated system failed for {symbol}")
            return False
            
    except Exception as e:
        print(f"❌ Error in integrated system test: {e}")
        return False

def main():
    """Main test function"""
    # Setup logging
    logger = setup_logging('INFO')
    
    print("KITE API INTEGRATION TESTING")
    print("="*60)
    print(f"Test Time: {datetime.now()}")
    print()
    
    # Test configuration
    config_ok = test_kite_configuration()
    
    if not config_ok:
        print("\n❌ KITE API NOT CONFIGURED")
        print("Please set up your Kite API credentials:")
        print("1. Copy 'kite_credentials_template.txt' to 'kite_credentials.txt'")
        print("2. Fill in your actual API credentials")
        print("3. Or set environment variables: KITE_API_KEY, KITE_ACCESS_TOKEN")
        return False
    
    # Test connection
    connection_ok = test_kite_connection()
    
    if not connection_ok:
        print("\n❌ KITE API CONNECTION FAILED")
        print("Please check your credentials and network connection")
        return False
    
    # Test current price
    symbol = "INFY"
    current_price = test_current_price(symbol)
    
    # Test historical data
    historical_ok = test_historical_data(symbol)
    
    # Test integrated system
    integrated_ok = test_integrated_system(symbol)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Configuration: {'✅ Pass' if config_ok else '❌ Fail'}")
    print(f"Connection: {'✅ Pass' if connection_ok else '❌ Fail'}")
    print(f"Current Price: {'✅ Pass' if current_price else '❌ Fail'}")
    print(f"Historical Data: {'✅ Pass' if historical_ok else '❌ Fail'}")
    print(f"Integrated System: {'✅ Pass' if integrated_ok else '❌ Fail'}")
    
    if current_price:
        print(f"\n🎯 REAL {symbol} PRICE: ₹{current_price}")
        print("This is the actual current market price from Kite API!")
    
    all_tests_passed = all([config_ok, connection_ok, current_price, historical_ok, integrated_ok])
    
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED! Kite API integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and try again.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
