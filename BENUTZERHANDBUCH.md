# Buchführung - Benutzerhandbuch

## Inhaltsverzeichnis
1. [Installation](#installation)
2. [Erste Schritte](#erste-schritte)
3. [Hauptfunktionen](#hauptfunktionen)
4. [Buchungen verwalten](#buchungen-verwalten)
5. [Berichte erstellen](#berichte-erstellen)
6. [Steuerberater-Export](#steuerberater-export)
7. [Häufig gestellte Fragen](#häufig-gestellte-fragen)

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)
- tkinter (in den meisten Python-Installationen enthalten)

### Schnellstart

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

**Manuell:**
```bash
pip install -r requirements.txt
```

## Erste Schritte

### Anwendung starten
```bash
python src/main.py
```

### Beispieldaten erstellen (optional)
Um die Anwendung mit Beispieldaten zu testen:
```bash
python create_sample_data.py
```

## Hauptfunktionen

### Übersicht der Benutzeroberfläche

Die Hauptoberfläche besteht aus:
- **Schaltflächen-Leiste**: Neue Buchung, Bearbeiten, Löschen, Monatsbericht, Steuerberater Export
- **Buchungsliste**: Tabelle mit allen Buchungen
- **Statusleiste**: Zeigt die Anzahl der Buchungen an

## Buchungen verwalten

### Neue Buchung erstellen

1. Klicken Sie auf **"Neue Buchung"**
2. Füllen Sie die Felder aus:
   - **Datum**: Format YYYY-MM-DD (z.B., 2024-01-15)
   - **Beschreibung**: Kurze Beschreibung der Buchung
   - **Konto**: Klicken Sie auf "Auswählen" für die Kontenauswahl
   - **Gegenkonto**: Wählen Sie "1000 - Kasse" oder "1200 - SPK"
   - **Soll**: Sollbetrag in Euro
   - **Haben**: Habenbetrag in Euro
3. Klicken Sie auf **"Speichern"**

#### Kontenauswahl
Die Konten sind farbcodiert nach Gruppen:
- **Blau**: Bankkonten (Kasse, SPK, Bank)
- **Grün**: Erlöskonten
- **Orange**: Steuerkonten
- **Rot**: Kostenkonten

### Buchung bearbeiten

**Option 1**: Doppelklicken Sie auf die Buchung in der Liste

**Option 2**: 
1. Wählen Sie die Buchung aus
2. Klicken Sie auf **"Bearbeiten"**
3. Ändern Sie die gewünschten Felder
4. Klicken Sie auf **"Speichern"**

### Buchung löschen

1. Wählen Sie die Buchung aus der Liste
2. Klicken Sie auf **"Löschen"**
3. Bestätigen Sie die Löschung

## Berichte erstellen

### Monatsbericht

1. Klicken Sie auf **"Monatsbericht"**
2. Geben Sie Jahr und Monat ein:
   - Jahr: z.B., 2024
   - Monat: 1-12 (1 = Januar, 12 = Dezember)
3. Klicken Sie auf **"Erstellen"**
4. Wählen Sie einen Speicherort für die PDF-Datei
5. Die PDF wird automatisch erstellt und gespeichert

#### Inhalt des Monatsberichts
- Gesamtanzahl der Buchungen
- Gesamt Soll und Haben
- Saldo des Monats
- Detaillierte Buchungsliste mit allen Transaktionen

## Steuerberater-Export

### Export erstellen

1. Klicken Sie auf **"Steuerberater Export"**
2. Geben Sie Jahr und Monat ein
3. Klicken Sie auf **"Exportieren"**
4. Wählen Sie einen Speicherort für die PDF-Datei

#### Inhalt des Steuerberater-Exports
- **Übersicht**:
  - Anzahl der Buchungen
  - Gesamt Soll und Haben
  - Differenz
- **Kontenbewegungen**:
  - Liste aller Konten mit Bewegungen
  - Soll, Haben und Saldo pro Konto
- **Detaillierte Buchungen**:
  - Vollständige Buchungsliste mit allen Details

## Häufig gestellte Fragen

### Wo werden die Daten gespeichert?
Alle Buchungen werden in der Datei `data/buchungen.json` gespeichert. Diese Datei wird automatisch erstellt und aktualisiert.

### Kann ich die Daten sichern?
Ja, kopieren Sie einfach die Datei `data/buchungen.json` an einen sicheren Ort. Um eine Sicherung wiederherzustellen, ersetzen Sie die aktuelle Datei durch die gesicherte Version.

### Welche Konten sind verfügbar?
Die Standardkonten sind:
- **Bankkonten**: 1000 - Kasse, 1200 - SPK, 1800 - Bank
- **Erlöskonten**: 4000 - Erlöse, 4100 - Sonstige Erlöse
- **Steuerkonten**: 4900 - Umsatzsteuer
- **Kostenkonten**: 6000 - Wareneinkauf, 6300 - Fremdleistungen, 6800 - Sonstige Kosten, 6820 - Versicherungen, 6850 - Büromaterial

### Kann ich eigene Konten hinzufügen?
Ja, Sie können die Kontenliste in der Datei `src/buchung.py` anpassen. Suchen Sie nach dem `KONTEN` Dictionary und fügen Sie neue Konten hinzu.

### Was ist der Unterschied zwischen Soll und Haben?
- **Soll**: Ausgaben oder Kosten (z.B., Einkauf von Waren)
- **Haben**: Einnahmen oder Erlöse (z.B., Verkauf von Waren)

### Wie kann ich Buchungen nach Datum sortieren?
Die Buchungsliste ist standardmäßig nach Datum sortiert (neueste zuerst).

### Kann ich mehrere Buchungen gleichzeitig löschen?
Nein, Buchungen können nur einzeln gelöscht werden. Dies ist eine Sicherheitsmaßnahme, um versehentliches Löschen zu verhindern.

### Was passiert, wenn ich das Programm schließe?
Alle Buchungen werden automatisch in `data/buchungen.json` gespeichert und sind beim nächsten Start wieder verfügbar.

### Wie kann ich die Anwendung aktualisieren?
```bash
git pull
pip install -r requirements.txt --upgrade
```

### Gibt es eine Undo-Funktion?
Nein, gelöschte Buchungen können nicht wiederhergestellt werden. Erstellen Sie regelmäßig Sicherungen der `data/buchungen.json` Datei.

### Kann ich die PDF-Exporte anpassen?
Ja, die PDF-Generierung kann in den Dateien `src/report.py` und `src/steuerberater.py` angepasst werden.

## Technischer Support

Bei Problemen oder Fragen:
1. Überprüfen Sie die [README.md](README.md) für technische Details
2. Erstellen Sie ein Issue auf GitHub
3. Kontaktieren Sie den Entwickler

## Lizenz

Siehe [LICENSE](LICENSE) für Details.
