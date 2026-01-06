"""
ui.py
All Tkinter UI code for the booking application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from buchung import BuchungManager
import konten_loader


class BuchungUI:
    """Main UI window for booking application."""
    
    def __init__(self):
        """Initialize the booking UI."""
        # Initialize business logic
        self.manager = BuchungManager()
        
        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("Buchung")
        
        # Create UI widgets
        self.create_widgets()
        
        # Load initial booking if exists
        if self.manager.get_buchungen_count() > 0:
            self.show_current_buchung()
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Buchungsdatum
        tk.Label(self.root, text="Buchungsdatum:").grid(row=0, column=0, sticky="w")
        self.datum_entry = tk.Entry(self.root)
        self.datum_entry.grid(row=0, column=1)
        
        # Gegenkonto Dropdown
        tk.Label(self.root, text="Gegenkonto:").grid(row=0, column=3, sticky="w")
        self.gegenkonto_var = tk.StringVar()
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
        self.mwst_combo = ttk.Combobox(self.root, textvariable=self.mwst_var, values=["00", "30", "80", "90"])
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
        """Open the account selection popup with color-coded groups."""
        selector = tk.Toplevel(self.root)
        selector.title("Konto auswählen")
        canvas = tk.Canvas(selector)
        frame = tk.Frame(canvas)
        vsb = tk.Scrollbar(selector, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Get accounts using konten_loader
        accounts = konten_loader.get_all_accounts()
        
        konten_vars = []
        for konto in accounts:
            var_k = tk.IntVar()
            color = konten_loader.get_group_color(konto["gruppe"])
            cb = tk.Checkbutton(
                frame, 
                text=f'{konto["nummer"]} - {konto["bezeichnung"]}',
                variable=var_k,
                bg=color
            )
            cb.pack(anchor="w")
            konten_vars.append((konto, var_k))
        
        def confirm_selection():
            selected = [k for k, v in konten_vars if v.get() == 1]
            if selected:
                konto_text = f'{selected[0]["nummer"]} - {selected[0]["bezeichnung"]}'
                self.konto_var.set(konto_text)
                color = konten_loader.get_group_color(selected[0]["gruppe"])
                self.konto_display.config(text=konto_text, bg=color)
            selector.destroy()
        
        tk.Button(selector, text="OK", command=confirm_selection).pack()
    
    def show_current_buchung(self):
        """Display the current booking in the UI."""
        buchung = self.manager.get_current_buchung()
        if buchung is None:
            return
        
        # Clear and populate fields
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, buchung.get("datum", ""))
        
        self.gegenkonto_var.set(buchung.get("gegenkonto", ""))
        
        self.beschreibung_entry.delete(0, tk.END)
        self.beschreibung_entry.insert(0, buchung.get("beschreibung", ""))
        
        self.kundennummer_entry.delete(0, tk.END)
        self.kundennummer_entry.insert(0, buchung.get("kundennummer", ""))
        
        self.rechnungsnummer_entry.delete(0, tk.END)
        self.rechnungsnummer_entry.insert(0, buchung.get("rechnungsnummer", ""))
        
        self.rechnungsdatum_entry.delete(0, tk.END)
        self.rechnungsdatum_entry.insert(0, buchung.get("rechnungsdatum", ""))
        
        self.mwst_var.set(buchung.get("mwst", ""))
        
        konto = buchung.get("konto", "")
        self.konto_var.set(konto)
        self.konto_display.config(text=konto)
        
        self.soll_entry.delete(0, tk.END)
        self.soll_entry.insert(0, buchung.get("soll", ""))
        
        self.haben_entry.delete(0, tk.END)
        self.haben_entry.insert(0, buchung.get("haben", ""))
        
        self.lfd_nr_label.config(text=str(buchung.get("lfd_nr", "")))
    
    def save_buchung(self):
        """Save the current booking."""
        buchung_data = {
            "datum": self.datum_entry.get(),
            "gegenkonto": self.gegenkonto_var.get(),
            "beschreibung": self.beschreibung_entry.get(),
            "kundennummer": self.kundennummer_entry.get(),
            "rechnungsnummer": self.rechnungsnummer_entry.get(),
            "rechnungsdatum": self.rechnungsdatum_entry.get(),
            "mwst": self.mwst_var.get(),
            "konto": self.konto_var.get(),
            "soll": self.soll_entry.get(),
            "haben": self.haben_entry.get()
        }
        
        self.manager.save_current_buchung(buchung_data)
        self.show_current_buchung()
        messagebox.showinfo("Info", "Buchung gespeichert.")
    
    def prev_buchung(self):
        """Navigate to previous booking."""
        if self.manager.navigate_previous():
            self.show_current_buchung()
    
    def next_buchung(self):
        """Navigate to next booking."""
        if self.manager.navigate_next():
            self.show_current_buchung()
    
    def run(self):
        """Start the UI main loop."""
        self.root.mainloop()


def start_ui():
    """Entry point to start the booking UI."""
    app = BuchungUI()
    app.run()


if __name__ == "__main__":
    start_ui()
