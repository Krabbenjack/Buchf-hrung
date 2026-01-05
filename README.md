Buchführung - Booking Program

A Python project for managing and booking financial data for the annual financial statement.

Overview

The booking program is a desktop application for managing and recording financial data. It provides a user-friendly graphical interface (GUI) for creating, editing, and deleting bookings, generating monthly reports, and exporting data for the tax advisor.

Features
Core Features

Manage Bookings: Create, edit, and delete bookings

JSON Storage: All bookings are saved in data/buchungen.json

Account Selection: Color-coded account selection by groups

Counter Accounts: Dropdown menu to choose between "1000 - Kasse" and "1200 - SPK"

Monthly Reports: Generate monthly reports with booking summaries

PDF Export: Export reports as PDF files

Tax Advisor Export: Special export feature for the tax advisor with account movements

User Interface

Clear booking list sorted by date

Form for entering new bookings

Color-coded account selection (Blue, Green, Orange, Red)

Buttons for monthly reports and tax advisor export

Project Structure
Buchf-hrung/
├── src/
│   ├── main.py              # Entry point of the application
│   ├── gui.py               # GUI components and dialogs
│   ├── buchung.py           # Booking management and data model
│   ├── report.py            # Report generation and PDF export
│   └── steuerberater.py     # Tax advisor export
├── data/
│   └── buchungen.json       # JSON database for bookings
├── assets/                  # Static files (icons, PDFs, etc.)
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore file

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

The application uses the following standard accounts:

Bank Accounts (Blue)

1000 - Kasse

1200 - SPK

1800 - Bank

Revenue Accounts (Green)

4000 - Erlöse

4100 - Sonstige Erlöse

Tax Accounts (Orange)

4900 - Umsatzsteuer

Expense Accounts (Red)

6000 - Wareneinkauf

6300 - Fremdleistungen

6800 - Sonstige Kosten

6820 - Versicherungen

6850 - Büromaterial

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
buchung.py

Buchung: Data model for a booking

BuchungManager: Manages all bookings and JSON storage

KONTEN: Standard account list with color coding

gui.py

BuchfuehrungGUI: Main window of the application

BuchungDialog: Dialog for creating/editing bookings

KontoSelectionDialog: Color-coded account selection

report.py

ReportGenerator: Generates monthly reports

PDF export of reports with booking details

steuerberater.py

SteuerberaterExport: Special export function for the tax advisor

Account movements and booking summaries

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
