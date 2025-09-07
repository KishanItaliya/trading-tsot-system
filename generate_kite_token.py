#!/usr/bin/env python3
"""
Helper script to generate Kite API access token
"""

import sys
import os
import webbrowser
from urllib.parse import urlparse, parse_qs

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from kiteconnect import KiteConnect
    KITE_AVAILABLE = True
except ImportError:
    KITE_AVAILABLE = False

from trading_system.config.settings import config

def load_credentials():
    """Load API credentials"""
    # Try to load from file first
    cred_file = "kite_credentials.txt"
    if os.path.exists(cred_file):
        with open(cred_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith('API_KEY='):
                config.kite.api_key = line.split('=', 1)[1]
            elif line.startswith('API_SECRET='):
                config.kite.api_secret = line.split('=', 1)[1]
    
    # Try environment variables
    if not config.kite.api_key:
        config.kite.api_key = os.getenv('KITE_API_KEY', '')
    if not config.kite.api_secret:
        config.kite.api_secret = os.getenv('KITE_API_SECRET', '')
    
    return config.kite.api_key, config.kite.api_secret

def generate_login_url(api_key):
    """Generate login URL for OAuth flow"""
    return f"https://kite.trade/connect/login?api_key={api_key}&v=3"

def extract_request_token(redirect_url):
    """Extract request token from redirect URL"""
    try:
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'request_token' in query_params:
            return query_params['request_token'][0]
        else:
            print("❌ No request_token found in the URL")
            return None
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        return None

def generate_access_token(api_key, api_secret, request_token):
    """Generate access token using request token"""
    try:
        if not KITE_AVAILABLE:
            print("❌ kiteconnect library not installed. Run: pip install kiteconnect")
            return None
        
        kite = KiteConnect(api_key=api_key)
        data = kite.generate_session(request_token, api_secret=api_secret)
        
        return data['access_token']
        
    except Exception as e:
        print(f"❌ Error generating access token: {e}")
        return None

def save_access_token(access_token):
    """Save access token to credentials file"""
    try:
        cred_file = "kite_credentials.txt"
        
        # Read existing content
        lines = []
        if os.path.exists(cred_file):
            with open(cred_file, 'r') as f:
                lines = f.readlines()
        
        # Update or add access token
        token_found = False
        for i, line in enumerate(lines):
            if line.strip().startswith('ACCESS_TOKEN='):
                lines[i] = f"ACCESS_TOKEN={access_token}\n"
                token_found = True
                break
        
        if not token_found:
            lines.append(f"ACCESS_TOKEN={access_token}\n")
        
        # Write back to file
        with open(cred_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Access token saved to {cred_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving access token: {e}")
        return False

def main():
    """Main token generation flow"""
    print("="*60)
    print("KITE API ACCESS TOKEN GENERATOR")
    print("="*60)
    
    # Check if kiteconnect is available
    if not KITE_AVAILABLE:
        print("❌ kiteconnect library not installed")
        print("Please run: pip install kiteconnect")
        return False
    
    # Load credentials
    api_key, api_secret = load_credentials()
    
    if not api_key or not api_secret:
        print("❌ API Key or Secret not found")
        print("Please set up your credentials in 'kite_credentials.txt' or environment variables")
        print("Required: API_KEY and API_SECRET")
        return False
    
    print(f"✅ API Key: {api_key[:8]}...")
    print(f"✅ API Secret: {'*' * len(api_secret)}")
    
    # Generate login URL
    login_url = generate_login_url(api_key)
    print(f"\n📋 Step 1: Login URL Generated")
    print(f"URL: {login_url}")
    
    # Open browser automatically
    try:
        print(f"\n🌐 Opening browser automatically...")
        webbrowser.open(login_url)
        print("✅ Browser opened. Please complete the login process.")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please copy and paste the URL above into your browser.")
    
    print(f"\n📋 Step 2: Complete Login Process")
    print("1. Login with your Zerodha credentials")
    print("2. Authorize the app")
    print("3. You'll be redirected to a URL with request_token")
    print("4. Copy the complete redirect URL")
    
    # Get redirect URL from user
    print(f"\n📋 Step 3: Enter Redirect URL")
    redirect_url = input("Paste the complete redirect URL here: ").strip()
    
    if not redirect_url:
        print("❌ No URL provided")
        return False
    
    # Extract request token
    request_token = extract_request_token(redirect_url)
    
    if not request_token:
        print("❌ Could not extract request token from URL")
        print("Make sure you copied the complete redirect URL")
        return False
    
    print(f"✅ Request Token: {request_token[:10]}...")
    
    # Generate access token
    print(f"\n📋 Step 4: Generating Access Token")
    access_token = generate_access_token(api_key, api_secret, request_token)
    
    if not access_token:
        print("❌ Failed to generate access token")
        return False
    
    print(f"✅ Access Token Generated: {access_token[:10]}...")
    
    # Save access token
    print(f"\n📋 Step 5: Saving Access Token")
    if save_access_token(access_token):
        print("✅ Access token saved successfully")
    else:
        print("❌ Failed to save access token")
        print(f"Manual save required - Access Token: {access_token}")
    
    # Test the token
    print(f"\n📋 Step 6: Testing Integration")
    print("Run the following command to test:")
    print("python test_kite_integration.py")
    
    print(f"\n🎉 TOKEN GENERATION COMPLETE!")
    print("="*60)
    print("Your Kite API is now ready to use with real market data!")
    print("The access token is valid until the end of the trading day.")
    print("You'll need to regenerate it daily or implement auto-refresh.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
