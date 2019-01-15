import processing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *


def Calcul_mode_pose_cable_function(shape_cables,shape_support,Fichier_CONF_PYTHON):
	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_SECTION='CB_SECTION'
	shape_CB_name_CM_MODE_POSE='CM_MODE_POSE'

	#Declaration des noms des entites
	shape_CM_name_CM_MODE_POSE_AER='CM_MODE_POSE_AER'
	shape_CM_name_CM_MODE_POSE_SOUT='CM_MODE_POSE_SOUT'
	shape_CM_name_CM_MODE_POSE_IMB='CM_MODE_POSE_IMB'
	shape_CM_name_CM_MODE_POSE_FAC='CM_MODE_POSE_FAC'

	#Nom de colonne a ajouter
	Nom_Colonne_modepose_section='MDP_CB_SEC'
	Nom_Colonne_modepose_troncon='MDP_CB_CAB'

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

	#Recuperation des noms attributs et entites dans le fichier de conf
	shape_cables_Nom_Colonne_Nom=get_field_name(shape_CB_name_CB_NOM,shape_cables)#CODE_CB
	Nom_Colonne_CB_SECTION=get_field_name(shape_CB_name_CB_SECTION,shape_cables)

	Nom_Colonne_CM_MODE_POSE=get_field_name(shape_CB_name_CM_MODE_POSE,shape_support)
	shape_support_Nom_CM_TYPE_INF_FAC=get_field_name(shape_CM_name_CM_MODE_POSE_FAC,shape_support)
	shape_support_Nom_CM_TYPE_INF_SOUT=get_field_name(shape_CM_name_CM_MODE_POSE_SOUT,shape_support)
	shape_support_Nom_CM_TYPE_INF_AER=get_field_name(shape_CM_name_CM_MODE_POSE_AER,shape_support)
	shape_support_Nom_CM_TYPE_INF_IMB=get_field_name(shape_CM_name_CM_MODE_POSE_IMB,shape_support)


	layershape_cables =  shape_cables
	layershape_support= shape_support

	#Ajout des attributs dans le shape
	def ajout_champs():
		
		#layershape_pbo = processing.getObject(shape_pbo)
		#layershape_cables = processing.getObject(shape_cables)

		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_cable=[]
		for k in layershape_cables.dataProvider().fields():
			nom_champs_cable.append(k.name()) 
		if  (Nom_Colonne_modepose_section not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_modepose_section,QVariant.String)])
		if  (Nom_Colonne_modepose_troncon not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_modepose_troncon,QVariant.String)])
		

		layershape_cables.updateFields()
		layershape_cables.commitChanges()

	def calcul_mode_pode():
		
		AERIEN='AERIEN'
		SOUTERRAIN='SOUTERRAIN'
		FACADE='FACADE'
		IMMEUBLE='IMMEUBLE'
		
		CONDUITE='CONDUITE'



		
		#Declaration de lindex de lattribut a ajouter
		indexe_mode_pose_section_cable=layershape_cables.fieldNameIndex(Nom_Colonne_modepose_section)
		indexe_mode_pose_troncon_cable=layershape_cables.fieldNameIndex(Nom_Colonne_modepose_troncon)
		list_cable_support=[]

		for cable in layershape_cables.getFeatures():
			geom_cable=cable.geometry()
			bboxinfra = geom_cable.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxinfra)
			
			for support in layershape_support.getFeatures(request):
				geom_support=support.geometry()
				if geom_support.within(geom_cable.buffer(0.1,0.1)):
					#print cable[0],';',cable['SECTION'],';',support[0],';',support['TYPE_INFRA']
					#Prendre que les sections 
					#if cable[Nom_Colonne_CB_SECTION] != NULL:
					list_cable_support.append([cable[Nom_Colonne_CB_SECTION],support[Nom_Colonne_CM_MODE_POSE],cable[shape_cables_Nom_Colonne_Nom],-1,-1])

		#Section
		dict_section_mode_pose2 = {}
		dict_troncon_mode_pose = {}
		for line in list_cable_support:
			if line[0] in dict_section_mode_pose2:
				# append the new number to the existing array at this slot
				dict_section_mode_pose2[line[0]].append(line[1])
			elif line[0] not in dict_section_mode_pose2:
				dict_section_mode_pose2[line[0]] = [line[1]]
			
			#Mode_pose_troncon
			if line[2] in dict_troncon_mode_pose:
				# append the new number to the existing array at this slot
				dict_troncon_mode_pose[line[2]].append(line[1])
			elif line[2] not in dict_troncon_mode_pose:
				# create a new array in this slot
				dict_troncon_mode_pose[line[2]] = [line[1]]


		for j,shape_cables in enumerate(list_cable_support):
			mode_pose_section='-1'#structure du cable
			mode_pose_troncon='-1'#mode_pose_troncon
			for key, value in dict_section_mode_pose2.items():
				if key == shape_cables[0]:
					#print shape_cables[0],';',value,';',shape_support_Nom_CM_TYPE_INF_AER,';',shape_support_Nom_CM_TYPE_INF_IMB
					#Mode_pose_section
					if shape_support_Nom_CM_TYPE_INF_IMB in value:
						mode_pose_section=IMMEUBLE
					if shape_support_Nom_CM_TYPE_INF_AER in value and shape_support_Nom_CM_TYPE_INF_IMB not in value :
						mode_pose_section=AERIEN
					if (shape_support_Nom_CM_TYPE_INF_SOUT in value or shape_support_Nom_CM_TYPE_INF_FAC in value) and (shape_support_Nom_CM_TYPE_INF_AER not in value and shape_support_Nom_CM_TYPE_INF_IMB not in value):
						mode_pose_section=CONDUITE
					
			#Mode_pose_troncon
			for key, value in dict_troncon_mode_pose.items():
				if key == shape_cables[2]:
					if shape_support_Nom_CM_TYPE_INF_IMB in value:
						mode_pose_troncon=IMMEUBLE
					if shape_support_Nom_CM_TYPE_INF_FAC in value and shape_support_Nom_CM_TYPE_INF_IMB not in value:
						mode_pose_troncon=FACADE
					if shape_support_Nom_CM_TYPE_INF_AER in value and shape_support_Nom_CM_TYPE_INF_FAC not in value and shape_support_Nom_CM_TYPE_INF_IMB not in value:
						mode_pose_troncon=AERIEN
					if shape_support_Nom_CM_TYPE_INF_SOUT in value and (shape_support_Nom_CM_TYPE_INF_AER not in value and shape_support_Nom_CM_TYPE_INF_FAC not in value and shape_support_Nom_CM_TYPE_INF_IMB not in value):
						mode_pose_troncon=SOUTERRAIN
					
			#if mode_pose_section != '':
			shape_cables[3]=mode_pose_section
			#if mode_pose_troncon != '':
			shape_cables[4]=mode_pose_troncon
			#print shape_cables[0],';',mode_pose_troncon
			
			#print shape_cables[0],';',shape_cables[2],';',shape_cables[3],';',shape_cables[4]

		layershape_cables.startEditing()    

		for shape_cables in layershape_cables.getFeatures():
			for list_mdps in list_cable_support:
				#print list_mdps[0],';',list_mdps[1],';',list_mdps[2],';',list_mdps[3]
				if  list_mdps[2] == shape_cables[shape_cables_Nom_Colonne_Nom]:
					#print list_mdps[0],';',list_mdps[1],';',list_mdps[2],';',list_mdps[3]
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_mode_pose_section_cable,list_mdps[3])
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_mode_pose_troncon_cable,list_mdps[4])
					
						
		layershape_cables.commitChanges()

	#Execution de la fonction ajout des champs
	ajout_champs()
	#Execution de la fonction calcul du mode de pose
	calcul_mode_pode()