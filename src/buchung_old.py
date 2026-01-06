# Buchung.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import konten  # Import der Kontenliste

BUCHUNGEN_FILE = "buchungen.json"

class Buchung:
    def __init__(self):
        # Lade Buchungen oder starte leer
        try:
            with open(BUCHUNGEN_FILE, "r", encoding="utf-8") as f:
                self.buchungen = json.load(f)
        except FileNotFoundError:
            self.buchungen = []
        self.index = len(self.buchungen) - 1

        # Tkinter Fenster
        self.root = tk.Tk()
        self.root.title("Buchung")

        self.create_widgets()
        if self.buchungen:
            self.show_buchung(self.index)
        self.root.mainloop()

    def create_widgets(self):
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

        farben = {
            "Anlagen": "lightblue",
            "Finanzen": "lightgreen",
            "Privat": "lightyellow",
            "Erträge": "lightcyan",
            "Material": "lightpink",
            "Löhne": "orange",
            "Miete": "violet",
            "Steuern": "violet",
            "Versicherung": "lightgray",
            "Fahrzeug": "lightgray",
            "Werbung": "lightgray",
            "Reisen": "lightgray",
            "Allgemein": "wheat",
            "Fortbildung": "wheat",
            "Beratung": "wheat",
            "Betrieb": "wheat",
            "Serviceleistungen": "red",
            "Verkäufe": "gold"
        }

        konten_vars = []
        for konto in konten.konten_liste:
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
        if index < 0 or index >= len(self.buchungen):
            return
        b = self.buchungen[index]
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, b["datum"])
        self.gegenkonto_var.set(b.get("gegenkonto", ""))
        self.beschreibung_entry.delete(0, tk.END)
        self.beschreibung_entry.insert(0, b["beschreibung"])
        self.kundennummer_entry.delete(0, tk.END)
        self.kundennummer_entry.insert(0, b["kundennummer"])
        self.rechnungsnummer_entry.delete(0, tk.END)
        self.rechnungsnummer_entry.insert(0, b["rechnungsnummer"])
        self.rechnungsdatum_entry.delete(0, tk.END)
        self.rechnungsdatum_entry.insert(0, b["rechnungsdatum"])
        self.mwst_var.set(b["mwst"])
        self.konto_var.set(b["konto"])
        self.konto_display.config(text=b["konto"])
        self.soll_entry.delete(0, tk.END)
        self.soll_entry.insert(0, b["soll"])
        self.haben_entry.delete(0, tk.END)
        self.haben_entry.insert(0, b["haben"])
        self.lfd_nr_label.config(text=str(b["lfd_nr"]))

    def save_buchung(self):
        datum = self.datum_entry.get() or datetime.now().strftime("%Y-%m-%d")
        buchung = {
            "datum": datum,
            "gegenkonto": self.gegenkonto_var.get(),
            "beschreibung": self.beschreibung_entry.get(),
            "kundennummer": self.kundennummer_entry.get(),
            "rechnungsnummer": self.rechnungsnummer_entry.get(),
            "rechnungsdatum": self.rechnungsdatum_entry.get(),
            "mwst": self.mwst_var.get(),
            "konto": self.konto_var.get(),
            "soll": self.soll_entry.get(),
            "haben": self.haben_entry.get(),
            "lfd_nr": self.index+2
        }
        if self.index+1 < len(self.buchungen):
            self.buchungen[self.index] = buchung
        else:
            self.buchungen.append(buchung)
            self.index = len(self.buchungen) - 1

        with open(BUCHUNGEN_FILE, "w", encoding="utf-8") as f:
            json.dump(self.buchungen, f, ensure_ascii=False, indent=4)
        self.show_buchung(self.index)
        messagebox.showinfo("Info", "Buchung gespeichert.")

    def prev_buchung(self):
        if self.index > 0:
            self.index -= 1
            self.show_buchung(self.index)

    def next_buchung(self):
        if self.index < len(self.buchungen)-1:
            self.index += 1
            self.show_buchung(self.index)

if __name__ == "__main__":
    Buchung()
