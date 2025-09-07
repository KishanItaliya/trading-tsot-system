# Trading System - Stock Analysis and Opportunity Detection

A comprehensive trading system implementation following "The Trader's Playbook" methodology for NSE stocks.

## Features

### 🚀 **Core Trading Analysis**
- **🔴 Real-Time Data**: Integrated with Zerodha Kite API for live, accurate NSE market data
- **📊 Multi-timeframe Analysis**: Analyzes stocks across multiple timeframes (weekly, daily, 4H, hourly, 15min, 5min)
- **📈 Technical Analysis**: Detects trendlines, support/resistance levels, Fibonacci retracements, and price structure
- **🎯 Liquidity Zone Detection**: Identifies high-confluence liquidity zones using multiple confirmation methods
- **⚡ Entry Model Detection**: Implements Entry Model 1 (direct entry) and Entry Model 2 (confirmation entry)
- **🛡️ Risk Management**: Built-in risk management with configurable parameters and corrected R:R calculations

### 📊 **Enhanced Batch Processing**
- **⚡ Smart Batch Processing**: Process stocks in configurable batches (default: 20 stocks per batch)
- **🎛️ Flexible Controls**: Set batch size, maximum stocks, and starting position via CLI
- **📈 Real-time Progress**: Live progress tracking with batch completion summaries
- **🔄 Incremental Results**: See results as each batch completes for faster feedback

### 🎨 **Advanced Interactive Reports**
- **🎯 Grouped Opportunities**: Stocks grouped by symbol with expandable detailed views
- **📈📉 Bullish/Bearish Indicators**: Clear visual indicators showing trade direction
- **🖱️ Click-to-Expand**: Interactive stock headers reveal detailed opportunity tables
- **🎨 Color-Coded Elements**: 
  - Green/Red headers for bullish/bearish stocks
  - Color-coded R:R ratios (Excellent/Good/Fair/Poor)
  - Score badges with performance-based colors
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **⚡ Hover Effects**: Smooth animations and visual feedback for better UX

### 🔍 **Automated Screening & Analysis**
- **🔍 Automated Screening**: Daily screening of 1000+ NSE stocks with real market prices
- **📊 Interactive Charts**: Generates beautiful interactive HTML charts for opportunities
- **📋 Comprehensive Reports**: Enhanced HTML, text and JSON reports with detailed analysis
- **🎯 Smart Filtering**: Advanced filtering and ranking based on confluence scores

## Project Structure

```
Stock_TSOT/
├── src/trading_system/
│   ├── analysis/           # Technical analysis modules
│   ├── config/            # Configuration settings
│   ├── data/              # Data fetching and processing
│   ├── models/            # Data models and classes
│   └── utils/             # Utilities (logging, reports, dashboard)
├── main.py                # Main execution script
├── requirements.txt       # Python dependencies
├── reports/              # Generated reports
├── charts/               # Generated charts
└── logs/                 # System logs
```

## Installation

1. **Clone or download the project**

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If you encounter issues with TA-Lib installation:
   - **Windows**: Download the appropriate wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   - **macOS**: `brew install ta-lib` first
   - **Linux**: Install development packages first: `sudo apt-get install build-essential`

4. **Set up Kite API (Recommended for Real Data)**:
   ```bash
   # Copy credentials template
   cp kite_credentials_template.txt kite_credentials.txt
   
   # Edit kite_credentials.txt with your actual Kite API credentials
   # See KITE_API_SETUP.md for detailed instructions
   
   # Generate access token
   python generate_kite_token.py
   
   # Test integration
   python test_kite_integration.py
   ```

   **Without Kite API**: The system will use sample data for demonstration purposes.

## Usage

### 🚀 **Enhanced Batch Screening**

**Basic Screening** (20 stocks per batch):
```bash
python main.py --screening-only
```

**Custom Batch Processing**:
```bash
# Process first 100 stocks in batches of 25
python main.py --screening-only --max-stocks 100 --batch-size 25

# Process first 50 stocks in batches of 10
python main.py --screening-only --max-stocks 50 --batch-size 10

# Start from stock 100, process 200 stocks in batches of 20
python main.py --screening-only --start-from 100 --max-stocks 200 --batch-size 20
```

**All Available Options**:
```bash
python main.py --screening-only \
  --max-stocks 100 \      # Maximum stocks to analyze
  --batch-size 20 \       # Stocks per batch
  --start-from 0 \        # Starting stock index
  --log-level INFO        # Logging level
```

### 📊 **Single Stock Analysis**
Analyze a specific stock in detail:
```bash
python main.py --symbol RELIANCE
python main.py --symbol TCS
python main.py --symbol HDFCBANK
```

