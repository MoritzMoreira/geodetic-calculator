#include "mainwindow.h"

//HelmertTransformation::HelmertTransformation(std::map<std::string, Punkt>& p_punkte_alt, std::map<std::string, Punkt>& p_punkte_neu):
//    HelmertTransformation(p_punkte_alt, p_punkte_neu){}

float* HelmertTransformation::parameter_h(std::vector<Punkt>& punkte_alt_red, std::map<std::string, Punkt>& punkte_neu_red, Punkt& p_a_s, Punkt& p_n_s){
    float zaehler_o = 0.0;
    float zaehler_a = 0.0;
    float nenner = 0.0;
    std::string nr;
    Punkt p_red_neu;
    // Bildung der Summen durch for-Schleife durch Liste der alten reduzierten Passpunkte
    for(Punkt p_red_alt : punkte_alt_red){
        // Punktnummer holen
        nr = p_red_alt.hole_nr();
        // entsprechenden reduzierten neuen Passpunkt mit Punktnummer als Schlüssel holen
        p_red_neu = punkte_neu_red[nr];
        // Aufaddieren der verschiedenen Therme zur Summenbildung
        zaehler_o += p_red_alt.hole_x()*p_red_neu.hole_y()-p_red_alt.hole_y()*p_red_neu.hole_x();
        zaehler_a += p_red_alt.hole_x()*p_red_neu.hole_x()+p_red_alt.hole_y()*p_red_neu.hole_y();
        // Berechnung des Nenners aus den Summen
        nenner +=  pow(p_red_alt.hole_x(),2) + pow(p_red_alt.hole_y(),2);
    }
    // Berechnung der Transformationsparameter a1-a4 (bzw. a und o) durch Summen und Nenner. Doppelte Belegung der 4 Variablen für Nutzung der Elternklasse Transformation
    float a1 = zaehler_a/nenner;    //a
    float a3 = a1;                  //o
    float a2 = zaehler_o/nenner;    //a
    float a4 = a2;                  //o

    // Aufruf der base class method parameter mit Parametern a1-a4 und Schwerpunkten
    float* param = this->parameter_base(a1,a2,a3,a4,p_a_s,p_n_s);
    // restliche von base class method berechnete Transformationsparameter aus Ergebnistupel holen
    Punkt P0 = Punkt(param[0], param[1]);           // Translation
    float m1 = param[2];                      // Massstab
    float m2 = 0.0f;                                    // Belegung fuer Nutzung der Elternklasse Transformation
    float alpha = rad2gon(param[4]);    // Drehwinkel
    float beta = 0.0;                                  // Belegung fuer Nutzung der Elternklasse Transformation

    // Map mit allen Transformationsparametern
    std::map<std::string,float> trans_param = {{"Translation Y", param[0]}, {"Translation X", param[1]}, {"a", a1}, {"o", a2}, {"m", m1}, {"Drehwinkel", alpha}};
    // Map in string umwandeln mit json-interner Funktion dumps
    //ergebnis: str = json.dumps(trans_param)
    //Umwandlung von str in json-Format
    //meine_json_daten_antwort: object = json.loads(ergebnis)
    // JSON Ergebnisdatei schreiben
    //with open('../ergebnisdateien/Parameter_Helmert.json', 'w') as json_datei:
     //   json.dump(meine_json_daten_antwort, json_datei, sort_keys=False, indent=4)

    // Ausgabe der Transformationsarameter für Ausgabefelder, Funktion transformiere und Webdienst
    static float arr[] = {param[0], param[1], a1, a2, a3, a4, m1, m2, alpha, beta};
    return arr;
}

result_trans HelmertTransformation::transformiere_h(std::vector<Punkt>& p_ident_pkt_neu, std::map<std::string, Punkt>& p_ident_pkt_alt, float& a1, float& a2, float& a3, float& a4, float& Y0, float& X0){
    // Aufruf der base class method -> Transformation der Punkte + Berechnung der Restklaffen
    result_trans Ergebnisse = this->transformiere(p_ident_pkt_neu, p_ident_pkt_alt,  a1,  a2,  a3,  a4,  Y0,  X0);
    // Map mit Restklaffen aus Struct Ergebnisse holen
    //std::string antwort = Ergebnisse.restklaffen;
    // Dictionary mit transformierten Punkten aus Tupel Ergebnisse holen
    std::map<std::string, Punkt> antwort2 = Ergebnisse.transformierte_Pkt;

    // transformierte Punkte in json Datei schreiben
//    with open('../ergebnisdateien/P_N_Helmert.json', 'w') as json_datei:
//        json.dump(meine_json_daten_antwort2, json_datei, sort_keys=False, indent=4)

//    // Restklaffen in json Datei schreiben
//    with open('../ergebnisdateien/Restklaffen_Helmert.json', 'w') as json_datei:
//        json.dump(meine_json_daten_antwort, json_datei, sort_keys=True, indent=4)
    //Ausgabe der Dicts für Datendienst
    return Ergebnisse;
}


