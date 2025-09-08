"""
Console Formatter for Trading System
Creates beautiful, user-friendly console output
"""

from typing import List, Dict, Any
from datetime import datetime

from ..models.trading_opportunity import TradingOpportunity


class ConsoleFormatter:
    """Formats trading analysis output for beautiful console display"""
    
    @staticmethod
    def format_single_stock_analysis(analysis_result: Dict[str, Any]) -> str:
        """Format single stock analysis for console display"""
        
        symbol = analysis_result['symbol']
        current_price = analysis_result['current_price']
        passes_filters = analysis_result.get('passes_filters', False)
        opportunities = analysis_result.get('opportunities', [])
        
        # Header
        output = []
        output.append("=" * 80)
        output.append(f"📊 TRADING ANALYSIS REPORT - {symbol}")
        output.append("=" * 80)
        
        # Current price and status
        status_emoji = "✅" if passes_filters else "❌"
        status_text = "PASSES SCREENING" if passes_filters else "FAILED SCREENING"
        
        output.append(f"💰 Current Price: ₹{current_price:.2f}")
        output.append(f"{status_emoji} Status: {status_text}")
        output.append("")
        
        # Market structure
        structure = analysis_result.get('price_structure', {})
        trend = structure.get('trend', 'Unknown').title()
        quality = structure.get('structure_quality', 'Unknown').title()
        
        output.append("📈 MARKET STRUCTURE")
        output.append("-" * 40)
        output.append(f"   Trend Direction: {trend}")
        output.append(f"   Structure Quality: {quality}")
        output.append("")
        
        # Technical analysis summary
        output.append("🔍 TECHNICAL ANALYSIS SUMMARY")
        output.append("-" * 40)
        output.append(f"   📈 Trendlines Found: {analysis_result.get('trendlines_count', 0)}")
        output.append(f"   📊 Support/Resistance Levels: {analysis_result.get('support_resistance_levels', 0)}")
        output.append(f"   💧 Liquidity Zones: {analysis_result.get('liquidity_zones_count', 0)}")
        output.append(f"   🎯 Trading Opportunities: {analysis_result.get('opportunities_count', 0)}")
        output.append("")
        
        # Trading opportunities
        if opportunities:
            output.append("🎯 TRADING OPPORTUNITIES")
            output.append("-" * 40)
            
            for i, opp in enumerate(opportunities, 1):
                # Entry model emoji
                model_emoji = "🚀" if "Direct" in opp.entry_model else "⏳"
                
                # Score color coding
                if opp.confluence_score >= 35:
                    score_indicator = "🟢 HIGH"
                elif opp.confluence_score >= 25:
                    score_indicator = "🟡 MEDIUM"
                else:
                    score_indicator = "🔴 LOW"
                
                output.append(f"   {i}. {model_emoji} {opp.entry_model.replace('_', ' ').title()}")
                output.append(f"      💵 Entry Price: ₹{opp.entry_price:.2f}")
                output.append(f"      🛑 Stop Loss: ₹{opp.stop_loss:.2f}")
                output.append(f"      🎯 Target: ₹{opp.target:.2f}")
                output.append(f"      ⚖️  Risk/Reward: {opp.risk_reward_ratio:.2f}")
                output.append(f"      📊 Confluence Score: {opp.confluence_score} ({score_indicator})")
                
                if opp.confirmations:
                    confirmations = ", ".join(opp.confirmations)
                    output.append(f"      ✅ Confirmations: {confirmations}")
                
                if opp.notes:
                    output.append(f"      📝 Notes: {opp.notes}")
                
                output.append("")
        else:
            output.append("🎯 TRADING OPPORTUNITIES")
            output.append("-" * 40)
            output.append("   No trading opportunities found at current market conditions.")
            output.append("")
        
        # Fibonacci levels
        fib_data = analysis_result.get('fibonacci_data', {})
        if fib_data:
            output.append("🔢 FIBONACCI ANALYSIS")
            output.append("-" * 40)
            output.append(f"   Swing High: ₹{fib_data.get('swing_high', 0):.2f}")
            output.append(f"   Swing Low: ₹{fib_data.get('swing_low', 0):.2f}")
            
            levels = fib_data.get('levels', {})
            if levels:
                output.append("   Key Levels:")
                for level_name, level_value in levels.items():
                    if isinstance(level_value, (int, float)):
                        output.append(f"     {level_name}: ₹{level_value:.2f}")
            output.append("")
        
        # Footer
        output.append("=" * 80)
        output.append(f"📅 Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"📡 Data source: Kite API (Real-time)")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def format_screening_summary(opportunities: List[TradingOpportunity]) -> str:
        """Format daily screening summary for console display"""
        
        output = []
        output.append("=" * 80)
        output.append("📈 DAILY MARKET SCREENING RESULTS")
        output.append("=" * 80)
        
        if not opportunities:
            output.append("❌ No trading opportunities found in current market conditions.")
            output.append("💡 Try again later or adjust screening parameters.")
            output.append("=" * 80)
            return "\n".join(output)
        
        # Group by symbol
        by_symbol = {}
        for opp in opportunities:
            if opp.symbol not in by_symbol:
                by_symbol[opp.symbol] = []
            by_symbol[opp.symbol].append(opp)
        
        # Summary stats
        total_stocks = len(by_symbol)
        total_opportunities = len(opportunities)
        best_opp = max(opportunities, key=lambda x: x.confluence_score)
        
        output.append(f"📊 MARKET OVERVIEW")
        output.append("-" * 40)
        output.append(f"   🏢 Stocks with Opportunities: {total_stocks}")
        output.append(f"   🎯 Total Opportunities: {total_opportunities}")
        output.append(f"   ⭐ Best Score: {int(best_opp.confluence_score)} ({best_opp.symbol})")
        output.append(f"   📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        # Top opportunities
        output.append("🏆 TOP OPPORTUNITIES")
        output.append("-" * 40)
        
        # Sort opportunities by score
        sorted_opps = sorted(opportunities, key=lambda x: x.confluence_score, reverse=True)
        
        for i, opp in enumerate(sorted_opps, 1):  # Show all opportunities
            # Score indicator
            if opp.confluence_score >= 35:
                score_indicator = "🟢"
            elif opp.confluence_score >= 25:
                score_indicator = "🟡"
            else:
                score_indicator = "🔴"
            
            # Entry model emoji
            model_emoji = "🚀" if "Direct" in opp.entry_model else "⏳"
            
            output.append(f"   {i:2d}. {score_indicator} {opp.symbol:<12} "
                         f"{model_emoji} Entry: ₹{opp.entry_price:>8.2f} "
                         f"RR: {opp.risk_reward_ratio:>5.2f} "
                         f"Score: {int(opp.confluence_score):>2d}")
        
        output.append("")
        
        # Stock-wise summary
        output.append("📋 STOCK-WISE SUMMARY")
        output.append("-" * 40)
        
        for symbol in sorted(by_symbol.keys()):
            opps = by_symbol[symbol]
            best_stock_opp = max(opps, key=lambda x: x.confluence_score)
            
            output.append(f"   📈 {symbol:<12} "
                         f"Opportunities: {int(len(opps)):>2d} "
                         f"Best Score: {int(best_stock_opp.confluence_score):>2d} "
                         f"Entry: ₹{best_stock_opp.entry_price:>8.2f}")
        
        output.append("")
        output.append("=" * 80)
        output.append("💡 Open the HTML report for detailed analysis and charts!")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def format_progress_message(message: str, step: int = None, total_steps: int = None) -> str:
        """Format progress messages for console display"""
        
        if step and total_steps:
            progress = f"[{step}/{total_steps}] "
        else:
            progress = ""
        
        return f"🔄 {progress}{message}"
    
    @staticmethod
    def format_success_message(message: str) -> str:
        """Format success messages for console display"""
        return f"✅ {message}"
    
    @staticmethod
    def format_error_message(message: str) -> str:
        """Format error messages for console display"""
        return f"❌ {message}"
    
    @staticmethod
    def format_info_message(message: str) -> str:
        """Format info messages for console display"""
        return f"💡 {message}"
