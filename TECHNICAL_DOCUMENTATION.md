# Trading System - Technical Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Module Documentation](#module-documentation)
4. [Data Flow](#data-flow)
5. [Configuration](#configuration)
6. [API Reference](#api-reference)
7. [Development Guide](#development-guide)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## 🏗️ System Overview

The Trading System is a comprehensive stock analysis and opportunity detection platform built following "The Trader's Playbook" methodology. It analyzes NSE stocks across multiple timeframes to identify high-probability trading opportunities using confluence analysis.

### Key Features
- **Multi-timeframe Analysis**: Weekly, Daily, 4H, Hourly, 15min, 5min
- **Technical Analysis**: Trendlines, Support/Resistance, Fibonacci, Price Structure
- **Liquidity Zone Detection**: High-confluence zones using multiple confirmations
- **Entry Model Detection**: Model 1 (Direct Entry) and Model 2 (Confirmation Entry)
- **Risk Management**: Built-in risk controls and validation
- **Automated Screening**: Daily screening of 50+ NSE stocks
- **Professional Reports**: Text, JSON, and interactive HTML charts

### Technology Stack
- **Language**: Python 3.7+
- **Data Source**: Yahoo Finance API (yfinance)
- **Technical Analysis**: TA-Lib, NumPy, Pandas
- **Visualization**: Plotly
- **Configuration**: Dataclasses
- **Logging**: Python logging module

---

## 🏛️ Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    Trading System                           │
├─────────────────────────────────────────────────────────────┤
│  main.py (Entry Point)                                     │
│  ├── Command Line Interface                                │
│  ├── Argument Parsing                                      │
│  └── Execution Control                                     │
├─────────────────────────────────────────────────────────────┤
│  system_manager.py (Core Orchestrator)                     │
│  ├── Component Coordination                                │
│  ├── Workflow Management                                   │
│  └── Validation & Filtering                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│  │   Config    │ │    Data     │ │  Analysis   │ │  Utils  ││
│  │   Module    │ │   Module    │ │   Module    │ │ Module  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Design Principles
1. **Separation of Concerns**: Each module has a specific responsibility
2. **Dependency Injection**: Components are loosely coupled
3. **Configuration-Driven**: Behavior controlled through configuration
4. **Error Resilience**: Graceful handling of failures with fallbacks
5. **Extensibility**: Easy to add new features or modify existing ones

---

## 📚 Module Documentation

### 1. Configuration Module (`src/trading_system/config/`)

#### Purpose
Centralized configuration management for all system settings.

#### Files
- `settings.py`: Configuration dataclasses and global config instance
- `__init__.py`: Module exports

#### Key Classes

##### `MarketConfig`
```python
@dataclass
class MarketConfig:
    nse_stocks: List[str]           # List of NSE stocks to analyze
    default_period: str = "2y"      # Default data period
    hourly_period: str = "60d"      # Hourly data period
    minute_15_period: str = "30d"   # 15-minute data period
    minute_5_period: str = "10d"    # 5-minute data period
    market_open_time: str = "09:15" # Market opening time (IST)
    market_close_time: str = "15:30"# Market closing time (IST)
    screening_time: str = "10:00"   # Daily screening time
```

##### `AnalysisConfig`
```python
@dataclass
class AnalysisConfig:
    fib_levels: List[float]                    # Fibonacci retracement levels
    min_trendline_touches: int = 2             # Minimum touches for valid trendline
    trendline_tolerance: float = 0.005         # Trendline touch tolerance
    sr_lookback_period: int = 50               # Support/resistance lookback
    sr_consolidation_tolerance: float = 0.02   # Level consolidation tolerance
    liquidity_zone_range: float = 0.15         # Price zone range percentage
    min_confluence_confirmations: int = 3      # Minimum confirmations required
    min_confluence_score: int = 5              # Minimum confluence score
    swing_point_order: int = 3                 # Pivot point detection order
    structure_volatility_threshold: float = 0.05 # Structure quality threshold
```

##### `TradingConfig`
```python
@dataclass
class TradingConfig:
    max_risk_per_trade: float = 0.05          # Maximum 5% risk per trade
    min_risk_reward_ratio: float = 2.0        # Minimum R:R ratio
    max_daily_volatility: float = 0.1         # Maximum daily volatility
    min_price: float = 50.0                   # Minimum stock price
    max_price: float = 5000.0                 # Maximum stock price
    min_avg_volume: int = 50000               # Minimum average volume
    max_volatility: float = 0.1               # Maximum volatility filter
    max_avg_daily_change: float = 0.15        # Maximum average daily change
    model1_distance_tolerance: float = 0.02   # Model 1 distance tolerance
    model2_distance_tolerance: float = 0.05   # Model 2 distance tolerance
    retest_distance_tolerance: float = 0.02   # Retest distance tolerance
    max_market_volatility: float = 0.05       # Maximum market volatility
    max_opportunities: int = 20               # Maximum opportunities to return
    top_charts_count: int = 5                 # Number of charts to generate
```

#### Usage Example
```python
from trading_system.config.settings import config

# Access configuration
stocks = config.market.nse_stocks
min_rr = config.trading.min_risk_reward_ratio
fib_levels = config.analysis.fib_levels
```

---

### 2. Data Module (`src/trading_system/data/`)

#### Purpose
Handles all data fetching, processing, and validation operations.

#### Files
- `market_data_fetcher.py`: Fetches market data from external sources
- `data_processor.py`: Processes and validates market data
- `data_source_fallback.py`: Fallback mechanisms for data reliability
- `__init__.py`: Module exports

#### Key Classes

##### `MarketDataFetcher`
**Purpose**: Fetches multi-timeframe market data with timezone handling and fallback mechanisms.

**Key Methods**:
```python
def get_multi_timeframe_data(self, symbol: str) -> Optional[MarketData]:
    """
    Fetches data for all required timeframes
    
    Args:
        symbol: Stock symbol (without .NS suffix)
        
    Returns:
        MarketData object with all timeframes or None if error
    """

def get_market_index_data(self, index_symbol: str = "^NSEI") -> Optional[pd.DataFrame]:
    """
    Get market index data for market condition analysis
    
    Args:
        index_symbol: Index symbol (default: Nifty 50)
        
    Returns:
        DataFrame with index data or None if error
    """
```

**Features**:
- Automatic timezone conversion (UTC to IST)
- Data resampling for weekly and 4H timeframes
- Error handling with detailed logging
- Integration with fallback system

##### `DataProcessor`
**Purpose**: Validates and processes market data for analysis.

**Key Methods**:
```python
def validate_data(data: pd.DataFrame, min_length: int = 20) -> bool:
    """
    Validate market data quality
    
    Checks:
    - Minimum data length
    - Required columns presence
    - Null values in recent data
    - Zero or negative prices
    """

def apply_pre_screening_filters(data: pd.DataFrame) -> bool:
    """
    Apply pre-screening filters to eliminate unsuitable stocks
    
    Filters:
    - Price range (₹50 - ₹5000)
    - Minimum average volume (50,000)
    - Maximum volatility (10%)
    - Maximum average daily change (15%)
    """

def calculate_basic_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic technical indicators
    
    Indicators:
    - Simple Moving Averages (20, 50, 200)
    - Exponential Moving Averages (12, 26)
    - MACD and Signal Line
    - RSI (14 periods)
    - Bollinger Bands
    - Volume indicators
    """
```

##### `DataSourceManager`
**Purpose**: Manages data source reliability with retry logic and fallback mechanisms.

**Key Methods**:
```python
def fetch_with_retry(self, symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
    """
    Fetch data with retry logic and rate limiting
    
    Features:
    - Automatic retries (up to 3 attempts)
    - Rate limiting to avoid API blocks
    - Caching of working/failed symbols
    """

def create_sample_data(self, symbol: str, days: int = 100) -> pd.DataFrame:
    """
    Create realistic sample data for testing when live data is unavailable
    
    Features:
    - Symbol-specific base prices
    - Realistic price movements
    - Proper OHLCV relationships
    """

def test_data_connectivity(self) -> Dict[str, bool]:
    """
    Test connectivity with known symbols
    
    Returns:
    - Dictionary of symbol -> connectivity status
    """
```

---

### 3. Models Module (`src/trading_system/models/`)

#### Purpose
Defines data structures and models used throughout the system.

#### Files
- `trading_opportunity.py`: Trading opportunity data model
- `market_data.py`: Market data container models
- `__init__.py`: Module exports

#### Key Classes

##### `TradingOpportunity`
**Purpose**: Represents a complete trading opportunity with all necessary details.

```python
@dataclass
class TradingOpportunity:
    symbol: str                           # Stock symbol
    entry_model: str                      # "Model1" or "Model2"
    entry_price: float                    # Entry price
    stop_loss: float                      # Stop loss price
    target: float                         # Target price
    risk_reward_ratio: float              # Risk-reward ratio
    confluence_score: int                 # Confluence score
    confirmations: List[str]              # List of confirmations
    timeframe_analysis: Dict[str, Any]    # Multi-timeframe analysis
    chart_patterns: Dict[str, Any]        # Chart pattern details
    notes: str                            # Additional notes
    created_at: datetime = None           # Creation timestamp
```

**Properties**:
```python
@property
def risk_percentage(self) -> float:
    """Calculate risk as percentage of entry price"""

@property
def reward_percentage(self) -> float:
    """Calculate reward as percentage of entry price"""

def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary for serialization"""
```

##### `MarketData`
**Purpose**: Container for multi-timeframe market data.

```python
@dataclass
class MarketData:
    symbol: str                           # Stock symbol
    timeframes: Dict[str, TimeframeData]  # Timeframe data dictionary
    last_updated: datetime = None         # Last update timestamp
```

**Methods**:
```python
def get_timeframe(self, timeframe: str) -> Optional[TimeframeData]:
    """Get data for specific timeframe"""

def get_daily_data(self) -> Optional[pd.DataFrame]:
    """Get daily timeframe data"""

def get_hourly_data(self) -> Optional[pd.DataFrame]:
    """Get hourly timeframe data"""

@property
def current_price(self) -> Optional[float]:
    """Get current price from daily data"""

@property
def is_valid(self) -> bool:
    """Check if market data is valid"""

def has_timeframe(self, timeframe: str) -> bool:
    """Check if timeframe data exists and is valid"""
```

##### `TimeframeData`
**Purpose**: Data for a specific timeframe.

```python
@dataclass
class TimeframeData:
    timeframe: str          # Timeframe identifier
    data: pd.DataFrame      # OHLCV data
    last_updated: datetime  # Last update timestamp
```

---

### 4. Analysis Module (`src/trading_system/analysis/`)

#### Purpose
Core technical analysis and trading opportunity detection.

#### Files
- `technical_analyzer.py`: Core technical analysis engine
- `liquidity_detector.py`: Liquidity zone detection
- `entry_model_detector.py`: Entry model detection
- `__init__.py`: Module exports

#### Key Classes

##### `TechnicalAnalyzer`
**Purpose**: Core technical analysis engine following the playbook methodology.

**Key Methods**:

```python
def detect_trendlines(self, data: pd.DataFrame, min_touches: int = None) -> List[Dict]:
    """
    Detect trendlines using wick-based approach
    
    Process:
    1. Find pivot points (highs and lows)
    2. Create trendlines from pivot combinations
    3. Count touches and validate strength
    4. Filter by minimum touches requirement
    
    Returns:
    - List of trendline dictionaries sorted by strength
    """

def find_support_resistance_levels(self, data: pd.DataFrame, lookback: int = None) -> List[Dict]:
    """
    Find support and resistance levels using multiple methods
    
    Methods:
    1. Pivot-based levels
    2. Volume-based levels
    3. Psychological levels (round numbers)
    4. Historical levels (ATH, ATL, 52-week)
    
    Returns:
    - Consolidated list of levels sorted by strength
    """

def calculate_fibonacci_levels(self, data: pd.DataFrame, trend_type: str = 'auto') -> Dict:
    """
    Calculate Fibonacci retracement levels
    
    Process:
    1. Auto-detect trend direction or use specified
    2. Find swing high and swing low points
    3. Calculate retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%)
    
    Returns:
    - Dictionary with trend info and Fibonacci levels
    """

def identify_price_structure(self, data: pd.DataFrame) -> Dict:
    """
    Identify price structure as per playbook
    
    Analysis:
    1. Trend detection (bullish/bearish/sideways)
    2. Swing point identification
    3. Pullback pattern recognition
    4. Structure quality assessment
    
    Returns:
    - Dictionary with structure analysis
    """
```

**Internal Methods**:
```python
def _find_pivot_points(self, data: np.array, order: int = 3, pivot_type: str = 'high') -> List[int]:
    """Find pivot highs and lows using order-based detection"""

def _detect_trend(self, data: pd.DataFrame, period: int = 20) -> str:
    """Detect trend direction using linear regression on highs and lows"""

def _identify_swing_points(self, data: pd.DataFrame) -> Dict:
    """Identify swing highs and lows for structure analysis"""

def _identify_pullbacks(self, data: pd.DataFrame) -> List[Dict]:
    """Identify bullish and bearish pullback patterns"""
```

##### `LiquidityDetector`
**Purpose**: Detect high liquidity zones using confluence analysis.

**Key Methods**:
```python
def find_liquidity_zones(self, market_data: MarketData) -> List[Dict]:
    """
    Find high liquidity zones with multiple confirmations
    
    Process:
    1. Get technical analysis (trendlines, levels, Fibonacci)
    2. Create potential price zones around current price
    3. Check each zone for confluence confirmations
    4. Score zones based on confirmation strength
    5. Return top zones sorted by confluence score
    
    Confirmations:
    - Trendline intersections
    - Support/resistance levels
    - Fibonacci retracement levels
    - High volume areas
    - Psychological levels
    
    Returns:
    - List of liquidity zone dictionaries
    """
```

**Internal Methods**:
```python
def _create_price_zones(self, current_price: float, range_pct: float = None) -> List[Dict]:
    """Create potential price zones at different percentages from current price"""

def _price_near_level(self, price1: float, price2: float, tolerance: float = 0.02) -> bool:
    """Check if two prices are near each other within tolerance"""

def _check_volume_confluence(self, data: pd.DataFrame, target_price: float, tolerance: float = 0.02) -> bool:
    """Check if there was significant volume near target price"""
```

##### `EntryModelDetector`
**Purpose**: Detect Entry Model 1 and Entry Model 2 setups.

**Key Methods**:
```python
def detect_entry_models(self, market_data: MarketData) -> List[TradingOpportunity]:
    """
    Detect both entry models and return trading opportunities
    
    Process:
    1. Find liquidity zones using LiquidityDetector
    2. Check each zone for Entry Model 1 (Direct Entry)
    3. Check each zone for Entry Model 2 (Confirmation Entry)
    4. Filter by minimum risk-reward ratio
    5. Sort by confluence score
    
    Returns:
    - List of TradingOpportunity objects
    """
```

**Entry Model Methods**:
```python
def _check_entry_model_1(self, market_data: MarketData, zone: Dict, current_price: float) -> Optional[TradingOpportunity]:
    """
    Check for Entry Model 1: Direct entry at liquidity zone
    
    Requirements:
    - Price near liquidity zone (within 2%)
    - Clear directional bias (trend + zone type alignment)
    - Valid stop loss and target levels
    - Minimum 2:1 risk-reward ratio
    """

def _check_entry_model_2(self, market_data: MarketData, zone: Dict, current_price: float) -> Optional[TradingOpportunity]:
    """
    Check for Entry Model 2: Entry after trendline break + retest
    
    Requirements:
    - Recent trendline break on hourly timeframe
    - Price in retest phase at liquidity zone
    - Rejection signals (wick formations)
    - Clear directional bias
    - Valid stop loss and target levels
    - Minimum 2:1 risk-reward ratio
    """
```

**Support Methods**:
```python
def _find_next_resistance(self, data: pd.DataFrame, entry_price: float) -> Optional[float]:
    """Find next significant resistance level above entry price"""

def _find_next_support(self, data: pd.DataFrame, entry_price: float) -> Optional[float]:
    """Find next significant support level below entry price"""

def _calculate_stop_loss_long(self, data: pd.DataFrame, zone: Dict, entry_price: float) -> Optional[float]:
    """Calculate stop loss for long position"""

def _calculate_stop_loss_short(self, data: pd.DataFrame, zone: Dict, entry_price: float) -> Optional[float]:
    """Calculate stop loss for short position"""

def _is_trendline_recently_broken(self, data: pd.DataFrame, trendline: Dict, lookback: int = 5) -> bool:
    """Check if trendline was broken in recent candles"""

def _is_retest_scenario(self, data: pd.DataFrame, zone: Dict, broken_trendline: Dict) -> bool:
    """Check if current price action represents a retest"""
```

---

### 5. Utils Module (`src/trading_system/utils/`)

#### Purpose
Utility functions for logging, reporting, and visualization.

#### Files
- `logger.py`: Logging configuration
- `report_generator.py`: Report generation utilities
- `dashboard.py`: Chart and dashboard creation
- `__init__.py`: Module exports

#### Key Classes

##### `ReportGenerator`
**Purpose**: Generate various reports for trading opportunities.

**Key Methods**:
```python
def generate_daily_report(self, opportunities: List[TradingOpportunity]) -> str:
    """Generate human-readable daily report"""

def save_daily_report(self, opportunities: List[TradingOpportunity]) -> str:
    """Save daily report to file and return filename"""

def save_opportunities_json(self, opportunities: List[TradingOpportunity]) -> str:
    """Save opportunities as JSON for further processing"""

def generate_summary_stats(self, opportunities: List[TradingOpportunity]) -> dict:
    """Generate summary statistics for opportunities"""
```

##### `TradingDashboard`
**Purpose**: Create interactive charts and visualizations.

**Key Methods**:
```python
def create_opportunity_chart(self, opportunity: TradingOpportunity) -> go.Figure:
    """
    Create detailed chart for each opportunity
    
    Features:
    - Candlestick price chart
    - Volume bars
    - Entry, stop loss, and target lines
    - Support/resistance levels
    - Interactive annotations
    """

def save_opportunity_charts(self, opportunities: List[TradingOpportunity], max_charts: int = None) -> List[str]:
    """Save charts for top opportunities as HTML files"""
```

##### Logging Setup
```python
def setup_logging(log_level: str = None) -> logging.Logger:
    """
    Setup logging configuration
    
    Features:
    - File and console logging
    - Timestamped log files
    - Configurable log levels
    - Structured log format
    """
```

---

### 6. System Manager (`src/trading_system/system_manager.py`)

#### Purpose
Main orchestrator that coordinates all system components.

#### Key Class: `TradingSystemManager`

**Initialization**:
```python
def __init__(self):
    self.data_fetcher = MarketDataFetcher()
    self.data_processor = DataProcessor()
    self.analyzer = TechnicalAnalyzer()
    self.liquidity_detector = LiquidityDetector(self.analyzer)
    self.entry_detector = EntryModelDetector(self.analyzer, self.liquidity_detector)
    self.report_generator = ReportGenerator()
    self.dashboard = TradingDashboard()
    self.nse_stocks = config.market.nse_stocks
```

**Key Methods**:
```python
def daily_screening(self, target_time: str = None) -> List[TradingOpportunity]:
    """
    Main daily screening function
    
    Process:
    1. Iterate through all NSE stocks
    2. Fetch multi-timeframe data
    3. Apply pre-screening filters
    4. Detect entry opportunities
    5. Validate opportunities
    6. Sort by confluence score
    7. Return top opportunities
    """

def run_complete_analysis(self) -> dict:
    """
    Run complete analysis and generate all outputs
    
    Outputs:
    - Trading opportunities
    - Text and JSON reports
    - Interactive HTML charts
    - Summary statistics
    """

def analyze_single_stock(self, symbol: str) -> dict:
    """
    Analyze a single stock in detail
    
    Returns:
    - Detailed analysis results
    - Technical indicators
    - Opportunities found
    - Structure analysis
    """
```

**Validation Methods**:
```python
def _validate_opportunity(self, opportunity: TradingOpportunity, market_data) -> bool:
    """
    Final validation of trading opportunity
    
    Checks:
    - Risk management (max 5% risk per trade)
    - Market conditions
    - Structure quality
    - Minimum confluence score
    """

def _check_market_conditions(self) -> bool:
    """
    Check overall market conditions using Nifty
    
    Checks:
    - Market volatility levels
    - VIX levels (if available)
    - Overall market trend
    """
```

---

## 🔄 Data Flow

### 1. System Initialization
```
main.py → TradingSystemManager → Component Initialization
├── MarketDataFetcher
├── DataProcessor  
├── TechnicalAnalyzer
├── LiquidityDetector
├── EntryModelDetector
├── ReportGenerator
└── TradingDashboard
```

### 2. Daily Screening Flow
```
Stock List → Data Fetching → Pre-screening → Technical Analysis → Opportunity Detection → Validation → Reporting
     ↓              ↓              ↓               ↓                    ↓              ↓           ↓
NSE Stocks → Multi-timeframe → Price/Volume → Trendlines/Levels → Entry Models → Risk Check → Reports/Charts
             Data (OHLCV)      Filters       Fibonacci/Structure   Model1/Model2   Market Cond.
```

### 3. Technical Analysis Flow
```
Market Data → Technical Analyzer → Liquidity Detector → Entry Model Detector → Trading Opportunity
     ↓               ↓                    ↓                      ↓                      ↓
  OHLCV Data → Trendlines/Levels → Confluence Zones → Model1/Model2 Check → Validated Opportunity
               Fibonacci/Structure   Confirmations      Risk/Reward Calc.
```

### 4. Report Generation Flow
```
Trading Opportunities → Report Generator → Output Files
         ↓                     ↓              ↓
   Opportunity List → Text/JSON Reports → Saved Files
                      Summary Statistics   HTML Charts
```

---

## ⚙️ Configuration

### Environment Setup
```python
# Configuration is centralized in src/trading_system/config/settings.py
from trading_system.config.settings import config

# Access different configuration sections
market_config = config.market
analysis_config = config.analysis
trading_config = config.trading
```

### Customization Examples

#### Adding New Stocks
```python
# Edit src/trading_system/config/settings.py
config.market.nse_stocks.extend(['NEWSTOCK1', 'NEWSTOCK2'])
```

#### Adjusting Risk Parameters
```python
# Modify trading configuration
config.trading.max_risk_per_trade = 0.03  # 3% instead of 5%
config.trading.min_risk_reward_ratio = 3.0  # 3:1 instead of 2:1
```

#### Changing Analysis Parameters
```python
# Modify analysis configuration
config.analysis.min_confluence_confirmations = 4  # 4 instead of 3
config.analysis.min_confluence_score = 8  # 8 instead of 5
```

---

## 📡 API Reference

### Command Line Interface

#### Basic Usage
```bash
# Complete analysis with charts
python main.py

# Single stock analysis
python main.py --symbol RELIANCE

# Screening only (no charts)
python main.py --screening-only

# Debug mode
python main.py --log-level DEBUG
```

#### Arguments
- `--symbol, -s`: Analyze single stock symbol
- `--log-level, -l`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `--screening-only`: Run screening without generating charts

### Python API

#### System Manager
```python
from trading_system.system_manager import TradingSystemManager

# Initialize system
system = TradingSystemManager()

# Run daily screening
opportunities = system.daily_screening()

# Analyze single stock
result = system.analyze_single_stock('RELIANCE')

# Complete analysis
analysis_result = system.run_complete_analysis()
```

#### Individual Components
```python
# Technical Analysis
from trading_system.analysis import TechnicalAnalyzer
analyzer = TechnicalAnalyzer()
trendlines = analyzer.detect_trendlines(data)

# Data Fetching
from trading_system.data import MarketDataFetcher
fetcher = MarketDataFetcher()
market_data = fetcher.get_multi_timeframe_data('RELIANCE')

# Report Generation
from trading_system.utils import ReportGenerator
generator = ReportGenerator()
report = generator.generate_daily_report(opportunities)
```

---

## 🛠️ Development Guide

### Setting Up Development Environment

1. **Clone Repository**
```bash
git clone <repository-url>
cd Stock_TSOT
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Tests**
```bash
python test_system.py
```

### Adding New Features

#### Adding a New Technical Indicator
1. Add the indicator method to `TechnicalAnalyzer` class
2. Update configuration if needed
3. Add tests for the new indicator
4. Update documentation

Example:
```python
# In src/trading_system/analysis/technical_analyzer.py
def calculate_stochastic(self, data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    """Calculate Stochastic Oscillator"""
    high_max = data['High'].rolling(window=k_period).max()
    low_min = data['Low'].rolling(window=k_period).min()
    
    k_percent = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return pd.DataFrame({'%K': k_percent, '%D': d_percent})
```

#### Adding a New Entry Model
1. Add the model detection method to `EntryModelDetector`
2. Update the main detection loop
3. Add configuration parameters if needed
4. Add tests and documentation

Example:
```python
# In src/trading_system/analysis/entry_model_detector.py
def _check_entry_model_3(self, market_data: MarketData, zone: Dict, current_price: float) -> Optional[TradingOpportunity]:
    """Check for Entry Model 3: Custom pattern entry"""
    # Implementation here
    pass
```

#### Adding a New Data Source
1. Create a new fetcher class in the data module
2. Implement the same interface as `MarketDataFetcher`
3. Update `DataSourceManager` to use the new source
4. Add configuration for the new source

### Code Style Guidelines

#### Python Style
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Add docstrings for all classes and methods
- Use meaningful variable and function names

#### Documentation Style
```python
def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Brief description of the function
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 10)
        
    Returns:
        Dictionary containing the results
        
    Raises:
        ValueError: If param1 is empty
    """
    pass
```

#### Error Handling
- Use specific exception types
- Log errors with appropriate levels
- Provide fallback mechanisms where possible
- Don't suppress exceptions without good reason

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return fallback_value()
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

---

## 🧪 Testing

### Test Structure
```
tests/
├── unit/
│   ├── test_technical_analyzer.py
│   ├── test_liquidity_detector.py
│   ├── test_entry_model_detector.py
│   └── test_data_processor.py
├── integration/
│   ├── test_system_manager.py
│   └── test_complete_workflow.py
└── fixtures/
    ├── sample_data.py
    └── mock_responses.py
```

### Running Tests

#### Component Tests
```bash
# Test individual components
python test_system.py

# Test with mock data
python -m pytest tests/unit/ -v

# Test integration
python -m pytest tests/integration/ -v
```

#### Manual Testing
```bash
# Test single stock
python main.py --symbol INFY --log-level DEBUG

# Test screening with limited stocks
# (Edit config to use smaller stock list)
python main.py --screening-only
```

### Test Data
The system includes sample data generation for testing:
```python
from trading_system.data.data_source_fallback import DataSourceManager

manager = DataSourceManager()
sample_data = manager.create_sample_data('TEST', days=100)
```

---

## 🚀 Deployment

### Production Deployment

#### Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 10GB+ free space
- **Network**: Stable internet connection
- **OS**: Linux/Windows/macOS

#### Environment Setup
```bash
# Production environment
python -m venv prod_env
source prod_env/bin/activate
pip install -r requirements.txt

# Set production configuration
export TRADING_ENV=production
export LOG_LEVEL=INFO
```

#### Scheduled Execution
```bash
# Crontab entry for daily screening at 10:00 AM IST
0 10 * * 1-5 /path/to/prod_env/bin/python /path/to/main.py --screening-only
```

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY main.py .
COPY README.md .

CMD ["python", "main.py", "--screening-only"]
```

### Monitoring and Logging

#### Log Files
- **Location**: `logs/trading_system_YYYYMMDD.log`
- **Rotation**: Daily rotation
- **Levels**: DEBUG, INFO, WARNING, ERROR

#### Monitoring Metrics
- Execution time per screening
- Number of opportunities found
- Data fetch success rate
- Error rates by component

#### Alerts
Set up alerts for:
- System failures
- No opportunities found for multiple days
- Data source failures
- Unusual execution times

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Timezone Errors
**Problem**: `Cannot subtract tz-naive and tz-aware datetime-like objects`
**Solution**: Fixed in the new system with proper timezone handling

#### 2. Yahoo Finance API Failures
**Problem**: Rate limiting or API unavailability
**Solution**: System automatically falls back to sample data
```python
# Check data source status
from trading_system.data.data_source_fallback import DataSourceManager
manager = DataSourceManager()
status = manager.test_data_connectivity()
```

#### 3. No Opportunities Found
**Problem**: System returns no trading opportunities
**Possible Causes**:
- Market conditions filter too strict
- Confluence requirements too high
- Data quality issues

**Solutions**:
```python
# Adjust configuration
config.trading.max_market_volatility = 0.08  # Increase from 0.05
config.analysis.min_confluence_score = 3     # Decrease from 5
config.analysis.min_confluence_confirmations = 2  # Decrease from 3
```

#### 4. Memory Issues
**Problem**: High memory usage during screening
**Solutions**:
- Reduce stock list size
- Process stocks in batches
- Increase system RAM

#### 5. Slow Execution
**Problem**: Screening takes too long
**Solutions**:
- Use `--screening-only` flag
- Reduce data periods in configuration
- Implement parallel processing

### Debug Mode
```bash
# Enable debug logging
python main.py --log-level DEBUG

# Check specific component
python -c "
from trading_system.analysis import TechnicalAnalyzer
analyzer = TechnicalAnalyzer()
# Test specific functionality
"
```

### Log Analysis
```bash
# Check recent errors
grep "ERROR" logs/trading_system_$(date +%Y%m%d).log

# Check screening results
grep "Found opportunity" logs/trading_system_$(date +%Y%m%d).log

# Check data fetch issues
grep "Error fetching" logs/trading_system_$(date +%Y%m%d).log
```

---

## 📞 Support and Maintenance

### Regular Maintenance Tasks

#### Daily
- Check log files for errors
- Verify screening execution
- Monitor opportunity count trends

#### Weekly
- Review system performance metrics
- Update stock list if needed
- Check data source reliability

#### Monthly
- Review and update configuration
- Analyze false positive rates
- Update documentation

### Performance Optimization

#### Data Optimization
- Cache frequently used data
- Implement data compression
- Optimize database queries (if using database)

#### Code Optimization
- Profile slow functions
- Implement parallel processing
- Optimize memory usage

#### Configuration Tuning
- Adjust filter parameters based on results
- Fine-tune confluence requirements
- Optimize timeframe selection

---

## 📚 Additional Resources

### External Documentation
- [TA-Lib Documentation](https://ta-lib.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)

### Trading Resources
- "The Trader's Playbook" methodology
- Technical analysis fundamentals
- Risk management principles
- Market structure concepts

### Development Resources
- Python best practices
- Software architecture patterns
- Testing methodologies
- Documentation standards

---

This technical documentation provides a comprehensive guide for developers working with the Trading System. For specific implementation details, refer to the source code and inline documentation.
