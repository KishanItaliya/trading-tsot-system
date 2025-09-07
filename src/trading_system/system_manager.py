"""
Main system manager that coordinates all components
"""

import logging
from typing import List, Optional
from datetime import datetime
import yfinance as yf

from .data.market_data_fetcher import MarketDataFetcher
from .data.data_processor import DataProcessor
from .analysis.technical_analyzer import TechnicalAnalyzer
from .analysis.liquidity_detector import LiquidityDetector
from .analysis.entry_model_detector import EntryModelDetector
from .models.trading_opportunity import TradingOpportunity
from .utils.report_generator import ReportGenerator
from .utils.dashboard import TradingDashboard
from .config.settings import config

logger = logging.getLogger(__name__)


class TradingSystemManager:
    """Main system manager that coordinates all components"""
    
    def __init__(self):
        # Initialize components
        self.data_fetcher = MarketDataFetcher()
        self.data_processor = DataProcessor()
        self.analyzer = TechnicalAnalyzer()
        self.liquidity_detector = LiquidityDetector(self.analyzer)
        self.entry_detector = EntryModelDetector(self.analyzer, self.liquidity_detector)
        self.report_generator = ReportGenerator()
        self.dashboard = TradingDashboard()
        
        # Stock list
        self.nse_stocks = config.market.nse_stocks
        
        logger.info(f"Trading System Manager initialized with {len(self.nse_stocks)} stocks")
    
    def daily_screening(self, target_time: str = None) -> List[TradingOpportunity]:
        """Main daily screening function - run at specified time"""
        if target_time is None:
            target_time = config.market.screening_time
            
        logger.info(f"Starting daily screening at {datetime.now()}")
        all_opportunities = []
        
        for symbol in self.nse_stocks:
            try:
                logger.info(f"Analyzing {symbol}...")
                
                # Get multi-timeframe data
                market_data = self.data_fetcher.get_multi_timeframe_data(symbol)
                
                if not market_data or not market_data.is_valid:
                    logger.warning(f"No valid data available for {symbol}")
                    continue
                
                # Apply pre-screening filters
                daily_data = market_data.get_daily_data()
                if not self.data_processor.apply_pre_screening_filters(daily_data):
                    logger.debug(f"{symbol} failed pre-screening filters")
                    continue
                
                # Detect entry opportunities
                opportunities = self.entry_detector.detect_entry_models(market_data)
                
                for opp in opportunities:
                    # Additional validation
                    if self._validate_opportunity(opp, market_data):
                        all_opportunities.append(opp)
                        logger.info(f"Found opportunity: {symbol} - {opp.entry_model} - RR: {opp.risk_reward_ratio:.2f}")
                
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {e}")
                continue
        
        # Sort by confluence score and return top opportunities
        final_opportunities = sorted(
            all_opportunities, 
            key=lambda x: x.confluence_score, 
            reverse=True
        )
        
        max_opportunities = config.trading.max_opportunities
        final_opportunities = final_opportunities[:max_opportunities]
        
        logger.info(f"Screening complete. Found {len(final_opportunities)} opportunities.")
        return final_opportunities
    
    def _validate_opportunity(self, opportunity: TradingOpportunity, market_data) -> bool:
        """Final validation of trading opportunity"""
        try:
            # Risk management validation
            risk_pct = opportunity.risk_percentage
            if risk_pct > config.trading.max_risk_per_trade * 100:  # Convert to percentage
                logger.debug(f"{opportunity.symbol}: Risk {risk_pct:.2f}% exceeds maximum {config.trading.max_risk_per_trade * 100}%")
                return False
            
            # Market condition check
            if not self._check_market_conditions():
                logger.debug("Market conditions not favorable")
                return False
            
            # Structure quality check
            structure = opportunity.chart_patterns.get('liquidity_zone', {}).get('structure_context', {})
            if structure.get('structure_quality') == 'choppy':
                logger.debug(f"{opportunity.symbol}: Choppy structure quality")
                return False
            
            # Minimum confluence requirement
            if opportunity.confluence_score < config.analysis.min_confluence_score:
                logger.debug(f"{opportunity.symbol}: Confluence score {opportunity.confluence_score} below minimum {config.analysis.min_confluence_score}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating opportunity for {opportunity.symbol}: {e}")
            return False
    
    def _check_market_conditions(self) -> bool:
        """Check overall market conditions using Nifty"""
        try:
            nifty_data = self.data_fetcher.get_market_index_data("^NSEI")
            
            if nifty_data is None or len(nifty_data) < 10:
                logger.warning("Could not fetch Nifty data, allowing trades by default")
                return True  # Default to true if no data
            
            # Avoid trading in extreme volatility
            current_volatility = nifty_data['Close'].tail(10).pct_change().std()
            if current_volatility > config.trading.max_market_volatility:
                logger.warning(f"Market volatility {current_volatility:.4f} exceeds maximum {config.trading.max_market_volatility}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking market conditions: {e}")
            return True  # Default to allowing trades if market check fails
    
    def run_complete_analysis(self) -> dict:
        """Run complete analysis and generate all outputs"""
        try:
            logger.info("Starting complete trading system analysis")
            
            # Run screening
            opportunities = self.daily_screening()
            
            # Generate reports
            report_file = self.report_generator.save_daily_report(opportunities)
            json_file = self.report_generator.save_opportunities_json(opportunities)
            summary_stats = self.report_generator.generate_summary_stats(opportunities)
            
            # Generate charts
            chart_files = self.dashboard.save_opportunity_charts(opportunities)
            
            # Print summary to console
            if opportunities:
                print(f"\n{'='*60}")
                print(f"TRADING SYSTEM ANALYSIS COMPLETE")
                print(f"{'='*60}")
                print(f"Total Opportunities: {len(opportunities)}")
                print(f"Model 1 Opportunities: {summary_stats['model1_count']}")
                print(f"Model 2 Opportunities: {summary_stats['model2_count']}")
                print(f"Average Risk-Reward: {summary_stats['avg_risk_reward']}")
                print(f"Average Confluence Score: {summary_stats['avg_confluence']}")
                print(f"\nBest Opportunity: {summary_stats['best_opportunity']['symbol']} "
                      f"(Score: {summary_stats['best_opportunity']['confluence_score']})")
                print(f"\nFiles Generated:")
                print(f"- Report: {report_file}")
                print(f"- JSON Data: {json_file}")
                print(f"- Charts: {len(chart_files)} files")
                print(f"{'='*60}")
            else:
                print("\nNo trading opportunities found today.")
            
            return {
                'opportunities': opportunities,
                'summary_stats': summary_stats,
                'files': {
                    'report': report_file,
                    'json': json_file,
                    'charts': chart_files
                }
            }
            
        except Exception as e:
            logger.error(f"Error in complete analysis: {e}")
            return {
                'opportunities': [],
                'summary_stats': {'total': 0},
                'files': {'report': None, 'json': None, 'charts': []},
                'error': str(e)
            }
    
    def analyze_single_stock(self, symbol: str) -> dict:
        """Analyze a single stock in detail"""
        try:
            logger.info(f"Analyzing single stock: {symbol}")
            
            # Get market data
            market_data = self.data_fetcher.get_multi_timeframe_data(symbol)
            
            if not market_data or not market_data.is_valid:
                return {'error': f'No valid data available for {symbol}'}
            
            # Run analysis
            daily_data = market_data.get_daily_data()
            
            # Pre-screening
            passes_filters = self.data_processor.apply_pre_screening_filters(daily_data)
            
            # Technical analysis
            trendlines = self.analyzer.detect_trendlines(daily_data)
            levels = self.analyzer.find_support_resistance_levels(daily_data)
            fib_data = self.analyzer.calculate_fibonacci_levels(daily_data)
            structure = self.analyzer.identify_price_structure(daily_data)
            
            # Liquidity zones
            liquidity_zones = self.liquidity_detector.find_liquidity_zones(market_data)
            
            # Entry opportunities
            opportunities = self.entry_detector.detect_entry_models(market_data)
            
            return {
                'symbol': symbol,
                'current_price': market_data.current_price,
                'passes_filters': passes_filters,
                'trendlines_count': len(trendlines),
                'support_resistance_levels': len(levels),
                'fibonacci_data': fib_data,
                'price_structure': structure,
                'liquidity_zones_count': len(liquidity_zones),
                'opportunities_count': len(opportunities),
                'opportunities': [opp.to_dict() for opp in opportunities],
                'detailed_analysis': {
                    'trendlines': trendlines[:3],  # Top 3
                    'levels': levels[:5],  # Top 5
                    'liquidity_zones': liquidity_zones
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return {'error': str(e)}
