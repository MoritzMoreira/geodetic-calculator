from tkinter import *


def auswerten(eingabefeld):
    sz = eingabefeld.get()
    sz = sz.replace(",", ".")
    try:
        f=float(sz)
    except:
        f=0.0
    return f
def wert2fliess(p_wert):
    try:
        f=float(p_wert)
    except:
        f=0.0
    return f

def eingabefeld_schreiben(eingabefeld,p_wert):
    eingabefeld.delete(0,END)
    eingabefeld.insert(0,str(p_wert))
