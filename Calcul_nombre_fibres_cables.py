import processing, xlrd
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
from collections import Counter

def Calcul_nombre_fibres_cables_function(shape_pbo,shape_cables,Fichier_CONF_PYTHON):
	#shape_cables_Nom_Colonne_Nom=string=CODE_CB
	#shape_cables_Nom_Origine_Depart_Valeur=string=TC-ST-BELL0101
	#shape_pbo_Nom_Colonne_Nom=string=CODE_BPE

	#Nom_Colonne_Origine_cable='originee'
	#Nom_Colonne_cable_Extremite='extremitee'

	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	# Recuperation de la colonne des capacites des cables dans le fichier de configuration
	wb = xlrd.open_workbook(Fichier_CONF_PYTHON)
	sh = wb.sheet_by_name('capacite_cable')#Nom de la feuille pour les capacites  possibles des cables
	colonne_capacite_possible= sh.col_values(0)
	colonne_capacite_possible_brassage= sh.col_values(1)

	#shape_cables_Nom_Colonne_Nom=string=CODE_CB
	#shape_cables_Nom_Origine_Depart_Valeur=string=TC-ST-BELL0101
	#shape_pbo_Nom_Colonne_Nom=string=CODE_BPE

	#Nom_Colonne_Origine_cable='originee'
	#Nom_Colonne_cable_Extremite='extremitee'

	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_BP_name_BP_NOM='BP_NOM'
	shape_BP_name_BP_Brassage='BP_BRASSAGE'
	shape_BP_name_BP_BRASSAGE_OUI='BP_BRASSAGE_OUI'
	shape_BP_name_BP_BRASSAGE_NON='BP_BRASSAGE_NON'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_Origine='CB_Origine'
	shape_CB_name_CB_Extremite='CB_Extremite'
	#Declaration des noms des entites
	shape_CB_name_CB_Origine_SRO='CB_Origine_SRO'

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
	shape_cables_Nom_Origine_Depart_Valeur=get_field_name(shape_CB_name_CB_Origine_SRO,shape_cables)#TC-ST-BELL0101
	shape_pbo_Nom_Colonne_Nom=get_field_name(shape_BP_name_BP_NOM,shape_pbo)#CODE_BPE
	shape_pbo_Nom_Colonne_BP_Brassage=get_field_name(shape_BP_name_BP_Brassage,shape_pbo)#CODE_BPE
	shape_pbo_Nom_Colonne_BP_BRASSAGE_OUI=get_field_name(shape_BP_name_BP_BRASSAGE_OUI,shape_pbo)
	shape_pbo_Nom_Colonne_BP_BRASSAGE_NON=get_field_name(shape_BP_name_BP_BRASSAGE_NON,shape_pbo)
	Nom_Colonne_Origine_cable=get_field_name(shape_CB_name_CB_Origine,shape_cables)#'originee'
	Nom_Colonne_cable_Extremite=get_field_name(shape_CB_name_CB_Extremite,shape_cables)#'extremitee'


	Nom_Colonne_Nbre_FO_Util='nbrfo_sum' 
	Nom_Colonne_Nbre_FO_Reel='nbrfo_capa'
	Nom_Colonne_Nbre_Log='nbrloge'
	Nom_Colonne_Nbre_FO='nbrfo_mod'
	Nom_Colonne_Nbre_FO_sans_Modulo='nbrfo'
	Nom_Colonne_cable_utilisation='%_CB_Util'
	Nom_Colonne_SUM_Nbre_FO_sans_Modulo='%nbrfo_sum'
	Nom_Colonne_SUM_Nbre_FO_Brassage='nbrfo_Bras'
	Nom_Colonne_capacite_theorique='capa_theo'


	layershape_pbo = shape_pbo#processing.getObject(shape_pbo)
	layershape_cables = shape_cables#processing.getObject(shape_cables)

	def ajout_champs(layershape_pbo,layershape_cables,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel):
		
		#layershape_pbo = processing.getObject(shape_pbo)
		#layershape_cables = processing.getObject(shape_cables)

		#Partie des colonnes a ajouter  dans le shapefile shape_pbo
		nom_champs_shape_pbo=[]
		for j in layershape_pbo.dataProvider().fields():
			nom_champs_shape_pbo.append(j.name()) 
		if (Nom_Colonne_Nbre_FO_Util not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Util,QVariant.String)])
		if (Nom_Colonne_Nbre_FO_Reel not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Reel,QVariant.String)])
		if (Nom_Colonne_SUM_Nbre_FO_sans_Modulo not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_SUM_Nbre_FO_sans_Modulo,QVariant.String)])
		if (Nom_Colonne_SUM_Nbre_FO_Brassage not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_SUM_Nbre_FO_Brassage,QVariant.String)])
		layershape_pbo.updateFields()
		layershape_pbo.commitChanges()


		#Partie des colonnes a ajouter  dans le shapefile Cable
		nom_champs_cable=[]
		for k in layershape_cables.dataProvider().fields():
			nom_champs_cable.append(k.name()) 
		if  (Nom_Colonne_Nbre_FO_Util not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Util,QVariant.String)])
		if  (Nom_Colonne_Nbre_FO_Reel not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Reel,QVariant.Int)])
		if  (Nom_Colonne_cable_utilisation not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_cable_utilisation,QVariant.Int)])
		if  (Nom_Colonne_Nbre_Log not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log,QVariant.String)])
		if  (Nom_Colonne_SUM_Nbre_FO_sans_Modulo not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_SUM_Nbre_FO_sans_Modulo,QVariant.String)])
		if  (Nom_Colonne_SUM_Nbre_FO_Brassage not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_SUM_Nbre_FO_Brassage,QVariant.String)])
		if  (Nom_Colonne_capacite_theorique not in nom_champs_cable) :
			layershape_cables.dataProvider().addAttributes([QgsField(Nom_Colonne_capacite_theorique,QVariant.String)])

		layershape_cables.updateFields()
		layershape_cables.commitChanges()

	#Execution de la fonction ajout des champs
	ajout_champs(layershape_pbo,layershape_cables,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel)

	listorigine_extremite_cable=[]
	list_synoptique_cable=[]
	def SommeFibBesoinRec(noeud, niveau) :
		
		somme_fo = 0
		nbre_prise = 0
		somme_fo_sans_modulo = 0 #nombre de fo sans le modulo
		
		if niveau < 1000:
			#print "debut sommefib " + noeud
			for shape_cables in listshape_cables:
				if shape_cables[1] == noeud:
					somme_fo_aval, nbre_prises_aval,somme_fo_SM= SommeFibBesoinRec(shape_cables[2],niveau + 1)
					#print somme_fo_aval,';',nbre_prises_aval
					somme_fo= (somme_fo) + (somme_fo_aval)
					nbre_prise =(nbre_prise) + (nbre_prises_aval)
					somme_fo_sans_modulo=(somme_fo_sans_modulo)+(somme_fo_SM)
					#print somme_fo,';',nbre_prise
			listorigine_extremite_cable.append(noeud)
			for shape_pbo in listshape_pbo:
				if shape_pbo[0]== noeud:
					if shape_pbo[1] != NULL:
						nbre_prise = (nbre_prise) + float(shape_pbo[3])   
						somme_fo = (somme_fo) + float(shape_pbo[1] )   
						if shape_pbo[5] != NULL:
							somme_fo_sans_modulo = (somme_fo_sans_modulo) + float(shape_pbo[5] )  
					shape_pbo[2] = somme_fo
					shape_pbo[4] = nbre_prise
					shape_pbo[6] = (somme_fo_sans_modulo)
					if shape_pbo[7] ==shape_pbo_Nom_Colonne_BP_BRASSAGE_OUI: #SI Brassage alors on remonte nbrfo avec modulo
						shape_pbo[8]=somme_fo_sans_modulo
					elif shape_pbo[7] ==shape_pbo_Nom_Colonne_BP_BRASSAGE_NON: #Si pas de brassage on remonte nbro sans modulo
						shape_pbo[8]=somme_fo
					
					
						
		
		#print somme_fo, nbre_prise,somme_fo_sans_modulo
		return somme_fo, nbre_prise,somme_fo_sans_modulo
			
		return 0,0
		


	listshape_cables = []
	for shape_cables in layershape_cables.getFeatures():
		cable = [shape_cables[shape_cables_Nom_Colonne_Nom],shape_cables[Nom_Colonne_Origine_cable],shape_cables[Nom_Colonne_cable_Extremite]]
		listshape_cables.append(cable)
	listshape_pbo = []
	for shape_pbos in layershape_pbo.getFeatures():
		shape_pbo = [shape_pbos[shape_pbo_Nom_Colonne_Nom],shape_pbos[Nom_Colonne_Nbre_FO],-1,shape_pbos[Nom_Colonne_Nbre_Log],-1,shape_pbos[Nom_Colonne_Nbre_FO_sans_Modulo],-1,shape_pbos[shape_pbo_Nom_Colonne_BP_Brassage],-1]
		listshape_pbo.append(shape_pbo)



	#Fonction pour le calcul des capacites reelles en fonction dune liste de valeur des capacites possibles dans le fichier de configuration
	def CalculCapa(liste_capa_cable, nbrFU) :
		for fo_list in liste_capa_cable:
			if (int(nbrFU) <= fo_list):
				return int(fo_list)
		return 999999


	'''
	#Fonction pour le calcul des capacites reelles
	def CalculCapa(nbrFU) :
		if (nbrFU <= 6):
			return 6
		if (nbrFU <= 12):
			return 12
		if (nbrFU <= 24):
			return 24
		if (nbrFU <= 36):
			return 36
		if (nbrFU <= 48):
			return 48
		if (nbrFU <= 72):
			return 72
		if (nbrFU <= 96):
			return 96
		if (nbrFU <= 144):
			return 144
		if (nbrFU <= 288):
			return 288
		if (nbrFU <= 576):
			return 576
		if (nbrFU <= 720):
			return 720
		if (nbrFU <= 864):
			return 864
			
		return 999999

	#Fonction pour le calcul des capacites en fonction du brassage
	def CalculCapa_brassage(nbrFU) :
		if (nbrFU <= 12):
			return 12
		if (nbrFU <= 24):
			return 24
		if (nbrFU <= 36):
			return 36
		if (nbrFU <= 48):
			return 48
		if (nbrFU <= 72):
			return 72
		if (nbrFU <= 96):
			return 96
		if (nbrFU <= 144):
			return 144
		if (nbrFU <= 288):
			return 288
		if (nbrFU <= 432):
			return 432
		if (nbrFU <= 576):
			return 576
		if (nbrFU <= 720):
			return 720
		if (nbrFU <= 864):
			return 864
			
		return 999999'''

	def ajout_nbre_FO_shape_cables_Boites_Sommes(Nom_Colonne_cable_Extremite,shape_pbo_Nom_Colonne_Nom,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel,Nom_Colonne_Nbre_Log):
		
		#layershape_pbo = processing.getObject(shape_pbo)
		#layershape_cables = processing.getObject(shape_cables)
		
		idfosum_cable=layershape_cables.fieldNameIndex(Nom_Colonne_Nbre_FO_Util)
		idfocapa_cable=layershape_cables.fieldNameIndex(Nom_Colonne_Nbre_FO_Reel)
		id_sum_nbrfo_sans_modulo_shape_cable=layershape_cables.fieldNameIndex(Nom_Colonne_SUM_Nbre_FO_sans_Modulo)
		id_sum_nbrfo_brassage_shape_cable=layershape_cables.fieldNameIndex(Nom_Colonne_SUM_Nbre_FO_Brassage)
		id_capacite_theorique=layershape_cables.fieldNameIndex(Nom_Colonne_capacite_theorique)
		idfo_cable_Nbre_Log=layershape_cables.fieldNameIndex(Nom_Colonne_Nbre_Log)
		idfosum_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_FO_Util)
		idfocapa_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_FO_Reel)
		id_sum_nbrfo_sans_modulo_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_SUM_Nbre_FO_sans_Modulo)
		id_sum_nbrfo_brassage_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_SUM_Nbre_FO_Brassage)
		indexe_cable_utilisation_pourcent=layershape_cables.fieldNameIndex(Nom_Colonne_cable_utilisation)
		
		layershape_cables.startEditing()           
		layershape_pbo.startEditing()
		
		for shape_cables in layershape_cables.getFeatures():
			for shape_pbo in listshape_pbo:
				if shape_cables[Nom_Colonne_cable_Extremite] == shape_pbo[0]:
					#print shape_pbo[0]
					#Calcul et modifier pour prendre en compte les capacites possibles sur les shape_cables
					layershape_cables.changeAttributeValue(shape_cables.id(),idfosum_cable,shape_pbo[2])
					layershape_cables.changeAttributeValue(shape_cables.id(),idfocapa_cable,CalculCapa(colonne_capacite_possible,shape_pbo[2]))
					#if shape_pbo[5] !='PEC':
					layershape_cables.changeAttributeValue(shape_cables.id(),idfo_cable_Nbre_Log,shape_pbo[4])
					layershape_cables.changeAttributeValue(shape_cables.id(),id_sum_nbrfo_sans_modulo_shape_cable,shape_pbo[6])
					layershape_cables.changeAttributeValue(shape_cables.id(),id_sum_nbrfo_brassage_shape_cable,shape_pbo[8])
					layershape_cables.changeAttributeValue(shape_cables.id(),id_capacite_theorique,CalculCapa(colonne_capacite_possible_brassage,shape_pbo[8]))
						#print 'Babab'
					#layershape_cables.changeAttributeValue(shape_cables.id(),indexe_cable_utilisation_pourcent,(float(shape_pbo[2])/CalculCapa(colonne_capacite_possible,shape_pbo[2]))*100)
					#print (shape_pbo[2]),';',CalculCapa(shape_pbo[2]),';',(float(shape_pbo[2])/CalculCapa(shape_pbo[2]))*100
					#TODO Ajouter le champ capa / fibre utile
		for shape_pbos in layershape_pbo.getFeatures():
			for shape_pbo in listshape_pbo:
				if shape_pbos[shape_pbo_Nom_Colonne_Nom] == shape_pbo[0]:
					layershape_pbo.changeAttributeValue(shape_pbos.id(),idfosum_shape_pbo, shape_pbo[2])
					layershape_pbo.changeAttributeValue(shape_pbos.id(),idfocapa_shape_pbo, CalculCapa(colonne_capacite_possible,shape_pbo[2]))
					layershape_pbo.changeAttributeValue(shape_pbos.id(),id_sum_nbrfo_sans_modulo_shape_pbo, shape_pbo[6])
					layershape_pbo.changeAttributeValue(shape_pbos.id(),id_sum_nbrfo_brassage_shape_pbo, shape_pbo[8])
				
		layershape_cables.commitChanges()
		layershape_pbo.commitChanges()

	#Partie verification que toutes les boites correspodants aux origines et exremites des shape_cables sont parcours
	def verif_noeud_parcouru (shape_pbo_Nom_Colonne_Nom,listorigine_extremite_cable):
		
		#layershape_pbo = processing.getObject(shape_pbo)
		
		shape_pbo_non_parcouru = QgsVectorLayer("Point?crs=epsg:2154", "shape_pbo_non_parcouru", "memory")
		shape_pbo_pr2 = shape_pbo_non_parcouru.dataProvider()
		shape_pbo_attr2 = layershape_pbo.dataProvider().fields().toList()
		shape_pbo_pr2.addAttributes(shape_pbo_attr2)
		shape_pbo_non_parcouru.updateFields()

		for shape_pbo in layershape_pbo.getFeatures():
			if shape_pbo[shape_pbo_Nom_Colonne_Nom] not in listorigine_extremite_cable:
				shape_pbo_pr2.addFeatures([shape_pbo]) 
		QgsMapLayerRegistry.instance().addMapLayer(shape_pbo_non_parcouru)

	#Executtion de la fonction parcours
	SommeFibBesoinRec(shape_cables_Nom_Origine_Depart_Valeur,1)

	#Execution de la fonction verification des noeuds non parcouru
	verif_noeud_parcouru (shape_pbo_Nom_Colonne_Nom,listorigine_extremite_cable)

	#Execution de la fonction recalcul des capacites reelles des shape_cables et boites
	ajout_nbre_FO_shape_cables_Boites_Sommes(Nom_Colonne_cable_Extremite,shape_pbo_Nom_Colonne_Nom,Nom_Colonne_Nbre_FO_Util,Nom_Colonne_Nbre_FO_Reel,Nom_Colonne_Nbre_Log)