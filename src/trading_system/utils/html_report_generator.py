"""
HTML Report Generator for Trading System
Creates beautiful, user-friendly HTML reports
"""

import os
from datetime import datetime
from typing import List, Dict, Any
import logging

from ..models.trading_opportunity import TradingOpportunity
from ..config.settings import config

logger = logging.getLogger(__name__)


class HTMLReportGenerator:
    """Generates beautiful HTML reports for trading analysis"""
    
    def __init__(self):
        self.output_dir = config.trading.reports_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_stock_analysis_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a comprehensive HTML report for single stock analysis"""
        
        symbol = analysis_result['symbol']
        current_price = analysis_result['current_price']
        opportunities = analysis_result.get('opportunities', [])
        
        # Generate HTML content
        html_content = self._create_html_template()
        
        # Add stock header
        stock_header = self._create_stock_header(symbol, current_price, analysis_result)
        
        # Add analysis summary
        analysis_summary = self._create_analysis_summary(analysis_result)
        
        # Add opportunities section
        opportunities_section = self._create_opportunities_section(opportunities)
        
        # Add technical analysis details
        technical_details = self._create_technical_details(analysis_result)
        
        # Combine all sections
        html_content = html_content.replace('{{STOCK_HEADER}}', stock_header)
        html_content = html_content.replace('{{ANALYSIS_SUMMARY}}', analysis_summary)
        html_content = html_content.replace('{{OPPORTUNITIES_SECTION}}', opportunities_section)
        html_content = html_content.replace('{{TECHNICAL_DETAILS}}', technical_details)
        html_content = html_content.replace('{{SYMBOL}}', symbol)
        html_content = html_content.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Save to file
        filename = f"{symbol}_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {filepath}")
        return filepath
    
    def _create_html_template(self) -> str:
        """Create the base HTML template with CSS styling"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{SYMBOL}} - Trading Analysis Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #3498db;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
        }
        
        .section h2 .emoji {
            margin-right: 10px;
            font-size: 1.2em;
        }
        
        .price-display {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .price-display.negative {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-top: 4px solid #3498db;
        }
        
        .stat-card h3 {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .opportunities-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .opportunities-table th {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .opportunities-table td {
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .opportunities-table tr:hover {
            background: #f8f9fa;
        }
        
        .signal-badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        
        .signal-buy {
            background: #2ecc71;
            color: white;
        }
        
        .signal-sell {
            background: #e74c3c;
            color: white;
        }
        
        .signal-hold {
            background: #f39c12;
            color: white;
        }
        
        .score-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: bold;
            color: white;
        }
        
        .score-high { background: #27ae60; }
        .score-medium { background: #f39c12; }
        .score-low { background: #e74c3c; }
        
        .parameter-list {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .parameter-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .parameter-item:last-child {
            border-bottom: none;
        }
        
        .parameter-name {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .parameter-value {
            color: #7f8c8d;
            font-family: monospace;
        }
        
        .footer {
            background: #34495e;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        .no-opportunities {
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .opportunities-table {
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        {{STOCK_HEADER}}
        
        <div class="content">
            {{ANALYSIS_SUMMARY}}
            {{OPPORTUNITIES_SECTION}}
            {{TECHNICAL_DETAILS}}
        </div>
        
        <div class="footer">
            <p>Generated by Trading System • {{TIMESTAMP}} • Real-time data from Kite API</p>
        </div>
    </div>
</body>
</html>
        """
    
    def _create_stock_header(self, symbol: str, current_price: float, analysis: Dict) -> str:
        """Create the stock header section"""
        passes_screening = analysis.get('passes_filters', False)
        status_class = 'positive' if passes_screening else 'negative'
        status_text = '✅ Passes Screening' if passes_screening else '❌ Failed Screening'
        
        return f"""
        <div class="header">
            <h1>{symbol}</h1>
            <div class="subtitle">Stock Analysis Report</div>
            <div class="price-display {status_class}">
                Current Price: ₹{current_price:.2f}
                <br><small>{status_text}</small>
            </div>
        </div>
        """
    
    def _create_analysis_summary(self, analysis: Dict) -> str:
        """Create the analysis summary section"""
        structure = analysis.get('price_structure', {})
        trend = structure.get('trend', 'Unknown')
        quality = structure.get('structure_quality', 'Unknown')
        
        return f"""
        <div class="section">
            <h2><span class="emoji">📊</span>Analysis Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Price Trend</h3>
                    <div class="value">{trend.title()}</div>
                </div>
                <div class="stat-card">
                    <h3>Structure Quality</h3>
                    <div class="value">{quality.title()}</div>
                </div>
                <div class="stat-card">
                    <h3>Trendlines</h3>
                    <div class="value">{analysis.get('trendlines_count', 0)}</div>
                </div>
                <div class="stat-card">
                    <h3>S/R Levels</h3>
                    <div class="value">{analysis.get('support_resistance_levels', 0)}</div>
                </div>
                <div class="stat-card">
                    <h3>Liquidity Zones</h3>
                    <div class="value">{analysis.get('liquidity_zones_count', 0)}</div>
                </div>
                <div class="stat-card">
                    <h3>Opportunities</h3>
                    <div class="value">{analysis.get('opportunities_count', 0)}</div>
                </div>
            </div>
        </div>
        """
    
    def _create_opportunities_section(self, opportunities: List[TradingOpportunity]) -> str:
        """Create the trading opportunities section"""
        if not opportunities:
            return """
            <div class="section">
                <h2><span class="emoji">🎯</span>Trading Opportunities</h2>
                <div class="no-opportunities">
                    No trading opportunities found at current market conditions.
                </div>
            </div>
            """
        
        # Create table rows
        rows = ""
        for i, opp in enumerate(opportunities, 1):
            score_class = self._get_score_class(opp.confluence_score)
            signal_class = self._get_signal_class(opp.entry_model)
            
            # Format confirmations
            confirmations = ", ".join(opp.confirmations) if opp.confirmations else "None"
            
            rows += f"""
            <tr>
                <td>{i}</td>
                <td><span class="signal-badge {signal_class}">{opp.entry_model.replace('_', ' ').title()}</span></td>
                <td>₹{opp.entry_price:.2f}</td>
                <td>₹{opp.stop_loss:.2f}</td>
                <td>₹{opp.target:.2f}</td>
                <td>{opp.risk_reward_ratio:.2f}</td>
                <td>{opp.risk_percentage:.2f}%</td>
                <td>{opp.reward_percentage:.2f}%</td>
                <td><span class="score-badge {score_class}">{opp.confluence_score}</span></td>
                <td>{confirmations}</td>
                <td>{opp.notes}</td>
            </tr>
            """
        
        return f"""
        <div class="section">
            <h2><span class="emoji">🎯</span>Trading Opportunities</h2>
            <table class="opportunities-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Entry Model</th>
                        <th>Entry Price</th>
                        <th>Stop Loss</th>
                        <th>Target</th>
                        <th>Risk/Reward</th>
                        <th>Risk %</th>
                        <th>Reward %</th>
                        <th>Score</th>
                        <th>Confirmations</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _create_technical_details(self, analysis: Dict) -> str:
        """Create technical analysis details section"""
        fib_data = analysis.get('fibonacci_data', {})
        structure = analysis.get('price_structure', {})
        
        parameters = [
            ("Analysis Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ("Data Source", "Kite API (Real-time)"),
            ("Timeframes Analyzed", "Daily, Hourly, 15min, 5min, Weekly, 4H"),
            ("Fibonacci Swing High", f"₹{fib_data.get('swing_high', 0):.2f}"),
            ("Fibonacci Swing Low", f"₹{fib_data.get('swing_low', 0):.2f}"),
            ("Price Structure Trend", structure.get('trend', 'Unknown').title()),
            ("Structure Quality", structure.get('structure_quality', 'Unknown').title()),
            ("Higher Highs", str(structure.get('higher_highs', 0))),
            ("Higher Lows", str(structure.get('higher_lows', 0))),
            ("Lower Highs", str(structure.get('lower_highs', 0))),
            ("Lower Lows", str(structure.get('lower_lows', 0))),
        ]
        
        parameter_html = ""
        for name, value in parameters:
            parameter_html += f"""
            <div class="parameter-item">
                <span class="parameter-name">{name}</span>
                <span class="parameter-value">{value}</span>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2><span class="emoji">🔧</span>Technical Analysis Parameters</h2>
            <div class="parameter-list">
                {parameter_html}
            </div>
        </div>
        """
    
    def _get_score_class(self, score: int) -> str:
        """Get CSS class based on confluence score"""
        if score >= 35:
            return "score-high"
        elif score >= 25:
            return "score-medium"
        else:
            return "score-low"
    
    def _get_signal_class(self, entry_model: str) -> str:
        """Get CSS class based on entry model"""
        if "Direct" in entry_model:
            return "signal-buy"
        elif "Confirmation" in entry_model:
            return "signal-hold"
        else:
            return "signal-sell"
    
    def generate_batch_screening_report(self, opportunities: List[TradingOpportunity], 
                                       batch_info: Dict[str, Any] = None) -> str:
        """Generate or update HTML report for batch screening with incremental updates"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"batch_screening_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Check if this is an update to existing report
        if batch_info and batch_info.get('is_update', False):
            existing_file = batch_info.get('existing_file')
            if existing_file and os.path.exists(existing_file):
                return self._update_existing_report(existing_file, opportunities, batch_info)
        
        # Generate new report
        return self._generate_new_batch_report(opportunities, filepath, batch_info)
    
    def _generate_new_batch_report(self, opportunities: List[TradingOpportunity], 
                                  filepath: str, batch_info: Dict[str, Any] = None) -> str:
        """Generate a new batch screening report"""
        
        html_content = self._create_html_template()
        
        # Create header with batch information
        header_section = self._create_batch_header(opportunities, batch_info)
        
        # Create summary section
        summary_section = self._create_screening_summary(opportunities)
        
        # Create opportunities table
        opportunities_table = self._create_opportunities_table(opportunities)
        
        # Create stock-wise breakdown
        stock_breakdown = self._create_stock_breakdown(opportunities)
        
        # Replace placeholders
        html_content = html_content.replace('{{STOCK_HEADER}}', header_section)
        html_content = html_content.replace('{{ANALYSIS_SUMMARY}}', summary_section)
        html_content = html_content.replace('{{OPPORTUNITIES_SECTION}}', opportunities_table)
        html_content = html_content.replace('{{TECHNICAL_DETAILS}}', stock_breakdown)
        
        # Save the report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Batch screening HTML report generated: {filepath}")
        return filepath
    
    def _create_batch_header(self, opportunities: List[TradingOpportunity], 
                            batch_info: Dict[str, Any] = None) -> str:
        """Create header section for batch screening report"""
        
        total_stocks = batch_info.get('total_stocks', 'N/A') if batch_info else 'N/A'
        processed_stocks = batch_info.get('processed_stocks', 'N/A') if batch_info else 'N/A'
        batch_size = batch_info.get('batch_size', 'N/A') if batch_info else 'N/A'
        
        return f"""
        <div class="header-section">
            <h1>📊 Batch Trading Screening Report</h1>
            <div class="batch-info">
                <div class="info-card">
                    <h3>📈 Batch Information</h3>
                    <p><strong>Batch Size:</strong> {batch_size} stocks per batch</p>
                    <p><strong>Total Stocks:</strong> {total_stocks}</p>
                    <p><strong>Processed:</strong> {processed_stocks}</p>
                    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="info-card">
                    <h3>🎯 Results Summary</h3>
                    <p><strong>Opportunities Found:</strong> {len(opportunities)}</p>
                    <p><strong>Success Rate:</strong> {(len(opportunities)/max(processed_stocks, 1)*100):.1f}%</p>
                    <p><strong>Data Source:</strong> Kite API (Real-time)</p>
                </div>
            </div>
        </div>
        """

    def generate_daily_screening_report(self, opportunities: List[TradingOpportunity]) -> str:
        """Generate HTML report for daily screening results"""
        # Group opportunities by symbol
        by_symbol = {}
        for opp in opportunities:
            if opp.symbol not in by_symbol:
                by_symbol[opp.symbol] = []
            by_symbol[opp.symbol].append(opp)
        
        # Create summary table
        summary_rows = ""
        for symbol, opps in by_symbol.items():
            best_opp = max(opps, key=lambda x: x.confluence_score)
            score_class = self._get_score_class(best_opp.confluence_score)
            
            summary_rows += f"""
            <tr>
                <td><strong>{symbol}</strong></td>
                <td>₹{best_opp.entry_price:.2f}</td>
                <td>{len(opps)}</td>
                <td><span class="score-badge {score_class}">{best_opp.confluence_score}</span></td>
                <td>{best_opp.risk_reward_ratio:.2f}</td>
                <td>{best_opp.entry_model.replace('_', ' ').title()}</td>
            </tr>
            """
        
        html_content = self._create_html_template()
        
        header = f"""
        <div class="header">
            <h1>Daily Market Screening</h1>
            <div class="subtitle">NSE Trading Opportunities</div>
            <div class="price-display">
                Found {len(opportunities)} opportunities across {len(by_symbol)} stocks
            </div>
        </div>
        """
        
        summary_section = f"""
        <div class="section">
            <h2><span class="emoji">📈</span>Market Summary</h2>
            <table class="opportunities-table">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Best Entry Price</th>
                        <th>Opportunities</th>
                        <th>Best Score</th>
                        <th>Risk/Reward</th>
                        <th>Entry Model</th>
                    </tr>
                </thead>
                <tbody>
                    {summary_rows}
                </tbody>
            </table>
        </div>
        """
        
        # Add detailed opportunities
        detailed_section = self._create_opportunities_section(opportunities)
        
        # Technical parameters for screening
        tech_details = f"""
        <div class="section">
            <h2><span class="emoji">⚙️</span>Screening Parameters</h2>
            <div class="parameter-list">
                <div class="parameter-item">
                    <span class="parameter-name">Stocks Screened</span>
                    <span class="parameter-value">49 NSE Stocks</span>
                </div>
                <div class="parameter-item">
                    <span class="parameter-name">Minimum Risk/Reward</span>
                    <span class="parameter-value">2.0</span>
                </div>
                <div class="parameter-item">
                    <span class="parameter-name">Minimum Confluence Score</span>
                    <span class="parameter-value">25</span>
                </div>
                <div class="parameter-item">
                    <span class="parameter-name">Data Source</span>
                    <span class="parameter-value">Kite API (Real-time)</span>
                </div>
                <div class="parameter-item">
                    <span class="parameter-name">Analysis Time</span>
                    <span class="parameter-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
            </div>
        </div>
        """
        
        # Combine sections
        html_content = html_content.replace('{{STOCK_HEADER}}', header)
        html_content = html_content.replace('{{ANALYSIS_SUMMARY}}', summary_section)
        html_content = html_content.replace('{{OPPORTUNITIES_SECTION}}', detailed_section)
        html_content = html_content.replace('{{TECHNICAL_DETAILS}}', tech_details)
        html_content = html_content.replace('{{SYMBOL}}', 'Daily Screening')
        html_content = html_content.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Save to file
        filename = f"daily_screening_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Daily screening HTML report generated: {filepath}")
        return filepath
    
    def _create_screening_summary(self, opportunities: List[TradingOpportunity]) -> str:
        """Create screening summary section"""
        if not opportunities:
            return "<div class='analysis-summary'><p>No opportunities found.</p></div>"
        
        total_opportunities = len(opportunities)
        unique_stocks = len(set(opp.symbol for opp in opportunities))
        avg_score = sum(opp.confluence_score for opp in opportunities) / total_opportunities
        avg_rr = sum(opp.risk_reward_ratio for opp in opportunities) / total_opportunities
        
        # Count by entry model
        direct_entries = sum(1 for opp in opportunities if opp.entry_model == "Direct Entry")
        confirmation_entries = sum(1 for opp in opportunities if opp.entry_model == "Confirmation Entry")
        
        return f"""
        <div class="analysis-summary">
            <h2>📊 Market Overview</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <span class="summary-label">Total Opportunities:</span>
                    <span class="summary-value">{total_opportunities}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Unique Stocks:</span>
                    <span class="summary-value">{unique_stocks}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Average Score:</span>
                    <span class="summary-value">{avg_score:.1f}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Average R:R:</span>
                    <span class="summary-value">{avg_rr:.1f}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Direct Entries:</span>
                    <span class="summary-value">{direct_entries}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Confirmation Entries:</span>
                    <span class="summary-value">{confirmation_entries}</span>
                </div>
            </div>
        </div>
        """
    
    def _create_opportunities_table(self, opportunities: List[TradingOpportunity]) -> str:
        """Create opportunities table"""
        if not opportunities:
            return "<div class='opportunities-section'><p>No opportunities found.</p></div>"
        
        # Sort by confluence score
        sorted_opportunities = sorted(opportunities, key=lambda x: x.confluence_score, reverse=True)
        
        table_rows = ""
        for i, opp in enumerate(sorted_opportunities, 1):  # Show all opportunities
            entry_icon = "🚀" if opp.entry_model == "Direct Entry" else "⏳"
            
            table_rows += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{opp.symbol}</strong></td>
                <td>{entry_icon} {opp.entry_model}</td>
                <td>₹{opp.entry_price:.2f}</td>
                <td>₹{opp.stop_loss:.2f}</td>
                <td>₹{opp.target:.2f}</td>
                <td>{opp.risk_reward_ratio:.1f}</td>
                <td><span class="score-badge">{int(opp.confluence_score)}</span></td>
            </tr>
            """
        
        return f"""
        <div class="opportunities-section">
            <h2>🏆 Top Opportunities</h2>
            <table class="opportunities-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Symbol</th>
                        <th>Entry Model</th>
                        <th>Entry Price</th>
                        <th>Stop Loss</th>
                        <th>Target</th>
                        <th>R:R</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """
    
    def _create_stock_breakdown(self, opportunities: List[TradingOpportunity]) -> str:
        """Create stock-wise breakdown"""
        if not opportunities:
            return "<div class='technical-details'><p>No stock data available.</p></div>"
        
        # Group by symbol
        stock_groups = {}
        for opp in opportunities:
            if opp.symbol not in stock_groups:
                stock_groups[opp.symbol] = []
            stock_groups[opp.symbol].append(opp)
        
        breakdown_html = ""
        for symbol, stock_opps in sorted(stock_groups.items()):
            best_opp = max(stock_opps, key=lambda x: x.confluence_score)
            opp_count = len(stock_opps)
            
            breakdown_html += f"""
            <div class="stock-breakdown-item">
                <h3>📈 {symbol}</h3>
                <div class="breakdown-details">
                    <div class="breakdown-metric">
                        <span class="label">Opportunities:</span>
                        <span class="value">{opp_count}</span>
                    </div>
                    <div class="breakdown-metric">
                        <span class="label">Best Score:</span>
                        <span class="value">{int(best_opp.confluence_score)}</span>
                    </div>
                    <div class="breakdown-metric">
                        <span class="label">Best Entry:</span>
                        <span class="value">₹{best_opp.entry_price:.2f}</span>
                    </div>
                    <div class="breakdown-metric">
                        <span class="label">Best R:R:</span>
                        <span class="value">{best_opp.risk_reward_ratio:.1f}</span>
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="technical-details">
            <h2>📋 Stock-wise Breakdown</h2>
            <div class="stock-breakdown">
                {breakdown_html}
            </div>
        </div>
        """
    
    def generate_enhanced_batch_report(self, opportunities: List[TradingOpportunity], 
                                     batch_info: Dict[str, Any] = None) -> str:
        """Generate enhanced interactive HTML report with grouping and advanced features"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"enhanced_batch_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Group opportunities by symbol
        grouped_opportunities = {}
        for opp in opportunities:
            if opp.symbol not in grouped_opportunities:
                grouped_opportunities[opp.symbol] = []
            grouped_opportunities[opp.symbol].append(opp)
        
        # Sort groups by best score
        sorted_groups = sorted(grouped_opportunities.items(), 
                             key=lambda x: max(opp.confluence_score for opp in x[1]), 
                             reverse=True)
        
        html_content = self._create_enhanced_html_template()
        
        # Create header with batch information
        header_section = self._create_enhanced_header(opportunities, batch_info)
        
        # Create market overview
        overview_section = self._create_enhanced_overview(opportunities)
        
        # Create grouped opportunities table
        grouped_table = self._create_grouped_opportunities_table(sorted_groups)
        
        # Create detailed breakdown
        detailed_section = self._create_detailed_breakdown(sorted_groups)
        
        # Replace placeholders
        html_content = html_content.replace('{{HEADER}}', header_section)
        html_content = html_content.replace('{{OVERVIEW}}', overview_section)
        html_content = html_content.replace('{{GROUPED_TABLE}}', grouped_table)
        html_content = html_content.replace('{{DETAILED_SECTION}}', detailed_section)
        
        # Save the report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Enhanced batch screening HTML report generated: {filepath}")
        return filepath
    
    def _create_enhanced_html_template(self) -> str:
        """Create enhanced HTML template with interactive features"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Trading Screening Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .batch-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .info-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .overview-section {
            padding: 30px;
            background: #f8f9fa;
        }
        
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .metric-label {
            color: #666;
            margin-top: 5px;
        }
        
        .grouped-table {
            padding: 30px;
        }
        
        .stock-group {
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .stock-header {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s ease;
        }
        
        .stock-header:hover {
            background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
        }
        
        .stock-header.bearish {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }
        
        .stock-header.bearish:hover {
            background: linear-gradient(135deg, #c0392b 0%, #e74c3c 100%);
        }
        
        .stock-title {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .symbol {
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .direction-indicator {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .bullish {
            background: #27ae60;
            color: white;
        }
        
        .bearish {
            background: #e74c3c;
            color: white;
        }
        
        .stock-summary {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .summary-item {
            text-align: center;
        }
        
        .summary-label {
            font-size: 0.8em;
            opacity: 0.8;
        }
        
        .summary-value {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .expand-icon {
            font-size: 1.2em;
            transition: transform 0.3s ease;
        }
        
        .stock-details {
            display: none;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .stock-details.expanded {
            display: block;
        }
        
        .opportunities-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .opportunities-table th,
        .opportunities-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .opportunities-table th {
            background: #34495e;
            color: white;
            font-weight: 600;
        }
        
        .opportunities-table tr:hover {
            background: #f5f5f5;
        }
        
        .entry-model {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .direct-entry {
            background: #27ae60;
            color: white;
        }
        
        .confirmation-entry {
            background: #f39c12;
            color: white;
        }
        
        .score-badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            color: white;
        }
        
        .score-high {
            background: #27ae60;
        }
        
        .score-medium {
            background: #f39c12;
        }
        
        .score-low {
            background: #e74c3c;
        }
        
        .rr-badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
        }
        
        .rr-excellent {
            background: #27ae60;
            color: white;
        }
        
        .rr-good {
            background: #f39c12;
            color: white;
        }
        
        .rr-fair {
            background: #e67e22;
            color: white;
        }
        
        .rr-poor {
            background: #e74c3c;
            color: white;
        }
        
        .detailed-section {
            padding: 30px;
            background: #f8f9fa;
        }
        
        .analysis-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .confirmations {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        
        .confirmation-tag {
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
            }
            
            .batch-info,
            .overview-grid {
                grid-template-columns: 1fr;
            }
            
            .stock-summary {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        {{HEADER}}
        {{OVERVIEW}}
        {{GROUPED_TABLE}}
        {{DETAILED_SECTION}}
    </div>
    
    <script>
        // Toggle stock details
        function toggleStock(symbol) {
            const details = document.getElementById('details-' + symbol);
            const icon = document.getElementById('icon-' + symbol);
            
            if (details.classList.contains('expanded')) {
                details.classList.remove('expanded');
                icon.style.transform = 'rotate(0deg)';
            } else {
                details.classList.add('expanded');
                icon.style.transform = 'rotate(180deg)';
            }
        }
        
        // Initialize tooltips and interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Add click handlers to stock headers
            document.querySelectorAll('.stock-header').forEach(header => {
                header.addEventListener('click', function() {
                    const symbol = this.dataset.symbol;
                    toggleStock(symbol);
                });
            });
            
            // Add hover effects to metric cards
            document.querySelectorAll('.metric-card').forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.boxShadow = '0 5px 20px rgba(0,0,0,0.15)';
                });
                
                card.addEventListener('mouseleave', function() {
                    this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
                });
            });
        });
    </script>
</body>
</html>
        """
    
    def _create_enhanced_header(self, opportunities: List[TradingOpportunity], 
                              batch_info: Dict[str, Any] = None) -> str:
        """Create enhanced header with batch information"""
        
        total_opportunities = len(opportunities)
        unique_stocks = len(set(opp.symbol for opp in opportunities))
        
        if batch_info:
            batch_size = batch_info.get('batch_size', 'N/A')
            total_stocks = batch_info.get('total_stocks', 'N/A')
            processed_stocks = batch_info.get('processed_stocks', 'N/A')
        else:
            batch_size = total_stocks = processed_stocks = 'N/A'
        
        return f"""
        <div class="header">
            <h1>🚀 Enhanced Trading Screening Report</h1>
            <p>Advanced Interactive Analysis Dashboard</p>
            
            <div class="batch-info">
                <div class="info-card">
                    <h3>📊 Batch Information</h3>
                    <p><strong>Batch Size:</strong> {batch_size} stocks</p>
                    <p><strong>Total Stocks:</strong> {total_stocks}</p>
                    <p><strong>Processed:</strong> {processed_stocks}</p>
                    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="info-card">
                    <h3>🎯 Results Summary</h3>
                    <p><strong>Opportunities:</strong> {total_opportunities}</p>
                    <p><strong>Unique Stocks:</strong> {unique_stocks}</p>
                    <p><strong>Success Rate:</strong> {(unique_stocks/max(int(processed_stocks) if processed_stocks != 'N/A' else 1, 1)*100):.1f}%</p>
                    <p><strong>Data Source:</strong> Kite API (Real-time)</p>
                </div>
            </div>
        </div>
        """
    
    def _create_enhanced_overview(self, opportunities: List[TradingOpportunity]) -> str:
        """Create enhanced market overview with metrics"""
        
        if not opportunities:
            return "<div class='overview-section'><h2>No opportunities found</h2></div>"
        
        total_opportunities = len(opportunities)
        unique_stocks = len(set(opp.symbol for opp in opportunities))
        avg_score = sum(opp.confluence_score for opp in opportunities) / total_opportunities
        
        # Calculate correct R:R ratio
        avg_rr = sum(self._calculate_rr_ratio(opp) for opp in opportunities) / total_opportunities
        
        # Count by entry model and direction
        direct_entries = sum(1 for opp in opportunities if "Direct" in opp.entry_model)
        confirmation_entries = sum(1 for opp in opportunities if "Confirmation" in opp.entry_model)
        
        bullish_count = sum(1 for opp in opportunities if self._is_bullish_entry(opp))
        bearish_count = total_opportunities - bullish_count
        
        best_opp = max(opportunities, key=lambda x: x.confluence_score)
        
        return f"""
        <div class="overview-section">
            <h2>📊 Market Overview</h2>
            
            <div class="overview-grid">
                <div class="metric-card">
                    <div class="metric-value">{total_opportunities}</div>
                    <div class="metric-label">Total Opportunities</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{unique_stocks}</div>
                    <div class="metric-label">Unique Stocks</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{avg_score:.1f}</div>
                    <div class="metric-label">Average Score</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{avg_rr:.1f}</div>
                    <div class="metric-label">Average R:R</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{bullish_count}</div>
                    <div class="metric-label">Bullish Setups</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{bearish_count}</div>
                    <div class="metric-label">Bearish Setups</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{direct_entries}</div>
                    <div class="metric-label">Direct Entries</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{confirmation_entries}</div>
                    <div class="metric-label">Confirmation Entries</div>
                </div>
            </div>
        </div>
        """
    
    def _calculate_rr_ratio(self, opp: TradingOpportunity) -> float:
        """Calculate correct Risk:Reward ratio"""
        risk = abs(opp.entry_price - opp.stop_loss)
        reward = abs(opp.target - opp.entry_price)
        return reward / risk if risk > 0 else 0
    
    def _is_bullish_entry(self, opp: TradingOpportunity) -> bool:
        """Determine if entry is bullish based on target vs entry price"""
        return opp.target > opp.entry_price
    
    def _get_direction_indicator(self, opp: TradingOpportunity) -> str:
        """Get direction indicator HTML"""
        if self._is_bullish_entry(opp):
            return '<span class="direction-indicator bullish">📈 BULLISH</span>'
        else:
            return '<span class="direction-indicator bearish">📉 BEARISH</span>'
    
    def _get_rr_class(self, rr_ratio: float) -> str:
        """Get CSS class for R:R ratio"""
        if rr_ratio >= 3:
            return 'rr-excellent'
        elif rr_ratio >= 2:
            return 'rr-good'
        elif rr_ratio >= 1:
            return 'rr-fair'
        else:
            return 'rr-poor'
    
    def _create_grouped_opportunities_table(self, sorted_groups: List[tuple]) -> str:
        """Create grouped opportunities table with expandable details"""
        
        if not sorted_groups:
            return "<div class='grouped-table'><h2>No opportunities found</h2></div>"
        
        groups_html = ""
        
        for symbol, opps in sorted_groups:
            best_opp = max(opps, key=lambda x: x.confluence_score)
            best_rr = max(self._calculate_rr_ratio(opp) for opp in opps)
            
            # Determine if majority are bullish or bearish
            bullish_count = sum(1 for opp in opps if self._is_bullish_entry(opp))
            is_majority_bullish = bullish_count > len(opps) / 2
            
            header_class = "stock-header"
            if not is_majority_bullish:
                header_class += " bearish"
            
            direction_indicator = self._get_direction_indicator(best_opp)
            
            groups_html += f"""
            <div class="stock-group">
                <div class="{header_class}" data-symbol="{symbol}">
                    <div class="stock-title">
                        <span class="symbol">{symbol}</span>
                        {direction_indicator}
                    </div>
                    
                    <div class="stock-summary">
                        <div class="summary-item">
                            <div class="summary-label">Opportunities</div>
                            <div class="summary-value">{len(opps)}</div>
                        </div>
                        
                        <div class="summary-item">
                            <div class="summary-label">Best Score</div>
                            <div class="summary-value">{int(best_opp.confluence_score)}</div>
                        </div>
                        
                        <div class="summary-item">
                            <div class="summary-label">Best R:R</div>
                            <div class="summary-value">{best_rr:.1f}</div>
                        </div>
                        
                        <div class="summary-item">
                            <div class="summary-label">Entry Price</div>
                            <div class="summary-value">₹{best_opp.entry_price:.2f}</div>
                        </div>
                        
                        <div class="expand-icon" id="icon-{symbol}">▼</div>
                    </div>
                </div>
                
                <div class="stock-details" id="details-{symbol}">
                    {self._create_opportunities_detail_table(opps)}
                </div>
            </div>
            """
        
        return f"""
        <div class="grouped-table">
            <h2>🎯 Trading Opportunities by Stock</h2>
            <p>Click on any stock to view detailed opportunities</p>
            {groups_html}
        </div>
        """
    
    def _create_opportunities_detail_table(self, opportunities: List[TradingOpportunity]) -> str:
        """Create detailed table for opportunities of a single stock"""
        
        table_rows = ""
        for i, opp in enumerate(opportunities, 1):
            rr_ratio = self._calculate_rr_ratio(opp)
            rr_class = self._get_rr_class(rr_ratio)
            
            entry_model_class = "direct-entry" if "Direct" in opp.entry_model else "confirmation-entry"
            entry_model_text = opp.entry_model.replace("_", " ").title()
            
            score_class = self._get_score_class(opp.confluence_score)
            direction = "📈" if self._is_bullish_entry(opp) else "📉"
            
            confirmations_html = ""
            if opp.confirmations:
                confirmations_html = "<div class='confirmations'>"
                for conf in opp.confirmations[:5]:  # Show max 5 confirmations
                    confirmations_html += f"<span class='confirmation-tag'>{conf}</span>"
                confirmations_html += "</div>"
            
            table_rows += f"""
            <tr>
                <td>{i}</td>
                <td>{direction}</td>
                <td><span class="entry-model {entry_model_class}">{entry_model_text}</span></td>
                <td>₹{opp.entry_price:.2f}</td>
                <td>₹{opp.stop_loss:.2f}</td>
                <td>₹{opp.target:.2f}</td>
                <td><span class="rr-badge {rr_class}">{rr_ratio:.1f}</span></td>
                <td><span class="score-badge {score_class}">{int(opp.confluence_score)}</span></td>
                <td>{confirmations_html}</td>
            </tr>
            """
        
        return f"""
        <table class="opportunities-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Direction</th>
                    <th>Entry Model</th>
                    <th>Entry Price</th>
                    <th>Stop Loss</th>
                    <th>Target</th>
                    <th>R:R Ratio</th>
                    <th>Score</th>
                    <th>Confirmations</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """
    
    def _create_detailed_breakdown(self, sorted_groups: List[tuple]) -> str:
        """Create detailed analysis breakdown"""
        
        if not sorted_groups:
            return "<div class='detailed-section'><h2>No detailed analysis available</h2></div>"
        
        analysis_cards = ""
        
        for symbol, opps in sorted_groups[:10]:  # Show top 10 stocks
            best_opp = max(opps, key=lambda x: x.confluence_score)
            avg_score = sum(opp.confluence_score for opp in opps) / len(opps)
            avg_rr = sum(self._calculate_rr_ratio(opp) for opp in opps) / len(opps)
            
            bullish_count = sum(1 for opp in opps if self._is_bullish_entry(opp))
            bearish_count = len(opps) - bullish_count
            
            # Get unique confirmations
            all_confirmations = set()
            for opp in opps:
                all_confirmations.update(opp.confirmations)
            
            confirmations_html = ""
            for conf in list(all_confirmations)[:8]:  # Show max 8 unique confirmations
                confirmations_html += f"<span class='confirmation-tag'>{conf}</span>"
            
            analysis_cards += f"""
            <div class="analysis-card">
                <h3>📊 {symbol} - Detailed Analysis</h3>
                
                <div class="overview-grid" style="margin-top: 15px;">
                    <div class="metric-card" style="margin: 0;">
                        <div class="metric-value">{len(opps)}</div>
                        <div class="metric-label">Total Opportunities</div>
                    </div>
                    
                    <div class="metric-card" style="margin: 0;">
                        <div class="metric-value">{avg_score:.1f}</div>
                        <div class="metric-label">Average Score</div>
                    </div>
                    
                    <div class="metric-card" style="margin: 0;">
                        <div class="metric-value">{avg_rr:.1f}</div>
                        <div class="metric-label">Average R:R</div>
                    </div>
                    
                    <div class="metric-card" style="margin: 0;">
                        <div class="metric-value">{bullish_count}/{bearish_count}</div>
                        <div class="metric-label">Bullish/Bearish</div>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px; margin-bottom: 10px;">🎯 Key Confirmations:</h4>
                <div class="confirmations">
                    {confirmations_html}
                </div>
                
                <h4 style="margin-top: 20px; margin-bottom: 10px;">📈 Best Opportunity:</h4>
                <p><strong>Entry Model:</strong> {best_opp.entry_model.replace('_', ' ').title()}</p>
                <p><strong>Entry Price:</strong> ₹{best_opp.entry_price:.2f}</p>
                <p><strong>Target:</strong> ₹{best_opp.target:.2f}</p>
                <p><strong>Stop Loss:</strong> ₹{best_opp.stop_loss:.2f}</p>
                <p><strong>R:R Ratio:</strong> {self._calculate_rr_ratio(best_opp):.1f}</p>
                <p><strong>Score:</strong> {int(best_opp.confluence_score)}</p>
                
                {f'<p style="margin-top: 10px;"><strong>Notes:</strong> {best_opp.notes}</p>' if best_opp.notes else ''}
            </div>
            """
        
        return f"""
        <div class="detailed-section">
            <h2>📋 Detailed Stock Analysis</h2>
            <p>Comprehensive breakdown of top performing stocks</p>
            {analysis_cards}
        </div>
        """
