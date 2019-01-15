# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Calcul_Nbre_LOG_FO
                                 A QGIS plugin
 Calcul_Nbre_LOG_FO
                              -------------------
        begin                : 2018-07-25
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Circet
        email                : Babacar.FASSA@circet.fr
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
from qgis.core import * 
from qgis.utils import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from collections import defaultdict
from collections import Counter
# Initialize Qt resources from file resources.py
import resources
from Calcul_nombre_Logements_fibres_boites_ZPBO import Calcul_nombre_Logements_fibres_boites_ZPBO_function
from Calcul_nombre_fibres_cables import Calcul_nombre_fibres_cables_function
from Mis_jour_capacites_cables import Mis_jour_capacites_cables_function
from Calcul_modulo_cables import Calcul_modulo_cables_function
from Calcul_mode_pose_cable import Calcul_mode_pose_cable_function
from Calcul_nombre_cables_support import Calcul_nombre_cables_support_function
from dimensionnement_boite import dimensionnement_boite_function
from calcul_isole import function_isole
# Import the code for the dialog
from Calcul_Nbre_LOG_FO_dialog import Calcul_Nbre_LOG_FODialog
from Calcul_Nbre_LOG_FO_dialog import dimensionnement_boiteDialog
from Calcul_Nbre_LOG_FO_dialog import calcul_isoleDialog
from Calcul_Besoin_FO_Reseau_dialog import Calcul_Besoin_FO_ReseauDialog
from Mise_a_jour_capa_reel_dialog import Mise_a_jour_capa_reelDialog
from Calcul_modulo_cable_dialog import Calcul_modulo_cableDialog
from Calcul_mode_pose_section_dialog import Calcul_mode_pose_sectionDialog
from Calcul_nbr_Cable_infra_dialog import Calcul_nbr_Cable_infraDialog

import os.path
import processing


