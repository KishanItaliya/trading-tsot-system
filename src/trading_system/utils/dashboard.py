"""
Dashboard and visualization components
"""

import os
from typing import List
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta

from ..models.trading_opportunity import TradingOpportunity
from ..data.market_data_fetcher import MarketDataFetcher
from ..config.settings import config


class TradingDashboard:
    """Create interactive dashboard for manual review"""
    
    def __init__(self):
        self.data_fetcher = MarketDataFetcher()
        # Ensure charts directory exists
        os.makedirs(config.trading.charts_dir, exist_ok=True)
    
    def create_opportunity_chart(self, opportunity: TradingOpportunity) -> go.Figure:
        """Create detailed chart for each opportunity"""
        try:
            symbol = opportunity.symbol
            
            # Get data
            market_data = self.data_fetcher.get_multi_timeframe_data(symbol)
            if not market_data or not market_data.has_timeframe('daily'):
                return go.Figure()
            
            daily_data = market_data.get_daily_data()
            
            # Create candlestick chart
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                subplot_titles=(f'{symbol} - {opportunity.entry_model}', 'Volume'),
                row_heights=[0.7, 0.3]
            )
            
            # Add candlestick
            fig.add_trace(go.Candlestick(
                x=daily_data.index,
                open=daily_data['Open'],
                high=daily_data['High'],
                low=daily_data['Low'],
                close=daily_data['Close'],
                name='Price'
            ), row=1, col=1)
            
            # Add volume
            fig.add_trace(go.Bar(
                x=daily_data.index,
                y=daily_data['Volume'],
                name='Volume',
                marker_color='lightblue',
                opacity=0.7
            ), row=2, col=1)
            
            # Add entry, stop loss, and target lines
            # Entry line
            fig.add_hline(
                y=opportunity.entry_price,
                line=dict(color="blue", width=2, dash="dash"),
                annotation_text=f"Entry: ₹{opportunity.entry_price:.2f}",
                row=1, col=1
            )
            
            # Stop loss line
            fig.add_hline(
                y=opportunity.stop_loss,
                line=dict(color="red", width=2, dash="dash"),
                annotation_text=f"Stop Loss: ₹{opportunity.stop_loss:.2f}",
                row=1, col=1
            )
            
            # Target line
            fig.add_hline(
                y=opportunity.target,
                line=dict(color="green", width=2, dash="dash"),
                annotation_text=f"Target: ₹{opportunity.target:.2f}",
                row=1, col=1
            )
            
            # Add support/resistance levels
            liquidity_zone = opportunity.chart_patterns.get('liquidity_zone', {})
            if liquidity_zone:
                for level in liquidity_zone.get('levels', []):
                    color = 'orange' if level['type'] == 'resistance' else 'purple'
                    fig.add_hline(
                        y=level['level'],
                        line=dict(color=color, width=1, dash="dot"),
                        annotation_text=f"{level['type']}: ₹{level['level']:.2f}",
                        row=1, col=1
                    )
            
            # Update layout
            fig.update_layout(
                title=f"{symbol} - {opportunity.entry_model} (RR: {opportunity.risk_reward_ratio:.2f})",
                xaxis_rangeslider_visible=False,
                height=600,
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating chart for {opportunity.symbol}: {e}")
            return go.Figure()
    
    def save_opportunity_charts(self, opportunities: List[TradingOpportunity], 
                               max_charts: int = None) -> List[str]:
        """Save charts for top opportunities"""
        if max_charts is None:
            max_charts = config.trading.top_charts_count
        
        saved_files = []
        
        for i, opp in enumerate(opportunities[:max_charts]):
            try:
                fig = self.create_opportunity_chart(opp)
                if fig.data:  # Only save if chart has data
                    filename = f"chart_{opp.symbol}_{opp.entry_model.replace(' ', '_')}.html"
                    filepath = os.path.join(config.trading.charts_dir, filename)
                    fig.write_html(filepath)
                    saved_files.append(filepath)
                    print(f"Saved chart: {filename}")
            except Exception as e:
                print(f"Error saving chart for {opp.symbol}: {e}")
        
        return saved_files
