"""
Tax advisor export module for generating booking summaries and exports.
"""

from datetime import datetime
from typing import List, Dict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from buchung_model import Buchung
from buchung_manager import BuchungManager


class SteuerberaterExport:
    """Handles exports for tax advisor."""
    
    def __init__(self, manager: BuchungManager):
        """
        Initialize tax advisor export.
        
        Args:
            manager: BuchungManager instance
        """
        self.manager = manager
    
    def generate_account_movements(self, year: int, month: int) -> Dict[str, dict]:
        """
        Generate account movements for a specific month.
        
        Args:
            year: Year
            month: Month
            
        Returns:
            Dictionary with account movements
        """
        buchungen = self.manager.get_buchungen_by_month(year, month)
        
        movements = {}
        for b in buchungen:
            # Track main account
            if b.konto not in movements:
                movements[b.konto] = {
                    'buchungen': [],
                    'soll': 0.0,
                    'haben': 0.0
                }
            movements[b.konto]['buchungen'].append(b)
            movements[b.konto]['soll'] += b.soll
            movements[b.konto]['haben'] += b.haben
            
            # Track counter account
            if b.gegenkonto not in movements:
                movements[b.gegenkonto] = {
                    'buchungen': [],
                    'soll': 0.0,
                    'haben': 0.0
                }
            # Counter entry
            movements[b.gegenkonto]['soll'] += b.haben
            movements[b.gegenkonto]['haben'] += b.soll
        
        return movements
    
    def export_steuerberater_pdf(self, year: int, month: int, filename: str):
        """
        Export tax advisor report as PDF.
        
        Args:
            year: Year
            month: Month
            filename: Output PDF filename
        """
        movements = self.generate_account_movements(year, month)
        buchungen = self.manager.get_buchungen_by_month(year, month)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        title = Paragraph(
            f"Steuerberater Export - {month:02d}/{year}",
            title_style
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # Overview section
        overview_title = Paragraph("Übersicht", styles['Heading2'])
        elements.append(overview_title)
        elements.append(Spacer(1, 0.3*cm))
        
        total_soll = sum(b.soll for b in buchungen)
        total_haben = sum(b.haben for b in buchungen)
        
        overview_data = [
            ['Anzahl Buchungen:', str(len(buchungen))],
            ['Gesamt Soll:', f"{total_soll:.2f} €"],
            ['Gesamt Haben:', f"{total_haben:.2f} €"],
            ['Differenz:', f"{(total_soll - total_haben):.2f} €"]
        ]
        
        overview_table = Table(overview_data, colWidths=[8*cm, 8*cm])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(overview_table)
        elements.append(Spacer(1, 1*cm))
        
        # Account movements section
        movements_title = Paragraph("Kontenbewegungen", styles['Heading2'])
        elements.append(movements_title)
        elements.append(Spacer(1, 0.3*cm))
        
        movements_data = [['Konto', 'Soll', 'Haben', 'Saldo']]
        for account, data in sorted(movements.items()):
            saldo = data['soll'] - data['haben']
            movements_data.append([
                account,
                f"{data['soll']:.2f} €",
                f"{data['haben']:.2f} €",
                f"{saldo:.2f} €"
            ])
        
        movements_table = Table(movements_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
        movements_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(movements_table)
        elements.append(Spacer(1, 1*cm))
        
        # Detailed bookings section
        bookings_title = Paragraph("Detaillierte Buchungen", styles['Heading2'])
        elements.append(bookings_title)
        elements.append(Spacer(1, 0.3*cm))
        
        bookings_data = [['Datum', 'Beschreibung', 'Konto', 'Gegenkonto', 'Soll', 'Haben']]
        for b in sorted(buchungen, key=lambda x: x.datum):
            bookings_data.append([
                b.datum,
                b.beschreibung[:25],  # Truncate
                b.konto[:20],
                b.gegenkonto[:20],
                f"{b.soll:.2f}" if b.soll > 0 else "",
                f"{b.haben:.2f}" if b.haben > 0 else ""
            ])
        
        bookings_table = Table(
            bookings_data,
            colWidths=[2.2*cm, 4.5*cm, 3.5*cm, 3.5*cm, 2*cm, 2*cm]
        )
        bookings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (5, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(bookings_table)
        
        # Build PDF
        doc.build(elements)
    
    def get_monthly_summary_text(self, year: int, month: int) -> str:
        """
        Generate text summary for a month.
        
        Args:
            year: Year
            month: Month
            
        Returns:
            Text summary
        """
        movements = self.generate_account_movements(year, month)
        buchungen = self.manager.get_buchungen_by_month(year, month)
        
        text = f"Steuerberater Zusammenfassung {month:02d}/{year}\n"
        text += "=" * 60 + "\n\n"
        text += f"Anzahl Buchungen: {len(buchungen)}\n\n"
        text += "Kontenbewegungen:\n"
        text += "-" * 60 + "\n"
        
        for account, data in sorted(movements.items()):
            saldo = data['soll'] - data['haben']
            text += f"{account:30s} Soll: {data['soll']:10.2f} € "
            text += f"Haben: {data['haben']:10.2f} € Saldo: {saldo:10.2f} €\n"
        
        return text
