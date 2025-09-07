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
from trading_system.utils.html_report_generator import HTMLReportGenerator
from trading_system.utils.console_formatter import ConsoleFormatter
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
    parser.add_argument('--batch-size', '-b', type=int, default=20,
                       help='Number of stocks to process in each batch (default: 20)')
    parser.add_argument('--max-stocks', '-m', type=int, default=None,
                       help='Maximum number of stocks to analyze (default: all stocks)')
    parser.add_argument('--start-from', type=int, default=0,
                       help='Start analysis from stock index (default: 0)')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level)
    
    try:
        # Initialize trading system
        system = TradingSystemManager()
        html_generator = HTMLReportGenerator()
        console_formatter = ConsoleFormatter()
        
        if args.symbol:
            # Analyze single stock
            logger.info(f"Analyzing single stock: {args.symbol}")
            result = system.analyze_single_stock(args.symbol.upper())
            
            if 'error' in result:
                print(console_formatter.format_error_message(f"Analysis failed: {result['error']}"))
                return 1
            
            # Display beautiful console results
            print(console_formatter.format_single_stock_analysis(result))
            
            # Generate HTML report
            print(console_formatter.format_info_message("Generating detailed HTML report..."))
            html_report_path = html_generator.generate_stock_analysis_report(result)
            print(console_formatter.format_success_message(f"HTML Report saved: {html_report_path}"))
            print(console_formatter.format_info_message("Open the HTML file in your browser for a beautiful, detailed report!"))
            
        else:
            # Run complete screening
            logger.info("Starting complete daily screening")
            
            if args.screening_only:
                # Run batch screening
                all_opportunities = system.batch_screening(
                    batch_size=args.batch_size,
                    max_stocks=args.max_stocks,
                    start_from=args.start_from
                )
                
                if all_opportunities:
                    # Display beautiful console summary
                    print(console_formatter.format_screening_summary(all_opportunities))
                    
                    # Generate text report
                    report_file = system.report_generator.save_daily_report(all_opportunities)
                    
                    # Generate HTML report with batch information
                    print(console_formatter.format_info_message("Generating beautiful HTML report..."))
                    
                    # Prepare batch info for HTML report
                    batch_info = {
                        'batch_size': args.batch_size,
                        'max_stocks': args.max_stocks or len(system.nse_stocks),
                        'total_stocks': min(args.max_stocks or len(system.nse_stocks), len(system.nse_stocks) - args.start_from),
                        'processed_stocks': min(args.max_stocks or len(system.nse_stocks), len(system.nse_stocks) - args.start_from),
                        'start_from': args.start_from
                    }
                    
                    html_report_path = html_generator.generate_enhanced_batch_report(all_opportunities, batch_info)
                    print(console_formatter.format_success_message(f"HTML Report saved: {html_report_path}"))
                    print(console_formatter.format_success_message(f"Text Report saved: {report_file}"))
                else:
                    print(console_formatter.format_error_message("No opportunities found in current market conditions."))
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
