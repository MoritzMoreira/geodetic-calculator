from tkinter import *
import schnitte.vorwartsschnitt
import daten.punkt
import daten.strecke
from daten.punkt import Punkt
from grundlagen import gui
import datendienst.datendienst as datd
import json

class Anwendung(Frame):

    def __init__(self, master):
        """Konstruktor
        :param master: parent window (TKinter)
        :type object
        """

        # Erben des Objekts master (Fenster), von der Elternklasse Frame (TKinter)
        super().__init__(master)

        self.__meister = master

        # Definition der Ein- und Ausgabefelder
        self.__eingabe_x1 = Entry(self)
        self.__eingabe_x2 = Entry(self)
        self.__eingabe_x3 = Entry(self)
        self.__eingabe_x4 = Entry(self)
        self.__eingabe_y1 = Entry(self)
        self.__eingabe_y2 = Entry(self)
        self.__eingabe_y3 = Entry(self)
        self.__eingabe_y4 = Entry(self)
        self.__eingabe_phi = Entry(self)
        self.__eingabe_psi = Entry(self)
        self.__ausgabe_pn = Entry(self, width=50)

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui von Bogenschnittberechnung"""
        # TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()
        #Label zur Beschreibung der Funktionalität des Fensters
        Label(self, text="PGA | Vorwärtsschnitt").grid(row=0, column=1, columnspan=3)
        #Anordnung der Ein-/ Ausgabefelder
        self.__eingabe_y1.grid(row=0, column=0)
        self.__eingabe_x1.grid(row=1, column=0)
        self.__eingabe_y2.grid(row=2, column=0)
        self.__eingabe_x2.grid(row=3, column=0)
        self.__eingabe_y3.grid(row=4, column=0)
        self.__eingabe_x3.grid(row=5, column=0)
        self.__eingabe_y4.grid(row=6, column=0)
        self.__eingabe_x4.grid(row=7, column=0)
        self.__eingabe_phi.grid(row=8, column=0)
        self.__eingabe_psi.grid(row=9, column=0)

        self.__ausgabe_pn.grid(row=2, column=2)


        # Anordnung der Label zur Beschriftung der Ein- und Ausgabefelder
        Label(self, text="[y1]", anchor=W, justify=LEFT, width=10).grid(row=0, column=1)
        Label(self, text="[x1]", anchor=W, justify=LEFT, width=10).grid(row=1, column=1)
        Label(self, text="[y2]", anchor=W, justify=LEFT, width=10).grid(row=2, column=1)
        Label(self, text="[x2]", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)
        Label(self, text="[y3]", anchor=W, justify=LEFT, width=10).grid(row=4, column=1)
        Label(self, text="[x3]", anchor=W, justify=LEFT, width=10).grid(row=5, column=1)
        Label(self, text="[y4]", anchor=W, justify=LEFT, width=10).grid(row=6, column=1)
        Label(self, text="[x4]", anchor=W, justify=LEFT, width=10).grid(row=7, column=1)
        Label(self, text="[Phi]", anchor=W, justify=LEFT, width=10).grid(row=8, column=1)
        Label(self, text="[Psi]", anchor=W, justify=LEFT, width=10).grid(row=9, column=1)
        Label(self, text="[PN]", anchor=W, justify=LEFT, width=15).grid(row=1, column=2)


        # Anordnung der Buttons zum Ausfuehren der Berechnung/Laden von Testdaten/schliessen des Fensters
        Button(self, text="Berechne", command=self.berechne).grid(row=0, column=3)
        Button(self, text="Test", command=self.test).grid(row=2, column=3)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=6, column=3)

    def berechne(self) -> object:
        """berechne Vorwärtsschnitt mit Modul Bogenschnitt.py
        :return: json Datei
        :rtype: object"""

        #Definition der Variablen durch Auswertung der Eingabefelder
        y1: float = gui.eingabefeld_auswerten(self.__eingabe_y1)
        x1: float  = gui.eingabefeld_auswerten(self.__eingabe_x1)
        y2: float  = gui.eingabefeld_auswerten(self.__eingabe_y2)
        x2: float  = gui.eingabefeld_auswerten(self.__eingabe_x2)
        y3: float = gui.eingabefeld_auswerten(self.__eingabe_y3)
        x3: float = gui.eingabefeld_auswerten(self.__eingabe_x3)
        y4: float = gui.eingabefeld_auswerten(self.__eingabe_y4)
        x4: float = gui.eingabefeld_auswerten(self.__eingabe_x4)
        phi: float = gui.eingabefeld_auswerten(self.__eingabe_phi)
        psi: float = gui.eingabefeld_auswerten(self.__eingabe_psi)



        #Definition der gegebenen Punkte als Instanzen der Klasse Punkt
        p1: daten.punkt.Punkt = daten.punkt.Punkt(y1, x1)
        p2: daten.punkt.Punkt = daten.punkt.Punkt(y2, x2)
        p3: daten.punkt.Punkt = daten.punkt.Punkt(y3, x3)
        p4: daten.punkt.Punkt = daten.punkt.Punkt(y4, x4)



        #Ausführung der Berechnung durch die Klasse Vorwärtsschnitt, Erstellung der Instanz der Klasse, Übergabe der 4 Punktobjekte und Winkel an die Instanz
        vs: schnitte.vorwartsschnitt.Vorwärtsschnitt = schnitte.vorwartsschnitt.Vorwärtsschnitt(p1, p2, p3, p4, phi, psi)

        #Definition der Ergebnisvariablen durch Index slicing des Ergebnistupels der Instanz bs
        pn: daten.punkt.Punkt = vs.berechne()[0]


        #Weitergabe der Ergebnisvariablen zum Eintrag der Ergebnisfelder
        self.ausgabefeld_schreiben(pn)

        # Weitergabe der Ergebnisse an den Server
        # Instanz der Klasse Datendienst
        dd: datd.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', 'https://mapsrv.net/pga/service/',True)

        # Definition des von der Instanz rs erhaltenen Dictionaries mit allen Ergebnissen
        meine_json_daten_antwort: dict = vs.berechne()[1]
    #
        # Schreiben (und Empfangen)
        #
        print("SCHREIBEN ---------------")

        param_schreiben: dict = {
            'datasetid': 'schnittvorkahmen-punkte',
            'request': 'postdata'
        }

        meine_klasse_vorgabe = 'Punkt'

        # Parsen des Dictionaries mit allen Ergebnissen
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(meine_json_daten_antwort, meine_klasse_vorgabe)


        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)

        # Gibt es eine Antwort mit Daten?
        if dienst_json_daten_antwort2['data'] != '':

            if dd.hole_log():
                print("SCHREIBEN: Rückmeldung")
                print(json.dumps(dienst_json_daten_antwort2, sort_keys=True, indent=4))
        else:
            print(json.dumps(dienst_json_daten_antwort2, sort_keys=True, indent=4))
            print(dienst_json_daten_antwort2['error'])
        return meine_json_daten_antwort
        pass

    def test(self):
        """Testparameter"""
        #Definition der Testparameter
        y1: float = 24681.92
        x1: float = 90831.87
        y2: float = 24877.72
        x2: float = 89251.09
        y3: float = 22526.65
        x3: float = 89150.52
        y4: float = 23231.58
        x4: float = 91422.92
        phi: float = 331.6174
        psi: float = 60.7510

        #Eintrag der Parameter in die Eingabefelder
        self.eingabefelder_schreiben(y1, x1, y2, x2, y3, x3, y4, x4, phi, psi)


    def eingabefelder_schreiben(self, p_y1, p_x1, p_y2, p_x2, p_y3, p_x3, p_y4, p_x4, p_phi, p_psi):
        """Schreiben der Eingaben in Eingabefelder
        """

        gui.eingabefeld_schreiben(self.__eingabe_y1, p_y1)
        gui.eingabefeld_schreiben(self.__eingabe_x1, p_x1)
        gui.eingabefeld_schreiben(self.__eingabe_y2, p_y2)
        gui.eingabefeld_schreiben(self.__eingabe_x2, p_x2)
        gui.eingabefeld_schreiben(self.__eingabe_y3, p_y3)
        gui.eingabefeld_schreiben(self.__eingabe_x3, p_x3)
        gui.eingabefeld_schreiben(self.__eingabe_y4, p_y4)
        gui.eingabefeld_schreiben(self.__eingabe_x4, p_x4)
        gui.eingabefeld_schreiben(self.__eingabe_phi, p_phi)
        gui.eingabefeld_schreiben(self.__eingabe_psi, p_psi)

    def ausgabefeld_schreiben(self, p_n):
        """Schreiben der Ergebnisse in Ergebnisfelder
        """

        gui.eingabefeld_schreiben(self.__ausgabe_pn, p_n)




if __name__ == "__main__":

    fenster: Tk = Tk()
    anwendung = Anwendung(fenster)
    fenster.mainloop()
