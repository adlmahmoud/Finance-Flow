#!/usr/bin/env python
"""
Quick Start Guide - FinanceFlow v2.0

This script helps you quickly get started with FinanceFlow.
"""

import os
import sys
from pathlib import Path


def print_banner():
    """Print application banner."""
    print("""
    ╔═══════════════════════════════════════╗
    ║   FinanceFlow v2.0 - Quick Start      ║
    ║   Modern Expense Management App       ║
    ╚═══════════════════════════════════════╝
    """)


def check_python_version():
    """Check if Python version is compatible."""
    print("📋 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor} (requires 3.11+)")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'flet',
        'sqlalchemy',
        'sqlmodel',
        'pydantic',
        'loguru',
        'cryptography',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing


def install_dependencies(missing_packages):
    """Offer to install missing dependencies."""
    print(f"\n⚙️  Missing packages: {', '.join(missing_packages)}")
    response = input("Would you like to install them? (y/n): ").lower()
    
    if response == 'y':
        print("Installing dependencies...")
        os.system('pip install -r requirements.txt')
        print("✓ Dependencies installed")
        return True
    return False


def check_database():
    """Check database setup."""
    print("\n💾 Checking database setup...")
    
    db_path = Path("data/finance_flow.db")
    if db_path.exists():
        print(f"   ✓ Database exists at {db_path}")
    else:
        print(f"   ℹ Database will be created on first run at {db_path}")


def show_default_credentials():
    """Show how to create test credentials."""
    print("\n👤 Default Test Credentials:")
    print("   When you start the app, click 'S'inscrire' (Sign Up)")
    print("   Then create an account with:")
    print("      Username: demo")
    print("      Password: Demo@1234")


def main():
    """Run quick start checks."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Please upgrade Python to 3.11 or later")
        return False
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        if not install_dependencies(missing):
            print("\n❌ Please install dependencies: pip install -r requirements.txt")
            return False
    
    # Check database
    check_database()
    
    # Show credentials
    show_default_credentials()
    
    # Ready to start
    print("\n✅ All checks passed!")
    print("\n🚀 Ready to start? Run:")
    print("   python main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
