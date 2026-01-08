"""
UI module for the Buchführung application.
Contains only Tkinter UI components and delegates business logic to other modules.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime

from buchung_model import Buchung
from buchung_manager import BuchungManager
from konten_provider import KontenProvider


class BuchfuehrungApp:
    """Main application UI for managing bookings."""
    
    def __init__(self):
        self.manager = BuchungManager()
        self.konten_provider = KontenProvider()
        self.index = len(self.manager.buchungen) - 1
        self.current_counter_account = "1200 - SPK"  # Default counter account
        self.counter_account_number = "1200"  # Just the number
        self.counter_account_name = "SPK"  # Just the name

        # Tkinter Fenster
        self.root = tk.Tk()
        self.root.title("Buchführung")

        self.create_menu_bar()
        self.create_widgets()
        self.setup_keyboard_bindings()
        if self.manager.buchungen:
            self.show_buchung(self.index)
        self.root.mainloop()

    def create_menu_bar(self):
        """Create menu bar with Buchen and Berichte menus."""
        menubar = tk.Menu(self.root)

        # Buchen Menu
        buchen_menu = tk.Menu(menubar, tearoff=0)
        buchen_menu.add_command(label="Buchen Bank", command=self.buchen_bank)
        buchen_menu.add_command(label="Buchen Kasse", command=self.buchen_kasse)
        menubar.add_cascade(label="Buchen", menu=buchen_menu)

        # Reports Menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        reports_menu.add_command(label="Bericht Gegenkonto", command=self.generate_report_gegenkonto)
        reports_menu.add_command(label="Bericht Zusammenfassung", command=self.generate_report_zusammenfassung)
        reports_menu.add_command(label="Bericht Sparkasse", command=self.generate_report_sparkasse)
        reports_menu.add_command(label="Bericht Kasse", command=self.generate_report_kasse)
        menubar.add_cascade(label="Berichte", menu=reports_menu)

        self.root.config(menu=menubar)

    def buchen_bank(self):
        """Set counter account to Bank (1200)."""
        self.set_counter_account("Bank")

    def buchen_kasse(self):
        """Set counter account to Kasse (1000)."""
        self.set_counter_account("Kasse")

    def set_counter_account(self, account_type):
        """Set the default counter account based on selection."""
        if account_type == "Bank":
            self.current_counter_account = "1200 - SPK"
            self.counter_account_number = "1200"
            self.counter_account_name = "SPK"
        elif account_type == "Kasse":
            self.current_counter_account = "1000 - Kasse"
            self.counter_account_number = "1000"
            self.counter_account_name = "Kasse"
        
        # Update the header
        self.update_counter_account_header()

    def generate_report_gegenkonto(self):
        """Generate counter account report."""
        self._generate_report("Gegenkonto")

    def generate_report_zusammenfassung(self):
        """Generate summary report."""
        self._generate_report("Zusammenfassung")

    def generate_report_sparkasse(self):
        """Generate Sparkasse report."""
        self._generate_report("Sparkasse")

    def generate_report_kasse(self):
        """Generate Kasse report."""
        self._generate_report("Kasse")

    def _generate_report(self, report_type):
        """Generate a report with year/month dialog."""
        # Import here to avoid circular imports
        try:
            from steuerberater import SteuerberaterExport
            from report import ReportGenerator
        except ImportError as e:
            messagebox.showerror("Fehler", f"Kann Report-Module nicht laden: {e}")
            return
        
        # Ask for year and month
        year_str = simpledialog.askstring("Jahr eingeben", "Bitte Jahr eingeben (z.B. 2025):", 
                                          initialvalue=str(datetime.now().year))
        if not year_str:
            return
        
        month_str = simpledialog.askstring("Monat eingeben", "Bitte Monat eingeben (1-12):", 
                                           initialvalue=str(datetime.now().month))
        if not month_str:
            return
        
        try:
            year = int(year_str)
            month = int(month_str)
            if month < 1 or month > 12:
                raise ValueError("Monat muss zwischen 1 und 12 liegen")
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")
            return
        
        # Ask for save location
        default_filename = f"{report_type}_Report_{year}_{month:02d}.pdf"
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return
        
        try:
            if report_type in ["Gegenkonto", "Sparkasse", "Kasse"]:
                # Use Steuerberater export
                steuerberater = SteuerberaterExport(self.manager)
                steuerberater.export_steuerberater_pdf(year, month, filename)
            else:
                # Use regular report generator
                report_gen = ReportGenerator(self.manager)
                report_gen.export_monthly_report_pdf(year, month, filename)
            
            messagebox.showinfo("Erfolg", f"Report erfolgreich erstellt: {filename}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des Reports: {e}")

    def create_widgets(self):
        # Bold header for counter account at the top
        self.counter_account_header = tk.Label(
            self.root, 
            text=f"BUCHEN {self.counter_account_name.upper()} ({self.counter_account_number})",
            font=("TkDefaultFont", 10, "bold")
        )
        self.counter_account_header.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky="w")

        # Row 1: Buchungsdatum
        tk.Label(self.root, text="Buchungsdatum:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.datum_entry = tk.Entry(self.root, width=20)
        self.datum_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Row 2: Beschreibung
        tk.Label(self.root, text="Beschreibung:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.beschreibung_entry = tk.Entry(self.root, width=50)
        self.beschreibung_entry.grid(row=2, column=1, columnspan=4, sticky="we", padx=5, pady=5)

        # Row 3: Kundennummer
        tk.Label(self.root, text="Kundennummer:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.kundennummer_entry = tk.Entry(self.root, width=20)
        self.kundennummer_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Row 4: Rechnungsnummer
        tk.Label(self.root, text="Rechnungsnummer:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.rechnungsnummer_entry = tk.Entry(self.root, width=20)
        self.rechnungsnummer_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Row 5: Rechnungsdatum
        tk.Label(self.root, text="Rechnungsdatum:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.rechnungsdatum_entry = tk.Entry(self.root, width=20)
        self.rechnungsdatum_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Row 6: Konto (Account number input + search button)
        tk.Label(self.root, text="Konto:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.konto_entry = tk.Entry(self.root, width=20)
        self.konto_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        tk.Button(self.root, text="Konto suchen", command=self.open_konto_selector).grid(row=6, column=2, sticky="w", padx=5, pady=5)

        # Row 7: MwSt
        tk.Label(self.root, text="MwSt:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.mwst_var = tk.StringVar()
        self.mwst_combo = ttk.Combobox(self.root, textvariable=self.mwst_var, values=["00","30","80","90"], width=17)
        self.mwst_combo.grid(row=7, column=1, sticky="w", padx=5, pady=5)

        # Row 8: Soll/Haben side by side
        tk.Label(self.root, text="Soll:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.soll_entry = tk.Entry(self.root, width=20)
        self.soll_entry.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self.root, text="Haben:").grid(row=8, column=2, sticky="w", padx=5, pady=5)
        self.haben_entry = tk.Entry(self.root, width=20)
        self.haben_entry.grid(row=8, column=3, sticky="w", padx=5, pady=5)

        # Row 9: Laufende Nummer (read-only, light grey)
        tk.Label(self.root, text="Lfd. Nr.:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.lfd_nr_label = tk.Label(self.root, text="", bg="lightgrey", width=18, anchor="w", relief="sunken")
        self.lfd_nr_label.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        # Row 10: Buttons
        tk.Button(self.root, text="Speichern", command=self.save_buchung).grid(row=10, column=0, padx=5, pady=10)
        tk.Button(self.root, text="Vor", command=self.prev_buchung).grid(row=10, column=1, sticky="w", padx=5, pady=10)
        tk.Button(self.root, text="Zurück", command=self.next_buchung).grid(row=10, column=2, sticky="w", padx=5, pady=10)

        # Row 11: Keyboard shortcuts help text (small, italic)
        shortcuts_text = ("Shortcuts: Enter = next field | ← → = Soll/Haben | "
                         "Ctrl+# = copy from previous | Ctrl+S = Save | F2 = Account search")
        self.shortcuts_label = tk.Label(
            self.root, 
            text=shortcuts_text,
            font=("TkDefaultFont", 8, "italic"),
            fg="gray"
        )
        self.shortcuts_label.grid(row=11, column=0, columnspan=5, pady=(10, 0), sticky="w", padx=5)

        # Store all input fields in order for tab traversal
        self.input_fields = [
            self.datum_entry,
            self.beschreibung_entry,
            self.kundennummer_entry,
            self.rechnungsnummer_entry,
            self.rechnungsdatum_entry,
            self.konto_entry,
            self.mwst_combo,
            self.soll_entry,
            self.haben_entry
        ]

        # Setup field highlighting
        self.setup_field_highlighting()

    def open_konto_selector(self):
        """Open account selection window with 3-column layout."""
        selector = tk.Toplevel(self.root)
        selector.title("Konto suchen")
        selector.geometry("800x600")
        
        # Main frame with scrollbar
        main_frame = tk.Frame(selector)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get accounts and colors
        farben = self.konten_provider.get_farben()
        all_konten = self.konten_provider.get_all_konten()
        
        # Organize accounts into 3 columns
        num_columns = 3
        konten_per_column = (len(all_konten) + num_columns - 1) // num_columns
        
        # Create 3 column frames
        column_frames = []
        for col in range(num_columns):
            frame = tk.Frame(scrollable_frame)
            frame.grid(row=0, column=col, sticky="n", padx=10)
            column_frames.append(frame)
        
        # Distribute accounts across columns
        for idx, konto in enumerate(all_konten):
            col_idx = idx // konten_per_column
            if col_idx >= num_columns:
                col_idx = num_columns - 1
            
            konto_text = f'{konto["nummer"]} - {konto["bezeichnung"]}'
            bg_color = farben.get(konto["gruppe"], "white")
            
            # Create button that selects the account
            btn = tk.Button(
                column_frames[col_idx],
                text=konto_text,
                bg=bg_color,
                anchor="w",
                width=35,
                command=lambda k=konto: self.select_account(k, selector)
            )
            btn.pack(anchor="w", pady=1)
        
        # Bind F2 to close without selection
        selector.bind("<Escape>", lambda e: selector.destroy())
    
    def select_account(self, konto, selector_window):
        """Select an account and close the selector window."""
        # Insert only the account number into the entry field
        self.konto_entry.delete(0, tk.END)
        self.konto_entry.insert(0, str(konto["nummer"]))
        # Trigger validation
        self.validate_account()
        # Close the selector
        selector_window.destroy()
    
    def update_counter_account_header(self):
        """Update the counter account header text."""
        header_text = f"BUCHEN {self.counter_account_name.upper()} ({self.counter_account_number})"
        self.counter_account_header.config(text=header_text)
    
    def setup_field_highlighting(self):
        """Setup focus highlighting for all input fields."""
        for field in self.input_fields:
            field.bind("<FocusIn>", self.on_field_focus_in)
            field.bind("<FocusOut>", self.on_field_focus_out)
    
    def on_field_focus_in(self, event):
        """Highlight field with light yellow when focused."""
        event.widget.config(bg="lightyellow")
    
    def on_field_focus_out(self, event):
        """Reset field to white when focus is lost."""
        event.widget.config(bg="white")
        # Trigger validation on focus out
        if event.widget == self.datum_entry:
            self.validate_date()
        elif event.widget == self.konto_entry:
            self.validate_account()
        elif event.widget == self.mwst_combo:
            self.validate_mwst()
    
    def setup_keyboard_bindings(self):
        """Setup all keyboard shortcuts and bindings."""
        # Bind Enter key to move to next field for all input fields
        for i, field in enumerate(self.input_fields):
            if i < len(self.input_fields) - 1:
                next_field = self.input_fields[i + 1]
                field.bind("<Return>", lambda e, nf=next_field: self.focus_next_field(nf, e))
            else:
                # Last field (haben_entry) confirms and sets the other to 0.00
                field.bind("<Return>", lambda e: self.confirm_amount_field(e))
        
        # Arrow key navigation for Soll/Haben
        self.soll_entry.bind("<Left>", lambda e: "break")  # Prevent default
        self.soll_entry.bind("<Right>", lambda e: self.haben_entry.focus())
        self.haben_entry.bind("<Left>", lambda e: self.soll_entry.focus())
        self.haben_entry.bind("<Right>", lambda e: "break")  # Prevent default
        
        # Special Enter behavior for Soll and Haben
        self.soll_entry.bind("<Return>", lambda e: self.confirm_amount_field(e))
        self.haben_entry.bind("<Return>", lambda e: self.confirm_amount_field(e))
        
        # Ctrl+# to copy from previous booking
        self.root.bind("<Control-numbersign>", self.copy_from_previous)
        self.root.bind("<Control-Key-3>", self.copy_from_previous)  # Ctrl+Shift+3 on some keyboards
        
        # Ctrl+S to save
        self.root.bind("<Control-s>", lambda e: self.save_buchung())
        self.root.bind("<Control-S>", lambda e: self.save_buchung())
        
        # F2 to open account search
        self.root.bind("<F2>", lambda e: self.open_konto_selector())
    
    def focus_next_field(self, next_field, event):
        """Move focus to the next field."""
        next_field.focus()
        return "break"  # Prevent default Enter behavior
    
    def confirm_amount_field(self, event):
        """Confirm the active amount field and set the other to 0.00."""
        if event.widget == self.soll_entry:
            # Soll is active, set Haben to 0.00
            if self.soll_entry.get().strip():
                self.haben_entry.delete(0, tk.END)
                self.haben_entry.insert(0, "0.00")
        elif event.widget == self.haben_entry:
            # Haben is active, set Soll to 0.00
            if self.haben_entry.get().strip():
                self.soll_entry.delete(0, tk.END)
                self.soll_entry.insert(0, "0.00")
        return "break"
    
    def copy_from_previous(self, event=None):
        """Copy value from the same field in the previous booking."""
        if self.index <= 0 or not self.manager.buchungen:
            return  # No previous booking, do nothing
        
        prev_booking = self.manager.buchungen[self.index - 1]
        focused_widget = self.root.focus_get()
        
        if focused_widget == self.mwst_combo:
            self.mwst_var.set(prev_booking.mwst)
        elif focused_widget == self.konto_entry:
            # Extract just the number from the previous konto
            prev_konto = prev_booking.konto
            if " - " in prev_konto:
                konto_number = prev_konto.split(" - ")[0]
            else:
                konto_number = prev_konto
            self.konto_entry.delete(0, tk.END)
            self.konto_entry.insert(0, konto_number)
        elif focused_widget == self.soll_entry:
            self.soll_entry.delete(0, tk.END)
            if prev_booking.soll:
                self.soll_entry.insert(0, str(prev_booking.soll))
        elif focused_widget == self.haben_entry:
            self.haben_entry.delete(0, tk.END)
            if prev_booking.haben:
                self.haben_entry.insert(0, str(prev_booking.haben))
        elif focused_widget == self.kundennummer_entry:
            self.kundennummer_entry.delete(0, tk.END)
            self.kundennummer_entry.insert(0, prev_booking.kundennummer)
        elif focused_widget == self.rechnungsnummer_entry:
            self.rechnungsnummer_entry.delete(0, tk.END)
            self.rechnungsnummer_entry.insert(0, prev_booking.rechnungsnummer)
    
    def validate_date(self):
        """Validate date field."""
        date_str = self.datum_entry.get().strip()
        if not date_str:
            self.datum_entry.config(bg="white")
            return True
        
        valid = False
        for fmt in ["%Y-%m-%d", "%d.%m.%y", "%d.%m.%Y"]:
            try:
                datetime.strptime(date_str, fmt)
                valid = True
                break
            except ValueError:
                continue
        
        if valid:
            self.datum_entry.config(bg="white")
        else:
            self.datum_entry.config(bg="red")
        return valid
    
    def validate_account(self):
        """Validate account field."""
        account_str = self.konto_entry.get().strip()
        if not account_str:
            self.konto_entry.config(bg="white")
            return True
        
        # Try to find account by number
        try:
            account_num = int(account_str)
            konto = self.konten_provider.get_konto_by_nummer(account_num)
            if konto:
                self.konto_entry.config(bg="white")
                return True
            else:
                self.konto_entry.config(bg="red")
                return False
        except ValueError:
            self.konto_entry.config(bg="red")
            return False
    
    def validate_mwst(self):
        """Validate VAT field."""
        mwst = self.mwst_var.get().strip()
        if not mwst or mwst in ["00", "30", "80", "90"]:
            self.mwst_combo.config(background="white")
            return True
        else:
            self.mwst_combo.config(background="red")
            return False
    
    def validate_amounts(self):
        """Validate that exactly one of Soll or Haben is non-zero."""
        try:
            soll = float(self.soll_entry.get() or "0")
            haben = float(self.haben_entry.get() or "0")
            
            # Both are zero or both are non-zero is invalid
            if (soll == 0 and haben == 0) or (soll != 0 and haben != 0):
                return False
            return True
        except ValueError:
            return False

    def show_buchung(self, index):
        if index < 0 or index >= len(self.manager.buchungen):
            return
        b = self.manager.buchungen[index]
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, b.datum)
        self.beschreibung_entry.delete(0, tk.END)
        self.beschreibung_entry.insert(0, b.beschreibung)
        self.kundennummer_entry.delete(0, tk.END)
        self.kundennummer_entry.insert(0, b.kundennummer)
        self.rechnungsnummer_entry.delete(0, tk.END)
        self.rechnungsnummer_entry.insert(0, b.rechnungsnummer)
        self.rechnungsdatum_entry.delete(0, tk.END)
        self.rechnungsdatum_entry.insert(0, b.rechnungsdatum)
        self.mwst_var.set(b.mwst)
        
        # Extract account number from konto (format: "number - name")
        konto_number = b.konto
        if " - " in b.konto:
            konto_number = b.konto.split(" - ")[0]
        self.konto_entry.delete(0, tk.END)
        self.konto_entry.insert(0, konto_number)
        
        self.soll_entry.delete(0, tk.END)
        self.soll_entry.insert(0, str(b.soll) if b.soll else "")
        self.haben_entry.delete(0, tk.END)
        self.haben_entry.insert(0, str(b.haben) if b.haben else "")
        self.lfd_nr_label.config(text=str(b.lfd_nr))

    def save_buchung(self):
        # Validate all fields
        valid = True
        errors = []
        
        # Validate date
        if not self.validate_date():
            valid = False
            errors.append("Datum ist ungültig")
        
        # Validate account
        konto_number = self.konto_entry.get().strip()
        if not konto_number:
            valid = False
            errors.append("Konto darf nicht leer sein")
        elif not self.validate_account():
            valid = False
            errors.append("Konto existiert nicht")
        
        # Validate MwSt
        if not self.validate_mwst():
            valid = False
            errors.append("MwSt muss 00, 30, 80 oder 90 sein")
        
        # Validate amounts
        if not self.validate_amounts():
            valid = False
            errors.append("Genau ein Wert (Soll oder Haben) muss ungleich Null sein")
        
        if not valid:
            messagebox.showerror("Validierungsfehler", "\n".join(errors))
            return
        
        # Get konto with full name
        try:
            konto_num = int(konto_number)
            konto_obj = self.konten_provider.get_konto_by_nummer(konto_num)
            if konto_obj:
                konto_full = f'{konto_obj["nummer"]} - {konto_obj["bezeichnung"]}'
            else:
                konto_full = konto_number
        except:
            konto_full = konto_number
        
        datum = self.datum_entry.get() or datetime.now().strftime("%Y-%m-%d")
        soll_value = self.soll_entry.get() or "0"
        haben_value = self.haben_entry.get() or "0"
        
        buchung = Buchung(
            datum=datum,
            gegenkonto=self.current_counter_account,
            beschreibung=self.beschreibung_entry.get(),
            kundennummer=self.kundennummer_entry.get(),
            rechnungsnummer=self.rechnungsnummer_entry.get(),
            rechnungsdatum=self.rechnungsdatum_entry.get(),
            mwst=self.mwst_var.get(),
            konto=konto_full,
            soll=soll_value,
            haben=haben_value,
            lfd_nr=self.index + 2
        )
        
        if self.index + 1 < len(self.manager.buchungen):
            self.manager.update_buchung(self.index, buchung)
        else:
            self.manager.add_buchung(buchung)
            self.index = len(self.manager.buchungen) - 1

        self.show_buchung(self.index)
        messagebox.showinfo("Info", "Buchung gespeichert.")

    def prev_buchung(self):
        if self.index > 0:
            self.index -= 1
            self.show_buchung(self.index)

    def next_buchung(self):
        if self.index < len(self.manager.buchungen) - 1:
            self.index += 1
            self.show_buchung(self.index)


if __name__ == "__main__":
    BuchfuehrungApp()
