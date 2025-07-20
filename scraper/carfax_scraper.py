import requests
from bs4 import BeautifulSoup
import json
import time
import os
import sys
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CarfaxScraper:
    def __init__(self, chrome_path=None, user_profile=None):
        """Initialize the scraper"""
        self.chrome_path = chrome_path or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.user_profile = user_profile or r"C:\Users\En Mina\AppData\Local\Google\Chrome\User Data"
        self.driver = None
        self.data = {}
        
    def setup_driver(self):
        """Setup Chrome driver with profile"""
        try:
            chrome_options = Options()
            
            # Try with user profile first
            try:
                chrome_options.add_argument(f'--user-data-dir={self.user_profile}')
                chrome_options.add_argument('--profile-directory=Default')
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as profile_error:
                print(f"⚠️ Profile error: {profile_error}")
                print("🔄 Trying without user profile...")
                
                # Try without user profile
                chrome_options = Options()
                chrome_options.add_argument('--no-first-run')
                chrome_options.add_argument('--no-default-browser-check')
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup successfully")
            return True
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            return False
    
    def navigate_to_carfax(self, vin):
        """Navigate to CARFAX page with VIN"""
        try:
            url = f"https://www.carfaxonline.com/vhr/{vin}"
            print(f"🌐 Navigating to: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Page loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error navigating to CARFAX: {e}")
            return False
    
    def extract_vehicle_info(self):
        """Extract vehicle information"""
        try:
            print("🔍 Extracting vehicle information...")
            
            # Basic vehicle info
            vehicle_info = {}
            
            # Try to find vehicle title/name
            try:
                title_elements = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, .vehicle-title, .car-title")
                if title_elements:
                    vehicle_info['title'] = title_elements[0].text.strip()
            except:
                vehicle_info['title'] = "N/A"
            
            # Try to find year, make, model
            try:
                year_make_model = self.driver.find_elements(By.CSS_SELECTOR, ".year-make-model, .vehicle-info, .car-info")
                if year_make_model:
                    vehicle_info['year_make_model'] = year_make_model[0].text.strip()
            except:
                vehicle_info['year_make_model'] = "N/A"
            
            # Try to find VIN
            try:
                vin_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-vin], .vin, .vehicle-vin")
                if vin_elements:
                    vehicle_info['vin'] = vin_elements[0].text.strip()
            except:
                vehicle_info['vin'] = "N/A"
            
            self.data['vehicle_info'] = vehicle_info
            print("✅ Vehicle information extracted")
            
        except Exception as e:
            print(f"❌ Error extracting vehicle info: {e}")
    
    def extract_ownership_history(self):
        """Extract ownership history"""
        try:
            print("🔍 Extracting ownership history...")
            
            ownership_data = []
            
            # Look for ownership history sections
            ownership_sections = self.driver.find_elements(By.CSS_SELECTOR, ".ownership, .owner, .history-item")
            
            for section in ownership_sections:
                try:
                    owner_info = {
                        'text': section.text.strip(),
                        'html': section.get_attribute('innerHTML')
                    }
                    ownership_data.append(owner_info)
                except:
                    continue
            
            self.data['ownership_history'] = ownership_data
            print(f"✅ Ownership history extracted ({len(ownership_data)} items)")
            
        except Exception as e:
            print(f"❌ Error extracting ownership history: {e}")
    
    def extract_accident_history(self):
        """Extract accident history"""
        try:
            print("🔍 Extracting accident history...")
            
            accident_data = []
            
            # Look for accident history sections
            accident_sections = self.driver.find_elements(By.CSS_SELECTOR, ".accident, .damage, .crash, .incident")
            
            for section in accident_sections:
                try:
                    accident_info = {
                        'text': section.text.strip(),
                        'html': section.get_attribute('innerHTML')
                    }
                    accident_data.append(accident_info)
                except:
                    continue
            
            self.data['accident_history'] = accident_data
            print(f"✅ Accident history extracted ({len(accident_data)} items)")
            
        except Exception as e:
            print(f"❌ Error extracting accident history: {e}")
    
    def extract_service_history(self):
        """Extract service history"""
        try:
            print("🔍 Extracting service history...")
            
            service_data = []
            
            # Look for service history sections
            service_sections = self.driver.find_elements(By.CSS_SELECTOR, ".service, .maintenance, .repair")
            
            for section in service_sections:
                try:
                    service_info = {
                        'text': section.text.strip(),
                        'html': section.get_attribute('innerHTML')
                    }
                    service_data.append(service_info)
                except:
                    continue
            
            self.data['service_history'] = service_data
            print(f"✅ Service history extracted ({len(service_data)} items)")
            
        except Exception as e:
            print(f"❌ Error extracting service history: {e}")
    
    def extract_page_content(self):
        """Extract all page content"""
        try:
            print("🔍 Extracting page content...")
            
            # Get page title
            self.data['page_title'] = self.driver.title
            
            # Get page URL
            self.data['page_url'] = self.driver.current_url
            
            # Get all text content
            body = self.driver.find_element(By.TAG_NAME, "body")
            self.data['page_content'] = body.text
            
            # Get all links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            self.data['links'] = [link.get_attribute('href') for link in links if link.get_attribute('href')]
            
            # Get all images
            images = self.driver.find_elements(By.TAG_NAME, "img")
            self.data['images'] = [img.get_attribute('src') for img in images if img.get_attribute('src')]
            
            print("✅ Page content extracted")
            
        except Exception as e:
            print(f"❌ Error extracting page content: {e}")
    
    def save_data(self, vin, output_dir="output"):
        """Save extracted data to files"""
        try:
            # Create output directory
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/carfax_{vin}_{timestamp}"
            
            # Save as JSON
            json_file = f"{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to JSON: {json_file}")
            
            # Save as HTML
            html_file = f"{filename}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<html><head><title>CARFAX Data for {vin}</title></head><body>")
                f.write(f"<h1>CARFAX Data for VIN: {vin}</h1>")
                f.write(f"<p>Scraped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
                f.write(f"<p>URL: {self.data.get('page_url', 'N/A')}</p>")
                f.write("<hr>")
                
                # Vehicle Info
                if 'vehicle_info' in self.data:
                    f.write("<h2>Vehicle Information</h2>")
                    for key, value in self.data['vehicle_info'].items():
                        f.write(f"<p><strong>{key}:</strong> {value}</p>")
                
                # Ownership History
                if 'ownership_history' in self.data:
                    f.write("<h2>Ownership History</h2>")
                    for item in self.data['ownership_history']:
                        f.write(f"<div>{item['text']}</div>")
                
                # Accident History
                if 'accident_history' in self.data:
                    f.write("<h2>Accident History</h2>")
                    for item in self.data['accident_history']:
                        f.write(f"<div>{item['text']}</div>")
                
                # Service History
                if 'service_history' in self.data:
                    f.write("<h2>Service History</h2>")
                    for item in self.data['service_history']:
                        f.write(f"<div>{item['text']}</div>")
                
                f.write("</body></html>")
            print(f"✅ Data saved to HTML: {html_file}")
            
            # Save as TXT
            txt_file = f"{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"CARFAX Data for VIN: {vin}\n")
                f.write(f"Scraped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"URL: {self.data.get('page_url', 'N/A')}\n")
                f.write("=" * 50 + "\n\n")
                
                # Vehicle Info
                if 'vehicle_info' in self.data:
                    f.write("VEHICLE INFORMATION:\n")
                    for key, value in self.data['vehicle_info'].items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
                
                # Page Content
                if 'page_content' in self.data:
                    f.write("PAGE CONTENT:\n")
                    f.write(self.data['page_content'])
                    f.write("\n")
            
            print(f"✅ Data saved to TXT: {txt_file}")
            
            return json_file, html_file, txt_file
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return None, None, None
    
    def scrape_carfax(self, vin):
        """Main scraping function"""
        try:
            print(f"🚀 Starting CARFAX scraping for VIN: {vin}")
            print("=" * 50)
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Navigate to CARFAX
            if not self.navigate_to_carfax(vin):
                return False
            
            # Wait for page to load completely
            time.sleep(5)
            
            # Extract data
            self.extract_vehicle_info()
            self.extract_ownership_history()
            self.extract_accident_history()
            self.extract_service_history()
            self.extract_page_content()
            
            # Save data
            json_file, html_file, txt_file = self.save_data(vin)
            
            print("\n🎉 Scraping completed successfully!")
            print(f"📁 Files saved:")
            if json_file: print(f"   - JSON: {json_file}")
            if html_file: print(f"   - HTML: {html_file}")
            if txt_file: print(f"   - TXT: {txt_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='CARFAX Data Scraper')
    parser.add_argument('vin', help='Vehicle VIN number')
    parser.add_argument('--output', '-o', default='output', help='Output directory')
    parser.add_argument('--chrome-path', help='Chrome executable path')
    parser.add_argument('--user-profile', help='Chrome user profile path')
    
    args = parser.parse_args()
    
    # Create scraper instance
    scraper = CarfaxScraper(
        chrome_path=args.chrome_path,
        user_profile=args.user_profile
    )
    
    # Start scraping
    success = scraper.scrape_carfax(args.vin)
    
    if success:
        print("\n✅ Scraping completed successfully!")
    else:
        print("\n❌ Scraping failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 