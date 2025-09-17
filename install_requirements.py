#!/usr/bin/env python3
"""
Install required packages for the TaskPriorityScheduler project
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    packages = [
        "flask>=2.0.0",
        "flask-sqlalchemy>=3.0.0",
        "sqlalchemy>=1.4.0",
        "werkzeug>=2.0.0",
        "email-validator>=1.1.0"
    ]
    
    print("Installing required packages for TaskPriorityScheduler...")
    print("=" * 50)
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("=" * 50)
    print(f"Installation complete: {success_count}/{len(packages)} packages installed successfully")
    
    if success_count == len(packages):
        print("\n✓ All packages installed successfully!")
        print("You can now run the project with:")
        print("  python run_dev.py")
    else:
        print(f"\n⚠ Some packages failed to install. Please install them manually.")

if __name__ == "__main__":
    main()