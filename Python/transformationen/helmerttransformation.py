import transformationen.transformation as tr
import daten.punkt as pkt
import datendienst.datendienst as dd
import json
import grundlagen.winkel as winkel

class HelmertTransformation(tr.Transformation):
    """Klasse HelmertTransformation, Transformation von Punkten"""

    def __init__(self, p_punkte_alt, p_punkte_neu):
        """Konstruktor
                :param p_punkte_alt: Liste der Punkte im lokalen System
                :type: dict
                :param p_punkte_neu: Liste der Punkte im uebergeordneten System
                :type: dict"""
        # Definition der Parameter durch Konstruktor der Elternklasse
        super().__init__(p_punkte_alt, p_punkte_neu)

    def parameter(self, punkte_alt_red, punkte_neu_red, p_a_s, p_n_s, *args) -> tuple:
        """parameter, Berechnung der Transformationsparameter aus auf Schwerpunkte reduzierten Passpunkten,
                derived class method from base class method in Transformation
                :param punkte_alt_red: auf Schwerpunkt reduzierte Punkte des lokalen Systems
                :type: list
                :param punkte_neu_red: auf Schwerpunkt reduzierte Punkte des uebergeordneten Systems
                :type: dict
                :param p_a_s: Schwerpunkt der Passpunkte des lokalen Systems
                :type: daten.punkt.Punkt
                :param p_n_s: Schwerpunkt der Passpunkte des uebergeordneten Systems
                :type: daten.punkt.Punkt
                :param *args: Platzhalter fuer gleiche Anzahl von Parametern wie base method
                :type: tuple
                :return: Transformationsparameter
                :rtype: tuple"""
        zaehler_o: float = 0.0
        zaehler_a: float = 0.0
        nenner: float = 0.0
        # Bildung der Summen durch for-Schleife durch Liste der alten reduzierten Passpunkte
        for p_red_alt in punkte_alt_red:
            # Punktnummer holen
            nr: str = p_red_alt.hole_nr()
            # entsprechenden reduzierten neuen Passpunkt mit Punktnummer als Schluessel holen
            p_red_neu = punkte_neu_red[nr]
            # Aufaddieren der verschiedenen Terme zur Summenbildung
            zaehler_o += p_red_alt.hole_x()*p_red_neu.hole_y()-p_red_alt.hole_y()*p_red_neu.hole_x()
            zaehler_a += p_red_alt.hole_x()*p_red_neu.hole_x()+p_red_alt.hole_y()*p_red_neu.hole_y()
            # Berechnung des Nenners aus den Summen
            nenner +=  p_red_alt.hole_x()**2+p_red_alt.hole_y()**2
        # Berechnun der Transforamtionsparameter a1-a4 (bzw. a und o) durch Summen und Nenner. Doppelte Belegung der 4 Variablen fuer Nutzung der Elternklasse Transformation
        a1: float = zaehler_a/nenner    #a
        a3: float = a1                  #o
        a2: float = zaehler_o/nenner    #a
        a4: float = a2                  #o
        print("a1 = ", a1)
        # Aufruf der base class method parameter mit Parametern a1-a4 und Schwerpunkten
        param = super(HelmertTransformation, self).parameter(a1,a2,a3,a4,p_a_s,p_n_s)
        # restliche von base class method berechnete Transformationsparameter aus Ergebnistupel holen
        P0: daten.punkt.Punkt = param[0]            # Translation
        m1: float = param[1]                        # Massstab
        m2 = 0.0                                    # Belegung fuer Nutzung der Elternklasse Transformation
        alpha: float = winkel.rad2gon(param[3])     # Drehwinkel
        beta = 0.0                                  # Belegung fuer Nutzung der Elternklasse Transformation

        # Dictionary mit allen Transformationsparametern
        trans_param: dict = {"Translation Y": P0.hole_y(), "Translation X": P0.hole_x(), "a": a1, "o": a2, "m": m1,"Drehwinkel": alpha}
        # Dictionary in string umwandeln mit json-interner Funktion dumps
        ergebnis: str = json.dumps(trans_param)
        #Umwandlung von str in json-Format
        meine_json_daten_antwort: object = json.loads(ergebnis)
        # JSON Ergebnisdatei schreiben
        with open('../ergebnisdateien/Parameter_Helmert.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=False, indent=4)

        # Ausgabe der Transformationsarameter fuer Ausgabefelder, Funktion transformiere und Webdienst
        return P0, a1,a2,a3,a4,m1,m2,alpha,beta,trans_param

    def transformiere(self, identische_punkte_neu, identische_punkte_alt,a1,a2,a3,a4,P0):
        """transformiere, Transformierung der Punkte und Berechnung der Restklaffen durch base class method und Schreiben der transformierten Punkte in json Datei
                    :param identische_punkte_neu: Passpunkte des uebergeordneten Systems
                    :type: list
                    :param identische_punkte_alt: Passpunkte des lokalen Systems
                    :type: dict
                    :param a1: Transformationsparameter a1
                    :type: float
                    :param a2: Transformationsparameter a2
                    :type: float
                    :param a3: Transformationsparameter a3
                    :type: float
                    :param a4: Transformationsparameter a4
                    :type: float
                    :param P0: Translation
                    :type: daten.punkt.Punkt"""
        # Aufruf der base class method -> Transformation der Punkte + Berechnung der Restklaffen
        Ergebnisse: tuple = super(HelmertTransformation, self).transformiere(identische_punkte_neu, identische_punkte_alt,a1,a2,a3,a4,P0)
        # Dictionary mit Restklaffen aus Tupel Ergebnisse holen
        meine_json_daten_antwort: dict = Ergebnisse[0]
        # Dictionary mit transformierten Punkten aus Tupel Ergebnisse holen
        meine_json_daten_antwort2: dict = Ergebnisse[1]

        # transformierte Punkte in json Datei schreiben
        with open('../ergebnisdateien/P_N_Helmert.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort2, json_datei, sort_keys=False, indent=4)

        # Restklaffen in json Datei schreiben
        with open('../ergebnisdateien/Restklaffen_Helmert.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent = 4)
        # Ausgabe der Dicts für Datendienst
        return meine_json_daten_antwort,meine_json_daten_antwort2

#bei isolierter Ausführung des Moduls
if __name__ == "__main__":

    # Dienst
    dienst: dd.DatenDienst = \
        dd.DatenDienst('../datendienst/datendienst.ini.xml', 'https://mapsrv.net/pga/service/', False)

    #
    # Punkte im lokalen System holen
    #
    param = {'request': 'getdata', 'datasetid': 'transgeodbmiii-alt'}

    # Ergebnis ist eine JSON-Struktur im Dienst-Format (Dictionary)
    json_punkte_alt_dienst = dienst.anfrage(param)

    # Umwandlung von JSON im Dienst-Format in das eigene JSON-Format (Dictionary)
    json_punkte_alt = dienst.parse_daten(json_punkte_alt_dienst)

    # Umwandlung vom eigenen JSON-Format in ein Dictionary mit Punktobjekten, also eine Punktliste (s.o.)
    punkte_alt = pkt.Punkt.json2punktliste(json_punkte_alt)

    #
    # Punkte im übergeordneten System holen
    #
    param['datasetid'] = 'transgeodbmiii-neu'
    json_punkte_neu_dienst = dienst.anfrage(param)
    json_punkte_neu = dienst.parse_daten(json_punkte_neu_dienst)
    punkte_neu = pkt.Punkt.json2punktliste(json_punkte_neu)

    # Transformation
    ht = HelmertTransformation(punkte_alt, punkte_neu)
    ht.berechne()

    if False:
        # Punkte zum Testen
        # Punktnummer ist prinzipiell redundant!
        punkte_alt: Dict[str, daten.punkt.Punkt] = {
            "101": pkt.Punkt(-916.300, 6078.720, "101"),
            "102": pkt.Punkt(3331.420, 6492.430, "102"),
            "2096": pkt.Punkt(5091.510, 2158.040, "2096")
        }
        punkte_neu: Dict[str, daten.punkt.Punkt] = {
            "101": pkt.Punkt(36935.000, 2630.170, "101"),
            "102": pkt.Punkt(41132.120, 27133.890, "102"),
            "FAKE9999": pkt.Punkt(0.0, 0.0, "FAKE9999")
        }
    # Instanz von HelmertTransformation
    ht2 = HelmertTransformation(punkte_alt, punkte_neu)
    # Aufruf der berechne Funktion der Elternklasse Transformation von HelmertTransformation
    ht2.berechne()

