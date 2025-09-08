"""
Configuration settings for the trading system
"""

from dataclasses import dataclass
from typing import List, Dict
import os


@dataclass
class MarketConfig:
    """Market-related configuration"""
    # NSE stock list
    nse_stocks: List[str] = None
    
    # Data fetching settings
    default_period: str = "2y"
    hourly_period: str = "60d"
    minute_15_period: str = "30d"
    minute_5_period: str = "10d"
    
    # Market hours (IST)
    market_open_time: str = "09:15"
    market_close_time: str = "15:30"
    
    # Screening time
    screening_time: str = "10:00"
    
    def __post_init__(self):
        if self.nse_stocks is None:
            # Comprehensive NSE stock list (400+ stocks for large-scale analysis)
            self.nse_stocks = [
                # Nifty 50 stocks
                'RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK', 'HINDUNILVR',
                'INFY', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
                'BAJFINANCE', 'LT', 'ASIANPAINT', 'HCLTECH', 'AXISBANK',
                'MARUTI', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND',
                'WIPRO', 'BAJAJFINSV', 'POWERGRID', 'NTPC', 'ONGC',
                'TECHM', 'M&M', 'TATASTEEL', 'ADANIPORTS', 'COALINDIA',
                'DRREDDY', 'GRASIM', 'BRITANNIA', 'CIPLA', 'EICHERMOT',
                'BPCL', 'TATACONSUM', 'DIVISLAB', 'HEROMOTOCO', 'JSWSTEEL',
                'HINDALCO', 'INDUSINDBK', 'BAJAJ-AUTO', 'APOLLOHOSP',
                'TATAMOTORS', 'UPL', 'SBILIFE', 'HDFCLIFE', 'ADANIENT',
                
                # Nifty Next 50 & Other Large Caps
                'ACC', 'AUBANK', 'BANDHANBNK', 'BERGEPAINT', 'BIOCON',
                'BOSCHLTD', 'CADILAHC', 'CHOLAFIN', 'COLPAL', 'CONCOR',
                'DABUR', 'DMART', 'DLFL', 'GODREJCP', 'HAVELLS',
                'HDFCAMC', 'HDFCLIFE', 'HINDPETRO', 'ICICIPRULI', 'IDEA',
                'INDIGO', 'INDUSTOWER', 'IOC', 'IRCTC', 'JINDALSTEL',
                'JUBLFOOD', 'LICHSGFIN', 'MARICO', 'MCDOWELL-N', 'MFSL',
                'MOTHERSUMI', 'MUTHOOTFIN', 'NAUKRI', 'NMDC', 'OFSS',
                'PAGEIND', 'PEL', 'PETRONET', 'PIDILITIND', 'PNB',
                'POLYCAB', 'PVR', 'RBLBANK', 'SBICARD', 'SHREECEM',
                'SIEMENS', 'SRF', 'TORNTPHARM', 'TRENT', 'VEDL',
                'VOLTAS', 'WHIRLPOOL', 'YESBANK', 'ZEEL', 'ZERODHA',
                
                # Mid Cap Stocks
                'ABCAPITAL', 'ABFRL', 'AJANTPHARM', 'ALKEM', 'AMBUJACEM',
                'APLLTD', 'ASHOKLEY', 'ASTRAL', 'ATUL', 'BALKRISIND',
                'BATAINDIA', 'BEL', 'BHARATFORG', 'BHEL', 'BIOCON',
                'CANBK', 'CANFINHOME', 'CHAMBLFERT', 'CUMMINSIND', 'DEEPAKNTR',
                'DELTACORP', 'DIXON', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK',
                'GAIL', 'GLENMARK', 'GMRINFRA', 'GNFC', 'GODREJPROP',
                'GRANULES', 'GUJGASLTD', 'HATSUN', 'ICICIGI', 'IDFCFIRSTB',
                'IEX', 'IGL', 'INDIANB', 'INDIAMART', 'INTELLECT',
                'IRB', 'IRFC', 'ISEC', 'KPITTECH', 'L&TFH',
                'LALPATHLAB', 'LAURUSLABS', 'LUPIN', 'MANAPPURAM', 'MINDTREE',
                'MRF', 'NIACL', 'NIITLTD', 'OBEROIRLTY', 'ONGC',
                'ORIENTBANK', 'PERSISTENT', 'PHOENIXLTD', 'PIIND', 'PLASTIBLENDS',
                'RALLIS', 'RECLTD', 'RELAXO', 'SAIL', 'SANOFI',
                'SCHAEFFLER', 'SCHNEIDER', 'SHRIRAMFIN', 'SPARC', 'STAR',
                'SUNTV', 'SYMPHONY', 'TATACHEM', 'TATACOMM', 'TATAELXSI',
                'TATAINVEST', 'TATAPOWER', 'TEAMLEASE', 'THERMAX', 'TORNTPOWER',
                'TV18BRDCST', 'UBL', 'UJJIVAN', 'UNOMINDA', 'VINATIORGA',
                'WABCOINDIA', 'WELCORP', 'WESTLIFE', 'ZYDUSLIFE',
                
                # Small Cap & Emerging Stocks
                'AAVAS', 'AFFLE', 'AIAENG', 'APLAPOLLO', 'ARVINDFASN',
                'BALRAMCHIN', 'BASF', 'BAYERCROP', 'BEML', 'BLISSGVS',
                'BLUEDART', 'BSOFT', 'CAPLIPOINT', 'CARERATING', 'CDSL',
                'CENTRALBK', 'CERA', 'CGCL', 'CHALET', 'CHOLAHLDNG',
                'CLEAN', 'COFORGE', 'CROMPTON', 'CSB', 'CSBBANK',
                'CUMMINSIND', 'DATAPATTNS', 'DBCORP', 'DCBBANK', 'DHANI',
                'DHANUKA', 'DISHTV', 'DLF', 'DREDGECORP', 'EDELWEISS',
                'EMAMILTD', 'ENDURANCE', 'ENGINERSIN', 'EQUITAS', 'FINEORG',
                'FINCABLES', 'FRETAIL', 'FSL', 'GALAXYSURF', 'GARFIBRES',
                'GATEWAY', 'GICRE', 'GILLETTE', 'GLAXO', 'GPPL',
                'GRAPHITE', 'GREAVESCOT', 'GRINDWELL', 'GSFC', 'GSPL',
                'GTLINFRA', 'GULFOILLUB', 'HAL', 'HAPPSTMNDS', 'HCC',
                'HEG', 'HEIDELBERG', 'HERITGFOOD', 'HFCL', 'HSCL',
                'HUDCO', 'IBREALEST', 'IDBI', 'IDFC', 'IFBIND',
                'IFCI', 'IIFL', 'INDBANK', 'INDHOTEL', 'INDIABULLS',
                'INDIACEM', 'INDIANHUME', 'INDOCO', 'INDUSINDBK', 'INFIBEAM',
                'INGERRAND', 'INOXLEISUR', 'INOXWIND', 'IOB', 'IOGL',
                'IPCA', 'ISMT', 'ITDCEM', 'JAGRAN', 'JAICORPLTD',
                'JAMNAAUTO', 'JAYNECOIND', 'JBCHEPHARM', 'JCHAC', 'JETAIRWAYS',
                'JKCEMENT', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JMFINANCIL',
                'JSL', 'JSWENERGY', 'JUSTDIAL', 'JYOTHYLAB', 'KAJARIACER',
                'KALPATPOWR', 'KALYANKJIL', 'KANSAINER', 'KARURVYSYA', 'KEC',
                'KEI', 'KNRCON', 'KRBL', 'KSCL', 'LAKSHVILAS',
                'LAOPALA', 'LAXMIMACH', 'LEMONTREE', 'LINDEINDIA', 'LUXIND',
                'MAGMA', 'MAHINDCIE', 'MAHLOG', 'MAHSCOOTER', 'MAHSEAMLES',
                'MAITHANALL', 'MAJESCO', 'MANINFRA', 'MASFIN', 'MAXHEALTH',
                'MAZAGON', 'MBAPL', 'MINDACORP', 'MIRZAINT', 'MOIL',
                'MONTECARLO', 'MOREPENLAB', 'MOTILALOFS', 'MPHASIS', 'MRPL',
                'MSUMI', 'MTARTECH', 'MUKANDLTD', 'NAM-INDIA', 'NATIONALUM',
                'NAUKRI', 'NAVINFLUOR', 'NAVNETEDUL', 'NBCC', 'NCC',
                'NECLIFE', 'NETWORK18', 'NEYVELI', 'NHPC', 'NIACL',
                'NILKAMAL', 'NLCINDIA', 'NOCIL', 'NRBBEARING', 'NSIL',
                'NSLNISP', 'NTPC', 'NUCLEUS', 'OAL', 'OCCL',
                'OFSS', 'OIL', 'OMAXE', 'ONEPOINT', 'ORIENTCEM',
                'ORIENTREF', 'ORISSAMINE', 'PAISALO', 'PANAMAPET', 'PARAGMILK',
                'PCJEWELLER', 'PFS', 'PGHL', 'PHILIPCARB', 'PHOENIXLTD',
                'PNBHOUSING', 'PNCINFRA', 'POINTCOOK', 'POLYMED', 'PRAJIND',
                'PRECAM', 'PRESTIGE', 'PRSMJOHNSN', 'PTC', 'PVP',
                'QUESS', 'RADICO', 'RAIN', 'RAJESHEXPO', 'RAMCOCEM',
                'RANBAXY', 'RANEENGINE', 'RATNAMANI', 'RAYMOND', 'RCOM',
                'RCF', 'RDBBANK', 'REDINGTON', 'RELCAPITAL', 'RELINFRA',
                'REPCOHOME', 'REPL', 'REXPIPES', 'RHIM', 'RITES',
                'ROLTA', 'RPOWER', 'RUPA', 'SADBHAV', 'SANOFI',
                'SARLAPOLY', 'SCHAEFFLER', 'SCHNEIDER', 'SCI', 'SDBL',
                'SESHAPAPER', 'SHANKARA', 'SHAREINDIA', 'SHILPAMED', 'SHOPERSTOP',
                'SHREECEM', 'SHREEPUSHP', 'SHRIRAMCIT', 'SHYAMMETL', 'SILVEROAK',
                'SIMPLEX', 'SKFINDIA', 'SIS', 'SMARTLINK', 'SMLISUZU',
                'SOLARINDS', 'SONATSOFTW', 'SOUTHBANK', 'SPANDANA', 'SPICEJET',
                'SPTL', 'SRHHYPNO', 'STAR', 'STARCEMENT', 'STLTECH',
                'SUBEXLTD', 'SUDARSCHEM', 'SUJANAHSNG', 'SUMICHEM', 'SUNDARMFIN',
                'SUNDRMFAST', 'SUPRAJIT', 'SUPRIYA', 'SURYAROSNI', 'SUULD',
                'SWANENERGY', 'SYMPHONY', 'SYNCOM', 'SYNGENE', 'TAKE',
                'TALBROAUTO', 'TANLA', 'TASTYBITE', 'TCI', 'TCNSBRANDS',
                'TCS', 'TDPOWERSYS', 'TEAMLEASE', 'TECHIN', 'TECHM',
                'TEXRAIL', 'TFL', 'THEMISMED', 'TIINDIA', 'TIMESINTRNT',
                'TIRUMALCHM', 'TISCAGRO', 'TITAGARH', 'TMB', 'TNPETRO',
                'TNPL', 'TRENT', 'TRIDENT', 'TRITURBINE', 'TSECURITE',
                'TTKPRESTIG', 'TTML', 'TUTICORIN', 'TV18BRDCST', 'TVSSRICHAK',
                'TVTODAY', 'TWLNVL', 'UCOBANK', 'UFLEX', 'UGARSUGAR',
                'UJJIVAN', 'UNICHEMLAB', 'UNIONBANK', 'UNITDSPR', 'UPL',
                'USHAMART', 'UTTAMGALVA', 'UTTAMSUGAR', 'V2RETAIL', 'VAIBHAVGBL',
                'VAKRANGEE', 'VBL', 'VCL', 'VENKEYS', 'VGUARD',
                'VINATIORGA', 'VIPIND', 'VMART', 'VRLLOG', 'VSTIND',
                'WABAG', 'WELENT', 'WELSPUNENT', 'WESTLIFE', 'WHEELS',
                'WILLAMAGOR', 'WINDLAS', 'WOCKPHARMA', 'WORTH', 'WSTCSTPAPR',
                'XCHANGING', 'YESBANK', 'ZEEL', 'ZENTEC', 'ZFCVINDIA'
            ]


