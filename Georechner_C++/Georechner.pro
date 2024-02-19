QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    affintransformation_gui.cpp \
    bogenschnitt_gui.cpp \
    daten/punkt.cpp \
    daten/strecke.cpp \
    daten/winkel_klasse.cpp \
    einstellung.cpp \
    erstegrund_gui.cpp \
    grundlagen/allgemein.cpp \
    grundlagen/erstegrund.cpp \
    grundlagen/winkel.cpp \
    helmerttransformation_gui.cpp \
    main.cpp \
    mainwindow.cpp \
    polygonzug_gui.cpp \
    rueckwaertsschnitt_gui.cpp \
    schnitte/bogenschnitt.cpp \
    schnitte/rueckwaertsschnitt.cpp \
    schnitte/vorwaertsschnitt.cpp \
    transformationen/affintransformation.cpp \
    transformationen/polygonzug.cpp \
    transformationen/transformation.cpp \
    vorwaertsschnitt_gui.cpp \
    winkel_gui.cpp \
    zweitegrund_gui.cpp

HEADERS += \
    affintransformation_gui.h \
    bogenschnitt_gui.h \
    einstellung.h \
    erstegrund_gui.h \
    helmerttransformation_gui.h \
    json.h \
    mainwindow.h \
    polygonzug_gui.h \
    rueckwaertsschnitt_gui.h \
    vorwaertsschnitt_gui.h \
    winkel_gui.h \
    zweitegrund_gui.h

FORMS += \
    affintransformation_gui.ui \
    bogenschnitt_gui.ui \
    einstellung.ui \
    erstegrund_gui.ui \
    helmerttransformation_gui.ui \
    mainwindow.ui \
    polygonzug_gui.ui \
    rueckwaertsschnitt_gui.ui \
    vorwaertsschnitt_gui.ui \
    winkel_gui.ui \
    zweitegrund_gui.ui

TRANSLATIONS += lang_en.ts  \
                lang_de.ts   \
                lang_fr.ts  \
                lang_es.ts



# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    translations.qrc

DISTFILES += \
    carl-friedrich-gauss.jpg
