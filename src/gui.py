"""
GUI module for the booking application.
Provides user interface for managing bookings, generating reports, and exports.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional
import os

from buchung import Buchung, BuchungManager
from konten import get_konten_by_color
from report import ReportGenerator
from steuerberater import SteuerberaterExport


class KontoSelectionDialog(tk.Toplevel):
    """Dialog for selecting an account with color-coded groups."""
    
    def __init__(self, parent, title="Konto auswählen"):
        super().__init__(parent)
        self.title(title)
        self.result = None
        
        # Center the dialog
        self.geometry("400x500")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create dialog widgets."""
        # Title label
        label = ttk.Label(self, text="Wählen Sie ein Konto:", font=('Arial', 12, 'bold'))
        label.pack(pady=10)
        
        # Frame for account list
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create scrollable treeview with columns
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Define columns
        columns = ('Account Name', 'Account Number')
        self.treeview = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        # Configure column headings
        self.treeview.heading('Account Name', text='Account Name')
        self.treeview.heading('Account Number', text='Account Number')
        
        # Configure column widths
        self.treeview.column('Account Name', width=250)
        self.treeview.column('Account Number', width=100)
        
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.treeview.yview)
        
        # Add accounts grouped by color
        konten_by_color = get_konten_by_color()
        
        # Configure tags for each color
        for color in konten_by_color.keys():
            # Remove the '#' and use the color hex as tag name
            tag_name = color.lstrip('#')
            self.treeview.tag_configure(tag_name, background=color)
        
        # Sort and display accounts by color
        for color, konten in sorted(konten_by_color.items()):
            for konto in sorted(konten):
                # Split account string into name and number
                if ': ' in konto:
                    account_name, account_number = konto.split(': ', 1)
                else:
                    account_name = konto
                    account_number = ''
                
                # Use color hex (without #) as tag
                tag_name = color.lstrip('#')
                self.treeview.insert('', tk.END, values=(account_name, account_number), tags=(tag_name,))
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Auswählen", command=self._on_select).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind double-click
        self.treeview.bind('<Double-Button-1>', lambda e: self._on_select())
    
    def _on_select(self):
        """Handle account selection."""
        selection = self.treeview.selection()
        if selection:
            # Get the values from the selected item
            item = selection[0]
            values = self.treeview.item(item)['values']
            # Reconstruct the account string in the format "Name: Number"
            account_name = values[0]
            account_number = values[1]
            # Handle empty account number case
            if account_number:
                self.result = f"{account_name}: {account_number}"
            else:
                self.result = account_name
            self.destroy()


