from math import *
import grundlagen.winkel as w
import grundlagen.erstegrund as e
import json
import daten.strecke as strecke
import daten.punkt as pkt



class Polygonzugbeidseitig:
    def __init__(self):

        """Konstruktor
                :param yo: gegebener y-Wert von Punkt
                :type: daten.strecke.Strecke
                :param p_s2: gemessene Strecke zum NP von Punkt 2
                :type: daten.strecke.Strecke
                :param p_s3: gemessene Strecke von Punkt 1 zu Punkt 2
                :type: daten.strecke.Strecke"""
        #Einlesen der gegebenen Punkte aus json-Datei
        with open('../polygonzug/punkte_polygon.json', 'r') as json_datei:
            json_daten = json.load(json_datei)

        # Definition der Klassenattribute (Protected)
            self.__y0 = json_daten["P0"]["y"]
            self.__x0 = json_daten["P0"]["x"]
            self.__y1 = json_daten["P1"]["y"]
            self.__x1 = json_daten["P1"]["x"]
            self.__yN = json_daten["PN"]["y"]
            self.__xN = json_daten["PN"]["x"]
            self.__yN1 = json_daten["PN+1"]["y"]
            self.__xN1 = json_daten["PN+1"]["x"]

        pass

    def berechne(self) -> tuple:
        """berechne
                   :return: y-x-Werte der zu bestimmenden Punkte
                   :rtype: dict """

        #Öffnen und speichern der Richtungen und Strecken in json_daten
        with open('../polygonzug/runds_polygon.json', 'r') as json_datei:
            json_daten = json.load(json_datei)

        #Protected Variablen einfügen
        y1 = self.__y1
        x1 = self.__x1
        y0 = self.__y0
        x0 = self.__x0
        yN = self.__yN
        xN = self.__xN
        yN1 = self.__yN1
        xN1 = self.__xN1

       # t01 = Richtungswinkel zwischen P0 und P1
       # tN = Richtungswinkel zwischen PN und PN+1
        t01 = strecke.Strecke(pkt.Punkt(y0, x0), pkt.Punkt(y1, x1)).riwi_laenge()[0]
        tN = round(strecke.Strecke(pkt.Punkt(yN, xN), pkt.Punkt(yN1, xN1)).riwi_laenge()[0], 4)
        print("t01: ", t01)
        print("tN: ", tN)
        print("yN = ", yN, ", xN = ", xN, ", yN1 = ", yN1, ", xN1 = ", xN1)
        #berechnung richtungsabweichung

        #speichern der gegeben Richtungen und Strecken in eine Liste
        werte = list(json_daten.items())
        """Konstruktor
                        :param x: Hilfskonstruktor
                        :param n: Anzahl Richtungsmessungen
                        :param s: Gesamtstrecke der Streckenmessungen 
                        :param b: Summe aller Richtungsmessungen                    
                         """
        x=0
        n=0
        s=0
        #Erstellen einer Liste mit den Keys der Werte-Liste zur Bestimmung von n und s
        liste = list(json_daten.keys())
        #While-Schleife die überprüft ob es sich bei dem gegebenen Wert um eine Richtung oder Strecke handelt
        while x<len(liste):
            anfang = liste[x]
            if anfang[0] == "r":
                n+=1
            elif anfang[0] == "s":
                s+=werte[x][1]
            x+=1
        x=0
        b=0
        print("anzahl r: ", n)
        print("summe s : ", s)
        #Bestimmung der Summe aller Richtungsmessungen
        while x<n:
            b += werte[x][1]
            x+=1
        n-=2

        print("summe r: ", b)
        ''':param wb: Winkelabschlussfehler'''
        wb=(tN-t01)-(b)
        print("WB vor if else: ", wb)
        #Bestimmung des Winkelabschlussfehlers
        if wb>0:
            wb-=n*200
        else:
            wb+=n*200
        n+=2
        wb = round(wb,4)
        print("WB: ", wb)
        '''berechnung verbesserte Richtungswinkel
        :param richt: Liste mit verbesserten Richtungswinkeln
        :type richt: List
        '''
        #Erstellen einer Liste mit den verbesserten Richtungswinkeln
        richt = [t01]
        x=0
        while x<n-1:
            r0 = (w.richtungswinkel_aus_richtung(richt[x], werte[x][1])+wb/n)
            richt.append(r0)
            x+=1

        """ :param deltay: Liste mit den delta y Werten
            :param deltax: Liste mit den delta x Werten
            :param y: Hilfskonstruktor
            :param v: Hilfskonstruktor"""

        #Berechnung der Koordinatenabweichungen wx und wy
        deltay = []
        deltax = []
        x=n
        v=0

        while v<n-1:
            dy = e.umrechnen_koordinatenunterschiedey((werte[x][1]), richt[v+1])
            deltay.append(dy)
            x+=1
            v+=1

        x = n
        v=0
        while v<n-1:
            dx = e.umrechnen_koordinatenunterschiedex((werte[x][1]), richt[v+1])
            deltax.append(dx)

            x+=1
            v+=1
        """:param sumy: Summe der deltay Werte
           :param sumx: Summe der deltax Werte
           :param wy: Koordinatenabweichung in y Richtung
           :param wx: Koordinatenabweichung in x Richtung
           :param Pkty: Liste der gesuchten Y-Werte der zu bestimmenen Punkte
           :param Pktx: Liste der gesuchten X-Werte der zu bestimmenen Punkte
           :param z: Hilfskonstruktor
           :param dict: Lösungs-Dictionary 
           """

        sumy=sum(deltay)
        sumx = sum(deltax)
        wy=(yN-y1)-sumy
        wx=(xN-x1)-sumx
        x=0
        y = y1
        z = round(len(werte)/2)

        Pkty = []
        # Bestimmen der gesuchten Y Werte der Punkte
        while x<len(deltay):
            yneu = y+deltay[x]+(wy/s)*werte[z][1]
            Pkty.append(yneu)
            y=yneu
            z+=1
            x+=1

        y = 0
        x = x1
        z = round(len(werte)/2)
        Pktx = []
        # Bestimmen der gesuchten X Werte der Punkte
        while y<len(deltax):
            xneu = x+deltax[y]+(wx/s)*werte[z][1]
            Pktx.append(xneu)
            x = xneu
            z += 1
            y += 1
        #Erstellen eines leeren Dictionarys zur Speicherung der gesuchten Punkte
        dict={}
        x=0
        pktnr=2
        while x < len(Pkty)-1:
            neu = {pktnr:{"y":Pkty[x],"x":Pktx[x]}}
            dict.update(neu)
            pktnr+=1
            x+=1

        '''nur zum austesten'''
        print(dict)
        #zurückgeben der gesuchten punkte über dictionary
        return dict

if __name__=="__main__":
    #Test zum ausführen in dieser python datei ohne gui

    pzb: Polygonzugbeidseitig=Polygonzugbeidseitig()
    pzb.berechne()
    pass