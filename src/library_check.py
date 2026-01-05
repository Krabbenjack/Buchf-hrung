"""
Library check module for verifying required dependencies.
Displays popup with installation instructions if any libraries are missing.
"""

import sys
import importlib.util

# Required libraries for the booking application
# Note: json is part of Python standard library and doesn't need checking
# tkinter comes bundled with Python but may need system-level installation
REQUIRED_LIBRARIES = ['pandas', 'openpyxl', 'reportlab', 'tkinter']

# Libraries that can be installed via pip (excludes tkinter which is bundled)
PIP_INSTALLABLE = ['pandas', 'openpyxl', 'reportlab']


def check_libraries():
    """
    Check if all required libraries are installed.
    
    Returns:
        bool: True if all libraries are installed, False otherwise
    """
    missing_libraries = []

    # Check each library
    for lib in REQUIRED_LIBRARIES:
        # Use find_spec to check if module exists without importing it
        if importlib.util.find_spec(lib) is None:
            missing_libraries.append(lib)

    if missing_libraries:
        # Import tkinter for the popup (if available)
        show_popup = False
        try:
            import tkinter as tk
            from tkinter import messagebox
            show_popup = True
        except ImportError:
            pass  # tkinter not available, will use console output
        
        # Separate pip-installable libraries from tkinter
        missing_pip = [lib for lib in missing_libraries if lib in PIP_INSTALLABLE]
        missing_tkinter = 'tkinter' in missing_libraries
        
        # Create a message with missing libraries and installation instructions
        libraries = ', '.join(missing_libraries)
        message = f"The following required libraries are missing: {libraries}.\n\n"
        
        if missing_pip:
            pip_command = f"pip install {' '.join(missing_pip)}"
            message += f"To install the missing libraries, open a command prompt or terminal and run:\n\n{pip_command}\n\n"
        
        if missing_tkinter:
            message += "If you're missing tkinter, it is usually included with Python.\n" \
                      "On Windows, you can install it by reinstalling Python from python.org."

        if show_popup:
            try:
                # Initialize the GUI window
                root = tk.Tk()
                root.withdraw()  # Hide the root window (we just need the popup)

                # Show popup message
                messagebox.showwarning("Missing Libraries", message)
                root.destroy()
            except (tk.TclError, RuntimeError) as e:
                # If popup fails (e.g., no display), fall back to console
                show_popup = False
        
        if not show_popup:
            # Print to console if popup not available or failed
            print("\n" + "="*60)
            print("ERROR: Missing Required Libraries")
            print("="*60)
            print(f"\nThe following required libraries are missing: {libraries}\n")
            if missing_pip:
                pip_command = f"pip install {' '.join(missing_pip)}"
                print("To install the missing libraries, open a command prompt or terminal and run:\n")
                print(f"    {pip_command}\n")
            if missing_tkinter:
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
