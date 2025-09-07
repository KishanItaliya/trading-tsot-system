# Kite API Setup Guide

## 🚀 Overview

This guide will help you set up Zerodha Kite API integration for real-time and historical market data. Kite API provides accurate, real-time NSE data directly from Zerodha's systems.

### ✨ **Latest Enhancements**
- **🎯 Pure Kite API Mode**: Yahoo Finance completely disabled when `fallback_to_yahoo = False`
- **🚀 Enhanced Batch Processing**: Process 1000+ stocks efficiently in configurable batches
- **🎨 Interactive HTML Reports**: Beautiful, responsive reports with click-to-expand features
- **📈📉 Bullish/Bearish Indicators**: Clear visual direction indicators for all trades
- **🔧 Corrected R:R Calculations**: Accurate risk-reward ratios using proper formulas
- **📱 Mobile-Optimized**: Reports work perfectly on all devices

## 📋 Prerequisites

1. **Zerodha Trading Account**: You need an active Zerodha trading account
2. **Kite Connect App**: Create a Kite Connect app on the Zerodha developer portal
3. **Python Environment**: Ensure you have the trading system environment set up

## 🔧 Step-by-Step Setup

### Step 1: Create Kite Connect App

1. **Visit Zerodha Developer Portal**
   - Go to https://developers.zerodha.com/
   - Login with your Zerodha credentials

2. **Create New App**
   - Click on "Create new app"
   - Fill in the details:
     - **App Name**: `NSE Trading System` (or any name you prefer)
     - **App Type**: `Connect`
     - **Redirect URL**: `http://localhost:8080` (for testing)
     - **Description**: `Personal trading system for NSE stock analysis`

3. **Get API Credentials**
   - After creating the app, you'll get:
     - **API Key** (Consumer Key)
     - **API Secret** (Consumer Secret)
   - Note these down securely

### Step 2: Install Dependencies

```bash
# Make sure you're in your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the updated requirements
pip install -r requirements.txt
```

### Step 3: Configure API Credentials

#### Option A: Using Credentials File (Recommended)

1. **Copy the template file**:
   ```bash
   cp kite_credentials_template.txt kite_credentials.txt
   ```

2. **Edit `kite_credentials.txt`**:
   ```
   API_KEY=your_actual_api_key_here
   API_SECRET=your_actual_api_secret_here
   ACCESS_TOKEN=your_access_token_here
   ```

#### Option B: Using Environment Variables

```bash
# On Linux/Mac
export KITE_API_KEY="your_api_key"
export KITE_API_SECRET="your_api_secret"
export KITE_ACCESS_TOKEN="your_access_token"

# On Windows
set KITE_API_KEY=your_api_key
set KITE_API_SECRET=your_api_secret
set KITE_ACCESS_TOKEN=your_access_token
```

### Step 4: Generate Access Token

The access token needs to be generated through the OAuth flow. Here's how:

#### Method 1: Manual Token Generation

1. **Create the login URL**:
   ```
   https://kite.trade/connect/login?api_key=YOUR_API_KEY&v=3
   ```

2. **Login Process**:
   - Replace `YOUR_API_KEY` with your actual API key
   - Visit the URL in your browser
   - Login with your Zerodha credentials
   - Authorize the app
   - You'll be redirected to your redirect URL with a `request_token`

3. **Generate Access Token**:
   ```python
   from kiteconnect import KiteConnect
   
   kite = KiteConnect(api_key="your_api_key")
   
   # Use the request_token from the redirect URL
   data = kite.generate_session("request_token_here", api_secret="your_api_secret")
   
   print(f"Access Token: {data['access_token']}")
   ```

#### Method 2: Using Our Helper Script

We'll create a helper script for token generation:

```bash
python generate_kite_token.py
```

### Step 5: Test the Integration

Run the test script to verify everything is working:

```bash
python test_kite_integration.py
```

Expected output:
```
✅ Configuration: Pass
✅ Connection: Pass  
✅ Current Price: Pass
✅ Historical Data: Pass
✅ Integrated System: Pass

🎯 REAL INFY PRICE: ₹1444.60
```

### Step 6: Run the Trading System

Now you can run the trading system with real data:

```bash
# Analyze single stock with real data
python main.py --symbol INFY

# Run complete screening with real data
python main.py --screening-only
```

## 🔒 Security Best Practices

