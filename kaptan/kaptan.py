#!/usr/bin/env python3
#
# Copyright 2016 Metehan Özbek <mthnzbk@gmail.com>
#           2020 Erdem Ersoy <erdemersoy@erdemersoy.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import sys
from PyQt6 import QtWidgets
from kaptan.libkaptan import *


class Kaptan(QtWidgets.QWizard):
    def __init__(self):
        super().__init__()
        self.setFixedSize(850, 600)

        self.setWindowTitle(self.tr("Kaptan"))
        self.setWindowIcon(QIcon.fromTheme("kaptan-icon"))
        self.setMinimumSize(850, 600)
        self.setMaximumSize(950, 620)

        self.setPixmap(QtWidgets.QWizard.WizardPixmap.LogoPixmap, QPixmap("/usr/share/kaptan/images/kaptan.png"))
        
        self.setButtonText(QtWidgets.QWizard.WizardButton.NextButton, self.tr("Next"))
        self.button(QtWidgets.QWizard.WizardButton.NextButton).setIcon(QIcon.fromTheme("arrow-right"))
        self.button(QtWidgets.QWizard.WizardButton.NextButton).setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.setButtonText(QtWidgets.QWizard.WizardButton.CancelButton, self.tr("Cancel"))
        self.button(QtWidgets.QWizard.WizardButton.CancelButton).setIcon(QIcon.fromTheme("dialog-cancel"))
        self.setOption(QtWidgets.QWizard.WizardOption.NoCancelButtonOnLastPage, True)
        self.setOption(QtWidgets.QWizard.WizardOption.CancelButtonOnLeft, True)

        self.setButtonText(QtWidgets.QWizard.WizardButton.BackButton, self.tr("Back"))
        self.setOption(QtWidgets.QWizard.WizardOption.NoBackButtonOnLastPage, True)
        self.setOption(QtWidgets.QWizard.WizardOption.NoBackButtonOnStartPage, True)
        self.button(QtWidgets.QWizard.WizardButton.BackButton).setIcon(QIcon.fromTheme("arrow-left"))

        self.setButtonText(QtWidgets.QWizard.WizardButton.FinishButton, self.tr("Finish"))
        self.button(QtWidgets.QWizard.WizardButton.FinishButton).setIcon(QIcon.fromTheme("dialog-ok-apply"))

        self.addPage(WelcomeWidget(self))
        self.addPage(MouseWidget(self))
        self.addPage(ThemeWidget(self))
        self.addPage(MenuWidget(self))
        self.addPage(WallpaperWidget(self))
        self.addPage(AvatarWidget(self))
        self.sumId = self.addPage(SummaryWidget(self))
        self.otherId = self.addPage(OtherWidget(self))

        self.currentIdChanged.connect(self.optionsAccepted)
        self.button(QtWidgets.QWizard.WizardButton.FinishButton).clicked.connect(self.close)

    summaryVisible = pyqtSignal()

    def optionsAccepted(self, identity):
        if identity == self.otherId:
            # MouseWidget
            self.page(1).execute()
            # ThemeWidget
            self.page(2).execute()
            # MenuWidget
            self.page(3).execute()
            # WallpaperWidget
            self.page(4).execute()
            # AvatarWidget
            self.page(5).execute()

            p = QProcess()
            p.startDetached("kquitapp5", ["plasmashell"])
            p.waitForStarted(2000)
            p.startDetached("kstart5", ["plasmashell"])

        if identity == self.sumId:
            self.setButtonText(QtWidgets.QWizard.WizardButton.NextButton, self.tr("Apply Settings"))
            self.button(QtWidgets.QWizard.WizardButton.NextButton).setIcon(QIcon.fromTheme("dialog-ok-apply"))
            self.summaryVisible.emit()
        else:
            self.setButtonText(QtWidgets.QWizard.WizardButton.NextButton, self.tr("Next"))
            self.button(QtWidgets.QWizard.WizardButton.NextButton).setIcon(QIcon.fromTheme("arrow-right"))

    def closeEvent(self, event):
        desktop_file = os.path.join(os.environ["HOME"], ".config", "autostart", "kaptan.desktop")
        if os.path.exists(desktop_file):
            os.remove(desktop_file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Kaptan")
    app.setOrganizationName("Kaptan")
    app.setApplicationVersion(Version.getVersion())
    # app.setStyleSheet(open(join(dirPath, "data/libkaptan.qss").read())

    locale = QLocale.system().name()
    translator = QTranslator(app)
    translator.load("/usr/share/kaptan/languages/{}.qm".format(locale))
    app.installTranslator(translator)

    kaptan = Kaptan()
    kaptan.show()
    app.exec()


if __name__ == "__main__":
    main()
