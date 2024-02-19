from tkinter import *
#
# Funktionen zur Benutzeroberflächensteuerung
#
def eingabefeld_auswerten(p_eingabefeld) -> float:
    '''
    Auslesen eines Eingabefeldes für Fließkommazahlen

    - Umwandlung von Komma in Punkt
    - Prüfen, ob das Feld eine "gültigen" Wert enthält

    :param p_eingabefeld: Eingabefeld
    :type p_eingabefeld: Entry
    :return:
    '''
    # Zeichenkette
    sz_wert = p_eingabefeld.get()
    # Evtl. Eingabe mit Komma als Komma in Punkt umwandeln
    sz_wert = sz_wert.replace(",", ".")
    # Umwandlung in Fließkomma und Rückgabe
    return wert2fliess(sz_wert)


def wert2fliess(p_wert):
    '''
    Umwandlung eines Wertes in eine Fließkommazahl

    :param p_wert:
    :return:
    '''
    # Ungültige Zeichenketten behandeln, damit kein Fehler geworfen wird
    try:
        # Versuch der Umwandlung in Fließkommazahl mit Zuweisung zur Variablen f
        f = float(p_wert)
    except:
        # Versuch ist fehlgeschlagen, eine Ausnahme wurde geworfen
        # f auf 0.0 setzen
        f = 0.0
    # Rückgabe: Bei erfolgreicher Umwandlung, den korrekten Wert, sonst 0.0a
    return f


def eingabefeld_schreiben(p_eingabefeld, p_wert):
    '''
    Eingabefeld löschen und neu schreiben

    :param p_eingabefeld:
    :param p_wert:
    :return:
    '''
    # Eingabefeld löschen
    p_eingabefeld.delete(0, END)
    # Eingabefelder mit den berechneten Werten füllen
    p_eingabefeld.insert(0, str(p_wert))