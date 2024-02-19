from tkinter import *
import schnitte.ruckwartsschnitt
import daten.punkt
import daten.strecke
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
        self.__eingabe_y1 = Entry(self)
        self.__eingabe_y2 = Entry(self)
        self.__eingabe_y3 = Entry(self)
        self.__eingabe_r1 = Entry(self)
        self.__eingabe_r2 = Entry(self)
        self.__eingabe_r3 = Entry(self)

        self.__ausgabe_pn = Entry(self, width=50)

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui von Rückwärtsschnittberechnung"""
        # TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()
        #Label zur Beschreibung der Funktionalität des Fensters
        Label(self, text="PGA | Rückwärtsschnitt").grid(row=0, column=1, columnspan=3)
        #Anordnung der Ein-/ Ausgabefelder
        self.__eingabe_y1.grid(row=0, column=0)
        self.__eingabe_y2.grid(row=1, column=0)
        self.__eingabe_x1.grid(row=2, column=0)
        self.__eingabe_x2.grid(row=3, column=0)
        self.__eingabe_y3.grid(row=4, column=0)
        self.__eingabe_x3.grid(row=5, column=0)
        self.__eingabe_r1.grid(row=6, column=0)
        self.__eingabe_r2.grid(row=7, column=0)
        self.__eingabe_r3.grid(row=8, column=0)

        self.__ausgabe_pn.grid(row=2, column=2)


        # Anordnung der Label zur Beschriftung der Ein- und Ausgabefelder
        Label(self, text="[y1]", anchor=W, justify=LEFT, width=10).grid(row=0, column=1)
        Label(self, text="[y2]", anchor=W, justify=LEFT, width=10).grid(row=1, column=1)
        Label(self, text="[x1]", anchor=W, justify=LEFT, width=10).grid(row=2, column=1)
        Label(self, text="[x2]", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)
        Label(self, text="[y3]", anchor=W, justify=LEFT, width=10).grid(row=4, column=1)
        Label(self, text="[x3]", anchor=W, justify=LEFT, width=10).grid(row=5, column=1)
        Label(self, text="[r1]", anchor=W, justify=LEFT, width=10).grid(row=6, column=1)
        Label(self, text="[r2]", anchor=W, justify=LEFT, width=10).grid(row=7, column=1)
        Label(self, text="[r3]", anchor=W, justify=LEFT, width=10).grid(row=8, column=1)
        Label(self, text="[PN]", anchor=W, justify=LEFT, width=15).grid(row=1, column=2)


        # Anordnung der Buttons zum Ausfuehren der Berechnung/Laden von Testdaten/schliessen des Fensters
        Button(self, text="Berechne", command=self.berechne).grid(row=0, column=3)
        Button(self, text="Test", command=self.test).grid(row=2, column=3)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=6, column=3)

    def berechne(self) -> object:
        """berechne Rückwärtsschnitt mit Modul rückwärtsschnitt.py
        :return: json Datei
        :rtype: object"""

        #Definition der Variablen durch Auswertung der Eingabefelder
        y1: float = gui.eingabefeld_auswerten(self.__eingabe_y1)
        x1: float = gui.eingabefeld_auswerten(self.__eingabe_x1)
        y2: float = gui.eingabefeld_auswerten(self.__eingabe_y2)
        x2: float = gui.eingabefeld_auswerten(self.__eingabe_x2)
        y3: float = gui.eingabefeld_auswerten(self.__eingabe_y3)
        x3: float = gui.eingabefeld_auswerten(self.__eingabe_x3)
        r1: float = gui.eingabefeld_auswerten(self.__eingabe_r1)
        r2: float = gui.eingabefeld_auswerten(self.__eingabe_r2)
        r3: float = gui.eingabefeld_auswerten(self.__eingabe_r3)



        #Definition der drei gegebenen Punkte als Instanzen der Klasse Punkt
        p1: daten.punkt.Punkt = daten.punkt.Punkt(y1, x1)
        p2: daten.punkt.Punkt = daten.punkt.Punkt(y2, x2)
        p3: daten.punkt.Punkt = daten.punkt.Punkt(y3, x3)

        #Ausfuehrung der Berechnung durch die Klasse Bogenschnitt, Kreation der Instanz rs der Klasse
        rs: schnitte.ruckwartsschnitt.Rückwärtsschnitt = schnitte.ruckwartsschnitt.Rückwärtsschnitt(p1, p2, p3, r1, r2, r3)

        #Definition der Ergebnisvariablen durch Index slicing des Ergebnistupels der Instanz rs
        pn: daten.punkt.Punkt = rs.berechne()[0]


        #Weitergabe der Ergebnisvariablen zum Eintrag der Ergebnisfelder
        self.ausgabefeld_schreiben(pn)

        # Weitergabe der Ergebnisse an den Server
        # Instanz der Klasse Datendienst
        dd: datd.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', 'https://mapsrv.net/pga/service/', True)


        # Definition des von der Instanz rs erhaltenen Dictionaries mit allen Ergebnissen
        meine_json_daten_antwort: dict = rs.berechne()[1]

        #
        # Schreiben (und Empfangen)
        #
        print("SCHREIBEN ---------------")

        param_schreiben: dict = {
            'datasetid': 'schnittrueckkahmen-punkte',
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
        y1: float = 49666.56
        x1: float = 4448.58
        y2: float = 46867.94
        x2: float = 5537.00
        y3: float = 51293.86
        x3: float = 6365.89
        r1: float = 66.8117
        r2: float = 294.7845
        r3: float = 362.8516

        #Eintrag der Parameter in die Eingabefelder
        self.eingabefelder_schreiben(y1, x1, y2, x2, y3, x3, r1, r2, r3)


    def eingabefelder_schreiben(self, p_y1, p_x1, p_y2, p_x2, p_y3, p_x3, p_r1, p_r2, p_r3):
        """Schreiben der Eingaben in Eingabefelder    """
        gui.eingabefeld_schreiben(self.__eingabe_y1, p_y1)
        gui.eingabefeld_schreiben(self.__eingabe_x1, p_x1)
        gui.eingabefeld_schreiben(self.__eingabe_y2, p_y2)
        gui.eingabefeld_schreiben(self.__eingabe_x2, p_x2)
        gui.eingabefeld_schreiben(self.__eingabe_y3, p_y3)
        gui.eingabefeld_schreiben(self.__eingabe_x3, p_x3)
        gui.eingabefeld_schreiben(self.__eingabe_r1, p_r1)
        gui.eingabefeld_schreiben(self.__eingabe_r2, p_r2)
        gui.eingabefeld_schreiben(self.__eingabe_r3, p_r3)

    def ausgabefeld_schreiben(self, p_n):
        """Schreiben der Ergebnisse in Ergebnisfelder     """
        gui.eingabefeld_schreiben(self.__ausgabe_pn, p_n)







if __name__ == "__main__":

    fenster: Tk = Tk()
    anwendung = Anwendung(fenster)
    fenster.mainloop()