@dataclass
class AnalysisConfig:
    """Technical analysis configuration"""
    # Fibonacci levels
    fib_levels: List[float] = None
    
    # Trendline detection
    min_trendline_touches: int = 2
    trendline_tolerance: float = 0.005
    
    # Support/resistance detection
    sr_lookback_period: int = 50
    sr_consolidation_tolerance: float = 0.02
    
    # Liquidity zone detection
    liquidity_zone_range: float = 0.15
    min_confluence_confirmations: int = 3
    min_confluence_score: int = 5
    
    # Price structure analysis
    swing_point_order: int = 3
    structure_volatility_threshold: float = 0.05
    
    def __post_init__(self):
        if self.fib_levels is None:
            self.fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]


@dataclass
class TradingConfig:
    """Trading and risk management configuration"""
    # Risk management
    max_risk_per_trade: float = 0.05  # 5%
    min_risk_reward_ratio: float = 2.0
    max_daily_volatility: float = 0.1  # 10%
    
    # Pre-screening filters
    min_price: float = 50.0
    max_price: float = 5000.0
    min_avg_volume: int = 50000
    max_volatility: float = 0.1
    max_avg_daily_change: float = 0.15
    
    # Entry model tolerances
    model1_distance_tolerance: float = 0.02  # 2%
    model2_distance_tolerance: float = 0.05  # 5%
    retest_distance_tolerance: float = 0.02  # 2%
    
    # Market condition checks
    max_market_volatility: float = 0.05  # 5% on Nifty
    
    # Output settings
    # max_opportunities: int = 20  # REMOVED - No limit on opportunities!
    top_charts_count: int = 5
    
    # File paths
    reports_dir: str = "reports"
    charts_dir: str = "charts"
    logs_dir: str = "logs"
    
    def __post_init__(self):
        # Create directories if they don't exist
        for directory in [self.reports_dir, self.charts_dir, self.logs_dir]:
            os.makedirs(directory, exist_ok=True)


