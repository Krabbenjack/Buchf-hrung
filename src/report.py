"""
Report module for generating monthly reports and exporting them as PDFs.
"""

from datetime import datetime
from typing import List
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from buchung import Buchung, BuchungManager


class ReportGenerator:
    """Generates monthly reports from bookings."""
    
    def __init__(self, manager: BuchungManager):
        """
        Initialize report generator.
        
        Args:
            manager: BuchungManager instance
        """
        self.manager = manager
    
    def generate_monthly_summary(self, year: int, month: int) -> dict:
        """
        Generate summary for a specific month.
        
        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            
        Returns:
            Dictionary with summary information
        """
        buchungen = self.manager.get_buchungen_by_month(year, month)
        
        total_soll = sum(b.soll for b in buchungen)
        total_haben = sum(b.haben for b in buchungen)
        balance = total_soll - total_haben
        
        # Group by account
        account_movements = {}
        for b in buchungen:
            if b.konto not in account_movements:
                account_movements[b.konto] = {'soll': 0.0, 'haben': 0.0}
            account_movements[b.konto]['soll'] += b.soll
            account_movements[b.konto]['haben'] += b.haben
        
        return {
            'year': year,
            'month': month,
            'total_bookings': len(buchungen),
            'total_soll': total_soll,
            'total_haben': total_haben,
            'balance': balance,
            'buchungen': buchungen,
            'account_movements': account_movements
        }
    
    def export_monthly_report_pdf(self, year: int, month: int, filename: str):
        """
        Export monthly report as PDF.
        
        Args:
            year: Year
            month: Month
            filename: Output PDF filename
        """
        summary = self.generate_monthly_summary(year, month)
        
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
        title = Paragraph(f"Monatsbericht {month:02d}/{year}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # Summary information
        summary_data = [
            ['Gesamtanzahl Buchungen:', str(summary['total_bookings'])],
            ['Gesamt Soll:', f"{summary['total_soll']:.2f} €"],
            ['Gesamt Haben:', f"{summary['total_haben']:.2f} €"],
            ['Saldo:', f"{summary['balance']:.2f} €"]
        ]
        
        summary_table = Table(summary_data, colWidths=[8*cm, 8*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 1*cm))
        
        # Bookings table
        if summary['buchungen']:
            buchungen_title = Paragraph("Buchungen:", styles['Heading2'])
            elements.append(buchungen_title)
            elements.append(Spacer(1, 0.3*cm))
            
            buchungen_data = [['Datum', 'Beschreibung', 'Konto', 'Gegenkonto', 'Soll', 'Haben']]
            for b in summary['buchungen']:
                buchungen_data.append([
                    b.datum,
                    b.beschreibung[:30],  # Truncate long descriptions
                    b.konto,
                    b.gegenkonto,
                    f"{b.soll:.2f}" if b.soll > 0 else "",
                    f"{b.haben:.2f}" if b.haben > 0 else ""
                ])
            
            buchungen_table = Table(buchungen_data, colWidths=[2.5*cm, 5*cm, 3*cm, 3*cm, 2*cm, 2*cm])
            buchungen_table.setStyle(TableStyle([
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
            elements.append(buchungen_table)
        
        # Build PDF
        doc.build(elements)
    
    def get_yearly_summary(self, year: int) -> dict:
        """
        Get summary for entire year.
        
        Args:
            year: Year
            
        Returns:
            Dictionary with yearly summary
        """
        buchungen = self.manager.get_buchungen_by_year(year)
        
        total_soll = sum(b.soll for b in buchungen)
        total_haben = sum(b.haben for b in buchungen)
        balance = total_soll - total_haben
        
        # Group by month
        monthly_data = {}
        for month in range(1, 13):
            month_buchungen = self.manager.get_buchungen_by_month(year, month)
            monthly_data[month] = {
                'count': len(month_buchungen),
                'soll': sum(b.soll for b in month_buchungen),
                'haben': sum(b.haben for b in month_buchungen)
            }
        
        return {
            'year': year,
            'total_bookings': len(buchungen),
            'total_soll': total_soll,
            'total_haben': total_haben,
            'balance': balance,
            'monthly_data': monthly_data
        }
