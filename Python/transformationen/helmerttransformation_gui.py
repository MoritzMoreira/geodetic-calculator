from tkinter import *
from tkinter import Entry, Tk
import daten.punkt
import daten.strecke
import datendienst.datendienst as datd
import transformationen.helmerttransformation as hl
import json
import grundlagen.gui as gui
import grundlagen.winkel as winkel
import daten.punkt as pkt

class Anwendung(Frame):
    """Klasse Anwendung
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

        # Definition der Ein- und Ausgabefelder
        self.__meister = master
        self.__eingabe_datei = Entry(self, width=50)
        self.__eingabe_URL = Entry(self, width=50)
        self.__ausgabe_m = Entry(self, width=50)
        self.__ausgabe_w = Entry(self, width=50)
        self.__ausgabe_t = Entry(self, width=50)
        self.__ausgabe_a = Entry(self, width=50)
        self.__ausgabe_o = Entry(self, width=50)

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui """
        #TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()
        # Anordung der Eingabefelder
        self.__eingabe_datei.grid(row=1, column=0)
        self.__eingabe_URL.grid(row=2, column=0)
        # Anordung der Ausgabefelder
        self.__ausgabe_m.grid(row=5, column=0)
        self.__ausgabe_w.grid(row=6, column=0)
        self.__ausgabe_t.grid(row=7, column=0)
        self.__ausgabe_a.grid(row=8, column=0)
        self.__ausgabe_o.grid(row=9, column=0)

        #Label zur Beschreibung der Ein- und Ausgaben
        Label(self, text="PGA | Helmerttransformation").grid(row=0, column=2, columnspan=3)
        Label(self, text="Eingangsdaten", justify=LEFT).grid(row=0, column=0, columnspan=1)
        Label(self, text="Transformationsparameter").grid(row=3, column=0, columnspan=1)
        Label(self, text="Dateipfad", anchor=W, justify=LEFT, width=15).grid(row=1, column=1)
        Label(self, text="URL", anchor=W, justify=LEFT, width=15).grid(row=2, column=1)
        Label(self, text="Massstab", anchor=W, justify=LEFT, width=15).grid(row=5, column=1)
        Label(self, text="Drehwinkel [gon]", anchor=W, justify=LEFT, width=15).grid(row=6, column=1)
        Label(self, text="Translation [m]", anchor=W, justify=LEFT, width=15).grid(row=7, column=1)
        Label(self, text="a", anchor=W, justify=LEFT, width=15).grid(row=8, column=1)
        Label(self, text="o", anchor=W, justify=LEFT, width=15).grid(row=9, column=1)
        Label(self, text="", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)

        #Anordnung der Buttons zum Ausfuehren der Berechnung/Laden von Testdaten/schliessen des Fensters
        Button(self, text="transformiere", command=self.punkte_lokal).grid(row=1, column=5)
        Button(self, text="transformiere", command=self.punkte_datendienst).grid(row=2, column=5)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=9, column=5)
        Button(self, text="test", command=self.test).grid(row=1, column=3)
        Button(self, text="test2", command=self.test2).grid(row=1, column=4)
        Button(self, text="test", command=self.test3).grid(row=2, column=3)

    def punkte_lokal(self) -> object:
        """punkte_lokal, initialisiert die Berechnung der Transformation mit der json-Datei deren Pfad
        im Eingabefeld eingabe_datei angegeben ist"""
        # Dateipfad aus Eingabefeld holen
        datei = self.__eingabe_datei.get()
        # JSON Datei öffnen, Datei in zwei Punktlisten Punkte_alt und punkte_neu umformen (Struktur der Datei ist bekannt)
        with open(datei, 'r') as json_datei:
            json_daten = json.load(json_datei)
            json_punkte_alt = json_daten["p_a"]
            json_punkte_neu = json_daten["p_n"]
            punkte_neu = daten.punkt.Punkt.json2punktliste(json_punkte_neu)
            punkte_alt = daten.punkt.Punkt.json2punktliste(json_punkte_alt)

        # Transformation durch Schaffung einer Instanz der Berechnungsanwendung mit den beiden Punktlisten als Parameter
        ht = hl.HelmertTransformation(punkte_alt, punkte_neu)
        # Aufruf der berechne Funktion der Elternklasse Transformation von AffinTransformation (automatisch, da es in Kindklasse keine Funktion berechnen gibt)
        ht.berechne()
        # Weitergabe der Ergebnisvariablen zum Eintrag der Ergebnisfelder
        self.ausgabefeld_schreiben(ht.berechne()[0])
        # Initialisierung von anDatendienst senden mit Parametern, transformierten Punkten und Restklaffen
        # Die Parameter sind doppelt als Tupel und Dictionary enthalten, weil sie bei der Helmerttrafo "unvollstaendig" sind
        # ausserdem soll in anDatendienst_senden nicht nochmal ein fertig formatiertes Dictionary definiert werden
        self.anDatendienst_senden(ht.berechne())

    def punkte_datendienst(self):
        """punkte_datendienst, initialisiert die Berechnung der Transformation mit einer json-Datei von einem Server, URL aus Eingabefeld """
        # URL aus Eingabefeld holen
        url = self.__eingabe_URL.get()
        # Instanz dienst der Klasse Datendienst schaffen
        dienst: datendienst.datendienst.DatenDienst = \
            datd.DatenDienst('../datendienst/datendienst.ini.xml', url, False)

        # Punkte im lokalen System holen
        param = {'request': 'getdata', 'datasetid': 'transgeodbmiii-alt'}

        # Ergebnis ist eine JSON-Struktur im Dienst-Format (Dictionary)
        json_punkte_alt_dienst = dienst.anfrage(param)

        # Umwandlung von JSON im Dienst-Format in das eigene JSON-Format (Dictionary)
        json_punkte_alt = dienst.parse_daten(json_punkte_alt_dienst)

        # Umwandlung vom eigenen JSON-Format in ein Dictionary mit Punktobjekten, also eine Punktliste (s.o.)
        punkte_alt = daten.punkt.Punkt.json2punktliste(json_punkte_alt)

        # Punkte im übergeordneten System holen, in Punktliste umformen durch Funktion der Klasse Punkt
        param['datasetid'] = 'transgeodbmiii-neu'
        json_punkte_neu_dienst = dienst.anfrage(param)
        json_punkte_neu = dienst.parse_daten(json_punkte_neu_dienst)
        punkte_neu = daten.punkt.Punkt.json2punktliste(json_punkte_neu)

        # Transformation durch Schaffung einer Instanz der Berechnungsanwendung mit den beiden Punktlisten als Parameter
        ht = hl.HelmertTransformation(punkte_alt, punkte_neu)
        # Aufruf der berechne Funktion der Elternklasse Transformation von AffinTransformation
        ht.berechne()

        # Weitergabe der Ergebnisvariablen zum Eintrag der Ergebnisfelder
        self.ausgabefeld_schreiben(ht.berechne()[0])
        # Initialisierung von anDatendienst senden mit Parametern, transformierten Punkten und Restklaffen
        # Die Parameter sind doppelt als Tupel und Dictionary enthalten, weil sie bei der Helmerttrafo "unvollstaendig" sind
        # ausserdem soll in anDatendienst_senden nicht nochmal ein fertig formatiertes Dictionary definiert werden
        self.anDatendienst_senden(ht.berechne())

    def anDatendienst_senden(self, p_t):
        meine_json_daten_antwort: dict = p_t[1][0]
        meine_json_daten_antwort2: dict = p_t[1][1]
        transformationsparameter: dict = p_t[0][9]

        # transformierte Punkte an Webdienst senden
        dienst_url = 'https://mapsrv.net/pga/service/'
        # Instanz der Datendienstklasse definieren
        dd: datendienst.datendienst.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', dienst_url, True)
        # datasetid fuer transformierte Punkte setzen
        param_schreiben: dict = {'datasetid': 'transaffingeodbmiii-neu','request': 'postdata'}
        # Klasse definieren
        meine_klasse_vorgabe = 'Punkt'
        # Dict in Datendienst bzw. Serverformat wandeln
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(meine_json_daten_antwort2, meine_klasse_vorgabe)

        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)
        print("antwort2", dienst_json_daten_antwort2)

        # Restklaffen an Webdienst senden (Vorgang wiederholt sich)
        param_schreiben: dict = {'datasetid': 'transaffingeodbmiii-klaffen','request': 'postdata'}

        dienst_json_daten_anfrage2: dict = dd.parse_meine_daten(meine_json_daten_antwort, meine_klasse_vorgabe)

        dienst_json_daten_antwort3: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage2)
        print("antwort3", dienst_json_daten_antwort3)

        # Transformationsparameter an Webdienst senden (Vorgang wiederholt sich)
        param_schreiben: dict = {'datasetid': 'transaffingeodbmiii-param','request': 'postdata'}

        dienst_json_daten_anfrage2: dict = dd.parse_meine_daten(transformationsparameter, meine_klasse_vorgabe)

        dienst_json_daten_antwort4: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage2)
        print("antwort4", dienst_json_daten_antwort4)

    def test(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten"""
        datei = "../transformationen/lokale_Punkte.json"
        # Eintrag des Pfades in das Eingabefeld
        self.eingabefelder_schreiben(datei)
    def test2(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten"""
        datei = "../transformationen/lokale_Punkte2.json"
        # Eintrag des Pfades in das Eingabefeld
        self.eingabefelder_schreiben(datei)
    def test3(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten von Webdienst"""
        # Definition der Testparamenter
        url = 'https://mapsrv.net/pga/service/'
        # Eintrag der url in das Eingabefeld
        self.eingabefelder_schreiben2(url)

    def eingabefelder_schreiben(self, p_datei):
        """Schreiben der Eingaben in Eingabefelder
        :param p_datei: str von Dateipfad aus Eingabe
        :type: object"""
        gui.eingabefeld_schreiben(self.__eingabe_datei, p_datei)
    def eingabefelder_schreiben2(self, p_datei):
        """Schreiben der Eingaben in Eingabefelder    """
        gui.eingabefeld_schreiben(self.__eingabe_URL, p_datei)

    def ausgabefeld_schreiben(self, ergebnistupel):
        """Schreiben der Transformationsparameter in Ergebnisfelder
        :param ergebnistupel: tupel mit allen Transformationsparametern
        :type: tuple"""
        #einzelne Parameter aus Ergebnistupel holen
        #Translation, Umwandlung des Punktobjekts in string mit Rechts- und Hochwert
        t = f"Y0: {ergebnistupel[0].hole_y()},   X0: {ergebnistupel[0].hole_x()}"
        a = ergebnistupel[1]
        o = ergebnistupel[2]
        m = ergebnistupel[5]                    #Massstab
        w = ergebnistupel[7]    #Drehwinkel

        gui.eingabefeld_schreiben(self.__ausgabe_m, m)
        gui.eingabefeld_schreiben(self.__ausgabe_w, w)
        gui.eingabefeld_schreiben(self.__ausgabe_t, t)
        gui.eingabefeld_schreiben(self.__ausgabe_a, a)
        gui.eingabefeld_schreiben(self.__ausgabe_o, o)