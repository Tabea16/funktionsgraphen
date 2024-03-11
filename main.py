# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import math

# Erstellen bzw. Verbinden der SQLite-Datenbank
conn = sqlite3.connect('user_database1.db')
c = conn.cursor()

# Erstellen der Tabelle, falls sie noch nicht existiert
c.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()


# Funktion zur Registrierung eines neuen Benutzers
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        try:
            c.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Erfolg", "Benutzer erfolgreich registriert!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Fehler", "Benutzername bereits vergeben.")
    else:
        messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")


# Funktion zur Anmeldung eines Benutzers
def login_user():
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    if c.fetchone():
        messagebox.showinfo("Erfolg", "Anmeldung erfolgreich!")
        open_main_window()
    else:
        messagebox.showerror("Fehler", "Benutzername oder Passwort falsch.")


# Funktion zum Öffnen des Hauptfensters für das Plotten
def open_main_window():
    main_window = tk.Toplevel()
    main_window.title("Funktionsformel-Eingabe")

    tk.Label(main_window, text="Funktionsformel (z.B. '5*x + 3'):").pack()
    lineare_formel_entry = tk.Entry(main_window)
    lineare_formel_entry.pack(side='top')
    reset_button = tk.Button(main_window, text="Reset", command=lambda: lineare_formel_entry.delete(0, 100))
    reset_button.pack(side='top')

    tk.Button(main_window, text="erstellen", command=lambda: plot_function(lineare_formel_entry.get())).pack(side='top')

    # Knöpfe für Beispielformeln
    tk.Label(main_window, text="Beispielformeln (z.B. '5*x**2 + 4*x + 3'):").pack()
    def_lin = tk.Button(main_window, text="Lineare Funktion", command=lambda: plot_function("5*x+3"))
    def_lin.pack(side='left')
    def_quad = tk.Button(main_window, text="Quadratische Funktion", command=lambda: plot_function("5*x**2 + 4*x + 3"))
    def_quad.pack(side='left')
    def_sin = tk.Button(main_window, text="Sinus Funktion", command=lambda: plot_function("3*math.sin(x)"))
    def_sin.pack(side='left')
    def_cos = tk.Button(main_window, text="Cosinus Funktion", command=lambda: plot_function("2*math.cos(x)"))
    def_cos.pack(side='left')
    """tk.Label(main_window, text="Quadratische Funktionsformel (z.B. '5*x**2 + 4*x + 3'):").pack()
    quadratische_formel_entry = tk.Entry(main_window)
    quadratische_formel_entry.pack()

    tk.Button(main_window, text="erstellen", command=lambda: plot_function(quadratische_formel_entry.get(),
                                                                           "Quadratische Funktion")).pack()

    tk.Label(main_window, text="Sinus-Funktion (z.B. '3*math.sin(x)'):").pack()
    sinus_formel_entry = tk.Entry(main_window)
    sinus_formel_entry.pack()

    tk.Button(main_window, text="erstellen", command=lambda: plot_function(sinus_formel_entry.get(),
                                                                           "Sinus-Funktion")).pack()

    tk.Label(main_window, text="Cosinus-Funktion (z.B. '2*math.cos(x)'):").pack()
    cosinus_formel_entry = tk.Entry(main_window)
    cosinus_formel_entry.pack()

    tk.Button(main_window, text="erstellen", command=lambda: plot_function(cosinus_formel_entry.get(),
                                                                           "Cosinus-Funktion")).pack()

    tk.Label(main_window, text="Tangens-Funktion (z.B. 'math.tan(x)'):").pack()
    tangens_formel_entry = tk.Entry(main_window)
    tangens_formel_entry.pack()

   tk.Button(main_window, text="erstellen", command=lambda: plot_function(tangens_formel_entry.get(),
                                                                           "Tangens-Funktion")).pack()
   """


# Funktion zum Plotten der Funktionen

def plot_function(formel_entry, default='5*x+3'):
    x_values = np.linspace(-15, 15, 400)

    if formel_entry == '':
        formel_entry = default

    plt.figure(figsize=(10, 5))
    # Create the plot

    y_values_lineare = [eval(formel_entry.replace("x", f"({x})")) for x in x_values]
    plt.plot(x_values, y_values_lineare, label='Funktion: ' + formel_entry)

    plt.title('Graphen der Funktionen')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()


# Erstellen des Login-Fensters
login_window = tk.Tk()
login_window.title("Login / Registrierung")
login_window.geometry("400x250")  # Festlegen der Größe des Fensters
login_window.configure(bg="black")  # Hintergrundfarbe des Fensters

# Schriftfarbe und Schriftart für das Fenster
font_color = "white"
font_style = ("Helvetica", 12)

# Rahmen für die Eingabefelder
frame = tk.Frame(login_window, bg="black", padx=10, pady=10)
frame.pack(expand=True, fill="both")

# Benutzername Label und Eingabefeld
username_label = tk.Label(frame, text="Benutzername:", bg="black", fg=font_color, font=font_style)
username_label.grid(row=0, column=0, pady=5, sticky="w")
username_entry = tk.Entry(frame, font=font_style)
username_entry.grid(row=0, column=1, pady=5, padx=5)

# Passwort Label und Eingabefeld
password_label = tk.Label(frame, text="Passwort:", bg="black", fg=font_color, font=font_style)
password_label.grid(row=1, column=0, pady=5, sticky="w")
password_entry = tk.Entry(frame, show="*", font=font_style)
password_entry.grid(row=1, column=1, pady=5, padx=5)

# Anmelde- und Registrierungsbuttons
login_button = ttk.Button(frame, text="Anmelden", command=login_user)
login_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

register_button = ttk.Button(frame, text="Registrieren", command=register_user)
register_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

login_window.mainloop()