class BuchungDialog(tk.Toplevel):
    """Dialog for creating or editing a booking."""
    
    def __init__(self, parent, manager: BuchungManager, buchung: Optional[Buchung] = None):
        super().__init__(parent)
        self.title("Buchung bearbeiten" if buchung else "Neue Buchung")
        self.manager = manager
        self.buchung = buchung
        self.result = None
        
        # Center the dialog
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if buchung:
            self._populate_fields()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Date
        ttk.Label(main_frame, text="Datum (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.datum_entry = ttk.Entry(main_frame, width=30)
        self.datum_entry.grid(row=0, column=1, pady=5, padx=5)
        self.datum_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Description
        ttk.Label(main_frame, text="Beschreibung:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.beschreibung_entry = ttk.Entry(main_frame, width=30)
        self.beschreibung_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Account (Konto)
        ttk.Label(main_frame, text="Konto:").grid(row=2, column=0, sticky=tk.W, pady=5)
        konto_frame = ttk.Frame(main_frame)
        konto_frame.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.konto_entry = ttk.Entry(konto_frame, width=20)
        self.konto_entry.pack(side=tk.LEFT)
        ttk.Button(konto_frame, text="Auswählen", command=self._select_konto).pack(side=tk.LEFT, padx=5)
        
        # Counter Account (Gegenkonto)
        ttk.Label(main_frame, text="Gegenkonto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.gegenkonto_var = tk.StringVar(value="1000 - Kasse")
        gegenkonto_combo = ttk.Combobox(
            main_frame,
            textvariable=self.gegenkonto_var,
            values=["1000 - Kasse", "1200 - SPK"],
            state="readonly",
            width=27
        )
        gegenkonto_combo.grid(row=3, column=1, pady=5, padx=5)
        
        # Soll (Debit)
        ttk.Label(main_frame, text="Soll (€):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.soll_entry = ttk.Entry(main_frame, width=30)
        self.soll_entry.grid(row=4, column=1, pady=5, padx=5)
        self.soll_entry.insert(0, "0.00")
        
        # Haben (Credit)
        ttk.Label(main_frame, text="Haben (€):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.haben_entry = ttk.Entry(main_frame, width=30)
        self.haben_entry.grid(row=5, column=1, pady=5, padx=5)
        self.haben_entry.insert(0, "0.00")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Speichern", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def _select_konto(self):
        """Open account selection dialog."""
        dialog = KontoSelectionDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            self.konto_entry.delete(0, tk.END)
            self.konto_entry.insert(0, dialog.result)
    
    def _populate_fields(self):
        """Populate fields with existing booking data."""
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, self.buchung.datum)
        
        self.beschreibung_entry.delete(0, tk.END)
        self.beschreibung_entry.insert(0, self.buchung.beschreibung)
        
        self.konto_entry.delete(0, tk.END)
        self.konto_entry.insert(0, self.buchung.konto)
        
        self.gegenkonto_var.set(self.buchung.gegenkonto)
        
        self.soll_entry.delete(0, tk.END)
        self.soll_entry.insert(0, f"{self.buchung.soll:.2f}")
        
        self.haben_entry.delete(0, tk.END)
        self.haben_entry.insert(0, f"{self.buchung.haben:.2f}")
    
    def _save(self):
        """Save the booking."""
        try:
            # Validate inputs
            datum = self.datum_entry.get().strip()
            beschreibung = self.beschreibung_entry.get().strip()
            konto = self.konto_entry.get().strip()
            gegenkonto = self.gegenkonto_var.get()
            soll = float(self.soll_entry.get().strip())
            haben = float(self.haben_entry.get().strip())
            
            if not all([datum, beschreibung, konto, gegenkonto]):
                messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
                return
            
            # Validate date format
            try:
                datetime.strptime(datum, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiges Datumsformat. Verwenden Sie YYYY-MM-DD (z.B. 2024-01-15).")
                return
            
            # Create or update booking
            if self.buchung:
                # Update existing
                updated = Buchung(datum, beschreibung, konto, gegenkonto, soll, haben)
                self.manager.update_buchung(self.buchung.buchung_id, updated)
            else:
                # Create new
                new_buchung = Buchung(datum, beschreibung, konto, gegenkonto, soll, haben)
                self.manager.add_buchung(new_buchung)
            
            self.result = True
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Fehler", "Ungültige Beträge für Soll oder Haben.")


class BuchfuehrungGUI:
    """Main GUI application for the booking system."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Buchführung - Booking Program")
        self.root.geometry("1000x600")
        
        # Initialize manager and generators
        self.manager = BuchungManager()
        self.report_gen = ReportGenerator(self.manager)
        self.steuerberater = SteuerberaterExport(self.manager)
        
        self._create_widgets()
        self._refresh_buchungen_list()
    
    def _create_widgets(self):
        """Create main window widgets."""
        # Title
        title_label = ttk.Label(
            self.root,
            text="Buchführungsprogramm",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            button_frame,
            text="Neue Buchung",
            command=self._new_buchung
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Bearbeiten",
            command=self._edit_buchung
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Löschen",
            command=self._delete_buchung
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Monatsbericht",
            command=self._generate_monthly_report
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Steuerberater Export",
            command=self._export_steuerberater
        ).pack(side=tk.LEFT, padx=5)
        
        # Bookings list
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ('Datum', 'Beschreibung', 'Konto', 'Gegenkonto', 'Soll', 'Haben')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label = ttk.Label(
            self.root,
            text="Bereit",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to edit
        self.tree.bind('<Double-Button-1>', lambda e: self._edit_buchung())
    
    def _refresh_buchungen_list(self):
        """Refresh the bookings list."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add all bookings
        buchungen = self.manager.get_all_buchungen()
        for buchung in sorted(buchungen, key=lambda b: b.datum, reverse=True):
            self.tree.insert('', tk.END, values=(
                buchung.datum,
                buchung.beschreibung,
                buchung.konto,
                buchung.gegenkonto,
                f"{buchung.soll:.2f}",
                f"{buchung.haben:.2f}"
            ), tags=(buchung.buchung_id,))
        
        self.status_label.config(text=f"Anzahl Buchungen: {len(buchungen)}")
    
    def _new_buchung(self):
        """Create a new booking."""
        dialog = BuchungDialog(self.root, self.manager)
        self.root.wait_window(dialog)
        if dialog.result:
            self._refresh_buchungen_list()
            messagebox.showinfo("Erfolg", "Buchung wurde erstellt.")
    
    def _edit_buchung(self):
        """Edit selected booking."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Buchung aus.")
            return
        
        # Get booking ID from tags
        item = selection[0]
        buchung_id = self.tree.item(item)['tags'][0]
        
        # Find booking
        buchung = None
        for b in self.manager.get_all_buchungen():
            if b.buchung_id == buchung_id:
                buchung = b
                break
        
        if buchung:
            dialog = BuchungDialog(self.root, self.manager, buchung)
            self.root.wait_window(dialog)
            if dialog.result:
                self._refresh_buchungen_list()
                messagebox.showinfo("Erfolg", "Buchung wurde aktualisiert.")
    
    def _delete_buchung(self):
        """Delete selected booking."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Buchung aus.")
            return
        
        if messagebox.askyesno("Bestätigung", "Möchten Sie diese Buchung wirklich löschen?"):
            item = selection[0]
            buchung_id = self.tree.item(item)['tags'][0]
            self.manager.delete_buchung(buchung_id)
            self._refresh_buchungen_list()
            messagebox.showinfo("Erfolg", "Buchung wurde gelöscht.")
    
    def _generate_monthly_report(self):
        """Generate monthly report."""
        # Ask for month and year
        dialog = tk.Toplevel(self.root)
        dialog.title("Monatsbericht erstellen")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Jahr:").pack(pady=5)
        year_entry = ttk.Entry(dialog)
        year_entry.insert(0, str(datetime.now().year))
        year_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Monat (1-12):").pack(pady=5)
        month_entry = ttk.Entry(dialog)
        month_entry.insert(0, str(datetime.now().month))
        month_entry.pack(pady=5)
        
        def generate():
            try:
                year = int(year_entry.get())
                month = int(month_entry.get())
                
                if not (1 <= month <= 12):
                    messagebox.showerror("Fehler", "Monat muss zwischen 1 und 12 liegen.")
                    return
                
                # Ask for filename
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=f"monatsbericht_{year}_{month:02d}.pdf"
                )
                
                if filename:
                    self.report_gen.export_monthly_report_pdf(year, month, filename)
                    messagebox.showinfo("Erfolg", f"Monatsbericht wurde erstellt:\n{filename}")
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Fehler", "Ungültige Eingaben.")
        
        ttk.Button(dialog, text="Erstellen", command=generate).pack(pady=10)
    
    def _export_steuerberater(self):
        """Export for tax advisor."""
        # Ask for month and year
        dialog = tk.Toplevel(self.root)
        dialog.title("Steuerberater Export")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Jahr:").pack(pady=5)
        year_entry = ttk.Entry(dialog)
        year_entry.insert(0, str(datetime.now().year))
        year_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Monat (1-12):").pack(pady=5)
        month_entry = ttk.Entry(dialog)
        month_entry.insert(0, str(datetime.now().month))
        month_entry.pack(pady=5)
        
        def export():
            try:
                year = int(year_entry.get())
                month = int(month_entry.get())
                
                if not (1 <= month <= 12):
                    messagebox.showerror("Fehler", "Monat muss zwischen 1 und 12 liegen.")
                    return
                
                # Ask for filename
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=f"steuerberater_{year}_{month:02d}.pdf"
                )
                
                if filename:
                    self.steuerberater.export_steuerberater_pdf(year, month, filename)
                    messagebox.showinfo("Erfolg", f"Steuerberater Export wurde erstellt:\n{filename}")
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Fehler", "Ungültige Eingaben.")
        
        ttk.Button(dialog, text="Exportieren", command=export).pack(pady=10)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
