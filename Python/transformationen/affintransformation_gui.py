from tkinter import *
from tkinter import Entry, Tk
import daten.punkt
import daten.strecke
import datendienst.datendienst as datd
import transformationen.affintransformation as af
import grundlagen.gui as gui
import grundlagen.winkel as winkel
import json

class Anwendung(Frame):
    """Klasse Anwendung
       Jade HS
       Vorlesung "Programmieren geodätischer Aufgaben"
       M. Hackenberg
       WiSe 2020/21
       Stand: 2021-02-17
       Version 1.0.0
       """

    def __init__(self, master: object):
        """Konstruktor
        :param master: parent window (TKinter)
        :type object"""

        #Erben des Objektes master (Fenster), von der Elternklasse Frame (TKinter)
        super().__init__(master)

        self.__meister: object = master
        # Definition der Ein- und Ausgabefelder
        self.__eingabe_datei: object = Entry(self, width=50)
        self.__eingabe_URL: object = Entry(self, width=50)

        self.__ausgabe_m1: object = Entry(self, width=50)
        self.__ausgabe_m2: object = Entry(self, width=50)
        self.__ausgabe_alpha: object = Entry(self, width=50)
        self.__ausgabe_beta: object = Entry(self, width=50)
        self.__ausgabe_t: object = Entry(self, width=50)
        self.__ausgabe_a1: object = Entry(self, width=50)
        self.__ausgabe_a2: object = Entry(self, width=50)
        self.__ausgabe_a3: object = Entry(self, width=50)
        self.__ausgabe_a4: object = Entry(self, width=50)

        #Initialisierung der GUI mit der entsprechenden Funktion
        self.initialisiere_gui()

    def initialisiere_gui(self):
        """initialisiere gui """
        #TKinter widget zur Anordnung der Eingabefelder und Labels
        self.grid()
        #Anordung der Eingabefelder
        self.__eingabe_datei.grid(row=1, column=0)
        self.__eingabe_URL.grid(row=2, column=0)
        #Anordung der Ausgabefelder
        self.__ausgabe_m1.grid(row=5, column=0)
        self.__ausgabe_m2.grid(row=6, column=0)
        self.__ausgabe_alpha.grid(row=7, column=0)
        self.__ausgabe_beta.grid(row=8, column=0)
        self.__ausgabe_t.grid(row=9, column=0)
        self.__ausgabe_a1.grid(row=10, column=0)
        self.__ausgabe_a2.grid(row=11, column=0)
        self.__ausgabe_a3.grid(row=12, column=0)
        self.__ausgabe_a4.grid(row=13, column=0)

        #Label zur Beschreibung der Ein- und Ausgaben
        Label(self, text="PGA | Affintransformation").grid(row=0, column=0, columnspan=3)
        Label(self, text="Eingangsdaten", justify=LEFT).grid(row=0, column=0, columnspan=1)
        Label(self, text="Transformationsparameter").grid(row=3, column=0, columnspan=1)
        Label(self, text="Dateipfad", anchor=W, justify=LEFT, width=25).grid(row=1, column=1)
        Label(self, text="URL", anchor=W, justify=LEFT, width=25).grid(row=2, column=1)
        Label(self, text="Massstab Abszisse", anchor=W, justify=LEFT, width=25).grid(row=5, column=1)
        Label(self, text="Massstab Ordinate", anchor=W, justify=LEFT, width=25).grid(row=6, column=1)
        Label(self, text="Drehwinkel Abszisse (alpha) [gon]", anchor=W, justify=LEFT, width=25).grid(row=7, column=1)
        Label(self, text="Drehwinkel Ordinate (beta) [gon]", anchor=W, justify=LEFT, width=25).grid(row=8, column=1)
        Label(self, text="Translation [m]", anchor=W, justify=LEFT, width=25).grid(row=9, column=1)
        Label(self, text="a1", anchor=W, justify=LEFT, width=25).grid(row=10, column=1)
        Label(self, text="a2", anchor=W, justify=LEFT, width=25).grid(row=11, column=1)
        Label(self, text="a3", anchor=W, justify=LEFT, width=25).grid(row=12, column=1)
        Label(self, text="a4", anchor=W, justify=LEFT, width=25).grid(row=13, column=1)
        Label(self, text="", anchor=W, justify=LEFT, width=10).grid(row=3, column=1)

        #Buttons zum Ausfuehren der Transformation/Laden von Testdaten/Schliessen des Fensters
        Button(self, text="transformiere", command=self.punkte_lokal).grid(row=1, column=5)
        Button(self, text="transformiere", command=self.punkte_datendienst).grid(row=2, column=5)
        Button(self, text="Beenden", command=self.__meister.destroy).grid(row=13, column=5)
        Button(self, text="test", command=self.test).grid(row=1, column=3)
        Button(self, text="test2", command=self.test2).grid(row=1, column=4)
        Button(self, text="test", command=self.test3).grid(row=2, column=3)

    def punkte_lokal(self):
        """punkte_lokal, initialisiert die Berechnung der Transformation mit der json-Datei deren Pfad
        im Eingabefeld eingabe_datei angegeben ist"""

        #Dateipfad aus Eingabefeld holen
        datei: object = self.__eingabe_datei.get()
        #JSON Datei oeffnen, Datei in zwei Punktlisten Punkte_alt und punkte_neu umformen (Struktur der Datei ist bekannt)
        with open(datei, 'r') as json_datei:
            json_daten: object = json.load(json_datei)

            json_punkte_alt: dict = json_daten["p_a"]
            json_punkte_neu: dict = json_daten["p_n"]

            punkte_neu: object = daten.punkt.Punkt.json2punktliste(json_punkte_neu)
            punkte_alt: object = daten.punkt.Punkt.json2punktliste(json_punkte_alt)

        # Transformation durch Schaffung einer Instanz der Berechnungsanwendung mit den beiden Punktlisten als Parameter
        at: transformationen.affintransformation.AffinTransformation = af.AffinTransformation(punkte_alt, punkte_neu)
        # Aufruf der berechne Funktion der Elternklasse Transformation von AffinTransformation (automatisch, da es in Kindklasse keine Funktion berechnen gibt)
        at.berechne()
        #Weiterleitung der Ergebnisparameter an ausgabe_feld schreiben fuer den Eintrag in den Ausgabefeldern
        self.ausgabefeld_schreiben(at.berechne()[0])
        # Initialisierung von anDatendienst senden mit Parametern, transformierten Punkten und Restklaffen
        # Die Parameter sind doppelt als Tupel und Dictionary enthalten, weil sie bei der Helmerttrafo "unvollstaendig sind
        # ausserdem soll in anDatendienst_senden nicht nochmal ein fertig formatiertes Dictionary definiert werden
        self.anDatendienst_senden(at.berechne())

    def punkte_datendienst(self):
        """punkte_datendienst, initialisiert die Berechnung der Transformation mit einer json-Datei von einem Server, URL aus Eingabefeld """
        # URL aus Eingabefeld holen
        url = self.__eingabe_URL.get()
        # Instanz dienst der Klasse Datendienst schaffen
        dienst: datendienst.datendienst.DatenDienst = \
            datd.DatenDienst('../datendienst/datendienst.ini.xml', url, True)

        # Punkte im lokalen System holen
        param: dict = {'request': 'getdata', 'datasetid': 'transgeodbmiii-alt'}

        # Ergebnis ist eine JSON-Struktur im Dienst-Format (Dictionary)
        json_punkte_alt_dienst: dict = dienst.anfrage(param)

        # Umwandlung von JSON im Dienst-Format in das eigene JSON-Format (Dictionary)
        json_punkte_alt: dict = dienst.parse_daten(json_punkte_alt_dienst)

        # Umwandlung vom eigenen JSON-Format in ein Dictionary mit Punktobjekten, also eine Punktliste (s.o.)
        punkte_alt: object = daten.punkt.Punkt.json2punktliste(json_punkte_alt)

        # Punkte im übergeordneten System holen, in Punktliste umformen durch Funktion der Klasse Punkt
        param['datasetid'] = 'transgeodbmiii-neu'
        json_punkte_neu_dienst: dict = dienst.anfrage(param)
        json_punkte_neu: dict = dienst.parse_daten(json_punkte_neu_dienst)
        punkte_neu: object = daten.punkt.Punkt.json2punktliste(json_punkte_neu)

        # Transformation durch Schaffung einer Instanz der Berechnungsanwendung mit den beiden Punktlisten als Parameter
        at: transformationen.affintransformation.AffinTransformation = af.AffinTransformation(punkte_alt, punkte_neu)
        # Aufruf der berechne Funktion der Elternklasse Transformation von AffinTransformation
        at.berechne()
        # Weiterleitung der Ergebnisparameter an ausgabe_feld schreiben fuer den Eintrag in den Ausgabefeldern
        self.ausgabefeld_schreiben(at.berechne()[0])
        #Initialisierung von anDatendienst senden mit Parametern, transformierten Punkten und Restklaffen
        #Die Parameter sind doppelt als Tupel und Dictionary enthalten, weil sie bei der Helmerttrafo "unvollstaendig" sind
        #ausserdem soll in anDatendienst_senden nicht nochmal ein fertig formatiertes Dictionary definiert werden
        self.anDatendienst_senden(at.berechne())
    def anDatendienst_senden(self,p_t):
        """anDatendienst_senden, uebermittlung der Transformationsergebnisse an Server mittels Datendienst
        :param p_t: Parameter als Tupel mit Dict an letzter Stelle, Restklaffen, transformierte Punkte als Dicts
        :type: tuple"""
        #fuer den Datendienst benoetigte Dicts aus Tupel holen
        meine_json_daten_antwort: dict = p_t[1][0]          #Restklaffen
        meine_json_daten_antwort2: dict = p_t[1][1]         #transformierte Punkte
        transformationsparameter: dict = p_t[0][9]

        # Datendienst

        #URL
        dienst_url: str = 'https://mapsrv.net/pga/service/'
        #Instanz der Datendienstklasse definieren
        dd: datendienst.datendienst.DatenDienst = datd.DatenDienst('../datendienst/datendienst.ini.xml', dienst_url, True)
        #datasetid fuer transformierte Punkte setzen
        param_schreiben: dict = {'datasetid': 'transaffingeodbmiii-neu','request': 'postdata'}
        #Klasse definieren
        meine_klasse_vorgabe = 'Punkt'
        #Dict in Datendienst bzw. Serverformat wandeln
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(meine_json_daten_antwort2, meine_klasse_vorgabe)
        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)
        print("antwort2", dienst_json_daten_antwort2)

        # Restklaffen an Webdienst senden (Vorgang wiederholt sich)
        #datasetid setzen
        param_schreiben: dict = {'datasetid': 'transaffingeodbmiii-klaffen','request': 'postdata'}
        dienst_json_daten_anfrage2: dict = dd.parse_meine_daten(meine_json_daten_antwort, meine_klasse_vorgabe)
        dienst_json_daten_antwort3: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage2)
        print("antwort3", dienst_json_daten_antwort3)

        # Transformationsparameter an Webdienst senden (Vorgang wiederholt sich)
        param_schreiben: dict = { 'datasetid': 'transaffingeodbmiii-param',  'request': 'postdata' }
        dienst_json_daten_anfrage2: dict = dd.parse_meine_daten(transformationsparameter, meine_klasse_vorgabe)

        dienst_json_daten_antwort4: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage2)
        print("antwort4", dienst_json_daten_antwort4)

    def test(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten"""
        datei: str = "../transformationen/lokale_Punkte.json"
        # Eintrag des Pfades in das Eingabefeld
        self.eingabefelder_schreiben(datei)

    def test2(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten"""
        datei: str = "../transformationen/lokale_Punkte2.json"
        # Eintrag des Pfades in das Eingabefeld
        self.eingabefelder_schreiben(datei)

    def test3(self):
        """test, Vorgabe einer vorhandenen JSON Datei mit Punkten von Webdienst"""
        url: str = 'https://mapsrv.net/pga/service/'
        # Eintrag der url in das Eingabefeld
        self.eingabefelder_schreiben2(url)

    def eingabefelder_schreiben(self, p_datei):
        """Schreiben der Eingaben in Eingabefelder
        :param p_datei: str von Dateipfad aus Eingabe
        :type: object"""
        gui.eingabefeld_schreiben(self.__eingabe_datei, p_datei)

    def eingabefelder_schreiben2(self, p_datei):
        """Schreiben der Eingaben in Eingabefelder
        :param p_datei: str von Dateipfad aus Eingabe
        :type: object"""
        gui.eingabefeld_schreiben(self.__eingabe_URL, p_datei)

    def ausgabefeld_schreiben(self, ergebnistupel):
        """Schreiben der Transformationsparameter in Ergebnisfelder
        :param ergebnistupel: tupel mit allen Transformationsparametern
        :type: tuple"""
        #einzelne Parameter aus Ergebnistupel holen

        #Translation, Umwandlung des Punktobjekts in string mit Rechts- und Hochwert
        t: str = f"Y0: {ergebnistupel[0].hole_y()},   X0: {ergebnistupel[0].hole_x()}"
        a1: float = ergebnistupel[1]
        a2: float = ergebnistupel[2]
        a3: float = ergebnistupel[3]
        a4: float = ergebnistupel[4]
        #Massstab Abszisse
        m1: float = ergebnistupel[5]
        # Massstab Ordinate
        m2: float = ergebnistupel[6]
        # Drehwinkel Abszisse, Umrechnung in gon
        alpha: float = winkel.rad2gon(ergebnistupel[7])
        # Drehwinkel Ordinate, Umrechnung in gon
        beta: float = winkel.rad2gon(ergebnistupel[8])

        gui.eingabefeld_schreiben(self.__ausgabe_m1, m1)
        gui.eingabefeld_schreiben(self.__ausgabe_m2, m2)
        gui.eingabefeld_schreiben(self.__ausgabe_alpha, alpha)
        gui.eingabefeld_schreiben(self.__ausgabe_beta, beta)
        gui.eingabefeld_schreiben(self.__ausgabe_t, t)
        gui.eingabefeld_schreiben(self.__ausgabe_a1, a1)
        gui.eingabefeld_schreiben(self.__ausgabe_a2, a2)
        gui.eingabefeld_schreiben(self.__ausgabe_a3, a3)
        gui.eingabefeld_schreiben(self.__ausgabe_a4, a4)