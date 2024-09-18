import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv
from datetime import datetime

today = datetime.today().date()

declined = [
    ["Order Reference", "Transaction Date", "Status", "Status Note"]
]

amended = [
    ["Order Reference", "Transaction Date", "Status", "Status Note", "New Sale Price", "Commission Breakdown", "Currency"]
]

accepted = [
    ["Order Reference", "Transaction Date", "Status"]
]

def on_button_click():
    label.config(text="Button clicked!")

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    with (open(filename, mode="r", encoding="utf-8") as file):
        reader = csv.reader(file, delimiter=";")
        firstRow = True
        for row in reader:
            if firstRow == True:
                firstRow = False
                continue
            testBestellung = row[8]
            if testBestellung == "R" or testBestellung == "Ja":
                declinedRow = [row[0], row[4], "DECLINED", row[11]]
                declined.append(declinedRow)
                continue
            elif testBestellung == "T":
                umsatzSplitted = row[6].split()
                #Falls da ausversehen aus der Schweiz was drin ist
                if umsatzSplitted[1] == "CHF":
                    declinedRow = [row[0], row[4], "DECLINED", row[11]]
                    declined.append(declinedRow)
                    continue
                amendedRow = [row[0], row[4], "AMENDED", row[11], row[6], "", "EUR"]
                amended.append(amendedRow)
                continue
            elif testBestellung == "" or row[11] == "Filialbelieferung, keine Provision":
                acceptedRow = [row[0], row[4], "ACCEPTED"]
                accepted.append(acceptedRow)
                continue
def save_file():
    # Öffnet den Dateidialog, um den Speicherort und Dateinamen auszuwählen
    file_path = filedialog.askdirectory()

    # Wenn der Benutzer keinen Pfad ausgewählt hat, abbrechen
    if not file_path:
        return

    # CSV-Datei erstellen und Daten schreiben
    with open(file_path + "/declined-" + today.strftime("%d-%m-%Y") + ".csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(declined)

    print(f"CSV-Datei erfolgreich erstellt unter {file_path}")

    # CSV-Datei erstellen und Daten schreiben
    with open(file_path + "/amended-" + today.strftime("%d-%m-%Y") + ".csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(amended)

    print(f"CSV-Datei erfolgreich erstellt unter {file_path}")

    # CSV-Datei erstellen und Daten schreiben
    with open(file_path + "/accepted-" + today.strftime("%d-%m-%Y") + ".csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(accepted)

    print(f"CSV-Datei erfolgreich erstellt unter {file_path}")

# Erstelle das Hauptfenster
root = tk.Tk()
root.title("coupling media AWIN Abgleiche")
root.geometry("500x200")
root.configure(bg="#1c1f24")
root.resizable(False, False)

# Erstelle einen neuen Stil
style = ttk.Style()

# Neuen Stil basierend auf einem vorhandenen Theme erstellen
style.theme_create("MyTheme", parent="clam", settings={
    "TButton": {
        "configure": {
            "foreground": "white",
            "background": "#12161c",
            "font": ("Arial", 12, "bold"),
            "padding": 10,
            "relief": "flat"
        },
        "map": {
            "background": [("active", "#272f3b"), ("disabled", "#f0f0f0")],
            "foreground": [("active", "white"), ("disabled", "gray")]
        }
    },
    "TLabel": {
        "configure": {
            "foreground": "white",
            "background": "#1c1f24",
            "font": ("inter", 10),
            "padding": 5
        }
    }
})

# Theme aktivieren
style.theme_use("MyTheme")

# Erstelle ein Label
label = ttk.Label(root, text="Wähle den Abgleich (.csv) aus und drücke dann auf Speichern!")
label.pack()

'''
def on_select(value):
    print(f"Ausgewählt: {value}")

# Variable, die den aktuellen Wert speichert
selected_option = tk.StringVar(root)
selected_option.set("Option 1")  # Standardwert festlegen

# Liste von Optionen
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Dropdown-Menü erstellen
dropdown = tk.OptionMenu(root, selected_option, *options, command=on_select)
dropdown.pack(pady=20)
'''

# Erstelle einen Button
button = ttk.Button(root, text='Öffnen', command=UploadAction)
button.place(relx=0.5, rely=0.4, anchor="center")

# Button erstellen und Funktion zum Speichern verknüpfen
save_button = ttk.Button(root, text="Speichern", command=save_file)
save_button.place(relx=0.5, rely=0.7, anchor="center")

# Starte die Haupt-Event-Schleife
root.mainloop()
