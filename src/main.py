"""
main.py
Application entry point for the bookkeeping application.
"""

import sys
from library_check import check_libraries
from ui import start_ui


def main():
    """Main entry point for the application."""
    # Check if all required libraries are installed
    if not check_libraries():
        print("\nBitte installieren Sie die fehlenden Bibliotheken und starten Sie die Anwendung erneut.")
        sys.exit(1)
    
    # Start the UI
    print("Starte Buchführungsanwendung...")
    start_ui()


if __name__ == "__main__":
    main()