@dataclass
class KiteConfig:
    """Kite API configuration"""
    # API credentials (to be set via environment variables or config file)
    api_key: str = ""
    api_secret: str = ""
    access_token: str = ""
    
    # API settings
    base_url: str = "https://api.kite.trade"
    timeout: int = 30
    
    # Data preferences
    use_kite_primary: bool = True      # Use Kite as primary data source
    fallback_to_yahoo: bool = False    # Disable Yahoo fallback - Kite only!
    
    # Rate limiting
    requests_per_second: int = 10      # Kite allows 10 requests per second
    
    # Instrument mapping
    exchange: str = "NSE"              # Default exchange
    
    def is_configured(self) -> bool:
        """Check if Kite API is properly configured"""
        return bool(self.api_key and self.access_token)


@dataclass
class SystemConfig:
    """Overall system configuration"""
    market: MarketConfig = None
    analysis: AnalysisConfig = None
    trading: TradingConfig = None
    kite: KiteConfig = None
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Timezone settings
    timezone: str = "Asia/Kolkata"
    
    def __post_init__(self):
        if self.market is None:
            self.market = MarketConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.trading is None:
            self.trading = TradingConfig()
        if self.kite is None:
            self.kite = KiteConfig()


# Global configuration instance
config = SystemConfig()
