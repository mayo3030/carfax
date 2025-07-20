#!/usr/bin/env python3
"""
Quick CARFAX Scraper
Simple script to scrape CARFAX data for a VIN
"""

import sys
import os
from carfax_scraper import CarfaxScraper

def main():
    """Quick scraper main function"""
    if len(sys.argv) < 2:
        print("Usage: python quick_scraper.py <VIN>")
        print("Example: python quick_scraper.py 1HGBH41JXMN109186")
        sys.exit(1)
    
    vin = sys.argv[1].strip().upper()
    
    print(f"🚀 Quick CARFAX Scraper")
    print(f"📋 VIN: {vin}")
    print("=" * 50)
    
    # Create scraper
    scraper = CarfaxScraper()
    
    # Start scraping
    success = scraper.scrape_carfax(vin)
    
    if success:
        print("\n✅ Scraping completed!")
        print("📁 Check the 'output' folder for results")
    else:
        print("\n❌ Scraping failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 