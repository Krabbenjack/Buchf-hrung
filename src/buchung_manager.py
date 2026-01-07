"""
Booking manager module for loading, saving, and filtering bookings.
Handles all JSON file access for bookings.
"""

import json
import os
from datetime import datetime

from buchung_model import Buchung


BUCHUNGEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'buchungen.json')


class BuchungManager:
    """Manages bookings and provides data access methods."""
    
    def __init__(self, buchungen_file=BUCHUNGEN_FILE):
        self.buchungen_file = buchungen_file
        self.buchungen = []
        self.load_buchungen()
    
    def load_buchungen(self):
        """Load bookings from JSON file."""
        try:
            with open(self.buchungen_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.buchungen = [Buchung.from_dict(b) for b in data]
        except FileNotFoundError:
            self.buchungen = []
    
    def save_buchungen(self):
        """Save bookings to JSON file."""
        with open(self.buchungen_file, "w", encoding="utf-8") as f:
            data = [b.to_dict() for b in self.buchungen]
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def add_buchung(self, buchung):
        """Add a new booking."""
        self.buchungen.append(buchung)
        self.save_buchungen()
    
    def update_buchung(self, index, buchung):
        """Update an existing booking."""
        if 0 <= index < len(self.buchungen):
            self.buchungen[index] = buchung
            self.save_buchungen()
    
    def get_buchungen_by_month(self, year, month):
        """Get all bookings for a specific month."""
        result = []
        for b in self.buchungen:
            if b.datum:
                try:
                    # Try different date formats
                    date_obj = None
                    for fmt in ["%Y-%m-%d", "%d.%m.%y", "%d.%m.%Y"]:
                        try:
                            date_obj = datetime.strptime(b.datum, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if date_obj and date_obj.year == year and date_obj.month == month:
                        result.append(b)
                except Exception:
                    continue
        return result
    
    def get_buchungen_by_year(self, year):
        """Get all bookings for a specific year."""
        result = []
        for b in self.buchungen:
            if b.datum:
                try:
                    date_obj = None
                    for fmt in ["%Y-%m-%d", "%d.%m.%y", "%d.%m.%Y"]:
                        try:
                            date_obj = datetime.strptime(b.datum, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if date_obj and date_obj.year == year:
                        result.append(b)
                except Exception:
                    continue
        return result
