"""
konten_loader.py
Loads account data from konten.json and provides helper functions.
"""

import json
import os

# Path to konten.json relative to this file
KONTEN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "konten.json")

_konten_data = None


def load_konten():
    """
    Load account data from konten.json.
    
    Returns:
        dict: Dictionary with group names as keys, containing color and accounts
    """
    global _konten_data
    if _konten_data is None:
        with open(KONTEN_FILE, "r", encoding="utf-8") as f:
            _konten_data = json.load(f)
    return _konten_data


def get_all_accounts():
    """
    Get all accounts as a flat list.
    
    Returns:
        list: List of account dictionaries with keys: nummer, bezeichnung, gruppe
    """
    data = load_konten()
    accounts = []
    for group_name, group_data in data.items():
        for account in group_data["accounts"]:
            accounts.append({
                "nummer": account["nummer"],
                "bezeichnung": account["bezeichnung"],
                "gruppe": group_name
            })
    return accounts


def get_accounts_by_group(group_name):
    """
    Get all accounts belonging to a specific group.
    
    Args:
        group_name: Name of the group
        
    Returns:
        list: List of account dictionaries for the specified group
    """
    data = load_konten()
    if group_name not in data:
        return []
    
    accounts = []
    for account in data[group_name]["accounts"]:
        accounts.append({
            "nummer": account["nummer"],
            "bezeichnung": account["bezeichnung"],
            "gruppe": group_name
        })
    return accounts


def get_group_color(group_name):
    """
    Get the color code for a specific group.
    
    Args:
        group_name: Name of the group
        
    Returns:
        str: Color code (e.g., "#A7C7E7") or "white" if group not found
    """
    data = load_konten()
    if group_name in data:
        return data[group_name].get("color", "white")
    return "white"


def get_all_groups():
    """
    Get list of all group names.
    
    Returns:
        list: List of group names
    """
    data = load_konten()
    return list(data.keys())
