# Buchführung - Booking Program

Ein Python-Projekt für die Verwaltung und Buchung von Finanzdaten für die jährliche Finanzabrechnung.

## Übersicht

Das Buchführungsprogramm ist eine Desktop-Anwendung zur Verwaltung und Erfassung von Finanzdaten. Es bietet eine benutzerfreundliche grafische Oberfläche (GUI) für das Erstellen, Bearbeiten und Löschen von Buchungen, das Generieren von Monatsberichten und das Exportieren von Daten für den Steuerberater.

## Funktionen

### Kernfunktionen
- **Buchungen verwalten**: Erstellen, Bearbeiten und Löschen von Buchungen
- **JSON-Speicherung**: Alle Buchungen werden in `data/buchungen.json` gespeichert
- **Kontenauswahl**: Farbcodierte Kontenauswahl nach Gruppen
- **Gegenkonten**: Dropdown-Menü zur Auswahl zwischen "1000 - Kasse" und "1200 - SPK"
- **Monatliche Berichte**: Generierung von Monatsberichten mit Buchungsübersicht
- **PDF-Export**: Export von Berichten als PDF-Dateien
- **Steuerberater-Export**: Spezielle Exportfunktion für den Steuerberater mit Kontenbewegungen

### Benutzeroberfläche
- Übersichtliche Buchungsliste mit Sortierung nach Datum
- Formular zur Eingabe neuer Buchungen
- Farbcodierte Kontenauswahl (Blau, Grün, Orange, Rot)
- Schaltflächen für Monatsbericht und Steuerberater-Export

## Projektstruktur

```
Buchf-hrung/
├── src/
│   ├── main.py              # Einstiegspunkt der Anwendung
│   ├── gui.py               # GUI-Komponenten und Dialoge
│   ├── buchung.py           # Buchungsverwaltung und Datenmodell
│   ├── report.py            # Berichtsgenerierung und PDF-Export
│   └── steuerberater.py     # Steuerberater-Export
├── data/
│   └── buchungen.json       # JSON-Datenbank für Buchungen
├── assets/                  # Statische Dateien (Icons, PDFs, etc.)
├── requirements.txt         # Python-Abhängigkeiten
├── README.md               # Diese Datei
└── .gitignore              # Git-Ignore-Datei
```

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritte

1. Repository klonen:
```bash
git clone https://github.com/Krabbenjack/Buchf-hrung.git
cd Buchf-hrung
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

### Anwendung starten

```bash
python src/main.py
```

### Buchung erstellen

1. Klicken Sie auf "Neue Buchung"
2. Füllen Sie das Formular aus:
   - **Datum**: Format YYYY-MM-DD (z.B. 2024-01-15)
   - **Beschreibung**: Beschreibung der Buchung
   - **Konto**: Klicken Sie auf "Auswählen" für die farbcodierte Kontenauswahl
   - **Gegenkonto**: Wählen Sie zwischen "1000 - Kasse" oder "1200 - SPK"
   - **Soll**: Sollbetrag in Euro
   - **Haben**: Habenbetrag in Euro
3. Klicken Sie auf "Speichern"

### Buchung bearbeiten

1. Doppelklicken Sie auf eine Buchung in der Liste oder
2. Wählen Sie eine Buchung aus und klicken Sie auf "Bearbeiten"
3. Ändern Sie die gewünschten Felder
4. Klicken Sie auf "Speichern"

### Buchung löschen

1. Wählen Sie eine Buchung aus der Liste
2. Klicken Sie auf "Löschen"
3. Bestätigen Sie die Löschung

### Monatsbericht erstellen

1. Klicken Sie auf "Monatsbericht"
2. Geben Sie Jahr und Monat ein
3. Klicken Sie auf "Erstellen"
4. Wählen Sie einen Speicherort für die PDF-Datei

Der Monatsbericht enthält:
- Gesamtanzahl der Buchungen
- Gesamt Soll und Haben
- Saldo
- Detaillierte Buchungsliste

### Steuerberater-Export

1. Klicken Sie auf "Steuerberater Export"
2. Geben Sie Jahr und Monat ein
3. Klicken Sie auf "Exportieren"
4. Wählen Sie einen Speicherort für die PDF-Datei

Der Steuerberater-Export enthält:
- Übersicht mit Anzahl Buchungen und Summen
- Kontenbewegungen (Soll, Haben, Saldo pro Konto)
- Detaillierte Buchungsliste

## Kontenplan

Die Anwendung verwendet folgende Standardkonten:

### Bankkonten (Blau)
- 1000 - Kasse
- 1200 - SPK
- 1800 - Bank

### Erlöskonten (Grün)
- 4000 - Erlöse
- 4100 - Sonstige Erlöse

### Steuerkonten (Orange)
- 4900 - Umsatzsteuer

### Kostenkonten (Rot)
- 6000 - Wareneinkauf
- 6300 - Fremdleistungen
- 6800 - Sonstige Kosten
- 6820 - Versicherungen
- 6850 - Büromaterial

## Datenformat

Buchungen werden als JSON-Array in `data/buchungen.json` gespeichert:

```json
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
```

## Entwicklung

### Module

#### buchung.py
- `Buchung`: Datenmodell für eine Buchung
- `BuchungManager`: Verwaltung aller Buchungen und JSON-Speicherung
- `KONTEN`: Standardkontenliste mit Farbzuordnung

#### gui.py
- `BuchfuehrungGUI`: Hauptfenster der Anwendung
- `BuchungDialog`: Dialog zum Erstellen/Bearbeiten von Buchungen
- `KontoSelectionDialog`: Farbcodierte Kontenauswahl

#### report.py
- `ReportGenerator`: Generierung von Monatsberichten
- PDF-Export von Berichten mit Buchungsdetails

#### steuerberater.py
- `SteuerberaterExport`: Spezielle Exportfunktion für Steuerberater
- Kontenbewegungen und Buchungszusammenfassungen

### Tests

Die Anwendung kann manuell getestet werden:
1. Buchungen erstellen, bearbeiten und löschen
2. Monatsbericht für verschiedene Monate generieren
3. Steuerberater-Export erstellen
4. Datenpersistenz überprüfen (Neustart der Anwendung)

## Lizenz

Siehe LICENSE-Datei für Details.

## Autor

Krabbenjack

## Mitwirken

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Verbesserungsvorschläge oder Fehlermeldungen.
