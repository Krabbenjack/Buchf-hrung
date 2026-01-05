"""
Library check module for verifying required dependencies.
Displays popup with installation instructions if any libraries are missing.
"""

import sys


def check_libraries():
    """
    Check if all required libraries are installed.
    
    Returns:
        bool: True if all libraries are installed, False otherwise
    """
    required_libraries = ['pandas', 'openpyxl', 'reportlab', 'tkinter']
    missing_libraries = []

    # Check each library
    for lib in required_libraries:
        try:
            __import__(lib)  # Try importing the library
        except ImportError:
            missing_libraries.append(lib)  # Add to missing list if ImportError is raised

    if missing_libraries:
        # Import tkinter for the popup (if available)
        show_popup = False
        try:
            import tkinter as tk
            from tkinter import messagebox
            show_popup = True
        except ImportError:
            pass  # tkinter not available, will use console output
        
        # Create a message with missing libraries and installation instructions
        libraries = ', '.join(missing_libraries)
        message = f"The following required libraries are missing: {libraries}.\n\n" \
                  "To install the missing libraries, open a command prompt or terminal and run:\n\n" \
                  "pip install pandas openpyxl reportlab\n\n" \
                  "If you're missing tkinter, it is usually included with Python.\n" \
                  "On Windows, you can install it by reinstalling Python from python.org."

        if show_popup:
            try:
                # Initialize the GUI window
                root = tk.Tk()
                root.withdraw()  # Hide the root window (we just need the popup)

                # Show popup message
                messagebox.showwarning("Missing Libraries", message)
                root.destroy()
            except Exception:
                # If popup fails (e.g., no display), fall back to console
                show_popup = False
        
        if not show_popup:
            # Print to console if popup not available or failed
            print("\n" + "="*60)
            print("ERROR: Missing Required Libraries")
            print("="*60)
            print(f"\nThe following required libraries are missing: {libraries}\n")
            print("To install the missing libraries, open a command prompt or terminal and run:\n")
            print("    pip install pandas openpyxl reportlab\n")
            print("If you're missing tkinter, it is usually included with Python.")
            print("On Windows, you can install it by reinstalling Python from python.org.\n")
            print("="*60 + "\n")
        
        return False
    
    return True


if __name__ == "__main__":
    # Allow testing the library check independently
    if not check_libraries():
        sys.exit(1)
    else:
        print("All required libraries are installed!")
