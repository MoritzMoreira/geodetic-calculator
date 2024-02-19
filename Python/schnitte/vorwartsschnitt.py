import daten.punkt as pkt
import daten.strecke as strecke
from math import *
import grundlagen.winkel as w
import grundlagen.erstegrund as e
import grundlagen.zweitegrund as z
import json


class Vorwärtsschnitt:
    """Klasse zur Berechnung des Vorwärtsschnittes"""

    def __init__(self,p_p1, p_p2, p_p3, p_p4, p_phi, p_psi):

        """Konstruktor
        :param p_p1: bekannter Punkt 1
        :type: daten.punkt.Punkt
        :param p_p2: bekannter Punkt 2
        :type: daten.punkt.Punkt
        :param p_p3: bekannter Punkt 3
        :type: daten.punkt.Punkt
        :param p_p4: bekannter Punkt 4
        :type: daten.punkt.Punkt
        :param p_phi: Winkel auf Punkt 1 zwischen Punkt 4 und Punkt N
        :type: float
        :param p_psi: Winkel auf Punkt 2 zwischen Punkt 3 und Punkt N
        :type: float
        """

        # Definition der Klassenattribute (Protected)
        self.__p1 = p_p1
        self.__p2 = p_p2
        self.__p3 = p_p3
        self.__p4 = p_p4
        self.__phi = p_phi
        self.__psi = p_psi

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
        y4: float = self.__p4.hole_y()
        x4: float = self.__p4.hole_x()

        # Umschreiben der Winkel fuer kompaktere Schreibweisen
        phi: float = self.__phi
        psi: float = self.__psi

        #Berechnung der Richtungswinkel t14 und t23 aus den Koordinaten
        t14: float = z.umrechnen_koordinaten(y1, x1, y4, x4)[1]
        t23: float = z.umrechnen_koordinaten(y2, x2, y3, x3)[1]

        # Berechnung der Richtungskoeffizienten mit den orientierten Richtungen

        p4n: float = w.gon2rad(t14 + phi)
        p2n: float = w.gon2rad(t23 + psi)

        # Berechnung der Koordinaten des Ergebnispunktes
        xn: float = x1 + ((y2-y1)-(x2-x1)*tan(p2n))/(tan(p4n)-tan(p2n))
        yn: float = y1 + (xn-x1) * tan(p4n)

        # Umwandlung der Koordinaten in ein Punktobjekte
        pn: pkt.Punkt = pkt.Punkt(yn, xn, "N")

        # Definition des Dictionaries zur Weitergabe der Ergebnisse als Datei und an Webdienst
        dict: dict = {"pn": pn.__dict__}
        # Dictionary in Zeichenkette umwandeln
        ergebnis: str = json.dumps(dict)
        # JSON Ergebnisdatei schreiben
        meine_json_daten_antwort: object = json.loads(ergebnis)
        with open('../ergebnisdateien/Ergebnis_Vorwärtsschnitt.json', 'w') as json_datei:
            json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
        # Ausgabe der Ergebnisdatei in Konsole
        with open('../ergebnisdateien/Ergebnis_Vorwärtsschnitt.json', 'r') as json_datei2:
            json_daten2 = json.load(json_datei2)

        return pn, meine_json_daten_antwort


if __name__ == "__main__":
    # Testparameter zum testen des Moduls bei isolierter manueller Ausfuehrung
    p1: pkt.Punkt = pkt.Punkt(24681.92, 90831.87, "P1")
    p4: pkt.Punkt = pkt.Punkt(23231.58, 91422.92, "P2")
    p2: pkt.Punkt = pkt.Punkt(24877.72, 89251.09, "P3")
    p3: pkt.Punkt = pkt.Punkt(22526.65, 89150.52, "P4")
    phi: float = 331.6174
    psi: float = 60.7510
    vs: Vorwärtsschnitt = Vorwärtsschnitt(p1, p2, p3, p4, phi, psi)
    vs.berechne()
    pass
