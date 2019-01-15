# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Calcul_Nbre_LOG_FODialog
                                 A QGIS plugin
 Calcul_Nbre_LOG_FO
                             -------------------
        begin                : 2018-07-25
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Circet
        email                : labhalmehdi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Calcul_Nbre_LOG_FO_dialog_base.ui'))


class Calcul_Nbre_LOG_FODialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Calcul_Nbre_LOG_FODialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

		
		
FORM_CLASS_dim_boite, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dimensionnement_boite_dialog_base.ui'))


class dimensionnement_boiteDialog(QtGui.QDialog, FORM_CLASS_dim_boite):
    def __init__(self, parent=None):
        """Constructor."""
        super(dimensionnement_boiteDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
		

FORM_CLASS_isole, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'calcul_isole_dialog_base.ui'))


class calcul_isoleDialog(QtGui.QDialog, FORM_CLASS_isole):
    def __init__(self, parent=None):
        """Constructor."""
        super(calcul_isoleDialog, self).__init__(parent)
        self.setupUi(self)