import daten.punkt as pkt
import json
import math

class Transformation:
    """Klasse Transformation, Elternklasse von HelmertTransformation und AffinTransformation
        Berechnung der fuer beide Kindklassen gleichen Rechenschritte"""

    def __init__(self, p_punkte_alt, p_punkte_neu):
        """Konstruktor
            :param p_punkte_alt: Punkte im lokalen System
            :type: dict
            :param p_punkte_neu: Passpunkte im uebergeordneten System
            :type: dict"""

        # todo: deepcopy? je nach Datentyp der Listen
        self.__punkte_alt: dict = p_punkte_alt
        self.__punkte_neu: dict = p_punkte_neu

    def berechne(self) -> tuple:
        """berechne, ruft nacheinander die verschiedenen Funktionen zur Berechnung der Transformation auf
            :return: Transformationsparameter
            :rtype: tuple"""
        # Liste mit identischen Passpunkten um uebergeordneten System, Dictionary mit Passpunkten im lokalen System und die Schwerpunkte von Funktion schwerpunkte
        s: tuple = self.schwerpunkte()
        # Liste der reduzierten Passpunkte im lokalen System und Dictionary der reduzierten Passpunkte im uebergeordneten System von Funktion reduktion
        r: tuple = self.reduktion(s)
        # Transformationsparameter durch Funktion parameter berechnen
        p: tuple = self.parameter(r[0],r[1], s[2],s[3])
        # Transformation der Punkte und Berechnung der Restklaffen, json Dateien schreiben, Ausgabe der Dicts fuer Datendienst in GUI
        print("a1 berechne = ", p[1])
        t: tuple = self.transformiere(s[1],s[0],p[1],p[2],p[3],p[4],p[0])
        #Ausgabe der Transformationsparameter, transformierte Punkte un Restklaffen fuer Ausgabefelder in GUI und Datendienst
        return p, t

    def reduktion(self, s) -> tuple:
        """reduktion, Reduziert Passpunkte auf Schwerpunkt
            :param s: Ausgabe von Funktion schwerpunkte
            :type: tuple
            :return: Liste der reduzierten Passpunkte im lokalen System, Dictionary der reduzierten Punkte im übergeordneten System
            :rtype: tuple"""
        # Punktlisten und Schwerpunkte aus Tupel holen
        identische_punkte_alt: dict = s[0]
        identische_punkte_neu: list = s[1]
        p_a_s: daten.punkt.Punkt = s[2]
        p_n_s: daten.punkt.Punkt = s[3]

        #Definition von Liste und Dictionary fuer reduzierte Punkte
        punkte_alt_red: list = []
        punkte_neu_red: dict = {}

        # Reduktion der Punkte im lokalen System
        for key, item in identische_punkte_alt.items():
            y_red = item.hole_y() - p_a_s.hole_y()
            x_red = item.hole_x() - p_a_s.hole_x()
            #Punktobjekt aus Y und X Wert
            p_red: daten.punkt.Punkt = pkt.Punkt(y_red, x_red, item.hole_nr())
            #Punkt in Liste einfügen
            punkte_alt_red.append(p_red)
        # Reduktion der Punkte im übergeordneten System
        for el in identische_punkte_neu:
            y_red = el.hole_y() - p_n_s.hole_y()
            x_red = el.hole_x() - p_n_s.hole_x()
            # Punktobjekt aus Y und X Wert
            p_red: daten.punkt.Punkt = pkt.Punkt(y_red, x_red, el.hole_nr())
            # Punkt in Dictionary mit Punktnummer als key einfügen
            punkte_neu_red[el.hole_nr()] = p_red
        # Ausgabe der reduzierten Punkte
        return punkte_alt_red, punkte_neu_red

    def transformiere(self,identische_punkte_neu, identische_punkte_alt,a1,a2,a3,a4,P0) -> tuple:
        """transformiere, Transformation der Punkte und Berechnung der Restklaffen
            :param identische_punkte_neu:
            :type: list
            :param identische_punkte_alt:
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
            :type P0: daten.punkt.Punkt
            :return: Restklaffen und transformierte Punkte im json Format
            :rtype: tuple"""
        #Restklaffen
        restklaffen: dict = {}
        # über Passpunkte im uebergeordneten System iterieren
        for p_n in identische_punkte_neu:
            # Punktnummer holen
            nr: str = p_n.hole_nr()
            # entsprechenden Passpunkt aus lokalem System mit Punktnummer als Schluessel holen
            p_a: daten.punkt.Punkt = identische_punkte_alt[nr]
            # Berechnung der Restklaffen
            Wy: float = -P0.hole_y() - a3 * p_a.hole_y() - a4 * p_a.hole_x() + p_n.hole_y()
            Wx: float = -P0.hole_x() - a1 * p_a.hole_x() + a2 * p_a.hole_y() + p_n.hole_x()
            # Restklaffen dem Dictionary hinzufügen mit Punktnummer als Schlüssel
            restklaffen[nr] = f"y: {Wy}, x: {Wx}"

        # Dictionary in Zeichenkette umwandeln
        ergebnis: str = json.dumps(restklaffen)
        # Zeichenkette in json Format umwandeln
        meine_json_daten_antwort: object = json.loads(ergebnis)


        #Transformation
        #Translation Y und X aus Punktobjekt holen
        Y0: float = P0.hole_y()
        X0: float = P0.hole_x()

        transformierte_punkte: dict = {}
        #ueber Punkte im lokalen System iterieren
        for item in self.__punkte_alt.items():
            # Rechts- und Hochwert des Punktes holen
            y = item[1].hole_y()
            x = item[1].hole_x()
            # Transformation berechnen
            Y: float = Y0 + a3 * y + a4 * x
            X: float = X0 + a1 * x - a2 * y
            #Punktobjekt aus Y und X Wert und Punktnummer
            p_n: daten.punkt.Punkt = pkt.Punkt(Y, X, item[0])
            # Hinzufuegen des Punktes zum Dictionary als Dictionary (nicht als Punktobjekt)
            transformierte_punkte[item[0]] = p_n.__dict__

        # Dictionary in Zeichenkette umwandeln
        ergebnis2: str = json.dumps(transformierte_punkte)
        # Zeichenkette in json Format umwandeln
        meine_json_daten_antwort2: object = json.loads(ergebnis2)
        # Ausgabe der Ergebnisdictionaries fuer Datendienst
        return meine_json_daten_antwort, meine_json_daten_antwort2

    def schwerpunkte(self) -> tuple:
        """schwerpunkte, Schwerpunkte der Passpunkte im alten und neuen System berechnen
        :return: identische_punkte_alt, identische_punkte_neu, Schwerpunkte
        :rtype: tuple"""
        #Definition der Summenvariablen
        summe_y_a: float = 0.0
        summe_x_a: float = 0.0
        summe_y_n: float = 0.0
        summe_x_n: float = 0.0

        anzahl: int = 0
        nr: str
        p_n: pkt.Punkt
        #Dictionary fuer Passpunkte alt
        identische_punkte_alt={}
        # Liste fuer Passpunkte neu
        identische_punkte_neu=[]
        # Iteration über die Punkte im neuen System
        for nr, p_n in self.__punkte_neu.items():

            # Existiert der Punkt auch im alten Sys?
            if nr in self.__punkte_alt:
                anzahl += 1
                # Alten Pkt aus Liste des alten Sys holen
                p_a: pkt.Punkt = self.__punkte_alt[nr]
                #Punkte dem Dict und der Liste hinzufuegen
                identische_punkte_alt[nr] = p_a
                identische_punkte_neu.append(p_n)

                summe_y_a += p_a.hole_y()
                summe_x_a += p_a.hole_x()

                summe_y_n += p_n.hole_y()
                summe_x_n += p_n.hole_x()
        # Schwerpunkte berechnen
        p_a_s: pkt.Punkt = pkt.Punkt(summe_y_a / anzahl, summe_x_a / anzahl, "pas")
        p_n_s: pkt.Punkt = pkt.Punkt(summe_y_n / anzahl, summe_x_n / anzahl, "pns")
        #Ausgabe Punktlisten und Schwerpunkte
        print(p_n_s.__str__())
        return identische_punkte_alt, identische_punkte_neu, p_a_s, p_n_s

    def parameter(self,a1,a2,a3,a4,p_a_s,p_n_s) -> tuple:
        """parameter, Transformationsparameter berechnen
           :return: Translation, Massstaebe, Drehwinkel
           :rtype: tuple"""
        #Translation berechnen
        Y0: float = p_n_s.hole_y() - a3 * p_a_s.hole_y() - a4 * p_a_s.hole_x()
        print("Y0 = ", Y0, ", pnsy = ", p_n_s.hole_y(), "a3 = ", a3, ", pasy = ", p_a_s.hole_y(), "a4 = ", a4, ", pasx = ", p_a_s.hole_x())
        X0: float = p_n_s.hole_x() - a1 * p_a_s.hole_x() + a2 * p_a_s.hole_y()
        #Punktobjekt aus Y und X Wert
        P0: daten.punkt.Punkt = pkt.Punkt(Y0, X0,"P0")

        #Massstab
        m1: float = math.sqrt(a1 ** 2 + a4 ** 2)
        m2: float = math.sqrt(a2 ** 2 + a3 ** 2)
        # Drehwinkel
        alpha: float = math.atan2(a4, a1)
        beta: float = math.atan2(a2, a3)
        #Ausgabe der Parameter
        return P0,m1,m2,alpha,beta