class Calcul_Nbre_LOG_FO:
	"""QGIS Plugin Implementation."""

	def __init__(self, iface):
		"""Constructor.

		:param iface: An interface instance that will be passed to this class
			which provides the hook by which you can manipulate the QGIS
			application at run time.
		:type iface: QgisInterface
		"""
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value('locale/userLocale')[0:2]
		locale_path = os.path.join(
			self.plugin_dir,
			'i18n',
			'Calcul_Nbre_LOG_FO_{}.qm'.format(locale))

		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)


		# Declare instance attributes
		self.actions = []
		self.menu = self.tr(u'&Dimmensionnement Cables')
		# TODO: We are going to let the user set this up in a future iteration
		self.toolbar = self.iface.addToolBar(u'Calcul_Nbre_LOG_FO')
		self.toolbar.setObjectName(u'Calcul_Nbre_LOG_FO')

    # noinspection PyMethodMayBeStatic
	def tr(self, message):
		"""Get the translation for a string using Qt translation API.

		We implement this ourselves since we do not inherit QObject.

		:param message: String for translation.
		:type message: str, QString

		:returns: Translated version of message.
		:rtype: QString
		"""
		# noinspection PyTypeChecker,PyArgumentList,PyCallByClass
		return message#QCoreApplication.translate('Calcul_Nbre_LOG_FO', message)


	'''def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Calcul_Nbre_LOG_FODialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Calcul_Nbre_LOG_FO/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Calcul_Nbre_LOG_FO'),
            callback=self.run,
            parent=self.iface.mainWindow())'''
	
	#Declaration des actions pour regrouper des plugins
	def initGui(self):
		self.menu = "&[Circet] A.2. Dimensionnement des cables"
		self.action = QAction(
			QIcon(':/plugins/Control_Avant_Detection/icon.png'),
			u"Dimensionnement_cables", self.iface.mainWindow())
		self.action0 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.1. Calcul du nombre de Logements et de fibres dans les boites et les ZPBO" ), self.iface.mainWindow() )
		self.action1 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.2. Calcul du nombre de fibres utilisees sur les cables" ), self.iface.mainWindow() )
		self.action2 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.3. Mis a jour des capacites des cables" ), self.iface.mainWindow() )
		self.action3 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.4. Calcul du modulo des cables" ), self.iface.mainWindow() )
		self.action4 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.5. Calcul du mode de pose d'un cable" ), self.iface.mainWindow() )
		self.action5 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.6. Calcul du nombre de cables dans un support" ), self.iface.mainWindow() )
		self.action6 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.7. Dimensionnement des boites" ), self.iface.mainWindow() )
		self.action7 = QAction( QCoreApplication.translate("Dimensionnement_cables", "A.2.8. Calcul du statut isole" ), self.iface.mainWindow() )


		
		# connect the action to the run method
		self.action.triggered.connect(self.run)
		self.action0.triggered.connect(self.run)
		self.action1.triggered.connect(self.runCalcul_nombre_fibres_cables)
		self.action2.triggered.connect(self.runMis_jour_capacites_cables)
		self.action3.triggered.connect(self.runCalcul_modulo_cables)
		self.action4.triggered.connect(self.runCalcul_mode_pose_cable)
		self.action5.triggered.connect(self.runCalcul_nombre_cables_support)
		self.action6.triggered.connect(self.runDimensionnementBoite)
		self.action7.triggered.connect(self.runcalcule_isole)

	 
		self.iface.addPluginToMenu(self.menu, self.action0)
		self.iface.addPluginToMenu(self.menu, self.action1)
		self.iface.addPluginToMenu(self.menu, self.action2)
		self.iface.addPluginToMenu(self.menu, self.action3)
		self.iface.addPluginToMenu(self.menu, self.action4)
		self.iface.addPluginToMenu(self.menu, self.action5)
		self.iface.addPluginToMenu(self.menu, self.action6)
		self.iface.addPluginToMenu(self.menu, self.action7)


		self.actions.append(self.action0)
		self.actions.append(self.action1)
		self.actions.append(self.action2)
		self.actions.append(self.action3)
		self.actions.append(self.action4)
		self.actions.append(self.action5)
		self.actions.append(self.action6)
		self.actions.append(self.action7)



	def unload(self):
		"""Removes the plugin menu item and icon from QGIS GUI."""
		for action in self.actions:
			self.iface.removePluginMenu(self.menu,action)
			#self.iface.removeToolBarIcon(action)
		# remove the toolbar
		#del self.toolbar


	def run(self):
		"""Run method that performs all the real work"""
		self.dlg = Calcul_Nbre_LOG_FODialog()
		self.dlg.comboPBO.clear()
		self.dlg.comboCABLES.clear()
		self.dlg.comboSITES.clear()
		self.dlg.comboZPBO.clear()
		

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())


		self.dlg.comboPBO.addItems(layer_list)
		self.dlg.comboCABLES.addItems(layer_list)
		self.dlg.comboSITES.addItems(layer_list)
		self.dlg.comboZPBO.addItems(layer_list)
		# show the dialog
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result:
			

			PBOLayerIndex = self.dlg.comboPBO.currentIndex()
			PBOLayer = layers[PBOLayerIndex]
			shape_pbo= PBOLayer

			CABLESLayerIndex = self.dlg.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			SITESLayerIndex = self.dlg.comboSITES.currentIndex()
			SITESLayer = layers[SITESLayerIndex]
			shape_sites= SITESLayer

			ZPBOLayerIndex = self.dlg.comboZPBO.currentIndex()
			ZPBOLayer = layers[ZPBOLayerIndex]
			shape_zpbo= ZPBOLayer
			# Do something useful here - delete the line containing pass and
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Calcul_nombre_Logements_fibres_boites_ZPBO_function(shape_pbo,shape_zpbo,shape_cables,shape_sites,Fichier_CONF_PYTHON)
			
			
			
			
	def runCalcul_nombre_fibres_cables(self):
		"""Run method that performs all the real work"""
		self.dlgcalcullogfocable = Calcul_Besoin_FO_ReseauDialog()
		self.dlgcalcullogfocable.comboPBO.clear()
		self.dlgcalcullogfocable.comboCABLES.clear()
		 

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())


		self.dlgcalcullogfocable.comboPBO.addItems(layer_list)
		self.dlgcalcullogfocable.comboCABLES.addItems(layer_list)
		 
		# show the dialog
		self.dlgcalcullogfocable.show()
		# Run the dialog event loop
		result = self.dlgcalcullogfocable.exec_()
		# See if OK was pressed
		if result:
			

			PBOLayerIndex = self.dlgcalcullogfocable.comboPBO.currentIndex()
			PBOLayer = layers[PBOLayerIndex]
			shape_pbo= PBOLayer

			CABLESLayerIndex = self.dlgcalcullogfocable.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Calcul_nombre_fibres_cables_function(shape_pbo,shape_cables,Fichier_CONF_PYTHON)
			
			
	def runMis_jour_capacites_cables(self):
		"""Run method that performs all the real work"""
		self.dlgmiseajourcapacable = Mise_a_jour_capa_reelDialog()
		self.dlgmiseajourcapacable.comboPBO.clear()
		self.dlgmiseajourcapacable.comboCABLES.clear()

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())


		self.dlgmiseajourcapacable.comboPBO.addItems(layer_list)
		self.dlgmiseajourcapacable.comboCABLES.addItems(layer_list)

		# show the dialog
		self.dlgmiseajourcapacable.show()
		# Run the dialog event loop
		result = self.dlgmiseajourcapacable.exec_()
		# See if OK was pressed
		if result:
			

			PBOLayerIndex = self.dlgmiseajourcapacable.comboPBO.currentIndex()
			PBOLayer = layers[PBOLayerIndex]
			shape_pbo= PBOLayer

			CABLESLayerIndex = self.dlgmiseajourcapacable.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Mis_jour_capacites_cables_function(shape_pbo,shape_cables,Fichier_CONF_PYTHON)
			
			
			
	def runCalcul_modulo_cables(self):
		"""Run method that performs all the real work"""
		self.dlgcalculcable = Calcul_modulo_cableDialog()
		self.dlgcalculcable.comboCABLES.clear()

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())

		self.dlgcalculcable.comboCABLES.addItems(layer_list)
		 
		# show the dialog
		self.dlgcalculcable.show()
		# Run the dialog event loop
		result = self.dlgcalculcable.exec_()
		# See if OK was pressed
		if result:

			CABLESLayerIndex = self.dlgcalculcable.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Calcul_modulo_cables_function(shape_cables,Fichier_CONF_PYTHON)
			
			
	def runCalcul_mode_pose_cable(self):
		"""Run method that performs all the real work"""
		self.dlgcalculmodeposecable = Calcul_mode_pose_sectionDialog()	 
		self.dlgcalculmodeposecable.comboCABLES.clear()
		self.dlgcalculmodeposecable.comboSUPPORT.clear()

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())

		self.dlgcalculmodeposecable.comboCABLES.addItems(layer_list)
		self.dlgcalculmodeposecable.comboSUPPORT.addItems(layer_list)
		 
		# show the dialog
		self.dlgcalculmodeposecable.show()
		# Run the dialog event loop
		result = self.dlgcalculmodeposecable.exec_()
		# See if OK was pressed
		if result:

			CABLESLayerIndex = self.dlgcalculmodeposecable.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			SUPPORTLayerIndex = self.dlgcalculmodeposecable.comboSUPPORT.currentIndex()
			SUPPORTLayer = layers[SUPPORTLayerIndex]
			shape_support= SUPPORTLayer

			#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Calcul_mode_pose_cable_function(shape_cables,shape_support,Fichier_CONF_PYTHON)
			
			
	def runCalcul_nombre_cables_support(self):
		"""Run method that performs all the real work"""
		self.dlgcalculnbrecablesupport = Calcul_nbr_Cable_infraDialog()
		self.dlgcalculnbrecablesupport.comboCABLES.clear()
		self.dlgcalculnbrecablesupport.comboINFRA.clear()
		 
		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())
				
		self.dlgcalculnbrecablesupport.comboINFRA.addItems(layer_list)
		self.dlgcalculnbrecablesupport.comboCABLES.addItems(layer_list)
		 
		# show the dialog
		self.dlgcalculnbrecablesupport.show()
		# Run the dialog event loop
		result = self.dlgcalculnbrecablesupport.exec_()
		# See if OK was pressed
		if result:

			INFRALayerIndex = self.dlgcalculnbrecablesupport.comboINFRA.currentIndex()
			INFRALayer = layers[INFRALayerIndex]
			shape_infra= INFRALayer

			CABLESLayerIndex = self.dlgcalculnbrecablesupport.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			Calcul_nombre_cables_support_function(shape_cables,shape_infra,Fichier_CONF_PYTHON)
	
	def runDimensionnementBoite(self):
		"""Run method that performs all the real work"""
		self.dlg = dimensionnement_boiteDialog()
		self.dlg.comboPBO.clear()
		self.dlg.comboPT.clear()
		self.dlg.comboCABLES.clear()
		self.dlg.comboSITES.clear()
		self.dlg.comboZPBO.clear()
		

		layers = self.iface.legendInterface().layers()
		layer_list = []
		for layer in layers:
			layerType = layer.type()
			if layerType == QgsMapLayer.VectorLayer:
				layer_list.append(layer.name())


		self.dlg.comboPBO.addItems(layer_list)
		self.dlg.comboPT.addItems(layer_list)
		self.dlg.comboCABLES.addItems(layer_list)
		self.dlg.comboSITES.addItems(layer_list)
		self.dlg.comboZPBO.addItems(layer_list)
		# show the dialog
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result:
			

			PBOLayerIndex = self.dlg.comboPBO.currentIndex()
			PBOLayer = layers[PBOLayerIndex]
			shape_boite= PBOLayer
			
			PTLayerIndex = self.dlg.comboPT.currentIndex()
			PTLayer = layers[PTLayerIndex]
			shape_point_technique= PTLayer

			CABLESLayerIndex = self.dlg.comboCABLES.currentIndex()
			CABLESLayer = layers[CABLESLayerIndex]
			shape_cables= CABLESLayer

			SITESLayerIndex = self.dlg.comboSITES.currentIndex()
			SITESLayer = layers[SITESLayerIndex]
			shape_sites= SITESLayer

			ZPBOLayerIndex = self.dlg.comboZPBO.currentIndex()
			ZPBOLayer = layers[ZPBOLayerIndex]
			shape_poche_boite= ZPBOLayer
			# Do something useful here - delete the line containing pass and
			Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
			fichier_ref_compare=QFileDialog.getOpenFileName(None, "Fichier_Ref_boite", "", "xlsx files (*.xlsx)")
			dimensionnement_boite_function(shape_boite,shape_point_technique,shape_poche_boite,shape_cables,shape_sites,Fichier_CONF_PYTHON,fichier_ref_compare)
			

			
			
			
	def runcalcule_isole(self):
			"""Run method that performs all the real work"""
			self.dlg = calcul_isoleDialog()
			self.dlg.comboPBO.clear()
			self.dlg.comboPT.clear()
			self.dlg.comboCABLES.clear()
			self.dlg.comboSITES.clear()
			self.dlg.combosupport.clear()
			

			layers = self.iface.legendInterface().layers()
			layer_list = []
			for layer in layers:
				layerType = layer.type()
				if layerType == QgsMapLayer.VectorLayer:
					layer_list.append(layer.name())


			self.dlg.comboPBO.addItems(layer_list)
			self.dlg.comboPT.addItems(layer_list)
			self.dlg.comboCABLES.addItems(layer_list)
			self.dlg.comboSITES.addItems(layer_list)
			self.dlg.combosupport.addItems(layer_list)
			# show the dialog
			self.dlg.show()
			# Run the dialog event loop
			result = self.dlg.exec_()
			# See if OK was pressed
			if result:
				

				PBOLayerIndex = self.dlg.comboPBO.currentIndex()
				PBOLayer = layers[PBOLayerIndex]
				shape_boite= PBOLayer
				
				PTLayerIndex = self.dlg.comboPT.currentIndex()
				PTLayer = layers[PTLayerIndex]
				shape_point_technique= PTLayer

				CABLESLayerIndex = self.dlg.comboCABLES.currentIndex()
				CABLESLayer = layers[CABLESLayerIndex]
				shape_cables= CABLESLayer

				SITESLayerIndex = self.dlg.comboSITES.currentIndex()
				SITESLayer = layers[SITESLayerIndex]
				shape_sites= SITESLayer

				SupportLayerIndex = self.dlg.combosupport.currentIndex()
				SupportLayer = layers[SupportLayerIndex]
				shape_support= SupportLayer
				# Do something useful here - delete the line containing pass and
				Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
				function_isole(shape_boite,shape_point_technique,shape_support,shape_cables,shape_sites,Fichier_CONF_PYTHON)
				