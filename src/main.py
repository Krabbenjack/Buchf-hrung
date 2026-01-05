"""
Main entry point for the booking application.
"""

import tkinter as tk
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from gui import BuchfuehrungGUI


def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = BuchfuehrungGUI(root)
    app.run()


if __name__ == "__main__":
    main()
