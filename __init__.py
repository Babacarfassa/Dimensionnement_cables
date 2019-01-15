# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Calcul_Nbre_LOG_FO
                                 A QGIS plugin
 Calcul_Nbre_LOG_FO
                             -------------------
        begin                : 2018-07-25
        copyright            : (C) 2018 by Circet
        email                : Babacar.FASSA@circet.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Calcul_Nbre_LOG_FO class from file Calcul_Nbre_LOG_FO.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Calcul_Nbre_LOG_FO import Calcul_Nbre_LOG_FO
    return Calcul_Nbre_LOG_FO(iface)
