"""
Main entry point for the booking application.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Check for required libraries before importing other modules
from library_check import check_libraries

if not check_libraries():
    sys.exit(1)  # Exit if libraries are missing

# Continue with imports if all libraries are present
import tkinter as tk
from gui import BuchfuehrungGUI


def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = BuchfuehrungGUI(root)
    app.run()


if __name__ == "__main__":
    main()