### 1. Protect Your Credentials
- **Never commit** `kite_credentials.txt` to version control
- **Use environment variables** in production
- **Rotate tokens** regularly

### 2. API Rate Limits
- Kite API allows **10 requests per second**
- Our system automatically handles rate limiting
- Avoid making unnecessary API calls

### 3. Token Management
- **Access tokens expire** after each trading day
- **Regenerate tokens** daily or implement auto-refresh
- **Monitor API usage** to avoid hitting limits

## 📊 Data Comparison

### Before (Yahoo Finance - Sample Data):
```
INFY Current Price: ₹2,048.77 (Mock Data)
Data Source: Sample/Generated
Accuracy: ❌ Inaccurate
Real-time: ❌ No
```

### After (Kite API - Real Data):
```
INFY Current Price: ₹1,444.60 (Real Data)
Data Source: Zerodha Kite API
Accuracy: ✅ 100% Accurate
Real-time: ✅ Yes
```

## 🛠️ Configuration Options

You can customize the Kite API behavior in `src/trading_system/config/settings.py`:

```python
@dataclass
class KiteConfig:
    use_kite_primary: bool = True      # Use Kite as primary source
    fallback_to_yahoo: bool = False    # 🎯 DISABLED - Kite API only for real data!
    requests_per_second: int = 10      # Rate limiting
    timeout: int = 30                  # Request timeout
    exchange: str = "NSE"              # Default exchange
```

### 🎯 **Pure Kite API Mode**
With `fallback_to_yahoo = False`, the system now operates in **Pure Kite API Mode**:
- ✅ **No Yahoo Finance calls**: Eliminates all yfinance error messages
- ✅ **Real-time data only**: All data comes directly from Zerodha's systems  
- ✅ **Cleaner logs**: No more unnecessary error spam in console output
- ✅ **Faster processing**: No time wasted on failed Yahoo Finance attempts
- ✅ **Accurate prices**: Live NSE prices with proper timezone handling

## 🔄 Daily Workflow

### 1. Morning Setup (Before Market Opens)
```bash
# Generate new access token (if needed)
python generate_kite_token.py

# Test connection
python test_kite_integration.py

# Run screening
python main.py --screening-only
```

### 2. During Market Hours
```bash
# Get real-time analysis
python main.py --symbol RELIANCE

# Monitor specific stocks
python main.py --symbol INFY --symbol TCS --symbol HDFCBANK
```

### 3. After Market Close
```bash
# Complete analysis with charts
python main.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Kite API not configured"
**Solution**: Check your credentials in `kite_credentials.txt` or environment variables

#### 2. "Access token expired"
**Solution**: Generate a new access token using the OAuth flow

#### 3. "Rate limit exceeded"
**Solution**: The system handles this automatically, but reduce concurrent requests if needed

#### 4. "Instrument not found"
**Solution**: Check if the symbol exists on NSE. Use exact symbol names (e.g., "INFY", not "INFOSYS")

#### 5. "No data available"
**Solution**: Check if market is open, or if the symbol is actively traded

### Debug Mode

Run with debug logging to see detailed API interactions:

```bash
python main.py --symbol INFY --log-level DEBUG
```

## 📈 Benefits of Kite API Integration

### 1. **Real-time Data**
- Live prices during market hours
- Accurate historical data
- No delays or approximations

### 2. **Reliable Source**
- Direct from Zerodha's systems
- High uptime and availability
- Professional-grade data quality

### 3. **Comprehensive Coverage**
- All NSE stocks
- Multiple timeframes
- Volume and other indicators

### 4. **Cost Effective**
- Free for Zerodha account holders
- No additional data fees
- Unlimited API calls (within limits)

## 📞 Support

### Zerodha Support
- **Kite Connect Documentation**: https://kite.trade/docs/connect/v3/
- **Developer Forum**: https://forum.zerodha.com/
- **Support Email**: connect@zerodha.com

### System Support
- Check logs in `logs/` directory
- Run test scripts for diagnostics
- Review configuration settings

## 🎯 Next Steps

Once Kite API is set up:

1. **Verify Real Data**: Compare prices with your Zerodha app
2. **Run Daily Screening**: Use real data for opportunity detection
3. **Monitor Performance**: Track system accuracy with real data
4. **Customize Settings**: Adjust parameters based on real market behavior

Your trading system is now connected to real, live market data! 🚀
