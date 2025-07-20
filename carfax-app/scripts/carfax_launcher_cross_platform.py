#!/usr/bin/env python3
"""
CARFAX Launcher - Cross-Platform Version
Compatible with Windows, Linux, and macOS
"""

import subprocess
import time
import os
import sys
import argparse
import platform
from pathlib import Path

class ChromeLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.chrome_paths = self._get_chrome_paths()
        self.user_profile_paths = self._get_user_profile_paths()
    
    def _get_chrome_paths(self):
        """Get Chrome executable paths for different systems"""
        if self.system == "windows":
            return [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe"
            ]
        elif self.system == "darwin":  # macOS
            return [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser"
            ]
        else:  # Linux
            return [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
                "/snap/bin/chromium"
            ]
    
    def _get_user_profile_paths(self):
        """Get user profile paths for different systems"""
        if self.system == "windows":
            username = os.getenv('USERNAME', '')
            return [
                rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data",
                r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data",
                r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
            ]
        elif self.system == "darwin":  # macOS
            home = os.path.expanduser("~")
            return [
                f"{home}/Library/Application Support/Google/Chrome",
                f"{home}/Library/Application Support/Chromium"
            ]
        else:  # Linux
            home = os.path.expanduser("~")
            return [
                f"{home}/.config/google-chrome",
                f"{home}/.config/chromium",
                f"{home}/.config/chrome"
            ]
    
    def find_chrome(self):
        """Find Chrome executable"""
        for path in self.chrome_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        
        # Try to find Chrome using system commands
        try:
            if self.system == "windows":
                result = subprocess.run(['where', 'chrome'], capture_output=True, text=True)
            else:
                result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return None
    
    def find_user_profile(self):
        """Find user profile directory"""
        for path in self.user_profile_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        return None
    
    def kill_chrome_processes(self):
        """Kill Chrome processes based on system"""
        try:
            if self.system == "windows":
                subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], 
                             capture_output=True, check=False)
            elif self.system == "darwin":  # macOS
                subprocess.run(["pkill", "-f", "Google Chrome"], 
                             capture_output=True, check=False)
            else:  # Linux
                subprocess.run(["pkill", "-f", "chrome"], 
                             capture_output=True, check=False)
            
            print("Killed existing Chrome processes")
            time.sleep(2)
        except Exception as e:
            print(f"Warning: Could not kill Chrome processes: {e}")
    
    def validate_vin(self, vin):
        """Validate VIN number"""
        if not vin or len(vin) != 17:
            return False, "VIN must be 17 characters"
        
        # Check for valid characters
        valid_chars = set('ABCDEFGHJKLMNPRSTUVWXYZ0123456789')
        vin_chars = set(vin.upper())
        
        if not vin_chars.issubset(valid_chars):
            return False, "VIN contains invalid characters"
        
        return True, "VIN is valid"
    
    def launch_chrome(self, chrome_path, user_profile, profile_directory="Default", start_url="chrome://newtab/"):
        """Launch Chrome with specified profile"""
        try:
            args = [
                chrome_path,
                f'--user-data-dir={user_profile}',
                f'--profile-directory={profile_directory}',
                start_url,
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
            
            # Add system-specific arguments
            if self.system == "darwin":  # macOS
                args.append('--disable-gpu-sandbox')
            elif self.system != "windows":  # Linux
                args.append('--no-sandbox')
            
            subprocess.Popen(args)
            print(f"Chrome launched successfully!")
            print(f"Path: {chrome_path}")
            print(f"Profile: {profile_directory}")
            print(f"URL: {start_url}")
            return True
        except Exception as e:
            print(f"Error launching Chrome: {e}")
            return False
    
    def create_vin_search_script(self, vin):
        """Create JavaScript to search for VIN on CARFAX"""
        script = f"""
        // Wait for page to load
        setTimeout(function() {{
            // Look for VIN search input field
            var vinInput = document.querySelector('input[placeholder*="VIN"], input[name*="vin"], input[id*="vin"]');
            
            if (vinInput) {{
                // Clear and enter VIN
                vinInput.value = '{vin}';
                vinInput.focus();
                
                // Trigger input event
                var event = new Event('input', {{ bubbles: true }});
                vinInput.dispatchEvent(event);
                
                console.log('VIN entered: {vin}');
            }} else {{
                console.log('VIN input field not found');
            }}
        }}, 3000);
        """
        return script

def main():
    """Main function"""
    print("CARFAX Chrome Launcher - Cross-Platform")
    print("=" * 50)
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Launch Chrome with CARFAX')
    parser.add_argument('vin', nargs='?', help='Vehicle VIN number')
    parser.add_argument('--chrome-path', help='Custom Chrome executable path')
    parser.add_argument('--profile-path', help='Custom user profile path')
    args = parser.parse_args()
    
    # Initialize launcher
    launcher = ChromeLauncher()
    
    # Find Chrome
    chrome_path = args.chrome_path or launcher.find_chrome()
    if not chrome_path:
        print("Chrome not found!")
        print("Please install Chrome or specify the path using --chrome-path")
        return False
    
    print(f"Chrome found at: {chrome_path}")
    
    # Find user profile
    user_profile = args.profile_path or launcher.find_user_profile()
    if not user_profile:
        print("User profile not found!")
        print("Please specify the profile path using --profile-path")
        return False
    
    print(f"User profile found at: {user_profile}")
    
    # Determine start URL
    if args.vin:
        # Validate VIN
        is_valid, message = launcher.validate_vin(args.vin)
        if not is_valid:
            print(f"Invalid VIN: {message}")
            return False
        
        print(f"VIN entered: {args.vin}")
        # Open CARFAX VHR page with VIN
        start_url = f"https://www.carfaxonline.com/vhr/{args.vin}"
        print("Opening CARFAX VHR page with VIN")
    else:
        # Regular URL without VIN
        start_url = "https://www.carfaxonline.com/"
        print("No VIN specified, opening main CARFAX")
    
    # Kill existing Chrome processes
    launcher.kill_chrome_processes()
    
    # Launch Chrome
    success = launcher.launch_chrome(
        chrome_path=chrome_path,
        user_profile=user_profile,
        profile_directory="Default",
        start_url=start_url
    )
    
    if success:
        print("\nChrome launched successfully!")
        if args.vin:
            print(f"Opened CARFAX VHR page with VIN: {args.vin}")
            print(f"URL: https://www.carfaxonline.com/vhr/{args.vin}")
        else:
            print("Opened main CARFAX")
    else:
        print("\nFailed to launch Chrome")
    
    return success

if __name__ == "__main__":
    main() 