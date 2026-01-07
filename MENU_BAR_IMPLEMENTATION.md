# Implementation Summary - Menu Bar and Steuerberater Integration

## Overview
This implementation adds a menu bar to the Buchführung application with functionality for:
1. Selecting counter accounts (Buchen Bank, Buchen Kasse)
2. Generating various reports (Gegenkonto, Zusammenfassung, Sparkasse, Kasse)

## Changes Made

### 1. Refactored `src/buchung.py`

#### Created Data Classes
- **`Buchung` class**: A data class representing a single booking entry with properties:
  - `datum`, `beschreibung`, `konto`, `gegenkonto`, `soll`, `haben`
  - `kundennummer`, `rechnungsnummer`, `rechnungsdatum`, `mwst`, `lfd_nr`
  - Methods: `to_dict()`, `from_dict()`

- **`BuchungManager` class**: Manages booking data with methods:
  - `load_buchungen()`: Load bookings from JSON file
  - `save_buchungen()`: Save bookings to JSON file
  - `add_buchung()`: Add a new booking
  - `update_buchung()`: Update existing booking
  - `get_buchungen_by_month(year, month)`: Filter bookings by month
  - `get_buchungen_by_year(year)`: Filter bookings by year

#### Renamed UI Class
- Renamed `Buchung` (old UI class) to `BuchfuehrungApp`
- Updated to use `BuchungManager` for data operations

#### Added Menu Bar
The `create_menu_bar()` method creates two menus:

**Buchen Menu:**
- "Buchen Bank" → calls `buchen_bank()` → sets counter account to "1200 - SPK"
- "Buchen Kasse" → calls `buchen_kasse()` → sets counter account to "1000 - Kasse"

**Berichte Menu:**
- "Bericht Gegenkonto" → generates counter account report
- "Bericht Zusammenfassung" → generates summary report
- "Bericht Sparkasse" → generates Sparkasse-specific report
- "Bericht Kasse" → generates Kasse-specific report

#### Counter Account Management
- Added `current_counter_account` instance variable (default: "1200 - SPK")
- Method `set_counter_account(account_type)`:
  - Sets counter account based on "Bank" or "Kasse"
  - Updates the Gegenkonto dropdown in the UI

#### Report Generation
- Method `_generate_report(report_type)`:
  1. Prompts user for year and month
  2. Validates input
  3. Asks for PDF save location
  4. Uses appropriate report generator:
     - `SteuerberaterExport` for: Gegenkonto, Sparkasse, Kasse
     - `ReportGenerator` for: Zusammenfassung
  5. Displays success/error messages

### 2. Created `src/main.py`

Entry point for the application:
- Checks for required libraries using `library_check.py`
- Imports and runs `BuchfuehrungApp`

### 3. Integration with Existing Modules

The refactored code now properly integrates with:
- **`src/report.py`**: `ReportGenerator` class
- **`src/steuerberater.py`**: `SteuerberaterExport` class

Both modules expect:
- A `BuchungManager` instance
- `Buchung` objects with properties: `datum`, `beschreibung`, `konto`, `gegenkonto`, `soll`, `haben`

## File Structure

```
Buchführung/
├── src/
│   ├── main.py              # Entry point (NEW)
│   ├── buchung.py           # Refactored with menu bar and data classes
│   ├── report.py            # Monthly report generator
│   ├── steuerberater.py     # Tax advisor export
│   └── library_check.py     # Dependency checker
├── data/
│   ├── buchungen.json       # Booking data
│   └── konten.py            # Account definitions
└── requirements.txt         # Dependencies
```

## How to Run

```bash
# From repository root
python src/main.py

# Or directly
python src/buchung.py
```

## Usage

### Setting Counter Account
1. Click "Buchen" menu
2. Select "Buchen Bank" or "Buchen Kasse"
3. The Gegenkonto dropdown will be updated accordingly
4. All new bookings will use this counter account by default

### Generating Reports
1. Click "Berichte" menu
2. Select desired report type
3. Enter year (e.g., 2025)
4. Enter month (1-12)
5. Choose save location for PDF
6. Report will be generated and saved

## Testing

All functionality has been tested:
- ✓ Buchung and BuchungManager classes work correctly
- ✓ Data serialization (to_dict/from_dict) works
- ✓ ReportGenerator and SteuerberaterExport can be instantiated
- ✓ PDF reports are generated successfully
- ✓ Date filtering (by month/year) works correctly
- ✓ All menu methods exist and are properly defined

## Technical Details

### Date Format Support
The `get_buchungen_by_month()` and `get_buchungen_by_year()` methods support multiple date formats:
- `%Y-%m-%d` (e.g., 2025-01-06)
- `%d.%m.%y` (e.g., 06.01.25)
- `%d.%m.%Y` (e.g., 06.01.2025)

### Counter Account Mapping
- Bank → 1200 (Account: "1200 - SPK")
- Kasse → 1000 (Account: "1000 - Kasse")

### Report Type Mapping
| Menu Item              | Report Generator      | Purpose                          |
|------------------------|----------------------|----------------------------------|
| Bericht Gegenkonto     | SteuerberaterExport  | Counter account movements        |
| Bericht Zusammenfassung| ReportGenerator      | Monthly summary                  |
| Bericht Sparkasse      | SteuerberaterExport  | Sparkasse-specific report        |
| Bericht Kasse          | SteuerberaterExport  | Kasse-specific report            |

## Compatibility

The refactored code maintains backward compatibility with existing data:
- Reads existing `buchungen.json` format
- Handles both old and new data structures
- Preserves all fields during save operations
