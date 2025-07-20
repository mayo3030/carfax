import subprocess
import time
import os
import sys
import argparse
from pathlib import Path

def check_chrome_installation(chrome_path):
    """Check if Chrome exists in the specified path"""
    if os.path.exists(chrome_path):
        return True
    return False

def check_user_profile(user_profile):
    """Check if profile directory exists"""
    if os.path.exists(user_profile):
        return True
    return False

def kill_chrome_processes():
    """Kill all Chrome processes"""
    try:
        os.system("taskkill /f /im chrome.exe >nul 2>&1")
        print("Killed existing Chrome processes")
        time.sleep(2)
    except Exception as e:
        print(f"Warning: {e}")

def validate_vin(vin):
    """Validate VIN number"""
    if not vin or len(vin) != 17:
        return False, "VIN must be 17 characters"
    
    # Check for valid characters
    valid_chars = set('ABCDEFGHJKLMNPRSTUVWXYZ0123456789')
    vin_chars = set(vin.upper())
    
    if not vin_chars.issubset(valid_chars):
        return False, "VIN contains invalid characters"
    
    return True, "VIN is valid"

def launch_chrome_with_profile(chrome_path, user_profile, profile_directory="Default", start_url="chrome://newtab/"):
    """Launch Chrome with specified profile"""
    try:
        subprocess.Popen([
            chrome_path,
            f'--user-data-dir={user_profile}',
            f'--profile-directory={profile_directory}',
            start_url,
            '--no-first-run',
            '--no-default-browser-check'
        ])
        print(f"Chrome launched successfully!")
        print(f"Path: {chrome_path}")
        print(f"Profile: {profile_directory}")
        print(f"URL: {start_url}")
        return True
    except Exception as e:
        print(f"Error launching Chrome: {e}")
        return False

def create_vin_search_script(vin):
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
    print("Chrome Launcher with Real Profile")
    print("=" * 50)
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Launch Chrome with CARFAX')
    parser.add_argument('vin', nargs='?', help='Vehicle VIN number')
    args = parser.parse_args()
    
    # Chrome path
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # User profile path - more flexible
    user_profile = r"C:\Users\En Mina\AppData\Local\Google\Chrome\User Data"
    
    # Check if path exists, if not use alternative
    if not check_user_profile(user_profile):
        # Try to find alternative path
        possible_paths = [
            r"C:\Users\En Mina\AppData\Local\Google\Chrome\User Data",
            r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data",
            r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if check_user_profile(expanded_path):
                user_profile = expanded_path
                break
    
    # Check Chrome installation
    if not check_chrome_installation(chrome_path):
        print(f"Chrome not found at: {chrome_path}")
        print("Make sure Chrome is installed or change the path")
        return False
    
    # Check profile existence
    if not check_user_profile(user_profile):
        print(f"Profile directory not found at: {user_profile}")
        print("Check the correct profile path")
        return False
    
    print("Chrome and profile verified")
    
    # Determine start URL
    if args.vin:
        # Validate VIN
        is_valid, message = validate_vin(args.vin)
        if not is_valid:
            print(f"{message}")
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
    kill_chrome_processes()
    
    # Launch Chrome
    success = launch_chrome_with_profile(
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