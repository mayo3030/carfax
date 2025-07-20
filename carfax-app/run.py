#!/usr/bin/env python3
"""
CARFAX VIN Checker - Main Application
Professional and Fast VIN Lookup Tool
"""

import os
import sys
from app import create_app

def main():
    """Main application entry point"""
    # Create Flask app
    app = create_app()
    
    # Get configuration
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting CARFAX VIN Checker...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    main() 