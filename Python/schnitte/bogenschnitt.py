import daten.punkt as pkt
import daten.strecke as strecke
from math import *
import grundlagen.winkel as w
import grundlagen.erstegrund as e
import json

class Bogenschnitt:
    """Klasse zur Berechnung des Bogenschnittes"""
    def __init__(self,p_s1,p_s2, p_s3):
        """Konstruktor
        :param p_s1: gemessene Strecke zum NP von Punkt 1
        :type: daten.strecke.Strecke
        :param p_s2: gemessene Strecke zum NP von Punkt 2
        :type: daten.strecke.Strecke
        :param p_s3: gemessene Strecke von Punkt 1 zu Punkt 2
        :type: daten.strecke.Strecke"""

        #Definition der Klassenattribute (Protected)
        self.__s1: strecke.Strecke = p_s1
        self.__s2: strecke.Strecke = p_s2
        self.__s3: strecke.Strecke = p_s3
        pass

    def berechne(self)-> tuple:
        """berechne
           :return: keinen, einen oder zwei Neupunkte und ggf. ein Massstab
           :rtype: tuple """
        #bekannte Punkte aus Streckenobjekten holen
        p1: pkt.Punkt = self.__s1.hole_p1()
        p2: pkt.Punkt = self.__s2.hole_p1()

        #Koordinaten von Punkt 1 holen
        y1: float = p1.hole_y()
        x1: float = p1.hole_x()

        #Strecken aus Streckenobjekten holen
        s1: float = self.__s1.riwi_laenge()[1]
        s2: float = self.__s2.riwi_laenge()[1]
        s3: float = self.__s3.riwi_laenge()[1]

        #Schaffen einer Instanz der Klasse Strecke aus den gegebenen Punkten
        s: strecke.Strecke = strecke.Strecke(p1, p2)
        #Aufteilung von Strecke und Richtungswinkel von der Streckeninstanz in zwei Variablen
        str0: float = s.riwi_laenge()[1]
        t0: float = s.riwi_laenge()[0]

        #Pruefen ob s3 eingegeben wurde
        if s3 == 0.0:
            #wenn nicht Massstab auf 1 setzen
            m: float = 1.0
        else:
            #wenn ja Massstab berechnen. str0 ist die aus den Koordinaten berechnete, s3 die gemessene Strecke zwischen den bekannten Punkten
            m: float = str0/s3
            #gemessene Strecken mit Massstab korrigieren
            s1 *= m
            s2 *= m

        #Pruefen ob der Sonderfall schlechter Schnitt vorliegt
        if s1+s2 == str0:
            #wenn ja: Koordinaten des Neupunkt durch erste Grundaufgabe berechnen
            yn1: float = e.umrechnen_koordinaten(y1,x1,s1,t0)[0]
            xn1: float = e.umrechnen_koordinaten(y1,x1,s1,t0)[1]
            #Koordinaten in Punktobjekt wandeln
            pn1: pkt.Punkt = pkt.Punkt(yn1, xn1, "1")
            #Belegung der Variable pn2 mit String fuer Anzeige im Ergebnisfeld und Uebergabe eines einheitlichen Ergebnistupels
            pn2: str = "schlechter Schnitt (nur eine Lösung)"
            #Definition des Dictionarie mit dem Ergebnispunkt und Massstab zur Ausgabe des Ergebnisses als JSON Datei und Weitergabe an den Webdienst
            dict: dict = {"pn1": pn1.__dict__, "m": m}
            # Dictionary in Zeichenkette umwandeln
            ergebnis: str = json.dumps(dict)
            # JSON Ergebnisdatei schreiben
            meine_json_daten_antwort: object = json.loads(ergebnis)
            with open('Ergebnis_Bogenschnitt.json', 'w') as json_datei:
                json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
            # Ausgabe der Ergebnisdatei in Konsole
            with open('Ergebnis_Bogenschnitt.json', 'r') as json_datei2:
                json_daten2 = json.load(json_datei2)
                print(json.dumps(json_daten2, sort_keys=True, indent=4))
            #Ausgabe des Ergebnistupels mit dem Dictionary
            return pn1, pn2,m, meine_json_daten_antwort

        #Pruefen ob Sonderfall keine Loesung vorliegt
        elif s1+s2 < str0:
            #wenn ja Definition des Ergebnisdictionaries mit 2 Strings als Eintrag
            dict: dict = {"Widerspruch Daten": "keine Loesung"}
            # Dictionary in Zeichenkette umwandeln
            ergebnis: str = json.dumps(dict)
            # JSON Ergebnisdatei schreiben
            meine_json_daten_antwort: object = json.loads(ergebnis)
            with open('Ergebnis_Bogenschnitt.json', 'w') as json_datei:
                json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
            # Ausgabe der Ergebnisdatei in Konsole
            with open('Ergebnis_Bogenschnitt.json', 'r') as json_datei2:
                json_daten2 = json.load(json_datei2)
                print(json.dumps(json_daten2, sort_keys=True, indent=4))
            # Ausgabe von 3 Strings und dem Dictionary als Tupel
            return "keine Lösung", "","", meine_json_daten_antwort

        #Wenn kein Sonderfall vorliegt: Bogenschnitt berechnen (Zwischenvariablen siehe Formeln im Handbuch)
        else:
            a: float = acos((s1 ** 2 + str0 ** 2 - s2 ** 2) / (2 * str0 * s1))
            #Definition des Richtungswinkels durch Indexslicing der Streckeninstanz s und Umrechnung in rad (Strecke zwischen bekannten Punkten)
            t: float = w.gon2rad(s.riwi_laenge()[0])

            t1n1: float = t + a
            t1n2: float = t - a
            #Berechnung der Koordinaten des Ergebnispunktes
            yn1: float = y1 + s1 * sin(t1n1)
            xn1: float = x1 + s1 * cos(t1n1)
            yn2: float = y1 + s1 * sin(t1n2)
            xn2: float = x1 + s1 * cos(t1n2)
            #Umwandlung der Koordinaten in 2 Punktobjekte
            pn1: pkt.Punkt = pkt.Punkt(yn1, xn1, "1")
            pn2: pkt.Punkt = pkt.Punkt(yn2, xn2, "2")
            #Definition des Dictionaries zur Weitergabe der Ergebnisse als Datei und an Webdienst
            dict: dict = {"pn1": pn1.__dict__,"pn2": pn2.__dict__, "m": m}
            #Dictionary in Zeichenkette umwandeln
            ergebnis: str = json.dumps(dict)
            # JSON Ergebnisdatei schreiben
            meine_json_daten_antwort: object = json.loads(ergebnis)
            with open('Ergebnis_Bogenschnitt.json', 'w') as json_datei:
                json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
            #Ausgabe der Ergebnisdatei in Konsole
            with open('Ergebnis_Bogenschnitt.json', 'r') as json_datei2:
                json_daten2 = json.load(json_datei2)
                print(json.dumps(json_daten2, sort_keys=True, indent=4))
            #Ausgabe der Ergebnisse und des Dict. als Tupel
            return pn1, pn2,m, meine_json_daten_antwort


if __name__=="__main__":
    #Testparameter zum testen des Moduls bei isolierter manueller Ausfuehrung (wie button test)
    p1: pkt.Punkt=pkt.Punkt(328.76,1207.85,"P1")
    p2: pkt.Punkt=pkt.Punkt(925.04,954.33,"P2" )
    s1: strecke.Strecke = strecke.Strecke.punkt_laenge(p1, 294.33)
    s2: strecke.Strecke = strecke.Strecke.punkt_laenge(p2, 506.42)
    s3: strecke.Strecke = strecke.Strecke.punkt_laenge(p1, 0.0)
    bs: Bogenschnitt=Bogenschnitt(s1,s2,s3)
    bs.berechne()
    pass


