import processing,xlrd
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import * 
from qgis.utils import *


#shape_boite=vector
#shape_cables=vector
#shape_point_technique=vector
#shape_sites=vector
#shape_support=vector





"""
shape_cable_Nom_Colonne_Nom='NOM'
shape_cable_Nom_Colonne_Origine='originee'
shape_cable_Nom_Colonne_Extremite='extremitee'
shape_cables_Nom_Origine_Depart_Valeur='N076GOD_S008'
shape_pbo_Nom_Colonne_Nom='NOM_BPE'
Nom_Colonne_SF_NOM='NOM'
Nom_Colonne_SF_ISOLE='UTILISABLE'
Nom_Colonne_SF_ISOLE_OUI='Oui'
Nom_Colonne_SF_ISOLE_NON='Non'"""


def function_isole(shape_boite,shape_point_technique,shape_support,shape_cables,shape_sites,Fichier_CONF_PYTHON):

	w = QWidget()
	succesMsg="Execution-Plugin-Fini!!!!!!!!!"

	#Creation dune liste de mon fichier de configuration
	#Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])
		

	#Declaration des noms des colonnes
	shape_BP_name_BP_NOM='BP_NOM'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_Origine='CB_Origine'
	shape_CB_name_CB_Extremite='CB_Extremite'
	shape_SF_NOM='SF_NOM'
	shape_SF_ISOLE='SF_ISOLE'
	shape_CB_Origine_SRO='CB_Origine_SRO'
	shape_SF_ISOLE_OUI='SF_ISOLE_OUI'
	shape_SF_ISOLE_NON='SF_ISOLE_NON'
			
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

	shape_pbo_Nom_Colonne_Nom=get_field_name(shape_BP_name_BP_NOM,shape_boite)#CODE_BPE
	shape_cable_Nom_Colonne_Nom=get_field_name(shape_CB_name_CB_NOM,shape_cables)#CODE_CB
	shape_cable_Nom_Colonne_Origine=get_field_name(shape_CB_name_CB_Origine,shape_cables)#'originee'
	shape_cable_Nom_Colonne_Extremite=get_field_name(shape_CB_name_CB_Extremite,shape_cables)#'extremitee'
	shape_cables_Nom_Origine_Depart_Valeur=get_field_name(shape_CB_Origine_SRO,shape_cables)#TC-ST-BELL0101
	Nom_Colonne_SF_NOM=get_field_name(shape_SF_NOM,shape_sites)
	Nom_Colonne_SF_ISOLE=get_field_name(shape_SF_ISOLE,shape_sites)
	Nom_Colonne_SF_ISOLE_OUI=get_field_name(shape_SF_ISOLE_OUI,shape_sites)
	Nom_Colonne_SF_ISOLE_NON=get_field_name(shape_SF_ISOLE_NON,shape_sites)



	Nom_Colonne_BP_ISOLE='ST_ISOLEE'

	List_attribut_Boite_ajout=Nom_Colonne_BP_ISOLE

	layershape_cables = shape_cables#processing.getObject(shape_cables)
	layershape_boite = shape_boite#processing.getObject(shape_boite)
	layershape_sites = shape_sites#processing.getObject(shape_sites)
	layershape_point_technique = shape_point_technique#processing.getObject(shape_point_technique)
	layershape_infra = shape_support#processing.getObject(shape_support)


	def delete_field(layershape_name,List_attribut):
		field_ids = []
		for field in layershape_name.fields():
			if field.name() in List_attribut:
			  field_ids.append(layershape_name.fieldNameIndex(field.name()))
		layershape_name.dataProvider().deleteAttributes(field_ids)
		layershape_name.updateFields()
		layershape_name.commitChanges()

	def ajout_champs_function(layershape_name,Name_Colonne_Shape):
		nom_champs_shape_name=[]
		for j in layershape_name.dataProvider().fields():
			nom_champs_shape_name.append(j.name()) 
		if (Name_Colonne_Shape not in nom_champs_shape_name) :
			layershape_name.dataProvider().addAttributes([QgsField(Name_Colonne_Shape,QVariant.String)])
		layershape_name.updateFields()
		layershape_name.commitChanges()


	delete_field(layershape_boite,List_attribut_Boite_ajout)
	ajout_champs_function(layershape_boite,List_attribut_Boite_ajout)

	delete_field(layershape_cables,List_attribut_Boite_ajout)
	ajout_champs_function(layershape_cables,List_attribut_Boite_ajout)

	delete_field(layershape_point_technique,List_attribut_Boite_ajout)
	ajout_champs_function(layershape_point_technique,List_attribut_Boite_ajout)

	delete_field(layershape_infra,List_attribut_Boite_ajout)
	ajout_champs_function(layershape_infra,List_attribut_Boite_ajout)

	#Decalration des indexes pour la mise a jours des statut isole dans les shapes
	indexe_BP_ISOLE=layershape_boite.fieldNameIndex(Nom_Colonne_BP_ISOLE)
	indexe_CB_ISOLE=layershape_cables.fieldNameIndex(Nom_Colonne_BP_ISOLE)
	indexe_PT_ISOLE=layershape_point_technique.fieldNameIndex(Nom_Colonne_BP_ISOLE)
	indexe_CM_ISOLE=layershape_infra.fieldNameIndex(Nom_Colonne_BP_ISOLE)

	#Deuxieme parcours pour mettre le statut isole dans cable sortant et cable rentrant

	def Est_isole(noeud, niveau) :

		if niveau < 1000:
			for shape_pbo in list_fusion_boite_sites:
				if shape_pbo[0]== noeud:
					if shape_pbo[1] != '-1': 
						shape_pbo[2] = shape_pbo[1]
						return shape_pbo[1]
					else:
						temp_isole = str(Nom_Colonne_SF_ISOLE_OUI)    
						nb_cable = 0
						for shape_cables in listshape_cables:
							if shape_cables[1] == noeud:
								nb_cable = nb_cable + 1
								boite_extremite_isolee = Est_isole(shape_cables[2],niveau + 1)
								shape_cables[3]  = boite_extremite_isolee
								if boite_extremite_isolee == str(Nom_Colonne_SF_ISOLE_NON):
									temp_isole = str(Nom_Colonne_SF_ISOLE_NON)
						if nb_cable == 0:
							shape_pbo[2] = '-2'
							return '-2'
						else:
							#print 'c est un intermediaire: '+str(noeud) + '  isole : ' + str(temp_isole)
							shape_pbo[2] = temp_isole
							return temp_isole
		return '-3','-3'


	listshape_cables = []
	for shape_cables in layershape_cables.getFeatures():
		cable = [shape_cables[shape_cable_Nom_Colonne_Nom],shape_cables[shape_cable_Nom_Colonne_Origine],shape_cables[shape_cable_Nom_Colonne_Extremite],'-1']#
		listshape_cables.append(cable)
		
	#Fusion des boites et sites pour faire le parcours des cables
	listPBO=[]
	listSITES=[]
	for pbo in layershape_boite.getFeatures():
		listPBO.append([pbo[shape_pbo_Nom_Colonne_Nom],'-1','-1'])
	for sites in layershape_sites.getFeatures():
		listSITES.append([sites[Nom_Colonne_SF_NOM],sites[Nom_Colonne_SF_ISOLE],'-1'])
	list_fusion_boite_sites=listPBO+listSITES



	#Execution de la fonction qui permet de faire le parcours et de calculer pour chaque noeud si il est isole
	Est_isole(shape_cables_Nom_Origine_Depart_Valeur,1)         

	#Mise a jour du statut isole dans les boites
	layershape_boite.startEditing()
	for boite in layershape_boite.getFeatures():
		boite_isole='-3'
		for fusion in list_fusion_boite_sites:
			if boite[shape_pbo_Nom_Colonne_Nom]==fusion[0]:
				boite_isole=fusion[2]
		layershape_boite.changeAttributeValue(boite.id(),indexe_BP_ISOLE,unicode(boite_isole))
	layershape_boite.commitChanges()


	#Mise a jour du statut isole dans les cables
	layershape_cables.startEditing()
	for shape_cables in layershape_cables.getFeatures():
		geom_cables=shape_cables.geometry()
		if geom_cables != NULL:
			bbox_cables = geom_cables.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bbox_cables)
			cable_isole='-3'
			for cable in listshape_cables:
				if shape_cables[shape_cable_Nom_Colonne_Nom] == cable[0]:
					cable_isole=cable[3]				
			
			#Mise a jour du statut isole dans les points techniques
			layershape_point_technique.startEditing()
			for shape_pt in layershape_point_technique.getFeatures(request):
				pt_isole='-3'
				res_pt_cable='KO'
				if shape_pt.geometry().within(geom_cables.buffer(0.1,0.1)):
					pt_isole=cable_isole
					res_pt_cable='OK'
				if res_pt_cable =='OK':
					
					layershape_point_technique.changeAttributeValue(shape_pt.id(),indexe_PT_ISOLE,unicode(pt_isole))
			layershape_point_technique.commitChanges()
					
			#Mise a jour du statut isole dans les supports
			layershape_infra.startEditing()
			for chem in layershape_infra.getFeatures(request):
				res = 'KO'
				cm_isole='-3'
				if chem.geometry().within(geom_cables.buffer(0.1,0.1)) :
					res = 'OK'
					cm_isole=cable_isole
				if res == 'OK':
					
					layershape_infra.changeAttributeValue(chem.id(),indexe_CM_ISOLE,unicode(cm_isole))
			layershape_infra.commitChanges()
			
						
			layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CB_ISOLE,unicode(cable_isole))
	layershape_cables.commitChanges()

	QMessageBox.information(w, "Message-Execution-Plugin", succesMsg)

	#function_isole(shape_cables,shape_boite,shape_sites,shape_point_technique,shape_support,Fichier_CONF_PYTHON)
