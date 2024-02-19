from tkinter import *
from grundlagen import gui, winkel


class Anwendung(Frame):

    def __init__(self, master):

        # Konstruktor der Elternklasse (Frame) aufrufen
        # Diese benötigt als Parameter das übergeordnete Widget
        # In diesem Fall also master, also das Toplevel-Widget (DIE Tkinter-Applikation an sich)
        super().__init__(master)

        # Master als Attribut ablegen (Benutzung erfolgt beim Schließen der Anwendung)
        self.meister = master


        # Eingabefelder als Attribute (Attribute immer im Konstruktor anlegen!)

        # HINWEIS: Oberflächenelemente, die später noch verändert oder ausgelesen werden müssen,
        # sollten Klassen-Variablen zugewiesen werden, über die der Zugriff dann erfolgen kann.
        # Andere Elemente, wie z.b. 'statische' Label, können einfach ohne Zuweisung erzeugt werden.

        # HINWEIS: Bitte nicht "eingaberad = Entry(fenster).grid(row=1, column=0)" verwenden!
        # Denn dann beinhaltet die Variable "eingaberad" das Grid-Element und nicht das Eingabefeld!
        self.eingabe_rad = Entry(self)
        self.eingabe_gon = Entry(self)
        self.eingabe_deg = Entry(self)

        # Oberfläche initialisieren
        self.initialisiere_gui()


    def initialisiere_gui(self):

        #
        # Benutzeroberfläche auf Grid-Basis (also ein regelmäßiges Gitter mit Zeilen und Spalten)
        #
        self.grid()

        # HINWEIS: Elemente in Zeile oder Spalte 0 benötigen kein "row" oder "column" Attribut
        # Zeile 0

        # Label mit Frame (also diese Klasse selber) als Masterelement. Ausdehnung über drei Spalten
        Label(self, text="PGA | Winkelumrechnungen").grid(row=0, column=0, columnspan=3)

        # Zeilen 1 - 3

        # Spalte 0: Eingabefelder

        self.eingabe_rad.grid(row=1, column=0)
        self.eingabe_gon.grid(row=2, column=0)
        self.eingabe_deg.grid(row=3, column=0)

        # Spalte 1: Beschriftungen

        # Anker ist an der westlichen Seite, linksbündig und Breite 10
        Label(self, text="[rad]", anchor=W, justify=LEFT, width=10).grid(row=1, column=1)
        Label(self, text="[gon]", anchor=W, justify=LEFT, width=10).grid(row=2, column=1)
        Label(self, text="[°]", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)

        # Spalte 2: Knöpfe

        # HINWEIS: Bitte nicht "command=umrechnenrad()", also mit Klammern, verwenden, da sonst "umrechnenrad"
        # unmittelbar beim Start des Programms aufgerufen wird und nicht erst beim Klick auf den Knopf!
        Button(self, text="Umrechnen", command=self.umrechnen_rad).grid(row=1, column=2)
        Button(self, text="Umrechnen", command=self.umrechnen_gon).grid(row=2, column=2)
        Button(self, text="Umrechnen", command=self.umrechnen_deg).grid(row=3, column=2)

        # Zeile 4
        Button(self, text="Beenden", command=self.meister.destroy).grid(row=4, column=0, columnspan=3)


    def umrechnen_rad(self):
        rad = gui.eingabefeld_auswerten(self.eingabe_rad)
        gon = winkel.rad2gon(rad)
        deg = winkel.rad2deg(rad)
        self.eingabefelder_schreiben(rad, gon, deg)


    def umrechnen_gon(self):
        gon = gui.eingabefeld_auswerten(self.eingabe_gon)
        rad = winkel.gon2rad(gon)
        deg = winkel.gon2deg(gon)
        self.eingabefelder_schreiben(rad, gon, deg)


    def umrechnen_deg(self):
        deg = gui.eingabefeld_auswerten(self.eingabe_deg)
        gon = winkel.deg2gon(deg)
        rad = winkel.deg2rad(deg)
        self.eingabefelder_schreiben(rad, gon, deg)


    def eingabefelder_schreiben(self, p_rad, p_gon, p_deg):
        gui.eingabefeld_schreiben(self.eingabe_rad, p_rad)
        gui.eingabefeld_schreiben(self.eingabe_gon, p_gon)
        gui.eingabefeld_schreiben(self.eingabe_deg, p_deg)


if __name__ == "__main__":

    # Toplevel-Widget (DIE Tkinter-Applikation an sich)
    fenster = Tk()

    # Frame-Widget, dass unsere Oberflächenelemente (Eingabe, Knöpfe, Beschriftungen) aufnimmt
    # Ein Frame kann dann später leicht woanders wieder integriert werden.
    # Als Parameter wird das Element übergeben, in das der Frame integriert werden soll (der sogenannte Master)
    anwendung = Anwendung(fenster)

    # Hauptschleife
    fenster.mainloop()
