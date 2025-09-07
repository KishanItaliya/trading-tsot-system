"""
Report generation utilities
"""

import os
from typing import List
from datetime import datetime
import json

from ..models.trading_opportunity import TradingOpportunity
from ..config.settings import config


class ReportGenerator:
    """Generate various reports for trading opportunities"""
    
    def __init__(self):
        # Ensure reports directory exists
        os.makedirs(config.trading.reports_dir, exist_ok=True)
    
    def generate_daily_report(self, opportunities: List[TradingOpportunity]) -> str:
        """Generate daily report for manual review"""
        report = f"""
DAILY TRADING OPPORTUNITIES REPORT
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Opportunities Found: {len(opportunities)}

{'='*80}

"""
        
        if not opportunities:
            report += "No trading opportunities found today.\n"
            return report
        
        for i, opp in enumerate(opportunities, 1):
            report += f"""
OPPORTUNITY #{i}
Symbol: {opp.symbol}
Entry Model: {opp.entry_model}
Entry Price: ₹{opp.entry_price:.2f}
Stop Loss: ₹{opp.stop_loss:.2f}
Target: ₹{opp.target:.2f}
Risk-Reward Ratio: {opp.risk_reward_ratio:.2f}
Risk Percentage: {opp.risk_percentage:.2f}%
Reward Percentage: {opp.reward_percentage:.2f}%
Confluence Score: {opp.confluence_score}
Confirmations: {', '.join(opp.confirmations)}
Notes: {opp.notes}

Timeframe Analysis:
"""
            for tf, analysis in opp.timeframe_analysis.items():
                report += f"  {tf.upper()}: Trend={analysis.get('trend', 'N/A')}, Quality={analysis.get('structure_quality', 'N/A')}\n"
            
            report += "\n" + "-"*80 + "\n"
        
        return report
    
    def save_daily_report(self, opportunities: List[TradingOpportunity]) -> str:
        """Save daily report to file and return filename"""
        report_content = self.generate_daily_report(opportunities)
        
        filename = f"daily_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        filepath = os.path.join(config.trading.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filepath
    
    def save_opportunities_json(self, opportunities: List[TradingOpportunity]) -> str:
        """Save opportunities as JSON for further processing"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'total_opportunities': len(opportunities),
            'opportunities': [opp.to_dict() for opp in opportunities]
        }
        
        filename = f"opportunities_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        filepath = os.path.join(config.trading.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def generate_summary_stats(self, opportunities: List[TradingOpportunity]) -> dict:
        """Generate summary statistics"""
        if not opportunities:
            return {"total": 0}
        
        model1_count = len([o for o in opportunities if "Model1" in o.entry_model])
        model2_count = len([o for o in opportunities if "Model2" in o.entry_model])
        
        avg_rr = sum(o.risk_reward_ratio for o in opportunities) / len(opportunities)
        avg_confluence = sum(o.confluence_score for o in opportunities) / len(opportunities)
        avg_risk = sum(o.risk_percentage for o in opportunities) / len(opportunities)
        avg_reward = sum(o.reward_percentage for o in opportunities) / len(opportunities)
        
        best_opportunity = max(opportunities, key=lambda x: x.confluence_score)
        
        return {
            "total": len(opportunities),
            "model1_count": model1_count,
            "model2_count": model2_count,
            "avg_risk_reward": round(avg_rr, 2),
            "avg_confluence": round(avg_confluence, 1),
            "avg_risk_percentage": round(avg_risk, 2),
            "avg_reward_percentage": round(avg_reward, 2),
            "best_opportunity": {
                "symbol": best_opportunity.symbol,
                "confluence_score": best_opportunity.confluence_score,
                "risk_reward_ratio": best_opportunity.risk_reward_ratio
            },
            "symbols": [o.symbol for o in opportunities]
        }
