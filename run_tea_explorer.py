#!/usr/bin/env python3
"""
Tea Collection Explorer - Application Launcher
Run this script to start the Tea Collection Explorer GUI application
"""

import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run the tea explorer
import tea_explorer

if __name__ == "__main__":
    print("="*60)
    print("  TEA COLLECTION EXPLORER")
    print("="*60)
    print("\nStarting the Tea Collection Explorer...")
    print("Features:")
    print("  • Browse 24+ tea varieties in database")
    print("  • Search by name, category, or flavor")
    print("  • View comprehensive tea guides")
    print("  • Explore tea history")
    print("  • Interactive world map of tea regions")
    print("\nLoading application...")
    print("="*60)
    print()
    
    tea_explorer.main()
