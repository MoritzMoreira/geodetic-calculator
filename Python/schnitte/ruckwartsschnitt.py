import daten.punkt as pkt
from math import *
import grundlagen.winkel as w
import grundlagen.zweitegrund as z
import json



class Rückwärtsschnitt:
    """Klasse zur Berechnung des Rückwärtsschnittes"""

    def __init__(self,p_p1, p_p2, p_p3, p_r1, p_r2, p_r3):

        """Konstruktor
        :param p_p1: bekannter Punkt 1
        :type: daten.punkt.Punkt
        :param p_p2: bekannter Punkt 2
        :type: daten.punkt.Punkt
        :param p_p3: bekannter Punkt 3
        :type: daten.punkt.Punkt
        :param p_r1: Richtung auf Punkt 1
        :type: float
        :param p_r2: Richtung auf Punkt 2
        :type: float
        :param p_r3: Richtung auf Punkt 3
        :type: float
        """

        # Definition der Klassenattribute (Protected)
        self.__p1 = p_p1
        self.__p2 = p_p2
        self.__p3 = p_p3
        self.__r1 = p_r1
        self.__r2 = p_r2
        self.__r3 = p_r3

        pass

    def berechne(self) -> tuple:
        """berechne
           :return: Koordinaten des Neupunktes
           :rtype: tuple """

        # Definition von Variablen fuer die Koordinaten
        y1: float = self.__p1.hole_y()
        x1: float = self.__p1.hole_x()
        y2: float = self.__p2.hole_y()
        x2: float = self.__p2.hole_x()
        y3: float = self.__p3.hole_y()
        x3: float = self.__p3.hole_x()


        # Umschreiben der Richtungsvariablen fuer kompaktere Schreibweisen
        r1: float = self.__r1
        r2: float = self.__r2
        r3: float = self.__r3

        #Berechnung der Winkel alpha und beta aus den Richtungswinkeln
        a: float = w.gon2rad(r1 - r3)
        b: float = w.gon2rad(r2 - r1)

        #Berchnung der Koordinaten der Hilfspunkte

        yc: float = y1 + (x2-x1) * w.cot(a)
        xc: float = x1 - (y2-y1) * w.cot(a)
        yd: float = y3 + (x3-x2) * w.cot(b)
        xd: float = x3 - (y3-y2) * w.cot(b)
        print("yc: ", yc)
        # Berechnung des Richtungswinkel tcd aus den Hilfskoordinaten

        tcd: float = w.gon2rad(z.umrechnen_koordinaten(yc, xc, yd, xd)[1])
        print("tdc: ", tcd)

        # Berechnung der Koordinaten des Ergebnispunktes
        xn: float = xc + (y2-yc+(x2-xc)*w.cot(tcd))/(tan(tcd)+w.cot(tcd))
        yn: float = yc + (xn-xc) * tan(tcd)

        # Umwandlung der Koordinaten in ein Punktobjekte
        pn: pkt.Punkt = pkt.Punkt(yn, xn, "PN")

        # Definition des Dictionaries zur Weitergabe der Ergebnisse als Datei und an Webdienst
        dict: dict = {"pn": pn.__dict__}
        # Dictionary in Zeichenkette umwandeln
        ergebnis: str = json.dumps(dict)
        # JSON Ergebnisdatei schreiben
        meine_json_daten_antwort: object = json.loads(ergebnis)
        with open('../ergebnisdateien/Ergebnis_Rückwärtsschnitt.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
        # Ausgabe der Ergebnisdatei in Konsole
        with open('../ergebnisdateien/Ergebnis_Rückwärtsschnitt.json', 'r') as json_datei2:
            json_daten2 = json.load(json_datei2)
            print(json.dumps(json_daten2, sort_keys=True, indent=4))






        # Ausgabe der Ergebnisse und des Dict. als Tupel
        return pn, meine_json_daten_antwort


if __name__ == "__main__":
    # Testparameter zum testen des Moduls bei isolierter manueller Ausfuehrung
    p1: pkt.Punkt = pkt.Punkt(49666.56, 4448.58, "P1")
    p2: pkt.Punkt = pkt.Punkt(46867.94, 5537.00, "P2")
    p3: pkt.Punkt = pkt.Punkt(51293.86, 6365.89, "P3")
    r1: float = 66.8117
    r2: float = 294.7845
    r3: float = 362.8516
    rs: Rückwärtsschnitt = Rückwärtsschnitt(p1, p2, p3, r1, r2, r3)
    rs.berechne()
    pass
