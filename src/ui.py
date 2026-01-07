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

        # Tkinter Fenster
        self.root = tk.Tk()
        self.root.title("Buchführung")

        self.create_menu_bar()
        self.create_widgets()
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
        messagebox.showinfo("Info", "Gegenkonto auf Bank (1200 - SPK) gesetzt")

    def buchen_kasse(self):
        """Set counter account to Kasse (1000)."""
        self.set_counter_account("Kasse")
        messagebox.showinfo("Info", "Gegenkonto auf Kasse (1000 - Kasse) gesetzt")

    def set_counter_account(self, account_type):
        """Set the default counter account based on selection."""
        if account_type == "Bank":
            self.current_counter_account = "1200 - SPK"
        elif account_type == "Kasse":
            self.current_counter_account = "1000 - Kasse"
        
        # Update the dropdown selection
        self.gegenkonto_var.set(self.current_counter_account)

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
        # Buchungsdatum
        tk.Label(self.root, text="Buchungsdatum:").grid(row=0, column=0, sticky="w")
        self.datum_entry = tk.Entry(self.root)
        self.datum_entry.grid(row=0, column=1)

        # Gegenkonto Dropdown
        tk.Label(self.root, text="Gegenkonto:").grid(row=0, column=3, sticky="w")
        self.gegenkonto_var = tk.StringVar(value=self.current_counter_account)
        self.gegenkonto_combo = ttk.Combobox(self.root, textvariable=self.gegenkonto_var, values=[
            "1000 - Kasse",
            "1200 - SPK"
        ])
        self.gegenkonto_combo.grid(row=0, column=4)

        # Beschreibung
        tk.Label(self.root, text="Beschreibung:").grid(row=1, column=0, sticky="w")
        self.beschreibung_entry = tk.Entry(self.root, width=50)
        self.beschreibung_entry.grid(row=1, column=1, columnspan=3, sticky="w")

        # Kundennummer
        tk.Label(self.root, text="Kundennummer:").grid(row=2, column=0, sticky="w")
        self.kundennummer_entry = tk.Entry(self.root)
        self.kundennummer_entry.grid(row=2, column=1, sticky="w")

        # Rechnungsnummer
        tk.Label(self.root, text="Rechnungsnummer:").grid(row=2, column=2, sticky="w")
        self.rechnungsnummer_entry = tk.Entry(self.root)
        self.rechnungsnummer_entry.grid(row=2, column=3, sticky="w")

        # Rechnungsdatum
        tk.Label(self.root, text="Rechnungsdatum:").grid(row=3, column=0, sticky="w")
        self.rechnungsdatum_entry = tk.Entry(self.root)
        self.rechnungsdatum_entry.grid(row=3, column=1, sticky="w")

        # MwSt
        tk.Label(self.root, text="MwSt:").grid(row=4, column=0, sticky="w")
        self.mwst_var = tk.StringVar()
        self.mwst_combo = ttk.Combobox(self.root, textvariable=self.mwst_var, values=["00","30","80","90"])
        self.mwst_combo.grid(row=4, column=1, sticky="w")

        # Konto Auswahl
        tk.Label(self.root, text="Konto:").grid(row=5, column=0, sticky="w")
        self.konto_var = tk.StringVar()
        self.konto_display = tk.Label(self.root, text="", width=50, anchor="w", relief="sunken")
        self.konto_display.grid(row=5, column=1, columnspan=3, sticky="w")
        tk.Button(self.root, text="Konto auswählen", command=self.open_konto_selector).grid(row=5, column=4)

        # Soll/Haben nebeneinander
        tk.Label(self.root, text="Soll:").grid(row=6, column=0, sticky="w")
        self.soll_entry = tk.Entry(self.root)
        self.soll_entry.grid(row=6, column=1, sticky="w")
        tk.Label(self.root, text="Haben:").grid(row=6, column=2, sticky="w")
        self.haben_entry = tk.Entry(self.root)
        self.haben_entry.grid(row=6, column=3, sticky="w")

        # Laufende Nummer
        tk.Label(self.root, text="Lfd. Nr.:").grid(row=7, column=0, sticky="w")
        self.lfd_nr_label = tk.Label(self.root, text="")
        self.lfd_nr_label.grid(row=7, column=1, sticky="w")

        # Buttons
        tk.Button(self.root, text="Speichern", command=self.save_buchung).grid(row=8, column=0)
        tk.Button(self.root, text="Vor", command=self.prev_buchung).grid(row=8, column=1)
        tk.Button(self.root, text="Zurück", command=self.next_buchung).grid(row=8, column=2)

    def open_konto_selector(self):
        selector = tk.Toplevel(self.root)
        selector.title("Konto auswählen")
        canvas = tk.Canvas(selector)
        frame = tk.Frame(canvas)
        vsb = tk.Scrollbar(selector, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        farben = self.konten_provider.get_farben()
        konten_vars = []
        for konto in self.konten_provider.get_all_konten():
            var_k = tk.IntVar()
            cb = tk.Checkbutton(frame, text=f'{konto["nummer"]} - {konto["bezeichnung"]}', 
                                variable=var_k, bg=farben.get(konto["gruppe"], "white"))
            cb.pack(anchor="w")
            konten_vars.append((konto, var_k))

        def confirm_selection():
            selected = [k for k,v in konten_vars if v.get()==1]
            if selected:
                konto_text = f'{selected[0]["nummer"]} - {selected[0]["bezeichnung"]}'
                self.konto_var.set(konto_text)
                self.konto_display.config(text=konto_text, bg=farben.get(selected[0]["gruppe"], "white"))
            selector.destroy()

        tk.Button(selector, text="OK", command=confirm_selection).pack()

    def show_buchung(self, index):
        if index < 0 or index >= len(self.manager.buchungen):
            return
        b = self.manager.buchungen[index]
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, b.datum)
        self.gegenkonto_var.set(b.gegenkonto)
        self.beschreibung_entry.delete(0, tk.END)
        self.beschreibung_entry.insert(0, b.beschreibung)
        self.kundennummer_entry.delete(0, tk.END)
        self.kundennummer_entry.insert(0, b.kundennummer)
        self.rechnungsnummer_entry.delete(0, tk.END)
        self.rechnungsnummer_entry.insert(0, b.rechnungsnummer)
        self.rechnungsdatum_entry.delete(0, tk.END)
        self.rechnungsdatum_entry.insert(0, b.rechnungsdatum)
        self.mwst_var.set(b.mwst)
        self.konto_var.set(b.konto)
        self.konto_display.config(text=b.konto)
        self.soll_entry.delete(0, tk.END)
        self.soll_entry.insert(0, str(b.soll) if b.soll else "")
        self.haben_entry.delete(0, tk.END)
        self.haben_entry.insert(0, str(b.haben) if b.haben else "")
        self.lfd_nr_label.config(text=str(b.lfd_nr))

    def save_buchung(self):
        datum = self.datum_entry.get() or datetime.now().strftime("%Y-%m-%d")
        soll_value = self.soll_entry.get() or "0"
        haben_value = self.haben_entry.get() or "0"
        
        buchung = Buchung(
            datum=datum,
            gegenkonto=self.gegenkonto_var.get(),
            beschreibung=self.beschreibung_entry.get(),
            kundennummer=self.kundennummer_entry.get(),
            rechnungsnummer=self.rechnungsnummer_entry.get(),
            rechnungsdatum=self.rechnungsdatum_entry.get(),
            mwst=self.mwst_var.get(),
            konto=self.konto_var.get(),
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
