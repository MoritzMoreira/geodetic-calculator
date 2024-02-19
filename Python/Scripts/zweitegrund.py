from tkinter import *
from math import *
from Scripts import winkel, gui


def umrechnen_gui():
    y1= gui.auswerten(eingabe_y1)
    x1 = gui.auswerten(eingabe_x1)
    y2= gui.auswerten(eingabe_y2)
    x2= gui.auswerten(eingabe_x2)

    s12, t12=umrechnen_koordinaten(y1,x1,y2,x2)

    gui.eingabefeld_schreiben(ausgabe_s12, s12)
    gui.eingabefeld_schreiben(ausgabe_t12, t12)

def umrechnen_koordinaten(y1,x1,y2,x2):
    t12=atan2((y2-y1),(x2-x1))
    s12=sqrt((y2-y1)**2+(x2-x1)**2)
    t12= winkel.rad2gon(t12)
    return s12,t12

def test2():
    y1=528.15
    x1=407.65
    y2=795.17
    x2=525.1

    gui.eingabefeld_schreiben(eingabe_y1, y1)
    gui.eingabefeld_schreiben(eingabe_x1, x1)
    gui.eingabefeld_schreiben(eingabe_y2, y2)
    gui.eingabefeld_schreiben(eingabe_x2, x2)


fenster=Tk()
Label(fenster,text="2.Hauptaufgabe", anchor=W,justify=LEFT,width=25).grid(row=0,column=0, columnspan=4)

Label(fenster,text="y1:",anchor=W,justify=LEFT,width=10).grid(row=1,column=0)
Label(fenster,text="x1:",anchor=W,justify=LEFT,width=10).grid(row=2,column=0)
Label(fenster,text="y2:",anchor=W,justify=LEFT,width=10).grid(row=3,column=0)
Label(fenster,text="x2:",anchor=W,justify=LEFT,width=10).grid(row=4,column=0)

eingabe_y1=Entry(fenster)
eingabe_x1=Entry(fenster)
eingabe_y2=Entry(fenster)
eingabe_x2=Entry(fenster)

eingabe_y1.grid(row=1, column=1)
eingabe_x1.grid(row=2, column=1)
eingabe_y2.grid(row=3, column=1)
eingabe_x2.grid(row=4, column=1)

Button(fenster,text="Umrechnen", command=umrechnen_gui).grid(row=0,column=2)

ausgabe_s12=Entry(fenster)
ausgabe_t12=Entry(fenster)

ausgabe_s12.grid(row=2, column=2)
ausgabe_t12.grid(row=4, column=2)

Label(fenster,text="Strecke, s12:", anchor=W,justify=LEFT,width=10).grid(row=1,column=2)
Label(fenster,text="Richtung, t12:", anchor=W,justify=LEFT,width=10).grid(row=3,column=2)

test2()
Button(fenster,text="Beenden",command=fenster.destroy).grid(row=5,column=2, columnspan=3)

fenster.mainloop()

