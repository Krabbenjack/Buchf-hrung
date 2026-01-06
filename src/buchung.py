"""
buchung.py
Booking logic and data persistence - no UI code.
"""

import json
import os
from datetime import datetime

# Path to buchungen.json
BUCHUNGEN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "buchungen.json")


class Buchung:
    """Represents a single booking entry."""
    
    def __init__(self, data):
        """
        Initialize a Buchung from a dictionary.
        
        Args:
            data: Dictionary with booking data
        """
        self.datum = data.get("datum", "")
        self.gegenkonto = data.get("gegenkonto", "")
        self.beschreibung = data.get("beschreibung", "")
        self.kundennummer = data.get("kundennummer", "")
        self.rechnungsnummer = data.get("rechnungsnummer", "")
        self.rechnungsdatum = data.get("rechnungsdatum", "")
        self.mwst = data.get("mwst", "")
        self.konto = data.get("konto", "")
        
        # Convert soll/haben to float, defaulting to 0.0
        try:
            self.soll = float(data.get("soll", 0) or 0)
        except (ValueError, TypeError):
            self.soll = 0.0
        
        try:
            self.haben = float(data.get("haben", 0) or 0)
        except (ValueError, TypeError):
            self.haben = 0.0
        
        self.lfd_nr = data.get("lfd_nr", 0)


class BuchungManager:
    """Manages booking data - loading, saving, and navigation."""
    
    def __init__(self):
        """Initialize the booking manager."""
        self.buchungen = []
        self.index = 0
        self.load_buchungen()
    
    def load_buchungen(self):
        """Load bookings from JSON file."""
        try:
            with open(BUCHUNGEN_FILE, "r", encoding="utf-8") as f:
                self.buchungen = json.load(f)
            if self.buchungen:
                self.index = len(self.buchungen) - 1
        except FileNotFoundError:
            self.buchungen = []
            self.index = 0
    
    def save_buchungen(self):
        """Save all bookings to JSON file."""
        with open(BUCHUNGEN_FILE, "w", encoding="utf-8") as f:
            json.dump(self.buchungen, f, ensure_ascii=False, indent=4)
    
    def get_current_buchung(self):
        """
        Get the current booking.
        
        Returns:
            dict: Current booking data or None if no bookings exist
        """
        if 0 <= self.index < len(self.buchungen):
            return self.buchungen[self.index]
        return None
    
    def save_current_buchung(self, buchung_data):
        """
        Save or update the current booking.
        
        Args:
            buchung_data: Dictionary with booking data
        """
        # Add default date if not provided
        if not buchung_data.get("datum"):
            buchung_data["datum"] = datetime.now().strftime("%Y-%m-%d")
        
        # Set lfd_nr (sequential number)
        buchung_data["lfd_nr"] = self.index + 2
        
        # Update existing or append new
        if self.index < len(self.buchungen):
            self.buchungen[self.index] = buchung_data
        else:
            self.buchungen.append(buchung_data)
            self.index = len(self.buchungen) - 1
        
        self.save_buchungen()
    
    def navigate_previous(self):
        """
        Navigate to previous booking.
        
        Returns:
            bool: True if navigation was successful, False otherwise
        """
        if self.index > 0:
            self.index -= 1
            return True
        return False
    
    def navigate_next(self):
        """
        Navigate to next booking.
        
        Returns:
            bool: True if navigation was successful, False otherwise
        """
        if self.index < len(self.buchungen) - 1:
            self.index += 1
            return True
        return False
    
    def get_buchungen_count(self):
        """
        Get total number of bookings.
        
        Returns:
            int: Number of bookings
        """
        return len(self.buchungen)
    
    def get_current_index(self):
        """
        Get current booking index.
        
        Returns:
            int: Current index
        """
        return self.index
    
    def get_buchungen_by_month(self, year, month):
        """
        Get all bookings for a specific month.
        
        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            
        Returns:
            list: List of Buchung objects for the specified month
        """
        result = []
        for buchung_data in self.buchungen:
            datum = buchung_data.get("datum", "")
            # Try to parse date in various formats
            try:
                # Try YYYY-MM-DD format
                if "-" in datum:
                    parts = datum.split("-")
                    if len(parts) == 3:
                        b_year = int(parts[0])
                        b_month = int(parts[1])
                        if b_year == year and b_month == month:
                            result.append(Buchung(buchung_data))
                # Try DD.MM.YY format
                elif "." in datum:
                    parts = datum.split(".")
                    if len(parts) == 3:
                        b_month = int(parts[1])
                        b_year = int(parts[2])
                        # Handle 2-digit year
                        if b_year < 100:
                            b_year += 2000
                        if b_year == year and b_month == month:
                            result.append(Buchung(buchung_data))
            except (ValueError, IndexError):
                pass  # Skip invalid dates
        return result
    
    def get_buchungen_by_year(self, year):
        """
        Get all bookings for a specific year.
        
        Args:
            year: Year (e.g., 2024)
            
        Returns:
            list: List of Buchung objects for the specified year
        """
        result = []
        for buchung_data in self.buchungen:
            datum = buchung_data.get("datum", "")
            try:
                # Try YYYY-MM-DD format
                if "-" in datum:
                    parts = datum.split("-")
                    if len(parts) == 3:
                        b_year = int(parts[0])
                        if b_year == year:
                            result.append(Buchung(buchung_data))
                # Try DD.MM.YY format
                elif "." in datum:
                    parts = datum.split(".")
                    if len(parts) == 3:
                        b_year = int(parts[2])
                        # Handle 2-digit year
                        if b_year < 100:
                            b_year += 2000
                        if b_year == year:
                            result.append(Buchung(buchung_data))
            except (ValueError, IndexError):
                pass  # Skip invalid dates
        return result
