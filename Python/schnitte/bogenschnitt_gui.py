from tkinter import *
from tkinter import Entry, Tk
import schnitte.bogenschnitt
import daten.punkt
import daten.strecke
from grundlagen import gui
import datendienst.datendienst as datd
import json
import numpy as np

class Anwendung(Frame):
    """Klasse Anwendung vom Modul Bogenschnitt
       Jade HS
       Vorlesung "Programmieren geodätischer Aufgaben"
       M. Hackenberg
       WiSe 2020/21
       Stand: 2021-02-09
       Version 1.0.0
       """

    def __init__(self, master: object):
        """Konstruktor
        :param master: parent window (TKinter)
        :type object"""

        #Erben des Objekts master (Fenster), von der Elternklasse Frame (TKinter)
        super().__init__(master)
        self.__meister = master
        # Definition der Ein- und Ausgabefelder
        self.__eingabe_y1: float = Entry(self)
        self.__eingabe_y2: float = Entry(self)
        self.__eingabe_x1: float = Entry(self)
        self.__eingabe_x2: float = Entry(self)
        self.__eingabe_s1: float = Entry(self)
        self.__eingabe_s2: float = Entry(self)
        self.__eingabe_s3: float = Entry(self)
        self.__ausgabe_pn1: daten.punkt.Punkt= Entry(self, width=50)
        self.__ausgabe_pn2: daten.punkt.Punkt =Entry(self, width=50)
        self.__ausgabe_m: float = Entry(self, width=50)

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui von Bogenschnittberechnung"""
        #TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()

        #Label zur Beschreibung der Funktionalitaet des Fensters
        Label(self, text="PGA | Bogenschnitt").grid(row=0, column=0, columnspan=3)

        #Anordnung der Ein- und Ausgabefelder im Fenster
        self.__eingabe_y1.grid(row=0, column=0)
        self.__eingabe_y2.grid(row=1, column=0)
        self.__eingabe_x1.grid(row=2, column=0)
        self.__eingabe_x2.grid(row=3, column=0)
        self.__eingabe_s1.grid(row=4, column=0)
        self.__eingabe_s2.grid(row=5, column=0)
        self.__eingabe_s3.grid(row=6, column=0)

        self.__ausgabe_pn1.grid(row=2, column=2)
        self.__ausgabe_pn2.grid(row=4, column=2)
        self.__ausgabe_m.grid(row=6, column=2)

        #Anordnung der Label zur Beschriftung der Ein- und Ausgabefelder
        Label(self, text="[y1]", anchor=W, justify=LEFT, width=10).grid(row=0, column=1)
        Label(self, text="[y2]", anchor=W, justify=LEFT, width=10).grid(row=1, column=1)
        Label(self, text="[x1]", anchor=W, justify=LEFT, width=10).grid(row=2, column=1)
        Label(self, text="[x2]", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)
        Label(self, text="[s1]", anchor=W, justify=LEFT, width=10).grid(row=4, column=1)
        Label(self, text="[s2]", anchor=W, justify=LEFT, width=10).grid(row=5, column=1)
        Label(self, text="[s3](optional)", anchor=W, justify=LEFT, width=10).grid(row=6, column=1)
        Label(self, text="[pn1]", anchor=W, justify=LEFT, width=15).grid(row=1, column=2)
        Label(self, text="[pn2]", anchor=W, justify=LEFT, width=15).grid(row=3, column=2)
        Label(self, text="[Maßstab]", anchor=W, justify=LEFT, width=15).grid(row=5, column=2)

        #Anordnung der Buttons zum Ausfuehren der Berechnung/Laden von Testdaten/schliessen des Fensters
        Button(self, text="berechne", command=self.berechne).grid(row=0, column=3)
        Button(self, text="test", command=self.test).grid(row=2, column=3)
        Button(self, text="test2", command=self.test2).grid(row=3, column=3)
        Button(self, text="test3", command=self.test3).grid(row=4, column=3)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=6, column=3)

    def berechne(self) -> object:
        """berechne Bogenschnitt mit Modul Bogenschnitt.py"""

        #Definition der Variablen durch Auswertung der Eingabefelder
        y1: float = gui.eingabefeld_auswerten(self.__eingabe_y1)
        x1: float  = gui.eingabefeld_auswerten(self.__eingabe_x1)
        y2: float  = gui.eingabefeld_auswerten(self.__eingabe_y2)
        x2: float  = gui.eingabefeld_auswerten(self.__eingabe_x2)

        s1: np.float64  = gui.eingabefeld_auswerten(self.__eingabe_s1)
        s2: np.float64  = gui.eingabefeld_auswerten(self.__eingabe_s2)
        s3: np.float64 = gui.eingabefeld_auswerten(self.__eingabe_s3)

        #Definition der beiden gegebenen Punkte als Instanzen der Klasse Punkt
        p1: daten.punkt.Punkt = daten.punkt.Punkt(y1, x1)
        p2: daten.punkt.Punkt = daten.punkt.Punkt(y2, x2)
        # Definition der drei Strecken als Instanzen der Klasse Strecke
        s1: daten.strecke.Strecke = daten.strecke.Strecke.punkt_laenge(p1, s1)
        s2: daten.strecke.Strecke = daten.strecke.Strecke.punkt_laenge(p2, s2)
        s3: daten.strecke.Strecke = daten.strecke.Strecke.punkt_laenge(p1, s3)


        #Ausfuehrung der Berechnung durch die Klasse Bogenschnitt, Kreation der Instanz bs der Klasse, Uebergabe der 3 Streckenobjekte an die Instanz
        bs: bogenschnitt.Bogenschnitt()
        bs: schnitte.bogenschnitt.Bogenschnitt=schnitte.bogenschnitt.Bogenschnitt(s1,s2,s3)

        #Definition der Ergebnisvariablen durch Index slicing des Ergebnistupels der Instanz bs
        pn1: daten.punkt.Punkt=bs.berechne()[0]
        pn2: daten.punkt.Punkt=bs.berechne()[1]
        m : float = bs.berechne()[2]

        #Weitergabe der Ergebnisvariablen zum Eintrag der Ergebnisfelder
        self.ausgabefeld_schreiben(pn1, pn2,m)

        #Weitergabe der Ergebnisse an den Server
        dienst_url = 'https://mapsrv.net/pga/service/'
        # dienst_url = 'http://dropbox.local/hostpoint/mapsrv.net/www/pga/service/'

        #Instanz der Klasse Datendienst
        dd: datd.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', dienst_url, True)

        #Definition des von der Instanz bs erhaltenen Dictionaries mit allen Ergebnissen
        meine_json_daten_antwort: dict = bs.berechne()[3]

        # Schreiben (und Empfangen)
        print("SCHREIBEN ---------------")

        param_schreiben: dict = {'datasetid': 'schnittbogenkahmen-punkte', 'request': 'postdata'}
        meine_klasse_vorgabe = 'Punkt'

        #Parsen des Dictionaries mit allen Ergebnissen
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(meine_json_daten_antwort, meine_klasse_vorgabe)

        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)
        print("dienst", dienst_json_daten_antwort2)

    def test(self):
        """Testparameter 1"""
        #Definition der Testparamenter
        y1: float = 328.76
        x1: float = 1207.85
        y2: float = 925.04
        x2: float = 954.33
        s1: float = 294.33
        s2: float = 506.42
        s3: float = 648.08
        #Eintrag der Parameter in die Eingabefelder
        self.eingabefelder_schreiben(y1, x1, y2, x2,s1,s2,s3)

    def test2(self):
        """Testparameter 2 (schlechter Schnitt)"""
        # Definition der Testparamenter
        y1: float = 328.76
        x1: float = 1207.85
        y2: float= 925.04
        x2: float = 954.33
        s1: float = 141.5169018662233
        s2: float = 506.42
        s3: float = 0.0
        # Eintrag der Parameter in die Eingabefelder
        self.eingabefelder_schreiben(y1, x1, y2, x2, s1, s2, s3)

    def test3(self):
        """Testparameter 3 (keine Loesung)"""
        # Definition der Testparamenter
        y1: float = 328.76
        x1: float = 1207.85
        y2: float = 925.04
        x2: float = 954.33
        s1: float = 141.5169018662233
        s2: float = 200
        s3: float=648.08
        # Eintrag der Parameter in die Eingabefelder
        self.eingabefelder_schreiben(y1, x1, y2, x2, s1, s2,s3)

    def eingabefelder_schreiben(self, p_y1, p_x1, p_y2, p_x2, p_s1,p_s2,p_s3):
        """Schreiben der Eingaben in Eingabefelder    """
        gui.eingabefeld_schreiben(self.__eingabe_y1, p_y1)
        gui.eingabefeld_schreiben(self.__eingabe_x1, p_x1)
        gui.eingabefeld_schreiben(self.__eingabe_y2, p_y2)
        gui.eingabefeld_schreiben(self.__eingabe_x2, p_x2)
        gui.eingabefeld_schreiben(self.__eingabe_s1, p_s1)
        gui.eingabefeld_schreiben(self.__eingabe_s2, p_s2)
        gui.eingabefeld_schreiben(self.__eingabe_s3, p_s3)

    def ausgabefeld_schreiben(self, p_n1, p_n2,p_m):
        """Schreiben der Ergebnisse in Ergebnisfelder     """
        gui.eingabefeld_schreiben(self.__ausgabe_pn1, p_n1)
        gui.eingabefeld_schreiben(self.__ausgabe_pn2, p_n2)
        gui.eingabefeld_schreiben(self.__ausgabe_m, p_m)



if __name__== "__main__":
    fenster: Tk = Tk()
    anwendung = Anwendung(fenster)
    fenster.mainloop()
