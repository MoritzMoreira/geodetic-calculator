import sys
def ausnahme(p_wert):
    f=0.0
    b_Ausnahme=True
    try:
        print("pruefe ausnahme")
        float(p_wert)
    except ValueError:
        print("value")
        pass
    except OverflowError:
        print("overflow")
        pass
    except:
        print("fehlgeschlagen", sys.exc_info()[0])
        pass

    else:
        f=float(p_wert)
        b_Ausnahme= False
    finally:
        if b_Ausnahme:
            print("mit Fehler")
        else:
            print("ohne Fehler")
    print("Ergebnis" + str(f))



if __name__ == "__main__":
    sz_alpha="pi"
    ausnahme(sz_alpha)

    sz_alphanumerisch= "3.14159pi"
    ausnahme(sz_alphanumerisch)

    sz_numerisch= "3.14159"
    ausnahme(sz_numerisch)

    i=10
    ausnahme(i)
    i_ganz_gross=2**10000
    ausnahme(i_ganz_gross)

    sz_exponential="3e-002"
    ausnahme(sz_exponential)
    liste=[3,1,4]
    ausnahme(liste)