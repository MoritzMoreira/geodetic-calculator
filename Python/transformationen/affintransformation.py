import transformationen.transformation as tr
import daten.punkt as pkt
import json
import grundlagen.winkel as winkel
import datendienst.datendienst as dat


class AffinTransformation(tr.Transformation):
    """Klasse AffinTransformation, Transformation von Punkten"""
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
        :param punkte_neu_red: auf Schwerpunkt reduzierte Punkte des lokalen Systems
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

        #Definition der Summenvariablen
        summe_xX: float = 0.0
        summe_yY: float = 0.0
        summe_y_quad: float = 0.0
        summe_x_quad: float = 0.0
        summe_yX: float = 0.0
        summe_xY: float = 0.0
        summe_xy: float = 0.0

        #Bildung der Summen durch for-Schleife durch Liste der alten reduzierten Passpunkte
        for p_r_a in punkte_alt_red:
            print("pra y = ", p_r_a.hole_y(), "pra x = ", p_r_a.hole_x())
            #Punktnummer holen
            nr: str = p_r_a.hole_nr()
            #entsprechenden reduzierten neuen Passpunkt mit Punktnummer als Schluessel holen
            p_r_n: daten.punkt.Punkt = punkte_neu_red[nr]

            # Aufaddieren der verschiedenen Produkte zur Summenbildung
            summe_xX += p_r_a.hole_x()*p_r_n.hole_x()
            summe_y_quad += p_r_a.hole_y()**2
            summe_x_quad += p_r_a.hole_x()**2
            summe_yX += p_r_a.hole_y() * p_r_n.hole_x()
            summe_xY += p_r_a.hole_x() * p_r_n.hole_y()
            summe_xy += p_r_a.hole_x() * p_r_a.hole_y()
            summe_yY += p_r_a.hole_y() * p_r_n.hole_y()

        #Berechnung des Nenners N aus den Summen
        N: float = summe_x_quad * summe_y_quad - (summe_xy)**2
        # Berechnun der Transforamtionsparameter a1-a4 durch Summen und Nenner
        a1: float = (summe_xX*summe_y_quad-summe_yX*summe_xy)/N
        a2: float = (summe_xX*summe_xy-summe_yX*summe_x_quad)/N
        a3: float = (summe_yY*summe_x_quad-summe_xY*summe_xy)/N
        a4: float = (summe_xY*summe_y_quad-summe_yY*summe_xy)/N
        print("yquad = ", summe_y_quad)
        # Aufruf der base class method parameter mit Parametern a1-a4 und Schwerpunkten
        param: tuple = super(AffinTransformation, self).parameter(a1, a2, a3, a4, p_a_s, p_n_s)
        # restliche von base class method berechnete Transformationsparameter aus Ergebnistupel holen
        #Translation
        P0: daten.punkt.Punkt = param[0]
        #Massstab Abszisse
        m1: float = param[1]
        #Massstab Ordinate
        m2: float = param[2]
        # Drehwinkel Abszisse
        alpha: float = winkel.rad2gon(param[3])
        # Drehwinkel Ordinate
        beta: float = winkel.rad2gon(param[4])
        # Dictionary mit allen Transformationsparametern
        trans_param: dict = {"Translation Y": P0.hole_y(), "Translation X": P0.hole_x(), "a1": a1, "a2": a2, "a3": a3,
                             "a4": a4, "m1": m1, "m2": m2, "alpha": alpha, "beta": beta}
        # Dictionary in string umwandeln mit json-interner Funktion dumps
        ergebnis: str = json.dumps(trans_param)
        #Umwandlung von str in json-Format
        meine_json_daten_antwort: object = json.loads(ergebnis)
        # JSON Ergebnisdatei schreiben
        with open('../ergebnisdateien/Parameter_Affin.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=False, indent=4)
        #Ausgabe der Transformationsarameter fuer Ausgabefelder und Funktion transformiere
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
        Ergebnisse: tuple = super(AffinTransformation, self).transformiere(identische_punkte_neu,
                                                                             identische_punkte_alt, a1, a2, a3, a4, P0)
        #Dictionary mit Restklaffen aus Tupel Ergebnisse holen
        meine_json_daten_antwort: dict = Ergebnisse[0]
        # Dictionary mit transformierten Punkten aus Tupel Ergebnisse holen
        meine_json_daten_antwort2: dict = Ergebnisse[1]
        #transformierte Punkte in json Datei schreiben
        with open('../ergebnisdateien/P_N_Affin.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort2, json_datei, sort_keys=True, indent=4)
        # Restklaffen in json Datei schreiben
        with open('../ergebnisdateien/Restklaffen_Affin.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
        return meine_json_daten_antwort,meine_json_daten_antwort2

#bei isolierter Ausfuehrung des Moduls
if __name__ == "__main__":
    # Punkte zum Testen
    # Punktnummer ist redundant!
    punkte_alt: dict = {
        "101": pkt.Punkt(-916.300, 6078.720, "101"),
        "102": pkt.Punkt(3331.420, 6492.430, "102"),
        "2096": pkt.Punkt(5091.510, 2158.040, "2096")
    }
    punkte_neu: dict = {
        "101": pkt.Punkt(36935.000, 2630.170, "101"),
        "102": pkt.Punkt(41132.120, 27133.890, "102"),
        "FAKE9999": pkt.Punkt(0.0, 0.0, "FAKE9999")
    }
    #Instanz von AffinTransformation
    at: transformationen.transformation.AffinTransformation = AffinTransformation(punkte_alt, punkte_neu)
    # Aufruf der berechne Funktion der Elternklasse Transformation von AffinTransformation
    at.berechne()

