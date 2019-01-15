import processing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
from collections import Counter


def Calcul_modulo_cables_function(shape_cables,Fichier_CONF_PYTHON):
	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_CB_name_CB_STRUCT='CB_STRUCT'
	shape_CB_name_CB_TYPE_FONC='CB_TYPE_FONC'
	#Declaration des noms des entites
	shape_CB_name_CB_TYPE_FONC_Transport='CB_TYPE_FONC_Transport'
	shape_CB_name_CB_STRUCT_conduite='CB_STRUCT_conduite'
	shape_CB_name_CB_STRUCT_aerien='CB_STRUCT_aerien'

	#Function pour la recuperation de mon code_parametre en fonction de mon fichier de parametrage
	def get_field_name(name_attribut,shape_name):
		field_name=''
		#prov = processing.getObject(shape_name).dataProvider()
		field_names_shape = [field.name() for field in shape_name.pendingFields()]
		for field_ref in list_file_con:
			for field_shape in field_names_shape:
				#if field_shape == field_ref[2]: #feat[1] == nom dattribut du shape dans le fichier de conf
				if field_ref[1] == name_attribut: #feat[4] == code du nom dattribut du shape dans le fichier de conf
						field_name=field_ref[2]
		return field_name


	shape_cables_Nom_Colonne_TYPE_FONC=get_field_name(shape_CB_name_CB_TYPE_FONC,shape_cables)#TYPE_FONC
	shape_cables_Nom_Colonne_Type_STRUC=get_field_name(shape_CB_name_CB_STRUCT,shape_cables)#STRUCT_CB
	shape_cables_TYPE_FONC_Transport_valeur=get_field_name(shape_CB_name_CB_TYPE_FONC_Transport,shape_cables)#CDI
	shape_cables_Type_STRUC_conduite_valeur=get_field_name(shape_CB_name_CB_STRUCT_conduite,shape_cables)#CND
	shape_cables_Type_STRUC_aerien_valeur=get_field_name(shape_CB_name_CB_STRUCT_aerien,shape_cables)#AER


	Nom_Colonne_modulo='modulo'
	Nom_concate_ref_mod='MOD'
	Nom_Colonne_ref_modulo='ref_mod'
	Nom_Colonne_capacite_cable='capacitee'


	def ajout_champs(shape_cables,Nom_Colonne_modulo,Nom_Colonne_ref_modulo):
		

		layershape_cables = shape_cables

		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_cable=[]
		for k in layershape_cables.dataProvider().fields():
			nom_champs_cable.append(k.name()) 
		if  (Nom_Colonne_modulo not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_modulo,QVariant.Int)])
		if  (Nom_Colonne_ref_modulo not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_ref_modulo,QVariant.String)])

		layershape_cables.updateFields()
		layershape_cables.commitChanges()

	ajout_champs(shape_cables,Nom_Colonne_modulo,Nom_Colonne_ref_modulo)

	#Partie pour le calcul du modulo ainsi que la reference du modulo
	#Parti fonction pour le calcul modulo
	def Calculmodulo_12(nbrFU) :
		if (nbrFU >= 72 and nbrFU <= 720):
			return 12
		return -1
			
	def Calculmodulo_06(nbrFU) :
		if (nbrFU >= 6 and nbrFU <= 96):
			return 6
		return -1

	def Calculmodulo(nbrFU) :
		if (nbrFU >= 6 and nbrFU <= 96):
			return 6
		if (nbrFU >= 72 and nbrFU <= 720):
			return 12
		return -1

	def calcul_modulo_cable(shape_cables,shape_cables_Nom_Colonne_TYPE_FONC,shape_cables_TYPE_FONC_Transport_valeur,Nom_Colonne_capacite_cable,Nom_concate_ref_mod,shape_cables_Nom_Colonne_Type_STRUC,shape_cables_Type_STRUC_aerien_valeur,shape_cables_Type_STRUC_conduite_valeur,Nom_Colonne_modulo,Nom_Colonne_ref_modulo):
		
		layershape_cables = shape_cables
		idx_modulo= layershape_cables.fieldNameIndex(Nom_Colonne_modulo)
		idx_ref_modulo= layershape_cables.fieldNameIndex(Nom_Colonne_ref_modulo)

		layershape_cables.startEditing()  
		for shape_cables in layershape_cables.getFeatures():
			#pour le transport
			if shape_cables[shape_cables_Nom_Colonne_TYPE_FONC] == shape_cables_TYPE_FONC_Transport_valeur:
				#a= 'MODULO:'+str(12), ';','REFERNCE:'+str(shape_cables[Nom_Colonne_capacite_cable])+'MOD'+str(12)
				layershape_cables.changeAttributeValue(shape_cables.id(),idx_modulo,Calculmodulo_12(shape_cables[Nom_Colonne_capacite_cable]))
				layershape_cables.changeAttributeValue(shape_cables.id(),idx_ref_modulo,unicode(str(shape_cables[Nom_Colonne_capacite_cable])+Nom_concate_ref_mod+str(Calculmodulo_12(shape_cables[Nom_Colonne_capacite_cable]))))
			
			#pour autres  dont la capacite est entre (6 et 96)  et (96 et 720) avec le type == CONDUITE
			if shape_cables[shape_cables_Nom_Colonne_TYPE_FONC] != shape_cables_TYPE_FONC_Transport_valeur and (shape_cables[shape_cables_Nom_Colonne_Type_STRUC] == shape_cables_Type_STRUC_aerien_valeur):
					layershape_cables.changeAttributeValue(shape_cables.id(),idx_modulo,Calculmodulo(shape_cables[Nom_Colonne_capacite_cable]))
					layershape_cables.changeAttributeValue(shape_cables.id(),idx_ref_modulo,unicode(str(shape_cables[Nom_Colonne_capacite_cable])+Nom_concate_ref_mod+str(Calculmodulo(shape_cables[Nom_Colonne_capacite_cable]))))
					
			#pour autres  dont la capacite est entre (6 et 96)  et (96 et 720)  avec le type ==  AERIEN 
			if shape_cables[shape_cables_Nom_Colonne_TYPE_FONC] != shape_cables_TYPE_FONC_Transport_valeur and (shape_cables[shape_cables_Nom_Colonne_Type_STRUC] == shape_cables_Type_STRUC_conduite_valeur):
					layershape_cables.changeAttributeValue(shape_cables.id(),idx_modulo,Calculmodulo(shape_cables[Nom_Colonne_capacite_cable]))
					layershape_cables.changeAttributeValue(shape_cables.id(),idx_ref_modulo,unicode(str(shape_cables[Nom_Colonne_capacite_cable])+Nom_concate_ref_mod+str(Calculmodulo(shape_cables[Nom_Colonne_capacite_cable]))))
					

		layershape_cables.commitChanges()


	calcul_modulo_cable(shape_cables,shape_cables_Nom_Colonne_TYPE_FONC,shape_cables_TYPE_FONC_Transport_valeur,Nom_Colonne_capacite_cable,Nom_concate_ref_mod,shape_cables_Nom_Colonne_Type_STRUC,shape_cables_Type_STRUC_aerien_valeur,shape_cables_Type_STRUC_conduite_valeur,Nom_Colonne_modulo,Nom_Colonne_ref_modulo)

