#!/usr/bin/env python3
"""
CARFAX Project Backup Script
Creates a backup of the project with date and time in folder name
"""

import os
import shutil
import datetime
import sys
from pathlib import Path

def create_backup():
    """Create a backup of the project with date and time"""
    
    # Get current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # Create backup folder name
    backup_folder_name = f"backup_{timestamp}"
    
    # Get current directory (project root)
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    
    # Create backup path
    backup_path = parent_dir / backup_folder_name
    
    # Files and folders to exclude from backup
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.gitignore',
        '*.pyc',
        '*.pyo',
        '*.log',
        'node_modules',
        '.env',
        '.venv',
        'venv',
        'env',
        '.DS_Store',
        'Thumbs.db',
        '*.tmp',
        '*.temp'
    ]
    
    def should_exclude(path):
        """Check if path should be excluded from backup"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False
    
    def copy_directory(src, dst):
        """Copy directory with exclusions"""
        try:
            if dst.exists():
                shutil.rmtree(dst)
            
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*exclude_patterns))
            return True
        except Exception as e:
            print(f"❌ Error copying {src}: {e}")
            return False
    
    print("🚀 Creating CARFAX Project Backup...")
    print(f"📁 Source: {current_dir}")
    print(f"📁 Backup: {backup_path}")
    print(f"⏰ Timestamp: {timestamp}")
    print("=" * 50)
    
    # Create backup
    try:
        if copy_directory(current_dir, backup_path):
            print("✅ Backup created successfully!")
            print(f"📂 Backup location: {backup_path}")
            
            # Calculate backup size
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except:
                        pass
            
            # Convert to MB
            size_mb = total_size / (1024 * 1024)
            print(f"📊 Backup size: {size_mb:.2f} MB")
            print(f"📄 Files backed up: {file_count}")
            
        else:
            print("❌ Backup failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False
    
    print("=" * 50)
    print("🎉 Backup completed successfully!")
    return True

def main():
    """Main function"""
    print("🔧 CARFAX Project Backup Tool")
    print("=" * 30)
    
    # Check if we're in the project directory
    current_dir = Path.cwd()
    if not (current_dir / "carfax-app").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Make sure you're in the folder containing 'carfax-app'")
        return False
    
    # Create backup
    success = create_backup()
    
    if success:
        print("\n💡 Tips:")
        print("   - Keep your backups in a safe location")
        print("   - Consider using cloud storage for important backups")
        print("   - Regular backups help prevent data loss")
    
    return success

if __name__ == "__main__":
    main() 