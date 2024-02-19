import copy
import grundlagen.zweitegrund
from typing import Tuple
import daten.punkt as pkt

class Strecke:
    """Klasse Strecke
    """
    def __init__(self,p_p1: pkt.Punkt,p_p2: pkt.Punkt,p_d=20, p_nr=""):
        """
        :param p_p1: Anfangspunkt
        :type: daten.punkt.Punkt
        :param p_p2: Endpunkt
        :type: daten.punkt.Punkt
        :param p_d: Dezimalstellen der eingegebenen Strecke
        :type: float """

        self.__p1: pkt.Punkt = copy.deepcopy(p_p1)
        self.__p2: pkt.Punkt = copy.deepcopy(p_p2)
        self.__d: float = p_d
        self.__nr: str=p_nr

    @classmethod
    def punkt_laenge(cls,p_p1: pkt.Punkt, p_laenge: float, p_nr=""):
        """alternativer Konstruktor
        :param p_p1: Punkt 1
        :type: daten.punkt.Punkt
        :param p_laenge: eingegebene Strecke
        :type: float
        :param p_nr: Punktnummer
        :type str"""

        #Dezimalstellen der Streckeneingabe holen
        p_d: float = len(str(p_laenge).split('.')[1])
        #Pseudopunkt auf x-Achse bilden
        p2:pkt.Punkt = pkt.Punkt(p_p1.hole_y(),p_p1.hole_x()+ p_laenge)
        return cls(p_p1, p2, p_d, p_nr)

    def setze_nr(self, p_nr: str):
        """setter in gon

        :param p_gon: Winkelgroesse in Gon
        :type: float
        """
        self.__nr = p_nr

    def hole_nr(self):
        """getter in gon
        :return: Winkelgroesse in Gon
        :rtype: float
        """
        return self.__nr

    def hole_p1(self) ->pkt.Punkt:
        """"Hole Startpunkt
        :return: Startpunkt
        :rtype: daten.punkt.Punkt
        """

        return self.__p1
    def hole_p2(self) ->pkt.Punkt:
        return self.__p2

    def riwi_laenge(self) -> Tuple[float, float]:
        """"Richtungswinkel und Strecke zurueckgeben
        :return: s12, t12
        :rtype: Tuple[float,float]
        
        """
        ts: Tuple[float,float]
        t,s=grundlagen.zweitegrund.umrechnen_koordinaten(self.__p1.hole_y(),self.__p1.hole_x(),self.__p2.hole_y(),self.__p2.hole_x())
        #Ausgabe des Richtungswinkels und der ggf. gerundeten Strecke
        return t,round(s, self.__d)
    def __str__(self) -> str:
        """Zeichenkette
        :return:Streckeninfos als Zeichenkette
        :rtype: str
        """
        ts: Tuple[float, float] = self.riwi_laenge()
        zeichen: str= "Nr:" + self.__nr + 'p1:' + str(self.__p1)+',p2:' + str(self.__p2) + ',t=' + str(ts[0]) + ',s=' + str(ts[1])
        return zeichen

if __name__=="__main__":
    p1: pkt.Punkt=pkt.Punkt(0.0,0.0, "p11")
    p2: pkt.Punkt=pkt.Punkt(1.0,1.0, "p12")
    s1: Strecke=Strecke.punkt_laenge(p1,5.0,"s1")
    s,t =s1.riwi_laenge()
    print(t)
    print(s)
    print(s1)
    pass
