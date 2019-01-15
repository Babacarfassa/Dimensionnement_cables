import processing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
from collections import Counter

def Calcul_nombre_Logements_fibres_boites_ZPBO_function(shape_pbo,shape_zpbo,shape_cables,shape_sites,Fichier_CONF_PYTHON):
	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	shape_sites_SF_PRO='SF_PRO'
	shape_sites_SF_PARTICULIER='SF_PARTICULIER'
	shape_none_Mod_Calcul_FO_Sans_Arrondi='Mod_Calcul_FO_Sans_Arrondi'
	shape_none_Mod_Calcul_FO_Avec_Arrondi='Mod_Calcul_FO_Avec_Arrondi'
	shape_none_Mod_Calcul_FO_executer='Mod_Calcul_FO_executer'
	shape_boites_BP_FONCTION='BP_FONCTION'
	shape_boites_BP_FONCTION_PEC='BP_FONCTION_PEC'

	shape_none_Modulo3_entite='MODULO3'
	shape_none_Modulo6_entite='MODULO6'
	shape_none_Reserve_entite='RESERVE'
	shape_none_Multiple_Pro_FO_entite='MULTIPLE_PRO_FO'


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

	shape_sites_Colonne_Particulier=get_field_name(shape_sites_SF_PARTICULIER,shape_sites)#NB_LC_LOGT
	shape_sites_Colonne_Professionel=get_field_name(shape_sites_SF_PRO,shape_sites)#NB_LC_PRO

	shape_boite_Colonne_FONCTION=get_field_name(shape_boites_BP_FONCTION,shape_pbo)
	shape_boite_entite_PEC=get_field_name(shape_boites_BP_FONCTION_PEC,shape_pbo)

	shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi=get_field_name(shape_none_Mod_Calcul_FO_Sans_Arrondi,shape_sites)#Mod_Calcul_FO_Projet
	shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi=get_field_name(shape_none_Mod_Calcul_FO_Avec_Arrondi,shape_sites)#Mod_Calcul_FO_Projet
	shape_none_Mod_Calcul_FO_Projet_executer=get_field_name(shape_none_Mod_Calcul_FO_executer,shape_sites)#Mod_Calcul_FO_Projet_Executer

	shape_none_Modulo3=int(get_field_name(shape_none_Modulo3_entite,shape_sites))#shape_none_Modulo3_entite
	shape_none__Modulo6=int(get_field_name(shape_none_Modulo6_entite,shape_sites))#shape_none_Modulo6_entite
	shape_none_Reserve=float(get_field_name(shape_none_Reserve_entite,shape_sites))#shape_none_Reserve_entite
	shape_none_Multiple_Pro_FO=int(get_field_name(shape_none_Multiple_Pro_FO_entite,shape_sites))#shape_none_Reserve_entite
	#list_mode_calcul_fo=[shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi,shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi]


	Nom_Colonne_Nbre_Log='nbrloge'
	Nom_Colonne_Nbre_FO='nbrfo_mod'
	Nom_Colonne_Nbre_FO_sans_Modulo='nbrfo'
	Nom_Colonne_Nbre_FO_Particulier='nbrfo_Part'
	Nom_Colonne_Nbre_FO_Professionel='nbrfo_Pro'
	Nom_Colonne_Nbre_Log_Part='NB_FTTH'	
	Nom_Colonne_Nbre_Log_PRO='NB_FTTE'

	def ajout_champs(shape_pbo,shape_zpbo,shape_cables,Nom_Colonne_Nbre_Log,Nom_Colonne_Nbre_FO,Nom_Colonne_Nbre_FO_Particulier,Nom_Colonne_Nbre_FO_Professionel):
		
		layershape_pbo = shape_pbo#processing.getObject(shape_pbo)
		layershape_zpbo = shape_zpbo#processing.getObject(shape_zpbo)
		layershape_cables = shape_cables#processing.getObject(shape_cables)
		
		#Partie des colonnes a ajouter  dans le shapefile shape_zpbo
		nom_champs=[]
		for i in layershape_zpbo.dataProvider().fields():
			nom_champs.append(i.name())
		if (Nom_Colonne_Nbre_Log_Part not in nom_champs):
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log_Part,QVariant.Int)])
		if (Nom_Colonne_Nbre_Log_PRO not in nom_champs):
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log_PRO,QVariant.Int)])
		if (Nom_Colonne_Nbre_Log not in nom_champs):
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log,QVariant.Int)])
		if (Nom_Colonne_Nbre_FO not in nom_champs) :
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO,QVariant.String)])
		if (Nom_Colonne_Nbre_FO_Particulier not in nom_champs) :
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Particulier,QVariant.String)])
		if (Nom_Colonne_Nbre_FO_Professionel not in nom_champs):
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_Professionel,QVariant.String)])
		if (Nom_Colonne_Nbre_FO_sans_Modulo not in nom_champs):
			layershape_zpbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_sans_Modulo,QVariant.String)])
		layershape_zpbo.updateFields()
		layershape_zpbo.commitChanges()

		#Partie des colonnes a ajouter  dans le shapefile shape_pbo
		nom_champs_shape_pbo=[]
		for j in layershape_pbo.dataProvider().fields():
			nom_champs_shape_pbo.append(j.name()) 
		if (Nom_Colonne_Nbre_Log not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log,QVariant.String)])
		if (Nom_Colonne_Nbre_FO not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO,QVariant.String)])
		if (Nom_Colonne_Nbre_FO_sans_Modulo not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_FO_sans_Modulo,QVariant.String)])
		if (Nom_Colonne_Nbre_Log_Part not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log_Part,QVariant.String)])
		if (Nom_Colonne_Nbre_Log_PRO not in nom_champs_shape_pbo) :
			layershape_pbo.dataProvider().addAttributes([QgsField(Nom_Colonne_Nbre_Log_PRO,QVariant.String)])
		layershape_pbo.updateFields()
		layershape_pbo.commitChanges()
		

	#Fonction pour le calcul du nombre de fibre util en fonction des shape_sites individuels et collectifs

	fo_avec_reserve=shape_none_Reserve#1.20
	def CalculFoPart(nbrFU_Indi) :
		nbrFU_Individuel= (((((int((nbrFU_Indi*fo_avec_reserve)-0.01))/shape_none_Modulo3)+1)*shape_none_Modulo3))
		return nbrFU_Individuel

	def CalculFoPro(nbrFU_Colle) :
		nbrFU_Collectif=(((((int((nbrFU_Colle* shape_none_Multiple_Pro_FO *fo_avec_reserve)-0.01))/shape_none__Modulo6)+1)*shape_none__Modulo6))
		return nbrFU_Collectif
	'''
	def CalculFoPart(nbrFU_Indi) :
		nbrFU_Individuel= (((((int((nbrFU_Indi*fo_avec_reserve)-0.01))/3)+1)*3))
		return nbrFU_Individuel

	def CalculFoPro(nbrFU_Colle) :
		nbrFU_Collectif=(((((int((nbrFU_Colle*2*fo_avec_reserve)-0.01))/6)+1)*6))
		return nbrFU_Collectif'''

	def CalculFoIndiivduel_Collectif(nbrFU_Indi,nbrFU_Colle) :
		nbrFU_Indiivduel_Collectif= (nbrFU_Indi+nbrFU_Colle)*fo_avec_reserve#1.20
		return nbrFU_Indiivduel_Collectif

	def mod_calcul_NbreFo_Sans_Arrondi(mod_calcul_choisir):
		if mod_calcul_choisir == shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi:
			return shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi
			
	def mod_calcul_NbreFo_Avec_Arrondi(mod_calcul_choisir):
		if mod_calcul_choisir == shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi:
			return shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi

	def mod_a_executer(a_executer):
		if a_executer == shape_none_Mod_Calcul_FO_Projet_executer:
			return shape_none_Mod_Calcul_FO_Projet_executer

	#Calcul Nombre de Fo sans le Modulo 
	def CalculFoPart_mod(nbrFU_Indi) :
		nbrFU_Individuel= (float((nbrFU_Indi*fo_avec_reserve))) 
		return nbrFU_Individuel

	def CalculFoPro_mod(nbrFU_Colle) :
		nbrFU_Collectif=(float((nbrFU_Colle* shape_none_Multiple_Pro_FO *fo_avec_reserve)))
		return nbrFU_Collectif
		

	#Partie du calcul du nombre de logements ainsi que le nombre de fibre utile dans la shape_zpbo
	def calcul_nbre_LOG_FO(shape_pbo,shape_zpbo,shape_cables,shape_sites,Nom_Colonne_Nbre_Log,Nom_Colonne_Nbre_FO,Nom_Colonne_Nbre_FO_Particulier,Nom_Colonne_Nbre_FO_Professionel,shape_sites_Colonne_Particulier,shape_sites_Colonne_Professionel):
		
		layershape_pbo = shape_pbo#processing.getObject(shape_pbo)
		layershape_zpbo = shape_zpbo#processing.getObject(shape_zpbo)
		layershape_cables = shape_cables#processing.getObject(shape_cables)
		layershape_sites = shape_sites#processing.getObject(shape_sites)
		
		idlog_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_Log)
		idlog_Part_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_Log_Part)
		idlog_PRO_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_Log_PRO)
		idfo_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_FO)
		idfo_mod_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_FO_sans_Modulo)
		idfo_ind_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_FO_Particulier)
		idfo_coll_shape_zpbo=layershape_zpbo.fieldNameIndex(Nom_Colonne_Nbre_FO_Professionel)
		idlog_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_Log)
		idfo_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_FO)
		
		idfo_mod_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_FO_sans_Modulo)
		idlog_Part_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_Log_Part) 
		idlog_PRO_shape_pbo=layershape_pbo.fieldNameIndex(Nom_Colonne_Nbre_Log_PRO)
		
		
		#Creation de shapefile pour le resultat des erreurs des id en doublons des cables
		erreur_pbo_double_ZPBO = QgsVectorLayer("Point?crs=epsg:2154", "erreur_Multiple_PBO_dans_ZPBO", "memory")
		erreur_pbo_double_ZPBO_pr = erreur_pbo_double_ZPBO.dataProvider()
		erreur_pbo_double_ZPBO_attr = layershape_pbo.dataProvider().fields().toList()
		erreur_pbo_double_ZPBO_pr.addAttributes(erreur_pbo_double_ZPBO_attr)
		erreur_pbo_double_ZPBO.updateFields()
		
		layershape_zpbo.startEditing()
		for shape_zpbo in layershape_zpbo.getFeatures():
			bboxshape_zpbo = shape_zpbo.geometry().boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxshape_zpbo)
			count_Particulier= 0
			count_Professionnel= 0
			for shape_sites in layershape_sites.getFeatures(request):
				if shape_sites.geometry().within (shape_zpbo.geometry()):
					if shape_sites[shape_sites_Colonne_Particulier] != 0:
						count_Particulier+=int(shape_sites[shape_sites_Colonne_Particulier]) 
					if shape_sites[shape_sites_Colonne_Professionel] != 0:
						count_Professionnel+=int(shape_sites[shape_sites_Colonne_Professionel])
						
			layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idlog_Part_shape_zpbo, unicode(count_Particulier)) #NB_FTTH
			layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idlog_PRO_shape_zpbo, unicode(count_Professionnel)) #NB_FTTE
			
			layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idlog_shape_zpbo, unicode(count_Particulier + count_Professionnel)) #Nbre_prise
					#print shape_zpbo['NOM'],';',int(shape_sites[shape_sites_Colonne_Particulier]) +int( shape_sites[shape_sites_Colonne_Particulier]),';',shape_sites[shape_sites_Colonne_Particulier],';', shape_sites[shape_sites_Colonne_Particulier]
			#Mode de calcul egal (pro*2 modulo6)+(particulier*1.20 modulo 3)
			
			#Nombre de fibre sans modulo
			nbrfo_FTTH_sans_mod=0
			nbrfo_FTTE_sans_mod=0

			
			if mod_calcul_NbreFo_Avec_Arrondi(shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi) and mod_a_executer(shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi):
				if count_Particulier != 0:
					nbrfo_FTTH_sans_mod=CalculFoPart_mod(count_Particulier)
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_ind_shape_zpbo, unicode(CalculFoPart(count_Particulier)))
					
				else : 
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_ind_shape_zpbo, 0)
				if count_Professionnel != 0:
					nbrfo_FTTE_sans_mod=CalculFoPro_mod(count_Particulier)
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_coll_shape_zpbo, unicode(CalculFoPro(count_Professionnel)))
				else :
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_coll_shape_zpbo, 0)
			#Mode de calcul egal (pro+particulier)*1.20
			if mod_calcul_NbreFo_Sans_Arrondi(shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi) and mod_a_executer(shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi):
				if count_Particulier != 0:
					nbrfo_FTTH_sans_mod=CalculFoPart_mod(count_Particulier)
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_ind_shape_zpbo, unicode(count_Particulier))
				else : 
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_ind_shape_zpbo, 0)
				if count_Professionnel != 0:
					nbrfo_FTTE_sans_mod=CalculFoPro_mod(count_Particulier)
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_coll_shape_zpbo, unicode(count_Professionnel))
				else :
					layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_coll_shape_zpbo, 0)
			#Nombre de fibre sans le modulo
			layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_mod_shape_zpbo, (nbrfo_FTTH_sans_mod+nbrfo_FTTE_sans_mod))
			#print nbrfo_FTTH_sans_mod,';',nbrfo_FTTE_sans_mod,';',nbrfo_FTTH_sans_mod+nbrfo_FTTE_sans_mod
					

		for shape_zpbo in layershape_zpbo.getFeatures():
			#Mode de calcul egal (pro+particulier)*1.20
			if mod_calcul_NbreFo_Sans_Arrondi(shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi) and mod_a_executer(shape_none_Mod_Calcul_FO_Projet_Sans_Arrondi):
				#layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_shape_zpbo, int(int(shape_zpbo[idfo_ind_shape_zpbo])+int(shape_zpbo[idfo_coll_shape_zpbo])))
				layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_shape_zpbo, unicode(((float(float(shape_zpbo[idfo_ind_shape_zpbo])+float(shape_zpbo[idfo_coll_shape_zpbo])))*fo_avec_reserve)))
				#layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_shape_zpbo, unicode())
			#Mode de calcul egal (pro*2 modulo6)+(particulier*1.20 modulo 3)
			if mod_calcul_NbreFo_Avec_Arrondi(shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi) and mod_a_executer(shape_none_Mod_Calcul_FO_Projet_Avec_Arrondi):
				layershape_zpbo.changeAttributeValue(shape_zpbo.id(),idfo_shape_zpbo, int(int(shape_zpbo[idfo_ind_shape_zpbo])+int(shape_zpbo[idfo_coll_shape_zpbo])))
		layershape_zpbo.commitChanges()

		#Partie du calcul du nombre de logements ainsi que le nombre de fibre utile dans le shape_pbo
		layershape_pbo.startEditing()
		for shape_zpbo in layershape_zpbo.getFeatures():
			bboxshape_zpbo = shape_zpbo.geometry().buffer(0.5,0.5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxshape_zpbo)
			count_pbo =0
			for shape_pbo in layershape_pbo.getFeatures(request):
				if shape_pbo.geometry().within (shape_zpbo.geometry()):
					count_pbo+= 1
					if shape_pbo[shape_boite_Colonne_FONCTION] == shape_boite_entite_PEC:#Mettre linformation que sur les PBO
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_shape_pbo, unicode(shape_zpbo[idlog_shape_zpbo]))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_Part_shape_pbo, unicode(shape_zpbo[Nom_Colonne_Nbre_Log_Part]))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_PRO_shape_pbo, unicode(shape_zpbo[Nom_Colonne_Nbre_Log_PRO]))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idfo_shape_pbo, unicode(shape_zpbo[idfo_shape_zpbo]))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idfo_mod_shape_pbo, unicode(shape_zpbo[Nom_Colonne_Nbre_FO_sans_Modulo]))
						
					elif shape_pbo[shape_boite_Colonne_FONCTION] != shape_boite_entite_PEC:
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_shape_pbo, unicode(0))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idfo_shape_pbo, unicode(0))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_Part_shape_pbo, unicode(0))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_PRO_shape_pbo, unicode(0))
						layershape_pbo.changeAttributeValue(shape_pbo.id(),idfo_mod_shape_pbo, unicode(0))
				"""else :
					layershape_pbo.changeAttributeValue(shape_pbo.id(),idlog_shape_pbo, unicode(0))
					layershape_pbo.changeAttributeValue(shape_pbo.id(),idfo_shape_pbo, unicode(0))"""
			if count_pbo > 1:
				erreur_pbo_double_ZPBO_pr.addFeatures([shape_pbo])

				
		layershape_pbo.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(erreur_pbo_double_ZPBO)
		


	#execution dela fonction ajout des champs utile 
	ajout_champs(shape_pbo,shape_zpbo,shape_cables,Nom_Colonne_Nbre_Log,Nom_Colonne_Nbre_FO,Nom_Colonne_Nbre_FO_Particulier,Nom_Colonne_Nbre_FO_Professionel)
	#Execution de la fonction calcul nombre de logement et de fibre utile
	calcul_nbre_LOG_FO(shape_pbo,shape_zpbo,shape_cables,shape_sites,Nom_Colonne_Nbre_Log,Nom_Colonne_Nbre_FO,Nom_Colonne_Nbre_FO_Particulier,Nom_Colonne_Nbre_FO_Professionel,shape_sites_Colonne_Particulier,shape_sites_Colonne_Professionel)