Buchführung - Booking Program

A Python project for managing and booking financial data for the annual financial statement.

Overview

The booking program is a desktop application for managing and recording financial data. It provides a user-friendly graphical interface (GUI) for creating, editing, and deleting bookings, generating monthly reports, and exporting data for the tax advisor.

Features
Core Features

Manage Bookings: Create, edit, and delete bookings

JSON Storage: All bookings are saved in data/buchungen.json

Account Selection: Color-coded account selection by groups (dynamically loaded from Konten.json)

Counter Accounts: Dropdown menu to choose between "1000 - Kasse" and "1200 - SPK"

Monthly Reports: Generate monthly reports with booking summaries

PDF Export: Export reports as PDF files

Tax Advisor Export: Special export feature for the tax advisor with account movements

User Interface

Clear booking list sorted by date

Form for entering new bookings

Color-coded account selection (colors defined in Konten.json)

Buttons for monthly reports and tax advisor export

Project Structure
```
Buchführung/
├── src/
│   ├── main.py              # Application entry point
│   ├── ui.py                # All Tkinter UI components
│   ├── buchung.py           # Booking logic and data persistence
│   ├── konten_loader.py     # Account loading from JSON
│   ├── library_check.py     # Dependency checker
│   ├── report.py            # Report generation and PDF export
│   └── steuerberater.py     # Tax advisor export
├── data/
│   ├── buchungen.json       # JSON database for bookings
│   └── konten.json          # Account definitions with categories and colors
├── assets/                  # Static files (icons, PDFs, etc.)
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore file
```

Installation
Prerequisites

Python 3.8 or higher

pip (Python Package Manager)

Steps

Clone the repository:

git clone https://github.com/Krabbenjack/Buchf-hrung.git
cd Buchf-hrung


Install the dependencies:

pip install -r requirements.txt

Checking for Missing Libraries

Upon opening the program, it will automatically check if the necessary libraries are installed. If any of the required libraries are missing, a popup window will inform you about the missing dependencies and provide instructions for installation.

The required libraries are:

pandas: Used for data manipulation and importing/exporting Excel files.

openpyxl: Required for reading and writing Excel files.

reportlab: Used for generating PDF reports.

json: Standard Python library for storing and loading booking data in JSON format.

tkinter: Provides the graphical user interface (GUI) for interacting with the program.

If any libraries are missing, the following instructions will be displayed in the popup:

pip install pandas openpyxl reportlab


In case tkinter is missing, you may need to reinstall Python with Tkinter included (usually bundled with Python).

Usage
Start the Application
python src/main.py

Create a Booking

Click "New Booking"

Fill out the form:

Date: Format YYYY-MM-DD (e.g., 2024-01-15)

Description: Description of the booking

Account: Click "Select" for the color-coded account selection

Counter Account: Choose between "1000 - Kasse" or "1200 - SPK"

Debit: Debit amount in EUR

Credit: Credit amount in EUR

Click "Save"

Edit a Booking

Double-click on a booking in the list or

Select a booking and click "Edit"

Modify the desired fields

Click "Save"

Delete a Booking

Select a booking from the list

Click "Delete"

Confirm deletion

Generate Monthly Report

Click "Monthly Report"

Enter the year and month

Click "Create"

Choose a location to save the PDF file

The monthly report includes:

Total number of bookings

Total debit and credit

Balance

Detailed list of bookings

Export for Tax Advisor

Click "Tax Advisor Export"

Enter the year and month

Click "Export"

Choose a location to save the PDF file

The tax advisor export includes:

Overview with the number of bookings and totals

Account movements (debit, credit, balance per account)

Detailed list of bookings

Accounts Plan

The application dynamically loads accounts from `data/konten.json`, which contains over 100 accounts organized in 18 categories:

- **Anlagen** (Assets): EDV-Software, Maschinen, PKW, etc.
- **Finanzen** (Finance): Kasse, SPK, Darlehen, Umsatzsteuer, etc.
- **Privat** (Private): Privat, Einkommensteuer, Krankenversicherung, etc.
- **Erträge** (Revenue): Privat-Einlagen, Zins-Erträge, etc.
- **Material** (Materials): Roh-Hilfs-Betriebsstoffe, Fremdleistungen, etc.
- **Löhne** (Wages): Löhne und Gehälter, Soziale Aufwendungen, etc.
- **Miete** (Rent): Miete Geschäftsräume, Gas/Strom/Wasser, etc.
- **Steuern** (Taxes): Gewerbesteuer, etc.
- **Versicherung** (Insurance): Versicherungen, Beiträge zu Verbänden, etc.
- **Fahrzeug** (Vehicle): Fahrzeugkosten, Kfz-Steuer, Benzin, etc.
- **Werbung** (Advertising): Werbekosten, Bewirtung, etc.
- **Reisen** (Travel): Reisekosten, etc.
- **Allgemein** (General): Porto, Telefon, Bürobedarf, etc.
- **Fortbildung** (Training): Zeitschriften, Fortbildung, etc.
- **Beratung** (Consulting): Rechts- und Beratungskosten, Buchführungskosten, etc.
- **Betrieb** (Operations): Betriebsbedarf, Werkzeuge, etc.
- **Serviceleistungen** (Services): Klavierstimmungen, Reparaturen, etc.
- **Verkäufe** (Sales): Kfz-Verkäufe, Anlagen-Verkäufe

Each category has an associated color for visual grouping in the GUI. You can add or modify accounts by editing the `data/konten.json` file.

Data Format

Bookings are saved as a JSON array in data/buchungen.json:

[
  {
    "id": "20240115120000000000",
    "datum": "2024-01-15",
    "beschreibung": "Büromaterial",
    "konto": "6850 - Büromaterial",
    "gegenkonto": "1000 - Kasse",
    "soll": 45.50,
    "haben": 0.0
  }
]

Development
Modules
**buchung.py**
- `Buchung`: Data model class for a booking
- `BuchungManager`: Manages all bookings and JSON storage
- Methods: `load_buchungen()`, `save_buchungen()`, `get_current_buchung()`, `save_current_buchung()`, `navigate_previous()`, `navigate_next()`, `get_buchungen_by_month()`, `get_buchungen_by_year()`

**konten_loader.py**
- `load_konten()`: Loads accounts from data/konten.json
- `get_all_accounts()`: Returns flat list of all accounts
- `get_accounts_by_group()`: Returns accounts for a specific group
- `get_group_color()`: Returns the color for a specific group
- `get_all_groups()`: Returns list of all group names

**ui.py**
- `BuchungUI`: Main UI window with all Tkinter components
- `create_widgets()`: Creates all UI elements (labels, entries, buttons)
- `open_konto_selector()`: Opens color-coded account selection popup
- `show_current_buchung()`: Displays current booking in UI
- `save_buchung()`: Saves current booking
- `prev_buchung()`, `next_buchung()`: Navigation methods

**library_check.py**
- `check_libraries()`: Checks if all required dependencies are installed
- Shows popup or console message with installation instructions if libraries are missing

**report.py**
- `ReportGenerator`: Generates monthly reports
- PDF export of reports with booking details

**steuerberater.py**
- `SteuerberaterExport`: Special export function for the tax advisor
- Account movements and booking summaries

Tests

The application can be manually tested:

Create, edit, and delete bookings

Generate monthly reports for different months

Generate tax advisor export

Verify data persistence (restarting the application)

License

See LICENSE file for details.

Author

Krabbenjack

Contributing

Contributions are welcome! Please create a pull request or open an issue for suggestions or bug reports.
