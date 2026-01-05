"""
Account management module for loading accounts from konten.json.
Provides functions to load and organize account data dynamically.
"""

import json
import os
from typing import Dict, List


def load_konten() -> Dict:
    """
    Load accounts from konten.json file.
    
    Returns:
        Dictionary containing account categories with their colors and accounts.
        
    Raises:
        FileNotFoundError: If konten.json file is not found.
        json.JSONDecodeError: If the JSON file is malformed.
    """
    # Get the path to konten.json (data directory is one level up from src)
    konten_datei = os.path.join(os.path.dirname(__file__), '../data/Konten.json')
    
    if not os.path.exists(konten_datei):
        raise FileNotFoundError(f"Die Datei {konten_datei} wurde nicht gefunden!")
    
    with open(konten_datei, 'r', encoding='utf-8') as f:
        konten = json.load(f)
    
    return konten


def get_konten_by_color() -> Dict[str, List[str]]:
    """
    Get accounts grouped by their category color.
    
    Returns:
        Dictionary mapping colors to lists of account strings (format: "Name: Number").
    """
    konten_data = load_konten()
    grouped = {}
    
    for category, data in konten_data.items():
        color = data.get('farbe', '#FFFFFF')  # Default to white if no color
        konten_dict = data.get('konten', {})
        
        if color not in grouped:
            grouped[color] = []
        
        # Format accounts as "Name: Number" for backward compatibility
        for name, number in konten_dict.items():
            account_string = f"{name}: {number}"
            grouped[color].append(account_string)
    
    return grouped


def get_all_konten_list() -> List[str]:
    """
    Get a flat list of all accounts in format "Name: Number".
    
    Returns:
        List of all account strings sorted by account number.
    """
    konten_data = load_konten()
    all_konten = []
    
    for category, data in konten_data.items():
        konten_dict = data.get('konten', {})
        for name, number in konten_dict.items():
            account_string = f"{name}: {number}"
            all_konten.append((number, account_string))
    
    # Sort by account number
    all_konten.sort(key=lambda x: x[0])
    
    return [account for _, account in all_konten]


def get_konten_dict() -> Dict[str, str]:
    """
    Get accounts as a dictionary mapping account strings to colors.
    For backward compatibility with the old KONTEN format.
    
    Returns:
        Dictionary mapping account strings to their category colors.
    """
    konten_data = load_konten()
    konten_dict = {}
    
    for category, data in konten_data.items():
        color = data.get('farbe', '#FFFFFF')
        konten_items = data.get('konten', {})
        
        for name, number in konten_items.items():
            account_string = f"{name}: {number}"
            konten_dict[account_string] = color
    
    return konten_dict
