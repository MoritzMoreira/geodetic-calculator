from tkinter import *
from tkinter import Tk
import polygonzug.polygonzug_beidseitig
from grundlagen import gui
import datendienst.datendienst as datd
import json

class Anwendung(Frame):

    def __init__(self, master: object):
        """Konstruktor
        :param master: parent window (TKinter)
        :type object"""

        #Erben des Objekts master (Fenster), von der Elternklasse Frame (TKinter)
        super().__init__(master)

        # Definition der Ein- und Ausgabefelder
        self.__meister = master

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui von Bogenschnittberechnung"""
        #TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()

        #Label zur Beschreibung der Funktionalitaet des Fensters
        Label(self, text="PGA | Polygonzug Beidseitig").grid(row=0, column=0, columnspan=3)


        #Anordnung der Buttons zum Ausfuehren der Berechnung/schliessen des Fensters
        Button(self, text="berechne", command=self.berechne).grid(row=0, column=3)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=6, column=3)

    def berechne(self) -> object:
        """berechne Bogenschnitt mit Modul Polygonzug_beidseitig.py
        :return: json Datei
        :rtype: object"""


        #Ausfuehrung der Berechnung durch die Klasse Polygonzugbeidseitig
        pzb: polygonzug.Polygonzugbeidseitig()
        pzb: polygonzug.polygonzug_beidseitig.Polygonzugbeidseitig=polygonzug.polygonzug_beidseitig.Polygonzugbeidseitig()


        #ergebnis: str = json.dumps(pzb.berechne())
        dict = pzb.berechne()
        #meine_json_daten_antwort: object = json.loads(dict)

        # Dictionary in Zeichenkette umwandeln
        #ergebnis: str = json.dumps(dict)
        # JSON Ergebnisdatei schreiben
        #meine_json_daten_antwort: object = json.loads(ergebnis)
        with open('polygonzug.Ergebnis_polygon.json', 'w') as json_datei:
            json.dump(dict, json_datei, sort_keys=True, indent=4)
        # Ausgabe der Ergebnisdatei in Konsole
        with open('polygonzug.Ergebnis_polygon.json', 'r') as json_datei2:
            json_daten2 = json.load(json_datei2)
            print(json.dumps(json_daten2, sort_keys=True, indent=4))


        #Weitergabe der Ergebnisse an den Server
        dienst_url = 'https://mapsrv.net/pga/service/'
        # dienst_url = 'http://dropbox.local/hostpoint/mapsrv.net/www/pga/service/'

        #Instanz der Klasse Datendienst
        dd: datd.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', dienst_url, True)
        param_schreiben: dict = {'datasetid': 'polybeidseitigkahmen-punkte','request': 'postdata'}
        # Klasse definieren
        meine_klasse_vorgabe = 'Punkt'
        # Dict in Datendienst bzw. Serverformat wandeln
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(dict, meine_klasse_vorgabe)

        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)
        print("antwort2", dienst_json_daten_antwort2)





    def ausgabefeld_schreiben(self, p2, p3, p4, p5):
        """Schreiben der Ergebnisse in Ergebnisfelder     """
        gui.eingabefeld_schreiben(self.__ausgabe_p2, p2)
        gui.eingabefeld_schreiben(self.__ausgabe_p3, p3)
        gui.eingabefeld_schreiben(self.__ausgabe_p4, p4)
        gui.eingabefeld_schreiben(self.__ausgabe_p5, p5)



if __name__== "__main__":
    fenster: Tk = Tk()
    anwendung = Anwendung(fenster)
    fenster.mainloop()
