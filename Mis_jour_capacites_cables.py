import processing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
from collections import Counter



def Mis_jour_capacites_cables_function(shape_pbo,shape_cables,Fichier_CONF_PYTHON):
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_BP_name_BP_NOM='BP_NOM'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_SECTION='CB_SECTION'

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


	shape_cables_Nom_Colonne_Nom=get_field_name(shape_CB_name_CB_NOM,shape_cables)#CODE_CB
	shape_cables_Nom_Colonne_Section=get_field_name(shape_CB_name_CB_SECTION,shape_cables)#SECTION 
	shape_pbo_Nom_Colonne_NOM=get_field_name(shape_BP_name_BP_NOM,shape_pbo)#CODE_BPE

	Nom_Colonne_Nbre_FO_Util='nbrfo_sum'
	Nom_Colonne_Nbre_FO_Reel='nbrfo_capa' 
	Nom_Colonne_capacite_cable='capacitee'
	Nom_Colonne_Nbre_FO='nbrfo'
	Nom_Colonne_cable_utilisation='%_CB_Util'

	def ajout_champs(shape_cables,Nom_Colonne_capacite_cable,Nom_Colonne_cable_utilisation):
		
		
		layershape_cables = shape_cables


		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_cable=[]
		for k in layershape_cables.dataProvider().fields():
			nom_champs_cable.append(k.name()) 

		if  (Nom_Colonne_capacite_cable not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_capacite_cable,QVariant.Int)])
		if  (Nom_Colonne_cable_utilisation not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_cable_utilisation,QVariant.Int)])
			
		layershape_cables.updateFields()
		layershape_cables.commitChanges()

	ajout_champs(shape_cables,Nom_Colonne_capacite_cable,Nom_Colonne_cable_utilisation)

	def mise_jour_capa_reel(shape_pbo,shape_cables,shape_pbo_Nom_Colonne_NOM,shape_cables_Nom_Colonne_Section,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel,Nom_Colonne_capacite_cable,Nom_Colonne_cable_utilisation):
		
		layershape_pbo = shape_pbo
		layershape_cables = shape_cables
		
		idfocapacite_cable=layershape_cables.fieldNameIndex(Nom_Colonne_capacite_cable)
		idx_section= layershape_cables.fieldNameIndex(shape_cables_Nom_Colonne_Section)
		values_unique_section = layershape_cables.uniqueValues(idx_section)
		indexe_cable_utilisation_pourcent=layershape_cables.fieldNameIndex(Nom_Colonne_cable_utilisation)
		
		listshape_cables = []
		for shape_cables in layershape_cables.getFeatures():
			cable = [shape_cables[shape_cables_Nom_Colonne_Nom],shape_cables[shape_cables_Nom_Colonne_Section],shape_cables[Nom_Colonne_Nbre_FO_Reel],shape_cables[Nom_Colonne_Nbre_FO_Util],-1,-1]
			listshape_cables.append(cable)
		

		#Mise a jour de la capacite du cable en fonction de la section
		d1 = defaultdict(list)
		for i in values_unique_section:
			for shape_cables in listshape_cables:
			   if  shape_cables[1] == i:
				   d1[i].append(shape_cables[2])
		list_highest=[]
		for i in d1.keys():
			#while len(d1.keys()) != 0:
			#Obtenir la clee avec le maximun de valeur
			highest = max(d1, key = d1.get)
			#Afficher la clee et le maximun de valeur
			#print(highest, max(sorting[highest]))
			list_highest.append([highest,max(d1[highest])])
			del d1[highest]
			#print highest,';',max(d1[highest])    
			#del d1[highest]
		for key_highest in list_highest:
			#layershape_cables.startEditing() 
			for lis_cab in listshape_cables:
				
			#for shape_cables in layershape_cables.getFeatures():
				if lis_cab[1]  == key_highest[0]:
					lis_cab[4]=key_highest[1]
					#layershape_cables.changeAttributeValue(shape_cables.id(),idfocapacite_cable,key_highest[1])
					if lis_cab[3] != NULL:
					#if shape_cables[Nom_Colonne_Nbre_FO_Util] != NULL:
						lis_cab[5]=(float(lis_cab[3])/key_highest[1])*100
						#layershape_cables.changeAttributeValue(shape_cables.id(),indexe_cable_utilisation_pourcent,(float(shape_cables[Nom_Colonne_Nbre_FO_Util])/key_highest[1])*100)
		#layershape_cables.commitChanges()
					#print key_highest[0],';',key_highest[1]
		
		layershape_cables.startEditing() 
		for shape_cables in layershape_cables.getFeatures():
			for cable in listshape_cables:
				if shape_cables[shape_cables_Nom_Colonne_Nom]==cable[0]:
					layershape_cables.changeAttributeValue(shape_cables.id(),idfocapacite_cable,cable[4])
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_cable_utilisation_pourcent,cable[5])
		layershape_cables.commitChanges()
					

	mise_jour_capa_reel(shape_pbo,shape_cables,shape_pbo_Nom_Colonne_NOM,shape_cables_Nom_Colonne_Section,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel,Nom_Colonne_capacite_cable,Nom_Colonne_cable_utilisation)