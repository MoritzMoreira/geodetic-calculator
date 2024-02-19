import xml.etree.ElementTree as ElTr
import ssl
import urllib.request
import urllib.error
import urllib.parse
import json
import socket
import http.client


class DatenDienst:
    """Klasse DatenDienst

    Jade HS
    Vorlesung "Programmieren geodätischer Aufgaben"
    A. Gollenstede
    WiSe 2020/21

    Stand: 2021-01-17

    Version 1.0.2
    """

    def __init__(self, p_ini: str, p_url: str, p_log: bool = False):
        """Konstruktor

        :todo: Innerhalb der Klasse gibt es z.Zt. kein Logging mehr

        :param p_ini: Ini-Datei mit Pfad, Dateiname und Endung
        :type p_ini: str
        :param p_url: Dienst-URL
        :type p_url: str
        """
        self.__xml_ini: ElTr.ElementTree = ElTr.parse(p_ini)
        self.__xml_wurzel: ElTr.Element = self.__xml_ini.getroot()

        self.__param: dict = {
            "service": self.__xml_wurzel.get('id'),
            "version": self.__xml_wurzel.get('version'),
            "user": self.__xml_wurzel.find('./benutzer').get('id'),
            "group": self.__xml_wurzel.find('./benutzer').get('gruppe')
        }

        self.__jwt = self.__xml_wurzel.find('./benutzer/jwt').text

        self.__url: str = p_url

        self.__log: bool = p_log

        self.__datumzeit: str = ''

        pass

    def anfrage(self, p_param: dict, p_json_daten: dict = None) -> dict:
        """

        Quelle(n):
        https://docs.python.org/3/library/urllib.request.html#urllib-examples

        :param p_param: An den Dienst zu übermittelnde Parameter (z.B. datasetid, user)
        :type p_param: dict
        :param p_json_daten: Zu übermittelnde Daten im JSON-Format
        :type p_json_daten: dict
        :return:
        :rtype: dict
        """

        dienst_json_daten: dict = {}

        #
        if p_json_daten is not None:
            daten: str = json.dumps(p_json_daten)
            p_param["dataset"] = daten

        param = {**p_param, **self.__param}
        dienst_param: str = urllib.parse.urlencode(param)
        dienst_daten: bytes = dienst_param.encode('utf-8')

        #
        dienst_kontext: ssl.SSLContext = ssl._create_unverified_context()

        #
        dienst_anfrage: urllib.request.Request = urllib.request.Request(self.__url)
        dienst_anfrage.add_header("Authorization", "Bearer %s" % self.__jwt)

        # todo: Fehlerbehandlung checken
        try:
            dienst_antwort: http.client.HTTPResponse = \
                urllib.request.urlopen(dienst_anfrage, context=dienst_kontext, data=dienst_daten)
            dienst_json_daten: dict = json.loads(dienst_antwort.read().decode('utf-8'))
            pass
        except socket.gaierror:
            print('Socket-Fehler')
        except urllib.error.URLError as e:
            if isinstance(e, str):
                print('URL-Fehler: ' + e.reason)
            else:
                print('URL-Fehler')
        # except urllib.error.HTTPError as e:
        #    print('HTTP-Fehler:' + e.code + ' ' + e.reason)
        except ValueError as e:
            print('Keine valide URL!')
        else:
            # Alles gut
            self.__datumzeit = dienst_json_daten["datetime_" + p_param["request"]]
        finally:
            try:
                dienst_antwort.close()
            except NameError:
                pass

        return dienst_json_daten

    def parse_daten(self, p_json_daten: dict) -> dict:
        """

        :param p_json_daten:
        :type p_json_daten: dict
        :return:
        :rtype: dict
        """
        json_daten: dict = {}

        # Klasse des Objektes bestimmen
        print(p_json_daten)
        klasse: str = p_json_daten["class"]
        meine_klasse: str = self._uebersetze_klasse(klasse)

        # Alle Datenelemente in "data" durchlaufen
        for schluessel, wert in p_json_daten["data"].items():

            # schluessel entspricht hier prinzipiell der id eines Objektes
            # Zweisung eigentlich nicht nötig
            mein_schluessel = schluessel
            mein_wert = wert
            if isinstance(wert, dict):
                mein_wert: dict = self._parse_klasse(klasse, meine_klasse, wert)

            json_daten[mein_schluessel] = mein_wert

        return json_daten

    def _parse_klasse(self, p_klasse, p_meine_klasse, p_json_klasse: dict) -> dict:
        """JSON mit den in der Ini-Datei definierten Schlüsseln versehen

        Vom Prinzip her identisch mit _parse_meine_klasse.
        Es werden jedoch andere Methoden zur Übersetzung aufgerufen.
        Da die Methode eh sehr kurz ist, würde das Zusammenführen mit Fall-
        unterscheidung wenig einsparen. Eine "dynamische" Umsetzung wäre u.U.
        denkbar.

        :param p_json_klasse: zu verändernde JSON-Daten
        :type p_json_klasse: dict
        :return: Überarbeitetes JSON
        :rtype: dict
        """
        json_meine_klasse: dict = {}

        for schluessel, wert in p_json_klasse.items():

            mein_schluessel: str = self._uebersetze_schluessel(p_klasse, p_meine_klasse, schluessel)

            # Ist der Wert ein Dictionary? Dann ist das aktuelle Element wohl ein Objekt
            if isinstance(wert, dict):
                # todo: verschachtelte Objekte
                mein_wert = wert
                pass
            else:
                mein_wert = wert
            json_meine_klasse[mein_schluessel] = mein_wert

        return json_meine_klasse

    def _uebersetze_klasse(self, p_klasse: str) -> str:
        """

        :param p_klasse:
        :return: meine_klasse
        :rtype: str
        """
        xml_element: ElTr.Element = self.__xml_wurzel.find('./klassen/' + p_klasse)

        if xml_element is None:
            meine_klasse: str = p_klasse
        else:
            meine_klasse: str = xml_element.attrib["klasse"]

        return meine_klasse

    def _uebersetze_schluessel(self, p_klasse: str, p_meine_klasse: str, p_schluessel: str) -> str:
        """
        :param p_klasse:
        :param p_meine_klasse:
        :param p_schluessel:
        :return:
        :rtype: str
        """
        xml_element: ElTr.Element = self.__xml_wurzel.find("./klassen/" + p_klasse + "/" + p_schluessel)

        if xml_element is None:
            # Muss das sein?
            mein_schluessel: str = p_schluessel
        else:
            # ungenutzt
            typ: str = xml_element.attrib["typ"]

            mein_schluessel: str = xml_element.attrib["attribut"]

            # private Attribute
            if mein_schluessel[:2] == '__':
                mein_schluessel = '_' + p_meine_klasse + mein_schluessel
            else:
                # todo: ?
                pass

        return mein_schluessel

    def parse_meine_daten(self, p_json_meine_daten: dict, p_meine_klasse: str) -> dict:

        # todo: Klasse direkt aus den JSON-Daten ableiten; setzt private Attribute voraus(?)
        meine_klasse = p_meine_klasse
        klasse = self._uebersetze_meine_klasse(meine_klasse)

        # todo: Messung setzen
        # todo: Metadaten
        daten: dict = {
            "class": klasse,
            "measurement": False,
            "meta": {},
            "data": {}
        }

        for mein_schluessel, mein_wert in p_json_meine_daten.items():

            # Zweisung eigentlich nicht nötig
            schluessel = mein_schluessel
            wert = mein_wert
            if isinstance(mein_wert, dict):
                wert: dict = self._parse_meine_klasse(meine_klasse, klasse, mein_wert)

            daten["data"][schluessel] = wert

        return daten

    def _parse_meine_klasse(self, p_meine_klasse, p_klasse, p_json_meine_klasse: dict):
        """

        Vom Prinzip her identisch mit _parse_klasse.
        Es werden jedoch andere Methoden zur Übersetzung aufgerufen.
        Da die Methode eh sehr kurz ist, würde das Zusammenführen mit Fall-
        unterscheidung wenig einsparen. Eine "dynamische" Umsetzung wäre u.U.
        denkbar.

        :param p_meine_klasse:
        :param p_klasse:
        :param p_json_meine_klasse:
        :return:
        """
        json_klasse: dict = {}

        for mein_schluessel, mein_wert in p_json_meine_klasse.items():

            schluessel: str = self._uebersetze_meinen_schluessel(p_meine_klasse, p_klasse, mein_schluessel)

            # Ist der Wert ein Dictionary? Dann ist das aktuelle Element wohl ein Objekt
            if isinstance(mein_wert, dict):
                # todo: verschachtelte Objekte
                wert = mein_wert
                pass
            else:
                wert = mein_wert
            json_klasse[schluessel] = wert

        return json_klasse

    def _uebersetze_meine_klasse(self, p_meine_klasse) -> str:


        element_liste: list = self.__xml_wurzel.findall('./klassen/*[@klasse="' + p_meine_klasse + '"]')

        if element_liste:
            # Theoretisch kann es nur ein Element geben
            klasse: str = element_liste[0].tag
        else:
            klasse = p_meine_klasse

        return klasse

    def _uebersetze_meinen_schluessel(self, p_meine_klasse, p_klasse, p_mein_schluessel) -> str:

        # Kurzform (ohne Klassenangabe) meines Schlüssels
        # todo: z.Zt. nur private Attribute
        # todo: Ist es "sicherer" hier zunächst auch die __ zu suchen (und zu ersetzen)?
        mein_schluessel = p_mein_schluessel.replace('_' + p_meine_klasse + '__', '')

        element_liste: list = \
            self.__xml_wurzel.findall('./klassen/' + p_klasse + '/*[@attribut="__' + mein_schluessel + '"]')

        if element_liste:
            # Theoretisch kann es nur ein Element geben
            schluessel: str = element_liste[0].tag
        else:
            schluessel: str = mein_schluessel

        return schluessel

    def hole_log(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return self.__log

    def hole_datumzeit(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self.__datumzeit


if __name__ == '__main__':

    dienst_url = 'https://mapsrv.net/pga/service/'
    # dienst_url = 'http://dropbox.local/hostpoint/mapsrv.net/www/pga/service/'

    dd: DatenDienst = DatenDienst('datendienst.ini.xml', dienst_url, True)

    #
    # Lesen
    #
    print("LESEN -------------------")

    param_lesen: dict = {
        'datasetid': 'test-punkte',
        'request': 'getdata'
    }

    dienst_json_daten_antwort: dict = dd.anfrage(param_lesen)

    # Gibt es eine Antwort mit Daten?
    if dienst_json_daten_antwort['data'] != '':

        meine_json_daten_antwort: dict = dd.parse_daten(dienst_json_daten_antwort)

        if dd.hole_log():
            print("LESEN: Antwort")
            print(json.dumps(dienst_json_daten_antwort, sort_keys=True, indent=4))
            print("LESEN: angepasste Antwort")
            print(json.dumps(meine_json_daten_antwort, sort_keys=True, indent=4))

        #
        # Schreiben (und Empfangen)
        #
        print("SCHREIBEN ---------------")

        param_schreiben: dict = {
            'datasetid': 'test-punkte',
            'request': 'postdata'
        }

        # Gerade gelesene Daten wieder auf dem Server speichern
        meine_json_daten_anfrage: dict = meine_json_daten_antwort

        meine_klasse_vorgabe = 'Punkt'
        dienst_json_daten_anfrage: dict = dd.parse_meine_daten(meine_json_daten_anfrage, meine_klasse_vorgabe)

        if dd.hole_log():
            print("SCHREIBEN: Daten")
            print(json.dumps(meine_json_daten_anfrage, sort_keys=True, indent=4))
            print("SCHREIBEN: angepasste Daten")
            print(json.dumps(dienst_json_daten_anfrage, sort_keys=True, indent=4))

        dienst_json_daten_antwort2: dict = dd.anfrage(param_schreiben, dienst_json_daten_anfrage)

        # Gibt es eine Antwort mit Daten?
        if dienst_json_daten_antwort2['data'] != '':

            if dd.hole_log():
                print("SCHREIBEN: Rückmeldung")
                print(json.dumps(dienst_json_daten_antwort2, sort_keys=True, indent=4))
        else:
            print(json.dumps(dienst_json_daten_antwort2, sort_keys=True, indent=4))
            print(dienst_json_daten_antwort2['error'])
    else:
        print(json.dumps(dienst_json_daten_antwort, sort_keys=True, indent=4))
        print(dienst_json_daten_antwort['error'])

    pass