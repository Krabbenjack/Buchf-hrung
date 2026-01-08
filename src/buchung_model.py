"""
Data model for booking entries.
Contains pure data class without business logic or file access.
"""


class Buchung:
    """Data class for a single booking entry."""
    
    def __init__(self, datum, beschreibung, konto, gegenkonto, soll, haben, 
                 kundennummer="", rechnungsnummer="", rechnungsdatum="", mwst="", lfd_nr=0):
        self.datum = datum
        self.beschreibung = beschreibung
        self.konto = konto
        self.gegenkonto = gegenkonto
        # Safely convert soll and haben to float, handling invalid values
        try:
            self.soll = float(soll) if soll else 0.0
        except (ValueError, TypeError):
            self.soll = 0.0
        try:
            self.haben = float(haben) if haben else 0.0
        except (ValueError, TypeError):
            self.haben = 0.0
        self.kundennummer = kundennummer
        self.rechnungsnummer = rechnungsnummer
        self.rechnungsdatum = rechnungsdatum
        self.mwst = mwst
        self.lfd_nr = lfd_nr
    
    def to_dict(self):
        """Convert booking to dictionary."""
        return {
            "datum": self.datum,
            "beschreibung": self.beschreibung,
            "konto": self.konto,
            "gegenkonto": self.gegenkonto,
            "soll": str(self.soll),
            "haben": str(self.haben),
            "kundennummer": self.kundennummer,
            "rechnungsnummer": self.rechnungsnummer,
            "rechnungsdatum": self.rechnungsdatum,
            "mwst": self.mwst,
            "lfd_nr": self.lfd_nr
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create booking from dictionary."""
        return cls(
            datum=data.get("datum", ""),
            beschreibung=data.get("beschreibung", ""),
            konto=data.get("konto", ""),
            gegenkonto=data.get("gegenkonto", ""),
            soll=data.get("soll", 0),
            haben=data.get("haben", 0),
            kundennummer=data.get("kundennummer", ""),
            rechnungsnummer=data.get("rechnungsnummer", ""),
            rechnungsdatum=data.get("rechnungsdatum", ""),
            mwst=data.get("mwst", ""),
            lfd_nr=data.get("lfd_nr", 0)
        )
