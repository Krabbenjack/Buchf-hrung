"""
Booking module for managing financial bookings.
Handles creating, editing, deleting, and storing bookings in JSON format.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Import account loading functions from konten module
try:
    from konten import get_konten_by_color, get_konten_dict
except ImportError:
    # Fallback for when konten module is not available
    def get_konten_by_color() -> Dict[str, List[str]]:
        """Fallback implementation."""
        return {}
    
    def get_konten_dict() -> Dict[str, str]:
        """Fallback implementation."""
        return {}


class Buchung:
    """Represents a single financial booking entry."""
    
    def __init__(self, datum: str, beschreibung: str, konto: str, 
                 gegenkonto: str, soll: float = 0.0, haben: float = 0.0,
                 buchung_id: Optional[str] = None):
        """
        Initialize a booking entry.
        
        Args:
            datum: Date of booking in format YYYY-MM-DD
            beschreibung: Description of the booking
            konto: Account number/name
            gegenkonto: Counter account (1000-Kasse or 1200-SPK)
            soll: Debit amount
            haben: Credit amount
            buchung_id: Optional unique ID for the booking
        """
        self.datum = datum
        self.beschreibung = beschreibung
        self.konto = konto
        self.gegenkonto = gegenkonto
        self.soll = float(soll)
        self.haben = float(haben)
        self.buchung_id = buchung_id or self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the booking."""
        return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def to_dict(self) -> Dict:
        """Convert booking to dictionary for JSON serialization."""
        return {
            'id': self.buchung_id,
            'datum': self.datum,
            'beschreibung': self.beschreibung,
            'konto': self.konto,
            'gegenkonto': self.gegenkonto,
            'soll': self.soll,
            'haben': self.haben
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Buchung':
        """Create booking from dictionary."""
        return cls(
            datum=data['datum'],
            beschreibung=data['beschreibung'],
            konto=data['konto'],
            gegenkonto=data['gegenkonto'],
            soll=data.get('soll', 0.0),
            haben=data.get('haben', 0.0),
            buchung_id=data.get('id')
        )


class BuchungManager:
    """Manages all bookings and handles storage."""
    
    def __init__(self, data_file: str = 'data/buchungen.json'):
        """
        Initialize the booking manager.
        
        Args:
            data_file: Path to the JSON file storing bookings
        """
        self.data_file = data_file
        self.buchungen: List[Buchung] = []
        self._ensure_data_file()
        self.load_buchungen()
    
    def _ensure_data_file(self):
        """Ensure the data file and directory exist."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def load_buchungen(self):
        """Load bookings from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.buchungen = [Buchung.from_dict(b) for b in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.buchungen = []
    
    def save_buchungen(self):
        """Save all bookings to JSON file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            data = [b.to_dict() for b in self.buchungen]
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_buchung(self, buchung: Buchung):
        """Add a new booking."""
        self.buchungen.append(buchung)
        self.save_buchungen()
    
    def update_buchung(self, buchung_id: str, updated_buchung: Buchung):
        """Update an existing booking."""
        for i, b in enumerate(self.buchungen):
            if b.buchung_id == buchung_id:
                updated_buchung.buchung_id = buchung_id
                self.buchungen[i] = updated_buchung
                self.save_buchungen()
                return True
        return False
    
    def delete_buchung(self, buchung_id: str):
        """Delete a booking by ID."""
        self.buchungen = [b for b in self.buchungen if b.buchung_id != buchung_id]
        self.save_buchungen()
    
    def get_buchungen_by_month(self, year: int, month: int) -> List[Buchung]:
        """Get all bookings for a specific month."""
        return [b for b in self.buchungen 
                if b.datum.startswith(f"{year:04d}-{month:02d}")]
    
    def get_buchungen_by_year(self, year: int) -> List[Buchung]:
        """Get all bookings for a specific year."""
        return [b for b in self.buchungen 
                if b.datum.startswith(f"{year:04d}")]
    
    def get_all_buchungen(self) -> List[Buchung]:
        """Get all bookings."""
        return self.buchungen


# Maintain backward compatibility by providing KONTEN as a function
def get_konten() -> Dict[str, str]:
    """
    Get accounts dictionary for backward compatibility.
    
    Returns:
        Dictionary mapping account strings to their category colors.
    """
    return get_konten_dict()
