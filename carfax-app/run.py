#!/usr/bin/env python3
"""
CARFAX VIN Checker - Main Application
Professional and Fast VIN Lookup Tool
"""

import os
import sys
from app import create_app

def get_local_ip():
    """Get local IP address for network access"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def main():
    """Main application entry point"""
    # Create Flask app
    app = create_app()
    
    # Get configuration
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Get local IP for network access
    local_ip = get_local_ip()
    
    print("🚀 Starting CARFAX VIN Checker...")
    print("=" * 50)
    print(f"📍 Local Access:  http://localhost:{port}")
    print(f"📍 Network Access: http://{local_ip}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"🌐 Host: {host}:{port}")
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