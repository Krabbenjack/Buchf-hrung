"""
Main entry point for the Buchführung application.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Check for required libraries
try:
    from library_check import check_libraries
    check_libraries()
except ImportError:
    print("Warning: Could not check libraries. Continuing anyway.")

# Import and run the application
from buchung import BuchfuehrungApp

def main():
    """Main entry point."""
    # BuchfuehrungApp.__init__ calls self.root.mainloop() internally,
    # so the app will start and run until the window is closed
    app = BuchfuehrungApp()

if __name__ == "__main__":
    main()
