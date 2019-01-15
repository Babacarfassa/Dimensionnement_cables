import processing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
from collections import Counter

def Calcul_nombre_cables_support_function(shape_cables,shape_infra,Fichier_CONF_PYTHON):
	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_CB_name_CB_CAPACITE='CB_CAPACITE'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CM_name_CM_NOM='CM_NOM'
	shape_CM_name_CM_COMPOSITION='CM_COMPOSITION'
	#Declaration des noms des entites


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


	shape_cables_Nom_Colonne_capacite=get_field_name(shape_CB_name_CB_CAPACITE,shape_cables)#capacitee
	shape_cables_Nom_Colonne_Nom=get_field_name(shape_CB_name_CB_NOM,shape_cables)#CODE_CB
	shape_infra_Nom_Colonne_Nom=get_field_name(shape_CM_name_CM_NOM,shape_infra)#CODE_INF
	shape_infra_Nom_Colonne_Composition=get_field_name(shape_CM_name_CM_COMPOSITION,shape_infra)#TYPE_FX

	nombre_cable='nbre_Cable'
	capacite_cable='capa_cable'

	def ajout_champs(shape_infra,nombre_cable,capacite_cable):
		
		layershape_infra = shape_infra
	
		#Partie des colonnes a ajouter  dans le shapefile Infra
		nom_champs_infra=[]
		for i in layershape_infra.dataProvider().fields():
			nom_champs_infra.append(i.name())
		if (nombre_cable not in nom_champs_infra):
			layershape_infra.dataProvider().addAttributes([QgsField(nombre_cable,QVariant.Int)])
		if (capacite_cable not in nom_champs_infra):
			layershape_infra.dataProvider().addAttributes([QgsField(capacite_cable,QVariant.String)])
		layershape_infra.updateFields()
		layershape_infra.commitChanges()

	ajout_champs(shape_infra,nombre_cable,capacite_cable)

	#Description : Cette partie du script permet de calculer le nombre de shape_cables que contient un shape_infra. On part du principe que les shape_cables doivent etre exactement superposes avec les shape_infra ( ou avec une tolerance de 5cm). Partant de cette superposition, on creee un buffer au tout des shape_infras et on calcule le pourcentage dinteresction de la longueur du cable par rapport au buffer sur lshape_infra  pour nen supprimer les intersections entre les extremites et nen garder que les troncons de shape_cables qui ont un porurcentage dinteresection differente de celles des extremites. 


	def shape_infra_cable(shape_cables,shape_infra,shape_cables_Nom_Colonne_capacite,shape_cables_Nom_Colonne_Nom,shape_infra_Nom_Colonne_Nom,shape_infra_Nom_Colonne_Composition):
		
		'''nom_fichier_cable_shape_infra=QFileDialog.getSaveFileName(caption=QCoreApplication.translate("Save node layer as","Save nodes layer as"),directory=os.getcwd(),filter="CSV file (*.csv)")
		
		nombre_shape_cables_shape_infra= open(nom_fichier_cable_shape_infra, 'w')'''
		
		layershape_cables = shape_cables
		layershape_infra = shape_infra
		
		indexe_Attribut_nombre_cable=layershape_infra.fieldNameIndex(nombre_cable)
		indexe_Attribut_capacite_cable=layershape_infra.fieldNameIndex(capacite_cable)

		#list_shape_infra = [feat for feat in layershape_infra.getFeatures()]
		#list_shape_cables = [feat for feat in layershape_cables.getFeatures()]

		layershape_infra.startEditing()
		
		for shape_infra in layershape_infra.getFeatures():

			list_shape_cables_shape_infra = []
			shape_infra_dict = defaultdict(list)
			count_cable = 0
			bboxshape_infra = shape_infra.geometry().buffer(1, 1).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxshape_infra)
			#print shape_cables.geometry().union(shape_cables.geometry())
			for shape_cables in layershape_cables.getFeatures(request):
				a=shape_cables
				if shape_infra.geometry().buffer(0.1, 0.1).intersects(shape_cables.geometry()):
					geom = shape_infra.geometry().buffer(0.1, 0.1).intersection(shape_cables.geometry())
					
					#calcul dun pourcentage dintersection
					if (geom.length()/shape_cables.geometry().length())*100 >= 6:
						count_cable += 1
						shape_infra_dict[shape_infra[shape_infra_Nom_Colonne_Nom]].append(shape_cables[shape_cables_Nom_Colonne_capacite])
						list_shape_cables_shape_infra.append([shape_cables[shape_cables_Nom_Colonne_Nom],shape_cables[shape_cables_Nom_Colonne_capacite],shape_infra[shape_infra_Nom_Colonne_Nom],shape_infra[shape_infra_Nom_Colonne_Composition]])
						
			for key, value in shape_infra_dict.items():
				#nbre_shape_cables=sum(1 for v in value if v)
				if key == shape_infra[shape_infra_Nom_Colonne_Nom]:
					counts= Counter(value)
					print_counts = [str(i).replace(',',' x') for i in counts.items()]
					#print key,';',count_cable,';',print_counts
					layershape_infra.changeAttributeValue(shape_infra.id(),indexe_Attribut_nombre_cable, count_cable)
					layershape_infra.changeAttributeValue(shape_infra.id(),indexe_Attribut_capacite_cable, unicode(print_counts))
				#print (key, nbre_shape_cables,counts,value)
				#print shape_infra['COMPOSITIO'],';',key,';',count_cable,';',[i  for i in counts.items() if i]
				#print key,';',count_cable,';',print_counts,';',shape_infra[shape_infra_Nom_Colonne_Composition]
				'''msgout_rentr = "%s; %s; %s; %s\n" % (key,count_cable,print_counts,shape_infra[shape_infra_Nom_Colonne_Composition])
				unicode_message_rentr = msgout_rentr.encode('utf-8')
				nombre_shape_cables_shape_infra.write(unicode_message_rentr)'''
				
				'''for shape_infra_cable in list_shape_cables_shape_infra:
					if key == shape_infra_cable[2]:
						a= shape_infra['COMPOSITIO'],';',key,';',count_cable,';',[i  for i in counts.items() if i]'''
		layershape_infra.commitChanges()

			

	shape_infra_cable(shape_cables,shape_infra,shape_cables_Nom_Colonne_capacite,shape_cables_Nom_Colonne_Nom,shape_infra_Nom_Colonne_Nom,shape_infra_Nom_Colonne_Composition)