### 🎛️ **Advanced Options**
```bash
# Debug mode with detailed logging
python main.py --screening-only --log-level DEBUG

# Quick test with first 10 stocks
python main.py --screening-only --max-stocks 10 --batch-size 5

# Process large dataset efficiently
python main.py --screening-only --max-stocks 500 --batch-size 50
```

## Configuration

The system uses configuration files in `src/trading_system/config/settings.py`. Key settings include:

- **Stock List**: NSE stocks to analyze
- **Risk Management**: Maximum risk per trade, minimum R:R ratio
- **Analysis Parameters**: Fibonacci levels, trendline settings, confluence requirements
- **Market Hours**: Trading session times
- **File Paths**: Output directories for reports and charts

## 📁 Output Files

### 📊 **Enhanced Reports Directory**
- **`enhanced_batch_report_YYYYMMDD_HHMM.html`**: 🎨 **Interactive HTML Report**
  - Grouped opportunities by stock symbol
  - Click-to-expand detailed views
  - Bullish/Bearish indicators
  - Color-coded R:R ratios and scores
  - Responsive design for all devices
  - Professional presentation ready for sharing

- **`daily_report_YYYYMMDD_HHMM.txt`**: 📋 Human-readable daily report
- **`opportunities_YYYYMMDD_HHMM.json`**: 🔧 Machine-readable opportunity data

### 📈 **Charts Directory**
- **`chart_SYMBOL_MODEL.html`**: Interactive charts for individual stock opportunities

### 📝 **Logs Directory**
- **`trading_system_YYYYMMDD.log`**: Clean system logs (no more yfinance errors!)

### 🎯 **Report Features**
- **Market Overview Dashboard**: Total opportunities, success rates, bullish/bearish breakdown
- **Grouped Stock Analysis**: All opportunities for each stock in expandable sections  
- **Detailed Breakdown**: Comprehensive analysis cards for top performing stocks
- **Interactive Elements**: Hover effects, smooth animations, click handlers
- **Mobile Optimized**: Perfect viewing experience on any device

## Key Features Explained

### Entry Models

1. **Model 1 - Direct Entry**: Direct entry at high-confluence liquidity zones
2. **Model 2 - Confirmation Entry**: Entry after trendline break and retest at liquidity zones

### Confluence Analysis

The system identifies liquidity zones using multiple confirmations:
- Trendline intersections
- Support/resistance levels
- Fibonacci retracement levels
- High volume areas
- Psychological levels (round numbers)

### Risk Management

- Maximum 5% risk per trade
- Minimum 2:1 risk-reward ratio
- Market volatility checks
- Pre-screening filters for stock selection

### Multi-timeframe Analysis

- **Weekly/Daily**: Overall trend and major levels
- **4H/Hourly**: Entry timing and confirmation
- **15min/5min**: Precise entry execution

## Troubleshooting

### Common Issues

1. **Timezone Errors**: Fixed in the new version with proper timezone handling
2. **TA-Lib Installation**: See installation notes above
3. **Data Fetching Errors**: Check internet connection and Yahoo Finance availability
4. **Memory Issues**: Reduce the stock list in configuration if needed

### Error Logs

Check the logs directory for detailed error information. The system logs all operations with timestamps.

## Customization

### Adding New Stocks
Edit `src/trading_system/config/settings.py` and modify the `nse_stocks` list.

### Adjusting Risk Parameters
Modify the `TradingConfig` class in the settings file.

### Changing Analysis Parameters
Update the `AnalysisConfig` class for technical analysis settings.

## ⚡ Performance & Scalability

### 🚀 **Enhanced Batch Performance**
- **Batch Processing**: ~1-2 minutes per 20 stocks (with Kite API)
- **Scalable Architecture**: Process 100s or 1000s of stocks efficiently
- **Smart Progress Tracking**: Real-time feedback on batch completion
- **Memory Efficient**: ~200-500MB during execution regardless of batch size

### 📊 **Processing Times**
- **Single Stock Analysis**: ~5-10 seconds
- **20 Stock Batch**: ~2-3 minutes  
- **100 Stock Analysis**: ~10-15 minutes (5 batches of 20)
- **500+ Stock Screening**: ~45-60 minutes (configurable batch sizes)

### 🎯 **Optimization Features**
- **Configurable Batch Sizes**: Balance speed vs memory usage
- **Incremental Results**: See opportunities as they're found
- **Clean Logging**: No more unnecessary yfinance error spam
- **Real-time Data**: Direct Kite API integration for accurate prices

## Disclaimer

This system is for educational and research purposes only. Always perform your own analysis and risk assessment before making any trading decisions. Past performance does not guarantee future results.

## Support

For issues or questions, check the logs directory for detailed error information. The system provides comprehensive logging to help diagnose any problems.
