#!/usr/bin/env python3
"""
Main execution script for the Trading System
"""

import sys
import os
import argparse
from datetime import datetime

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading_system.system_manager import TradingSystemManager
from trading_system.utils.logger import setup_logging
from trading_system.config.settings import config

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Trading System - Stock Analysis and Opportunity Detection')
    parser.add_argument('--symbol', '-s', type=str, help='Analyze single stock symbol')
    parser.add_argument('--log-level', '-l', type=str, default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Set logging level')
    parser.add_argument('--screening-only', action='store_true', 
                       help='Run screening only without generating charts')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level)
    
    try:
        # Initialize trading system
        system = TradingSystemManager()
        
        if args.symbol:
            # Analyze single stock
            logger.info(f"Analyzing single stock: {args.symbol}")
            result = system.analyze_single_stock(args.symbol.upper())
            
            if 'error' in result:
                print(f"Error analyzing {args.symbol}: {result['error']}")
                return 1
            
            # Print results
            print(f"\n{'='*60}")
            print(f"ANALYSIS RESULTS FOR {result['symbol']}")
            print(f"{'='*60}")
            print(f"Current Price: ₹{result['current_price']:.2f}")
            print(f"Passes Pre-screening: {'Yes' if result['passes_filters'] else 'No'}")
            print(f"Price Structure: {result['price_structure'].get('trend', 'N/A')} trend, "
                  f"{result['price_structure'].get('structure_quality', 'N/A')} quality")
            print(f"Trendlines Found: {result['trendlines_count']}")
            print(f"Support/Resistance Levels: {result['support_resistance_levels']}")
            print(f"Liquidity Zones: {result['liquidity_zones_count']}")
            print(f"Trading Opportunities: {result['opportunities_count']}")
            
            if result['opportunities']:
                print(f"\nOPPORTUNITIES:")
                for i, opp in enumerate(result['opportunities'], 1):
                    print(f"{i}. {opp['entry_model']} - Entry: ₹{opp['entry_price']:.2f}, "
                          f"RR: {opp['risk_reward_ratio']:.2f}, Score: {opp['confluence_score']}")
            
            print(f"{'='*60}")
            
        else:
            # Run complete screening
            logger.info("Starting complete daily screening")
            
            if args.screening_only:
                # Run screening only
                opportunities = system.daily_screening()
                
                if opportunities:
                    # Generate text report only
                    report_file = system.report_generator.save_daily_report(opportunities)
                    summary_stats = system.report_generator.generate_summary_stats(opportunities)
                    
                    print(f"\nScreening complete. Found {len(opportunities)} opportunities.")
                    print(f"Report saved to: {report_file}")
                    print(f"Best opportunity: {summary_stats['best_opportunity']['symbol']} "
                          f"(Score: {summary_stats['best_opportunity']['confluence_score']})")
                else:
                    print("No opportunities found today.")
            else:
                # Run complete analysis with charts
                result = system.run_complete_analysis()
                
                if 'error' in result:
                    print(f"Error in analysis: {result['error']}")
                    return 1
        
        logger.info("Trading system execution completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
