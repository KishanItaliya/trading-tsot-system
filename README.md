# Trading System - Stock Analysis and Opportunity Detection

A comprehensive trading system implementation following "The Trader's Playbook" methodology for NSE stocks.

## Features

- **Multi-timeframe Analysis**: Analyzes stocks across multiple timeframes (weekly, daily, 4H, hourly, 15min, 5min)
- **Technical Analysis**: Detects trendlines, support/resistance levels, Fibonacci retracements, and price structure
- **Liquidity Zone Detection**: Identifies high-confluence liquidity zones using multiple confirmation methods
- **Entry Model Detection**: Implements Entry Model 1 (direct entry) and Entry Model 2 (confirmation entry)
- **Risk Management**: Built-in risk management with configurable parameters
- **Automated Screening**: Daily screening of 50+ NSE stocks
- **Interactive Charts**: Generates interactive HTML charts for opportunities
- **Comprehensive Reports**: Text and JSON reports with detailed analysis

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

## Usage

### Complete Daily Screening
Run complete analysis with charts and reports:
```bash
python main.py
```

### Screening Only (No Charts)
Run screening without generating charts (faster):
```bash
python main.py --screening-only
```

### Analyze Single Stock
Analyze a specific stock in detail:
```bash
python main.py --symbol RELIANCE
```

### Set Log Level
Control logging verbosity:
```bash
python main.py --log-level DEBUG
```

## Configuration

The system uses configuration files in `src/trading_system/config/settings.py`. Key settings include:

- **Stock List**: NSE stocks to analyze
- **Risk Management**: Maximum risk per trade, minimum R:R ratio
- **Analysis Parameters**: Fibonacci levels, trendline settings, confluence requirements
- **Market Hours**: Trading session times
- **File Paths**: Output directories for reports and charts

## Output Files

### Reports Directory
- `daily_report_YYYYMMDD_HHMM.txt`: Human-readable daily report
- `opportunities_YYYYMMDD_HHMM.json`: Machine-readable opportunity data

### Charts Directory
- `chart_SYMBOL_MODEL.html`: Interactive charts for top opportunities

### Logs Directory
- `trading_system_YYYYMMDD.log`: System logs with timestamps

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

## Performance

- **Full Screening**: ~2-5 minutes for 50 stocks (depending on internet speed)
- **Single Stock Analysis**: ~5-10 seconds
- **Memory Usage**: ~200-500MB during execution

## Disclaimer

This system is for educational and research purposes only. Always perform your own analysis and risk assessment before making any trading decisions. Past performance does not guarantee future results.

## Support

For issues or questions, check the logs directory for detailed error information. The system provides comprehensive logging to help diagnose any problems.
