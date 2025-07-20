#!/usr/bin/env python3
"""
Get Local IP Address
Shows all available local IP addresses for network access
"""

import socket
import subprocess
import platform
import re

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def get_all_network_interfaces():
    """Get all network interfaces and their IPs"""
    interfaces = []
    
    try:
        if platform.system() == "Windows":
            # Windows command
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                current_adapter = ""
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(' '):
                        current_adapter = line
                    elif 'IPv4' in line and ':' in line:
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            if not ip.startswith('127.'):  # Skip localhost
                                interfaces.append({
                                    'adapter': current_adapter,
                                    'ip': ip
                                })
        else:
            # Linux/Mac command
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                current_adapter = ""
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(' '):
                        current_adapter = line.split(':')[0]
                    elif 'inet ' in line:
                        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            if not ip.startswith('127.'):  # Skip localhost
                                interfaces.append({
                                    'adapter': current_adapter,
                                    'ip': ip
                                })
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
    
    return interfaces

def main():
    """Main function"""
    print("🌐 Network Information for CARFAX VIN Checker")
    print("=" * 50)
    
    # Get primary local IP
    primary_ip = get_local_ip()
    print(f"📍 Primary Local IP: {primary_ip}")
    
    # Get all network interfaces
    interfaces = get_all_network_interfaces()
    
    if interfaces:
        print("\n📡 Available Network Interfaces:")
        print("-" * 30)
        for i, interface in enumerate(interfaces, 1):
            print(f"{i}. {interface['adapter']}")
            print(f"   IP: {interface['ip']}")
            print()
    
    print("🌍 Access URLs:")
    print("-" * 20)
    print(f"Local:     http://localhost:8080")
    print(f"Primary:   http://{primary_ip}:8080")
    
    if interfaces:
        for interface in interfaces:
            print(f"Network:   http://{interface['ip']}:8080")
    
    print("\n💡 Tips:")
    print("- Use the Network URLs to access from other devices")
    print("- Make sure your firewall allows connections on port 8080")
    print("- Other devices must be on the same network")
    
    return primary_ip

if __name__ == "__main__":
    main() 