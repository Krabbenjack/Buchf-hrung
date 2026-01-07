"""
Account provider module for accessing account data.
Abstracts access to account data, initially from konten.py.
"""

import sys
import os

# Add data directory to path for konten import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
import konten  # Import from legacy konten.py


class KontenProvider:
    """Provides access to account data."""
    
    def __init__(self):
        """Initialize account provider."""
        # Load accounts from legacy konten.py
        self.konten_liste = konten.konten_liste
    
    def get_all_konten(self):
        """
        Get all accounts.
        
        Returns:
            List of account dictionaries with keys: nummer, bezeichnung, gruppe
        """
        return self.konten_liste
    
    def get_konto_by_nummer(self, nummer):
        """
        Get account by number.
        
        Args:
            nummer: Account number
            
        Returns:
            Account dictionary or None if not found
        """
        for konto in self.konten_liste:
            if konto["nummer"] == nummer:
                return konto
        return None
    
    def get_konten_by_gruppe(self, gruppe):
        """
        Get all accounts in a specific group.
        
        Args:
            gruppe: Group name
            
        Returns:
            List of account dictionaries
        """
        return [k for k in self.konten_liste if k["gruppe"] == gruppe]
    
    def get_farben(self):
        """
        Get color mapping for account groups.
        
        Returns:
            Dictionary mapping group names to colors
        """
        return {
            "Anlagen": "lightblue",
            "Finanzen": "lightgreen",
            "Privat": "lightyellow",
            "Erträge": "lightcyan",
            "Material": "lightpink",
            "Löhne": "orange",
            "Miete": "violet",
            "Steuern": "violet",
            "Versicherung": "lightgray",
            "Fahrzeug": "lightgray",
            "Werbung": "lightgray",
            "Reisen": "lightgray",
            "Allgemein": "wheat",
            "Fortbildung": "wheat",
            "Beratung": "wheat",
            "Betrieb": "wheat",
            "Serviceleistungen": "red",
            "Verkäufe": "gold"
        }
