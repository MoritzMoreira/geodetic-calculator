from tkinter import *
from tkinter import Toplevel
import polygonzug.polygonzug_beidseitig_gui
#import polygonzug.p
import grundlagen.winkel_gui
import grundlagen.erstegrund_gui
import grundlagen.zweitegrund_gui
import schnitte.bogenschnitt_gui
import transformationen.helmerttransformation_gui
import transformationen.affintransformation_gui
import schnitte.ruckwartsschnitt_gui
import schnitte.vorwartsschnitt_gui


class Anwendung(Frame):
    """Klasse Anwendung, erbst von Frame (TKinter)"""

    def __init__(self, master):
        """Konstruktor
               :param master: parent window (TKinter)
               :type object"""
        #Aufruf des Konstruktors der Elternklasse
        super().__init__(master)

        self.meister: object = master
        #GUI initialisieren
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere_gui
                       """
        # TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()
        # Anordnung der Buttons zum Ausfuehren der geodaetischen Berechnungen
        Button(self, text="Winkel", command=self.fenster_winkel).grid(row=0)
        Button(self, text="1. Geod. GA", command=self.fenster_erstega).grid(row=1)
        Button(self, text="2. Geod. GA", command=self.fenster_zweitega).grid(row=2)
        Button(self, text="Bogenschnitt", command=self.fenster_bogenschnitt).grid(row=3)
        Button(self, text="Rückwärtsschnitt", command=self.fenster_rueckschnitt).grid(row=4)
        Button(self, text="Vorwärtsschnitt", command=self.fenster_vorschnitt).grid(row=5)
        Button(self, text="Helmerttransformation", command=self.fenster_helmerttrafo).grid(row=6)
        Button(self, text="Affintransformation", command=self.fenster_affintrafo).grid(row=7)
        Button(self, text="beidseitig angeschlossener Polygonzug", command=self.fenster_poly_beidseitig).grid(row=8)
        Button(self, text="Ringpolygonzug", command=self.fenster_ringpoly).grid(row=9)
        Button(self, text="Beenden", command=self.meister.destroy).grid(row=10)

    def fenster_ringpoly(self):
        """fenster_vorschnitt, definiert Instanz der Klasse Anwendung von der Vorwaertsschnitt-GUI
                               """
        top: Toplevel = Toplevel()
        #frame: object = schnitte.vorwartsschnitt_gui.Anwendung(top)
        pass
    def fenster_poly_beidseitig(self):
        """fenster_vorschnitt, definiert Instanz der Klasse Anwendung von der Vorwaertsschnitt-GUI
                               """
        top: Toplevel = Toplevel()
        frame: object = polygonzug.polygonzug_beidseitig_gui.Anwendung(top)

    def fenster_vorschnitt(self):
        """fenster_vorschnitt, definiert Instanz der Klasse Anwendung von der Vorwaertsschnitt-GUI
                               """
        top: Toplevel = Toplevel()
        frame: object = schnitte.vorwartsschnitt_gui.Anwendung(top)

    def fenster_rueckschnitt(self):
        """fenster_rueckschnitt, definiert Instanz der Klasse Anwendung von der Rueckwaertsschnitt-GUI
                                       """
        top: Toplevel = Toplevel()
        frame: object = schnitte.ruckwartsschnitt_gui.Anwendung(top)
    def fenster_bogenschnitt(self):
        """fenster_bogenschnitt, definiert Instanz der Klasse Anwendung von der Bogenschnitt-GUI
                                       """
        top: Toplevel=Toplevel()
        frame: object=schnitte.bogenschnitt_gui.Anwendung(top)

    def fenster_winkel(self):
        """fenster_winkel, definiert Instanz der Klasse Anwendung von der Winkel-GUI
                                       """
        top: Toplevel = Toplevel()
        frame: object = grundlagen.winkel_gui.Anwendung(top)

    def fenster_erstega(self):
        """fenster_erstega, definiert Instanz der Klasse Anwendung von der GUI der ersten Grundaufgabe
                                               """
        top: Toplevel = Toplevel()
        frame: object = grundlagen.erstegrund_gui.Anwendung(top)

    def fenster_zweitega(self):
        """fenster_zweitega, definiert Instanz der Klasse Anwendung von der GUI der zweiten Grundaufgabe
                                                       """
        top: Toplevel = Toplevel()
        frame: object = grundlagen.zweitegrund_gui.Anwendung(top)
    def fenster_helmerttrafo(self):
        """fenster_helmerttrafo, definiert Instanz der Klasse Anwendung von der GUI der Helmerttransformation
                                                       """
        top: Toplevel = Toplevel()
        frame: object = transformationen.helmerttransformation_gui.Anwendung(top)
    def fenster_affintrafo(self):
        """fenster_affintrafo, definiert Instanz der Klasse Anwendung von der GUI der Affintransformation
                                                               """
        top: Toplevel = Toplevel()
        frame: object = transformationen.affintransformation_gui.Anwendung(top)


if __name__ == "__main__":

    fenster = Tk()

    anwendung = Anwendung(fenster)

    fenster.mainloop()







