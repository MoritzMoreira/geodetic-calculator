//#include "mainwindow.h"
//#include <QActionGroup>
//#include <QLocale>
//#include <QApplication>
//#include <QDir>
//#include <QAction>

//// we create the menu entries dynamically, dependent on the existing translations.
//void MainWindow::createLanguageMenu(void) {
// QActionGroup* langGroup = new QActionGroup(ui.menuLanguage);
// langGroup->setExclusive(true);

// connect(langGroup, SIGNAL (triggered(QAction *)), this, SLOT (slotLanguageChanged(QAction *)));

// // format systems language
// QString defaultLocale = QLocale::system().name(); // e.g. "de_DE"
// defaultLocale.truncate(defaultLocale.lastIndexOf('_')); // e.g. "de"

// m_langPath = QApplication::applicationDirPath();
// m_langPath.append("/languages");
// QDir dir(m_langPath);
// QStringList fileNames = dir.entryList(QStringList("TranslationExample_*.qm"));

// for (int i = 0; i < fileNames.size(); ++i) {
//  // get locale extracted by filename
//  QString locale;
//  locale = fileNames[i]; // "TranslationExample_de.qm"
//  locale.truncate(locale.lastIndexOf('.')); // "TranslationExample_de"
//  locale.remove(0, locale.lastIndexOf('_') + 1); // "de"

//  QString lang = QLocale::languageToString(QLocale(locale).language());
//  QIcon ico(QString("%1/%2.png").arg(m_langPath).arg(locale));

//  QAction *action = new QAction(ico, lang, this);
//  action->setCheckable(true);
//  action->setData(locale);

//  ui->menuLanguage->addAction(action);
//  langGroup->addAction(action);

//  // set default translators and language checked
//  if (defaultLocale == locale) {
//   action->setChecked(true);
//  }
// }
//}
