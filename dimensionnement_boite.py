import processing,xlrd
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * 
from qgis.utils import *
from collections import defaultdict
#from collections import Counter

##shape_boite=vector
##shape_cables=vector
##shape_point_technique=vector
##shape_poche_boite=vector
##shape_sites=vector
##DISTANCE_NRO_PM=string=50

#Contraintes: La colonne des section et des nom des cables ne doivent pas etre null ainsi que les cable s et supports doivent etres exactement superposables 

#Fichier_CONF_PYTHON=string=C:\Certification_Gracethd\Fichier_CONF_PYTHON_User.xlsx
#Fichier_CONF_PYTHON=string=r'C:\Users\bfassa\Desktop\Temp\DONNEES_SCRIPT_24_07_2018\donnesTest_SRO9\Fichier_CONF_PYTHON.xlsx'
#fichier_ref_compare = r'C:\Users\bfassa\Desktop\Temp\DONNEES_SCRIPT_24_07_2018\ref_type_bpe_blo.xlsx'
#Fichier_CONF_PYTHON=QFileDialog.getOpenFileName(None, "Fichier_CONF_PYTHON", "", "xlsx files (*.xlsx)")
#fichier_ref_compare=QFileDialog.getOpenFileName(None, "Fichier_Ref_boite", "", "xlsx files (*.xlsx)")

def dimensionnement_boite_function(shape_boite,shape_point_technique,shape_poche_boite,shape_cables,shape_sites,Fichier_CONF_PYTHON,fichier_ref_compare):

	w = QWidget()
	succesMsg="Execution-Plugin-Fini!!!!!!!!!"

	#Creation dune liste de mon fichier de configuration
	list_file_con=[]
	layer_ref_conf = QgsVectorLayer(Fichier_CONF_PYTHON, 'Fichier_CONF_PYTHON', 'ogr')
	for field_ref in layer_ref_conf.getFeatures():
		list_file_con.append([field_ref[0],field_ref[1],field_ref[2],field_ref[3]])

	#Declaration des noms des colonnes
	shape_BP_name_BP_NOM='BP_NOM'
	shape_CB_name_CB_NOM='CB_NOM'
	shape_CB_name_CB_SECTION='CB_SECTION'
	shape_CB_name_CB_Origine='CB_Origine'
	shape_CB_name_CB_Extremite='CB_Extremite'
	shape_CB_TYPE_FONC='CB_TYPE_FONC'
	shape_CB_TYPE_FONC_DISTRIBUTION= 'CB_TYPE_FONC_DISTRIBUTION'
	shape_CB_TYPE_FONC_Transport= 'CB_TYPE_FONC_Transport'
	shape_CB_TYPE_FONC_Raccordement= 'CB_TYPE_FONC_RACCORDEMENT'
	shape_CB_Origine_SRO='CB_Origine_SRO'
	shape_SF_NOM='SF_NOM'
	shape_SF_ISOLE='SF_ISOLE'
	shape_SF_ISOLE_OUI='SF_ISOLE_OUI'
	shape_SF_ISOLE_NON='SF_ISOLE_NON'
	shape_ZP_NOM='ZP_NOM'
	conf_DISTANCE_NRO_PM='Distance_NRO_PM'
	conf_VAL_TYPE_RACCO='VAL_TYPE_RACCO'


	shape_boite_BP_NBRE_FO='BP_NBRE_FO'
	shape_boite_BP_NBRE_FO_SUM='BP_NBRE_FO_SUM'
	shape_boite_BP_NBRE_FO_MOD='nbrfo_mod'
	shape_cables_CB_NBRFO_SUM='CB_NBRFO_SUM'
	shape_PT_PT_TYPE='PT_TYPE'
	shape_PT_PT_STRUC='PT_STRUC'
	shape_PT_PT_STRUC_IMMEUBLE='PT_STRUC_IMMEUBLE'
	shape_PT_PT_STRUC_CHAMBRE='PT_STRUC_CHAMBRE'
	shape_PT_PT_STRUC_POTEAU='PT_STRUC_POTEAU'
	shape_PT_PT_STRUC_FACADE='PT_STRUC_FACADE'

	fichier_RF_MDP_SOUTERRAIN='RF_MDP_SOUTERRAIN'
	fichier_RF_MDP_AERIEN='RF_MDP_AERIEN'
	fichier_RF_MDP_FACADE='RF_MDP_FACADE'
	fichier_RF_MDP_IMMEUBLE='RF_MDP_IMMEUBLE'




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
	Nom_Colonne_CB_SECTION=get_field_name(shape_CB_name_CB_SECTION,shape_cables)#Section
	shape_cable_Nom_Colonne_Origine=get_field_name(shape_CB_name_CB_Origine,shape_cables)#'originee'
	shape_cable_Nom_Colonne_Extremite=get_field_name(shape_CB_name_CB_Extremite,shape_cables)#'extremitee'
	Nom_Colonne_CB_TYPE_FONC=get_field_name(shape_CB_TYPE_FONC,shape_cables)
	Nom_Colonne_CB_TYPE_FONC_DISTRIBUTION=get_field_name(shape_CB_TYPE_FONC_DISTRIBUTION,shape_cables)
	Nom_Colonne_CB_TYPE_FONC_Transport=get_field_name(shape_CB_TYPE_FONC_Transport,shape_cables)
	Nom_Colonne_CB_TYPE_FONC_Raccordement=get_field_name(shape_CB_TYPE_FONC_Raccordement,shape_cables)
	shape_cables_Nom_Origine_Depart_Valeur=get_field_name(shape_CB_Origine_SRO,shape_cables)#TC-ST-BELL0101

	Nom_Colonne_BP_NBRE_FO=get_field_name(shape_boite_BP_NBRE_FO,shape_boite)
	Nom_Colonne_BP_NBRE_FO_SUM=get_field_name(shape_boite_BP_NBRE_FO_SUM,shape_boite)
	Nom_Colonne_CB_NBRFO_SUM=get_field_name(shape_cables_CB_NBRFO_SUM,shape_cables)
	Nom_Colonne_PT_TYPE=get_field_name(shape_PT_PT_TYPE,shape_point_technique)
	Nom_Colonne_PT_STRUC=get_field_name(shape_PT_PT_STRUC,shape_point_technique)
	Nom_Colonne_PT_STRUC_IMMEUBLE=get_field_name(shape_PT_PT_STRUC_IMMEUBLE,shape_point_technique)#IMMEUBLE
	Nom_Colonne_PT_STRUC_CHAMBRE=get_field_name(shape_PT_PT_STRUC_CHAMBRE,shape_point_technique)#'CHAMBRE'
	Nom_Colonne_PT_STRUC_POTEAU=get_field_name(shape_PT_PT_STRUC_POTEAU,shape_point_technique)#'POTEAU'
	Nom_Colonne_PT_STRUC_FACADE=get_field_name(shape_PT_PT_STRUC_FACADE,shape_point_technique)#'FACADE'

	Nom_entite_MDP_ref_boite_souterrain=get_field_name(fichier_RF_MDP_SOUTERRAIN,shape_point_technique)#'SOUTERRAIN'
	Nom_entite_MDP_ref_boite_aerien=get_field_name(fichier_RF_MDP_AERIEN,shape_point_technique)#'AERIEN'
	Nom_entite_MDP_ref_boite_facade=get_field_name(fichier_RF_MDP_FACADE,shape_point_technique)#'FACADE'
	Nom_entite_MDP_ref_boite_immeuble=get_field_name(fichier_RF_MDP_IMMEUBLE,shape_point_technique)#'IMMEUBLE'
	DISTANCE_NRO_PM=get_field_name(conf_DISTANCE_NRO_PM,shape_point_technique)#conf_DISTANCE_NRO_PM
	ENTITE_VAL_TYPE_RACCO=get_field_name(conf_VAL_TYPE_RACCO,shape_point_technique)#conf_VAL_TYPE_RACCO

	Nom_Colonne_SF_NOM=get_field_name(shape_SF_NOM,shape_sites)
	Nom_Colonne_SF_ISOLE=get_field_name(shape_SF_ISOLE,shape_sites)
	Nom_Colonne_SF_ISOLE_OUI=get_field_name(shape_SF_ISOLE_OUI,shape_sites)
	Nom_Colonne_SF_ISOLE_NON=get_field_name(shape_SF_ISOLE_NON,shape_sites)
	Nom_Colonne_ZP_NOM=get_field_name(shape_ZP_NOM,shape_poche_boite)


	Nom_Colonne_Type_FONCTION_BOITE='TYPE_FONCC'
	Nom_Colonne_Type_prod_1_BOITE='TYP_Prod_1'
	Nom_Colonne_Type_prod_2_BOITE='TYP_Prod_2'
	Nom_Colonne_mode_pose_BOITE='MDP_BP'
	Nom_Colonne_mode_pose_nature_BOITE='MDP_BP_NAT'
	Nom_Colonne_Nbre_EPISSURE='NB_EPIS'
	Nom_Colonne_NB_CASSETTE='NB_CAS'
	Nom_Colonne_distance_PBO_NRO='D_PBO_SRO'
	Nom_Colonne_ST_ISOLE='BP_ISOLE'
	Nom_Colonne_distance_PBO_PTO='D_PBO_PTO'
	Nom_Colonne_distance_PM_PTO='D_PM_PTO'
	Nom_Colonne_distance_PM_PTO_2='D_PBO_PTO2'
	Nom_Colonne_RACCO_TYPE='RACCO_LONG'
	Nom_Colonne_distance_NRO_PM='D_NRO_PM'
	Nom_Colonne_distance_NRO_PTO='D_NRO_PTO'
	Nom_Colonne_capacite_cable_rentrant='Capa_Rent'
	Nom_Colonne_nbre_cable_derivation='NBRE_DERIV'

	Nom_Colonne_cb_nom_passage='cb_nom_pas'
	Nom_Colonne_bp_passage='bp_pas'
	Nom_Colonne_cb_capa_passage='cb_capa_pa'
	Nom_Colonne_nbrfo_passage='nbrfo_pas'
	Nom_Colonne_nbre_cable_passage='nbr_cb_pas'
	Nom_Colonne_REF_BOITE='REF_BOITE'
	Nom_Colonne_nbrloge='nbrloge'
	Nom_Colonne_CB_capacitee='capacitee'

	List_attribut_Boite_ajout=[Nom_Colonne_Type_FONCTION_BOITE,Nom_Colonne_Type_prod_1_BOITE,Nom_Colonne_Type_prod_2_BOITE,Nom_Colonne_mode_pose_BOITE,Nom_Colonne_Nbre_EPISSURE,Nom_Colonne_NB_CASSETTE,Nom_Colonne_distance_PBO_NRO,Nom_Colonne_ST_ISOLE,Nom_Colonne_capacite_cable_rentrant,Nom_Colonne_nbre_cable_derivation,Nom_Colonne_cb_nom_passage,Nom_Colonne_bp_passage,Nom_Colonne_cb_capa_passage,Nom_Colonne_nbrfo_passage,Nom_Colonne_nbre_cable_passage,Nom_Colonne_mode_pose_nature_BOITE,Nom_Colonne_REF_BOITE]
	List_attribut_Sites_ajout=[Nom_Colonne_distance_PBO_NRO,Nom_Colonne_distance_PBO_PTO,Nom_Colonne_distance_PM_PTO,Nom_Colonne_distance_PM_PTO_2,Nom_Colonne_RACCO_TYPE,Nom_Colonne_distance_NRO_PM,Nom_Colonne_distance_NRO_PTO]

	List_attribut_Cables_ajout=Nom_Colonne_ST_ISOLE


	layershape_cables = shape_cables#processing.getObject(shape_cables)
	layershape_boite = shape_boite#processing.getObject(shape_boite)
	layershape_poche_boite = shape_poche_boite#processing.getObject(shape_poche_boite)
	layershape_point_technique = shape_point_technique#processing.getObject(shape_point_technique)
	layershape_sites = shape_sites#processing.getObject(shape_sites)


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


	#Ajout des attributs dans les boites
	delete_field(layershape_boite,List_attribut_Boite_ajout)
	for attribut in List_attribut_Boite_ajout:
		ajout_champs_function(layershape_boite,attribut)

	#Ajout des attributs dans les sites
	delete_field(layershape_sites,List_attribut_Sites_ajout)
	for attribut in List_attribut_Sites_ajout:
		ajout_champs_function(layershape_sites,attribut)

	#Ajout des attributs dans les cables
	delete_field(layershape_cables,List_attribut_Cables_ajout)
	ajout_champs_function(layershape_cables,List_attribut_Cables_ajout)


	#Variable text a utiliser pour remplir lattribut du Type_prod1
	Boite_PASSAGE='PASSAGE'
	Boite_Change_Section='Change_Section'
	Boite_ARRET='ARRET'
	Boite_PM='PM'
	#Variable text a utiliser pour remplir lattribut du type_fonction
	PBO_CLIENT='PBO'
	PBO_PIQUAGE_SANS_CLIENT='PIQUAGE'
	PBO_DERIVATION_SANS_CLIENT='DERIVATION'
	PBO_RACCORDEMENT='RACCORDEMENT'
	#Variable text a utiliser pour remplir lattribut du type_prod_2
	Boite_PBO6='PBO6'
	Boite_PBO12='PBO12'
	Boite_PBO0='0'
	Boite_PBO3='PBO3'
	Boite_PBO9='PBO9'
	Boite_BPI='BPI'


	nombre_cassette_boite=12
	nombre_ajouter_boite_avec_prises=1

	#Parti Intermedaire pour identifier les cables et les boites en passage

	def calcul_boite_passage():
		
		def calcul_cable_passage(noeud, niveau,section_rentrant) :

			section_sortant=0
			cb_nom=0
			bp_passage=0
			extremite_bp=0
			cb_capa_passage=0
			nbrfo_passage=0
			if niveau < 1000:
				for shape_cables in listshape_cables:
					if shape_cables[1] == noeud:  
						distance_PBO_NRO= calcul_cable_passage(shape_cables[2],niveau + 1,shape_cables[4])
						section_sortant=shape_cables[4]
						cb_nom=shape_cables[0]
						extremite_bp=shape_cables[2]
						if section_rentrant==section_sortant:
							bp_passage=Boite_PASSAGE
							cb_capa_passage=shape_cables[4]
							nbrfo_passage=shape_cables[5]
							for list_boite in listshape_pbo:
								if list_boite[0]==noeud:
									list_boite[1]=cb_nom
									list_boite[2]=bp_passage
									list_boite[3]=cb_capa_passage
									list_boite[4]=nbrfo_passage

		listshape_cables = []
		for shape_cables in layershape_cables.getFeatures():
			cable = [shape_cables[shape_cable_Nom_Colonne_Nom],shape_cables[shape_cable_Nom_Colonne_Origine],shape_cables[shape_cable_Nom_Colonne_Extremite],shape_cables[Nom_Colonne_CB_SECTION],shape_cables[Nom_Colonne_CB_capacitee],shape_cables[Nom_Colonne_CB_NBRFO_SUM]]
			listshape_cables.append(cable)
		listshape_pbo = []
		for shape_pbos in layershape_boite.getFeatures():
			shape_pbo = [shape_pbos[shape_pbo_Nom_Colonne_Nom],0,0,0,0]
			listshape_pbo.append(shape_pbo)

		#Execution de la fonction calcul distance SRO-PBO
		calcul_cable_passage(shape_cables_Nom_Origine_Depart_Valeur,0,'depart')
		
		indexe_cb_nom_passage=layershape_boite.fieldNameIndex(Nom_Colonne_cb_nom_passage)
		indexe_cb_capa_passage=layershape_boite.fieldNameIndex(Nom_Colonne_cb_capa_passage)
		indexe_bp_passage=layershape_boite.fieldNameIndex(Nom_Colonne_bp_passage)
		indexe_nbrfo_passage=layershape_boite.fieldNameIndex(Nom_Colonne_nbrfo_passage)
		
		layershape_boite.startEditing()
		for shape_pbos in layershape_boite.getFeatures():
			cb_nom_passage=0
			bp_passage=0
			cb_capa_passage=0
			nbrfo_passage=0
			for list_boite in listshape_pbo:
				if list_boite[0]==shape_pbos[shape_pbo_Nom_Colonne_Nom]:
					cb_nom_passage=list_boite[1]
					bp_passage=list_boite[2]
					cb_capa_passage=list_boite[3]
					nbrfo_passage=list_boite[4]
			layershape_boite.changeAttributeValue(shape_pbos.id(),indexe_cb_nom_passage, unicode(cb_nom_passage))
			layershape_boite.changeAttributeValue(shape_pbos.id(),indexe_cb_capa_passage, unicode(cb_capa_passage))
			layershape_boite.changeAttributeValue(shape_pbos.id(),indexe_bp_passage, unicode(bp_passage))
			layershape_boite.changeAttributeValue(shape_pbos.id(),indexe_nbrfo_passage, unicode(nbrfo_passage))
		
		layershape_boite.commitChanges()
					
	calcul_boite_passage()

	#I.Calcul TYPE_FONCTION, TYPE PROD_1, TYPE PROD_2, MODE_POSE, NB_EPISSURES, NB_CASSETTE_12 des boites

	def TYPE_PROD_1():    

		#1.Calcule du type de prod_1
		list_cable_section_boite_rentrant=[]
		list_cable_section_boite_sortant=[]
		List_Type_Prod1=[]
		
		dict_sortant=defaultdict(list)
		dict_sortant_passage=defaultdict(list)
		dict_nbre_cable_sortant={}#defaultdict(list)

		#Type_fonction des boites
		list_boite_poche=[] #PBO

		
		for boite in layershape_boite.getFeatures():
			bboxnoeud = boite.geometry().buffer(5,5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxnoeud)
			
			count_sortant = 0
			count_rentrant = 0
			count_sortant_passage = 0
			
			info_cable_section_sortant='-1'
			info_cable_nbrefosum_sortant='-1'
			info_cable_nom_sortant='-1'
			info_cable_typefonct_sortant='-1'
			
			info_cable_section_rentrant='-1'
			info_cable_nbrefosum_rentrant='-1'
			info_cable_nom_rentrant='-1'
			info_cable_typefonct_rentrant='-1'
			
			capa_cable_rentrant=0
			
			"""for poche in layershape_poche_boite.getFeatures(request):
				if boite.geometry().within(poche.geometry()):
					#Recuperation de toutes les boites ayant des ZPBO
					list_boite_poche.append(boite[shape_pbo_Nom_Colonne_Nom])"""
			
			#Reucpertion des cables sortants et rentrants dans une boite
			for cables in layershape_cables.getFeatures(request):
				if cables[Nom_Colonne_CB_TYPE_FONC] != Nom_Colonne_CB_TYPE_FONC_Raccordement:
					#cable_rentrant
					if boite[shape_pbo_Nom_Colonne_Nom] == cables[shape_cable_Nom_Colonne_Extremite]:
						
						count_rentrant +=1
						info_cable_section_rentrant=cables[Nom_Colonne_CB_SECTION]
						info_cable_nbrefosum_rentrant=cables[Nom_Colonne_CB_NBRFO_SUM]
						info_cable_nom_rentrant=cables[shape_cable_Nom_Colonne_Nom]
						info_cable_typefonct_rentrant=cables[Nom_Colonne_CB_TYPE_FONC]
						capa_cable_rentrant=cables[Nom_Colonne_CB_capacitee]
						
					#cable_sortant
					if boite[shape_pbo_Nom_Colonne_Nom] == cables[shape_cable_Nom_Colonne_Origine]:
						count_sortant +=1
						info_cable_section_sortant=cables[Nom_Colonne_CB_SECTION]
						info_cable_nbrefosum_sortant=cables[Nom_Colonne_CB_NBRFO_SUM]
						info_cable_nom_sortant=cables[shape_cable_Nom_Colonne_Nom]
						info_cable_typefonct_sortant=cables[Nom_Colonne_CB_TYPE_FONC]
						dict_sortant[boite[shape_pbo_Nom_Colonne_Nom]].append(cables[Nom_Colonne_CB_SECTION])
						dict_sortant_passage[boite[shape_pbo_Nom_Colonne_Nom]].append(cables[Nom_Colonne_CB_SECTION])
						if boite[shape_pbo_Nom_Colonne_Nom] == cables[shape_cable_Nom_Colonne_Origine] and boite[Nom_Colonne_bp_passage] ==Boite_PASSAGE and cables[shape_cable_Nom_Colonne_Nom] == boite[Nom_Colonne_cb_nom_passage]:     
							count_sortant_passage +=1
						
			dict_nbre_cable_sortant[boite[shape_pbo_Nom_Colonne_Nom]]=([capa_cable_rentrant,count_sortant,count_sortant_passage])
			
			list_cable_section_boite_rentrant.append([boite[shape_pbo_Nom_Colonne_Nom],info_cable_section_rentrant,info_cable_nbrefosum_rentrant,info_cable_nom_rentrant,info_cable_typefonct_rentrant,count_rentrant])
			
			list_cable_section_boite_sortant.append([boite[shape_pbo_Nom_Colonne_Nom],info_cable_section_sortant,info_cable_nbrefosum_sortant,info_cable_nom_sortant,info_cable_typefonct_sortant,count_sortant])
		
		for rentrant in list_cable_section_boite_rentrant:
			Type_Prod1='-1'
			boite_sortant='-1'
			Boite_PASSAGE_filtre='-1'
			for key, value in dict_sortant.items():
				if rentrant[0]==key:
					if rentrant[1] in value:
						Type_Prod1=Boite_PASSAGE
						Boite_PASSAGE_filtre=Boite_PASSAGE
			for sortant in list_cable_section_boite_sortant:
				if rentrant[0]==sortant[0]:
					boite_sortant=sortant[0]
					#Condition pour remplir type_prod_1
					if sortant[5] == 0:
						Type_Prod1=Boite_ARRET
					elif rentrant[5] ==0:
						Type_Prod1=Boite_PM
					elif sortant[5] != 0 and rentrant[5] !=0 and Boite_PASSAGE_filtre !=Boite_PASSAGE:
						Type_Prod1=Boite_Change_Section
			List_Type_Prod1.append([boite_sortant,Type_Prod1])
					#print rentrant[0],';',sortant[0],';',rentrant[1],';',sortant[1],';',Type_Prod1
		
		#2.Calcul du nombre depissure des boites tout en soustraitant le cable sortant en passage  
		#Identifier les cables en passage pour calculer le nombre depissures des boites
		List_Cable_Passage=[]
		for rentrant in list_cable_section_boite_rentrant:
			nbrefo_sortant_cable_passage=0
			nbrefo_rentrant_cable=rentrant[2]
			value_var='-1'
			bp_passage= '-1'
			for boite in layershape_boite.getFeatures():
				if rentrant[0]==boite[shape_pbo_Nom_Colonne_Nom]:
					if boite[Nom_Colonne_bp_passage] == Boite_PASSAGE:
						value_var=value
						bp_passage= Boite_PASSAGE
						nbrefo_sortant_cable_passage=boite[Nom_Colonne_nbrfo_passage]
			List_Cable_Passage.append([rentrant[0],nbrefo_sortant_cable_passage,nbrefo_rentrant_cable,value_var,bp_passage])

		#Calcul du nombre de derivation == > Nombre de cable sortant - 1 sil y a un cable en passage ou o sil y a pas de cable en passage
		list_choix_boite_intermediaire=[]
		for sortant, value in dict_nbre_cable_sortant.items():
			cab_passage_value=0
			if value[1] != 0:
				for cab_passage in List_Cable_Passage:
					if sortant==cab_passage[0] and cab_passage[4] ==Boite_PASSAGE:
						cab_passage_value=1
			attribut_callcule=[sortant,value[1]-cab_passage_value,value[0],value[2]]
			list_choix_boite_intermediaire.append(attribut_callcule)
			#print sortant,';',value[1]-cab_passage_value,';',value[1],';',cab_passage_value,';',value[0]

		indexe_type_prod_1=layershape_boite.fieldNameIndex(Nom_Colonne_Type_prod_1_BOITE)
		indexe_nbre_EPISSURE=layershape_boite.fieldNameIndex(Nom_Colonne_Nbre_EPISSURE)
		indexe_nbre_cable_derivation=layershape_boite.fieldNameIndex(Nom_Colonne_nbre_cable_derivation)
		indexe_capacite_cable_rentrant=layershape_boite.fieldNameIndex(Nom_Colonne_capacite_cable_rentrant)
		indexe_nbre_cable_passage=layershape_boite.fieldNameIndex(Nom_Colonne_nbre_cable_passage)
		layershape_boite.startEditing()
		for boite in layershape_boite.getFeatures():
			type_prod_1='-1'
			nbre_epis=0
			nbre_cable_derivation=0
			capacite_cable_rentrant=0
			nbre_cable_passage = 0 
			for prod in List_Type_Prod1:
				if boite[shape_pbo_Nom_Colonne_Nom] == prod[0]:
					type_prod_1=prod[1]
					
			for epissure in List_Cable_Passage:
				if boite[shape_pbo_Nom_Colonne_Nom] ==epissure[0] and cab_passage[4] ==Boite_PASSAGE:
					if epissure[2] != NULL and epissure[1] != NULL and boite[Nom_Colonne_BP_NBRE_FO] != NULL:
						nbre_epis=int((float(epissure[2])-float(epissure[1]))-float(boite[shape_boite_BP_NBRE_FO_MOD]))#Nom_Colonne_BP_NBRE_FO_SUM Nom_Colonne_BP_NBRE_FO
						#print boite[shape_pbo_Nom_Colonne_Nom] ,';','capa_rentrant',float(epissure[2]),';','capa_passage',float(epissure[1]),';','nbefo_mod',float(boite[shape_boite_BP_NBRE_FO_MOD])
			for cab in list_choix_boite_intermediaire:
				if boite[shape_pbo_Nom_Colonne_Nom] ==cab[0]:
					nbre_cable_derivation=cab[1]
					capacite_cable_rentrant=cab[2]
					nbre_cable_passage=cab[3]
			layershape_boite.changeAttributeValue(boite.id(),indexe_nbre_cable_derivation, unicode(nbre_cable_derivation))
			layershape_boite.changeAttributeValue(boite.id(),indexe_capacite_cable_rentrant, unicode(capacite_cable_rentrant))
			layershape_boite.changeAttributeValue(boite.id(),indexe_type_prod_1, unicode(type_prod_1))
			layershape_boite.changeAttributeValue(boite.id(),indexe_nbre_EPISSURE, unicode(nbre_epis))
			layershape_boite.changeAttributeValue(boite.id(),indexe_nbre_cable_passage, unicode(nbre_cable_passage))
		
		layershape_boite.commitChanges()


	#2.Type_prod_2 et mode de pose de la boite

	def Type_prod_2():
		
		indexe_type_prod_2=layershape_boite.fieldNameIndex(Nom_Colonne_Type_prod_2_BOITE)
		indexe_mode_pose_BOITE=layershape_boite.fieldNameIndex(Nom_Colonne_mode_pose_BOITE)
		indexe_mode_pose_nature_BOITE=layershape_boite.fieldNameIndex(Nom_Colonne_mode_pose_nature_BOITE)
		layershape_boite.startEditing()
		List_boite_immeuble=[]

		for boite in layershape_boite.getFeatures():
			#a= boite[shape_pbo_Nom_Colonne_Nom]
			geom_boite=boite.geometry()
			bbox_boite = geom_boite.buffer(5, 5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bbox_boite)
			mode_pose='-1'
			mode_pose_nature='-1'
			#1.Mode_pose de la boite selon le point technique
			for pt in layershape_point_technique.getFeatures(request):
				if boite.geometry().within(pt.geometry().buffer(0.1,0.1)):
					mode_pose=pt[Nom_Colonne_PT_STRUC]
					mode_pose_nature=pt[Nom_Colonne_PT_TYPE]
					#layershape_boite.changeAttributeValue(boite.id(),indexe_mode_pose_BOITE, pt[Nom_Colonne_PT_STRUC])
					if pt[Nom_Colonne_PT_STRUC] == Nom_Colonne_PT_STRUC_IMMEUBLE:
						List_boite_immeuble.append(boite[shape_pbo_Nom_Colonne_Nom])
			Type_prod_2='-1'
			if boite[shape_boite_BP_NBRE_FO_MOD] != NULL:
				
				#PBO_0
				if float(boite[shape_boite_BP_NBRE_FO_MOD]) ==0:
					Type_prod_2=Boite_PBO0
				#PBO_3
				elif float(boite[shape_boite_BP_NBRE_FO_MOD]) >= 1 and  float(boite[shape_boite_BP_NBRE_FO_MOD]) <= 3:
					Type_prod_2=Boite_PBO3
				#PBO_6
				elif float(boite[shape_boite_BP_NBRE_FO_MOD]) >= 4 and  float(boite[shape_boite_BP_NBRE_FO_MOD]) <= 6:
					Type_prod_2=Boite_PBO6
				#PBO_6
				elif float(boite[shape_boite_BP_NBRE_FO_MOD]) >= 7 and  float(boite[shape_boite_BP_NBRE_FO_MOD]) <= 9:
					Type_prod_2=Boite_PBO9
				#PBO_12
				elif float(boite[shape_boite_BP_NBRE_FO_MOD]) > 10 and float(boite[shape_boite_BP_NBRE_FO_MOD]) <= 12:
					Type_prod_2=Boite_PBO12
				
			layershape_boite.changeAttributeValue(boite.id(),indexe_type_prod_2, unicode(Type_prod_2))
			layershape_boite.changeAttributeValue(boite.id(),indexe_mode_pose_BOITE, unicode(mode_pose))
			layershape_boite.changeAttributeValue(boite.id(),indexe_mode_pose_nature_BOITE, unicode(mode_pose_nature))
		layershape_boite.commitChanges()


	#NB_CASSETTE_12
	def calc_nbre_cassette():
		
		indexe_NB_CASSETTE=layershape_boite.fieldNameIndex(Nom_Colonne_NB_CASSETTE)
		layershape_boite.startEditing()
		for boite in layershape_boite.getFeatures():
			nbre_cassette=0
			if boite[shape_boite_BP_NBRE_FO_MOD] != NULL and float(boite[shape_boite_BP_NBRE_FO_MOD]) > 0 and boite[Nom_Colonne_Nbre_EPISSURE] != '-1':#and float(boite[Nom_Colonne_Nbre_EPISSURE]) > 0:boite[Nom_Colonne_BP_NBRE_FO] != NULL and float(boite[Nom_Colonne_BP_NBRE_FO]) > 0 :
				nbre_cassette=int(1)+(int(round(float(boite[Nom_Colonne_Nbre_EPISSURE])/12)))
			layershape_boite.changeAttributeValue(boite.id(),indexe_NB_CASSETTE, nbre_cassette)
		layershape_boite.commitChanges()


	#5.Type_FONCTION
	def type_foncc():
		indexe_type_foncc=layershape_boite.fieldNameIndex(Nom_Colonne_Type_FONCTION_BOITE)
		layershape_boite.startEditing()
		for boite in layershape_boite.getFeatures():
			type_foncc_boite='-1'
			if boite[Nom_Colonne_Nbre_EPISSURE] != NULL and boite[Nom_Colonne_BP_NBRE_FO] != NULL:
				#Boite de PBO
				if float(boite[Nom_Colonne_Nbre_EPISSURE])== float('0') and float(boite[Nom_Colonne_BP_NBRE_FO]) >= float('1'):
					type_foncc_boite='PBO'

				#Boite de piquage
				elif float(boite[Nom_Colonne_Nbre_EPISSURE]) >= float('1') and float(boite[Nom_Colonne_BP_NBRE_FO]) == float('0') and boite[Nom_Colonne_Type_prod_1_BOITE] == Boite_PASSAGE:
					type_foncc_boite='PIQUAGE'
				
				#Boite de double fonction piquage
				elif float(boite[Nom_Colonne_Nbre_EPISSURE]) >= float('1') and float(boite[Nom_Colonne_BP_NBRE_FO]) >= float('1') and boite[Nom_Colonne_Type_prod_1_BOITE] == Boite_PASSAGE:
					type_foncc_boite='DOUBLE_FONCTION_PIQUAGE'

				#Boite de Derivation
				elif float(boite[Nom_Colonne_Nbre_EPISSURE]) >= float('1') and float(boite[Nom_Colonne_BP_NBRE_FO]) == float('0') and boite[Nom_Colonne_Type_prod_1_BOITE] == Boite_Change_Section:
					type_foncc_boite='DERIVATION'
				
				#Boite de double fonction Derivation
				elif float(boite[Nom_Colonne_Nbre_EPISSURE]) >= float('1') and float(boite[Nom_Colonne_BP_NBRE_FO]) >= float('1') and boite[Nom_Colonne_Type_prod_1_BOITE] == Boite_Change_Section:
					type_foncc_boite='DOUBLE_FONCTION_DERIVATION'

				#Boite de PM
				elif  boite[Nom_Colonne_Type_prod_1_BOITE] == Boite_PM:
					type_foncc_boite='PM'
					
			layershape_boite.changeAttributeValue(boite.id(),indexe_type_foncc, unicode(type_foncc_boite))

		layershape_boite.commitChanges()


	#II.Calcul distance PBO-SRO
	def Distance_PBO_SRO():
		
		def calcul_distance_PBO_NRO(noeud, niveau,distance) :
			
			#somme_fo = 0
			if niveau < 1000:
				#print "debut sommefib " + noeud
				for shape_cables in listshape_cables:
					if shape_cables[1] == noeud:  
						distance_PBO_NRO= calcul_distance_PBO_NRO(shape_cables[2],niveau + 1,shape_cables[3]+distance)
							
				for shape_pbo in listshape_pbo:
					if shape_pbo[0]== noeud:
						shape_pbo[1]=distance                        
						#print shape_pbo[0],';',section,';',etat,';',cb_code,';',statu_cable,';',statu_boite
						#print noeud,';',niveau,';',cb_code,';',distance
			
			#print boite_amont
			#return somme_fo
				
			return 0,0

		listshape_cables = []
		for shape_cables in layershape_cables.getFeatures():
			#print shape_cables[0],';',shape_cables.geometry().length()
			#print shape_cables['SECTION'],';',shape_cables['ETAT']
			cable = [shape_cables[shape_cable_Nom_Colonne_Nom],shape_cables[shape_cable_Nom_Colonne_Origine],shape_cables[shape_cable_Nom_Colonne_Extremite],shape_cables.geometry().length(),shape_cables[Nom_Colonne_CB_SECTION],-1,-1]
			listshape_cables.append(cable)
		listshape_pbo = []
		for shape_pbos in layershape_boite.getFeatures():
			shape_pbo = [shape_pbos[shape_pbo_Nom_Colonne_Nom],-1,-1,-1]
			listshape_pbo.append(shape_pbo)

		#Execution de la fonction calcul distance SRO-PBO
		calcul_distance_PBO_NRO(shape_cables_Nom_Origine_Depart_Valeur,1,0)

		index_distane_PBO_NRO=layershape_boite.fieldNameIndex(Nom_Colonne_distance_PBO_NRO)
		layershape_boite.startEditing()
		for shape_pbos in layershape_boite.getFeatures():
			for boite in listshape_pbo:
				if shape_pbos[shape_pbo_Nom_Colonne_Nom]==boite[0]:
					layershape_boite.changeAttributeValue(shape_pbos.id(),index_distane_PBO_NRO,int(boite[1]))
					#print boite[0],';',boite[1]

		layershape_boite.commitChanges()

	#III.Calcul  de isoler de la boite fonction des sites
	def get_st_isole_boite():
		
		Nom_Colonne_ST_ISOLE
		indexe_ST_ISOLE=layershape_boite.fieldNameIndex(Nom_Colonne_ST_ISOLE)

		List_poche_ST_ISOLE=[]
		for poche in layershape_poche_boite.getFeatures():
			bboxpoche = poche.geometry().buffer(5,5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxpoche)
			for sites in layershape_sites.getFeatures(request):
				if sites.geometry().within(poche.geometry()):
					List_poche_ST_ISOLE.append([poche[Nom_Colonne_ZP_NOM],sites[Nom_Colonne_SF_NOM],sites[Nom_Colonne_SF_ISOLE]])
					

		#Creation dun dictionnaire pour regroupe les st_isole des sites en fonction des poches pour enfin faire le tri
		dict_sites_st_isole_poche={}
		for rent  in List_poche_ST_ISOLE:
			if rent[0] in dict_sites_st_isole_poche:
				dict_sites_st_isole_poche[rent[0]].append(rent[2])
			elif rent[0] not in dict_sites_st_isole_poche:
				dict_sites_st_isole_poche[rent[0]]=[rent[2]]
				
		for poche in layershape_poche_boite.getFeatures():
			bboxpoche = poche.geometry().buffer(5,5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxpoche)
			ST_ISOLE='-1'
			for key, values in dict_sites_st_isole_poche.items():
				if key == poche[Nom_Colonne_ZP_NOM]:
					if Nom_Colonne_SF_ISOLE_OUI in values:
						ST_ISOLE='OUI'
						#print key, ';',values
					elif Nom_Colonne_SF_ISOLE_OUI not in values:
						ST_ISOLE='NON'
			layershape_boite.startEditing()
			for boite in layershape_boite.getFeatures(request):
				if boite.geometry().within(poche.geometry()):
					#if boite['TYPE_FONC']=='PBO':
					layershape_boite.changeAttributeValue(boite.id(),indexe_ST_ISOLE,ST_ISOLE)
					#print poche['nom'],';',ST_ISOLE,';',boite['CODE_BPE']
		layershape_boite.commitChanges()


	#III.Calcul  de isoler du cable en fonction des boites
	def get_st_isole_cable():
		
		def SommeFibBesoinRec(noeud, niveau) :
			
			st_isole_BP = '-1'
			
			if niveau < 1000:
				#print "debut sommefib " + noeud
				for shape_cables in listshape_cables:
					if shape_cables[1] == noeud:
						somme_fo_aval= SommeFibBesoinRec(shape_cables[2],niveau + 1)
						st_isole_BP=somme_fo_aval
				for shape_pbo in listshape_pbo:
					if shape_pbo[0]== noeud:
						if shape_pbo[1] != NULL:  
							st_isole_BP = shape_pbo[1]
						shape_pbo[2] = st_isole_BP
			
			#print noeud,';',niveau,';',st_isole_BP
			return st_isole_BP
				
			return 0,0
			

		listshape_cables = []
		for shape_cables in layershape_cables.getFeatures():
			cable = [shape_cables[shape_cable_Nom_Colonne_Nom],shape_cables[shape_cable_Nom_Colonne_Origine],shape_cables[shape_cable_Nom_Colonne_Extremite]]
			listshape_cables.append(cable)
		listshape_pbo = []
		for shape_pbos in layershape_boite.getFeatures():
			shape_pbo = [shape_pbos[shape_pbo_Nom_Colonne_Nom],shape_pbos[Nom_Colonne_ST_ISOLE],-1]
			listshape_pbo.append(shape_pbo)

		SommeFibBesoinRec(shape_cables_Nom_Origine_Depart_Valeur,1)
		
		layershape_cables.startEditing()           
		#layershape_pbo.startEditing()
		
		indexe_CB_ISOLE=layershape_cables.fieldNameIndex(Nom_Colonne_ST_ISOLE)
		
		for shape_cables in layershape_cables.getFeatures():
			for shape_pbo in listshape_pbo:
				if shape_cables[shape_cable_Nom_Colonne_Extremite] == shape_pbo[0]:
					layershape_cables.changeAttributeValue(shape_cables.id(),indexe_CB_ISOLE,shape_pbo[2])
					
		layershape_cables.commitChanges()

	#IV.Calcul  des distances dans sites
	def distance_PM_PBO_PTO_SITES():
		
		for shape_cables in layershape_cables.getFeatures():
			bboxshape_cables = shape_cables.geometry().buffer(5,5).boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxshape_cables)
			#print shape_cables[0],';',shape_cables[shape_cable_Nom_Colonne_Origine],';',shape_cables.geometry().length()
			
			geom_cable=shape_cables.geometry()
			
			#Recuperation des origines et extremites des cables de type Multi-Linesting
			if geom_cable.wkbType()==QGis.WKBMultiLineString:
				geom_cable_type=geom_cable.asMultiPolyline()
				cable_origine=geom_cable_type[0][0]
				cable_extremite=geom_cable_type[-1][-1]
			
			#Recuperation des origines et extremites des cables de type Linesting
			if geom_cable.wkbType()==QGis.WKBLineString:
				geom_cable_type=geom_cable.asPolyline()
				cable_origine=geom_cable_type[0]
				cable_extremite=geom_cable_type[-1]
			
			distance_pbo_pm='-1'
			if geom_cable.wkbType() in [QGis.WKBMultiLineString,QGis.WKBLineString]:  
				
				for shape_pbos in layershape_boite.getFeatures(request):
					if  (QgsGeometry.fromPoint(QgsPoint(cable_origine))).within (shape_pbos.geometry().buffer(0.1,0.1)):
						distance_pbo_pm=shape_pbos[Nom_Colonne_distance_PBO_NRO]
						
				indexe_distance_PBO_PTO=layershape_sites.fieldNameIndex(Nom_Colonne_distance_PBO_PTO)
				indexe_distance_PM_PTO=layershape_sites.fieldNameIndex(Nom_Colonne_distance_PM_PTO)
				index_distane_PBO_NRO=layershape_sites.fieldNameIndex(Nom_Colonne_distance_PBO_NRO)
				
				layershape_sites.startEditing()  
				for shape_sites in layershape_sites.getFeatures(request):
					#if (QgsGeometry.fromPoint(QgsPoint(cable_origine))).within (shape_sites.geometry().buffer(0.1,0.1)):
					if  (QgsGeometry.fromPoint(QgsPoint(cable_extremite))).within (shape_sites.geometry().buffer(0.1,0.1)):
						layershape_sites.changeAttributeValue(shape_sites.id(),indexe_distance_PBO_PTO,int(shape_cables.geometry().length()))
						layershape_sites.changeAttributeValue(shape_sites.id(),index_distane_PBO_NRO,int(distance_pbo_pm))
						if distance_pbo_pm != '-1':
							layershape_sites.changeAttributeValue(shape_sites.id(),indexe_distance_PM_PTO,int(shape_cables.geometry().length()+float(distance_pbo_pm)))
						
				
				layershape_sites.commitChanges()
			#print shape_cables[0],';',distance_pbo_pm


	def calcul_dist_PBO_PTO_VOl_OISEAU():
		layerAdresses = layershape_sites#processing.getObject(adresses)
		layerPBO = layershape_boite#processing.getObject(pbos)
		layerContours = layershape_poche_boite#processing.getObject(contourspbo)

		indexe_distance_PM_PTO_2=layerAdresses.fieldNameIndex(Nom_Colonne_distance_PM_PTO_2)
		indexe_RACCO_TYPE=layerAdresses.fieldNameIndex(Nom_Colonne_RACCO_TYPE)
		indexe_distance_NRO_PM=layerAdresses.fieldNameIndex(Nom_Colonne_distance_NRO_PM)
		indexe_distance_NRO_PTO=layerAdresses.fieldNameIndex(Nom_Colonne_distance_NRO_PTO)
		
		

		# ---- 1. Creation du layer resultat -------------------------
		# ---- 2. Parcours des contours de PBO pour y tracer les adductions -------------------------
		list_distance_vol_oiseau=[]
		for contour in layerContours.getFeatures():
			bboxContour = contour.geometry().boundingBox()
			request = QgsFeatureRequest()
			request.setFilterRect(bboxContour)
			# ---- 2.1. Parcours des PBOs dans le bbox du contour PBO -------------------------
			for PBO in layerPBO.getFeatures(request):
				# ---- 2.2. On verifie que le PBO est bien dans le contour PBO (pas juste la bbox) -------------------------
				if PBO.geometry().within(contour.geometry()):
					# ---- 2.3. Parcours des adresses dans le bbox du contour PBO -------------------------
					for adresse in layerAdresses.getFeatures(request): 
						distance='-1'
						# ---- 2.4. On verifie que l adresse est bien dans le contour PBO (pas juste la bbox) -------------------------
						if adresse.geometry().within(contour.geometry()):
							# ---- 2.5. Creation de la ligne de l adductions -------------------------
							distance=(QgsGeometry.fromPolyline([PBO.geometry().asPoint(),adresse.geometry().asPoint()])).length()
							attr=[adresse[Nom_Colonne_SF_NOM],distance]
							list_distance_vol_oiseau.append(attr)
		layerAdresses.startEditing()  
		
		for adresse in layerAdresses.getFeatures():
			DISTANCE_PM_PTO_2_var=0
			RACCO_TYPE_var='-1'
			for lis_suf in list_distance_vol_oiseau:
				if adresse[Nom_Colonne_SF_NOM]==lis_suf[0]:
					DISTANCE_PM_PTO_2_var=int(lis_suf[1])
					#layerAdresses.changeAttributeValue(adresse.id(),indexe_distance_PM_PTO_2,unicode(int(lis_suf[1])))
					if int(lis_suf[1]) > int(ENTITE_VAL_TYPE_RACCO): #Valeur a parametrer 1 sur les tests
						RACCO_TYPE_var=1
						#layerAdresses.changeAttributeValue(adresse.id(),indexe_RACCO_TYPE,unicode(1))
					else:
						RACCO_TYPE_var=0
						#layerAdresses.changeAttributeValue(adresse.id(),indexe_RACCO_TYPE,unicode(0))
			if adresse[Nom_Colonne_distance_PBO_NRO] != '-1' and adresse[Nom_Colonne_distance_PBO_PTO] != '-1' and adresse[Nom_Colonne_distance_PBO_NRO] != NULL and adresse[Nom_Colonne_distance_PBO_PTO] != NULL:
				
				layerAdresses.changeAttributeValue(adresse.id(),indexe_distance_NRO_PTO,unicode(int(DISTANCE_NRO_PM)+int(adresse[Nom_Colonne_distance_PBO_NRO])+int(adresse[Nom_Colonne_distance_PBO_PTO])))
				
			layerAdresses.changeAttributeValue(adresse.id(),indexe_distance_NRO_PM,unicode(int(DISTANCE_NRO_PM)))
			layerAdresses.changeAttributeValue(adresse.id(),indexe_distance_PM_PTO_2,unicode(DISTANCE_PM_PTO_2_var))
			layerAdresses.changeAttributeValue(adresse.id(),indexe_RACCO_TYPE,unicode(RACCO_TYPE_var))
			
		layerAdresses.commitChanges()

		# ---- 3. Mise a jour de l etendue et ajout aux couches QGIS -------------------------


	#Calcul du choix de la reference de la boite

	def choix_ref_boite():
		
		Liste_BPE_DEF= []
		Liste_TYPE_BLO= []
		Liste_TYPE_BLO_Nat= []

		book = xlrd.open_workbook(fichier_ref_compare)
		sheet = book.sheet_by_index(1) 
		list_header_typblo=[]
		for i in range(sheet.ncols): 
			attr=(sheet.cell_value(0, i))
			list_header_typblo.append(attr)
			#print attr
		#print header_type_BLO
		#print sheet.ncols
		#sheet = book.sheet_by_index(0)  
		if book == None:
			raise "Open Excel(%s) failed!" % name
		for i in range(book.nsheets):
			s = book.sheet_by_index(i)
			#Recuperation des nom des feuilles
			sname = s.name
			#Filtre sur la feuille BPE_DEF
			if sname == 'BPE_DEF':
				for r in range(1,s.nrows):
					#List_Attribut_Value
				   #attr=s.row_values(r)
				   #s.cell_value(0, i)
				   REF_INTERNE_BPE=str(s.cell_value(r, 0))
				   FABRICANT=str(s.cell_value(r, 1))
				   TYPE_BLO=str(s.cell_value(r, 2).encode('utf8'))#encode('utf8')
				   MODE_POS=str(s.cell_value(r, 3))
				   MAX_CAPA_RENTRANT=str(s.cell_value(r, 4))
				   MAX_EPISSURE=str(s.cell_value(r, 5))
				   Max_NB_CABLE_PASSAGE=str(s.cell_value(r, 6))
				   Max_NB_CABLE_SORTANT=str(s.cell_value(r, 7))
				   Max_nbrloge=str(s.cell_value(r, 8))

				   
				   #print REF_INTERNE_BPE
				   attr=[REF_INTERNE_BPE,FABRICANT,TYPE_BLO,MODE_POS,MAX_CAPA_RENTRANT,MAX_EPISSURE,Max_NB_CABLE_PASSAGE,Max_NB_CABLE_SORTANT,Max_nbrloge]
				   Liste_BPE_DEF.append(attr)
				   
			
			if sname == 'TYPE_BLO':
				
				for r in range(1,s.nrows):          
				   
				   TYPE_PT_SOUT=str(s .cell_value(r, 0))#.decode("utf-8")
				   Micro_MANCHO=str(s .cell_value(r, 1))#.decode("utf-8")
				   MANCHON=str(s .cell_value(r, 2))
				   PEO1=str(s .cell_value(r, 3))
				   PEO2=str(s .cell_value(r, 4))
				   PEO3=str(s .cell_value(r, 5))
				   
				   attr_TYPE_BLO=[TYPE_PT_SOUT,int(float(Micro_MANCHO)),int(float(MANCHON)),int(float(PEO1)),int(float(PEO2)),int(float(PEO3))]
				   Liste_TYPE_BLO.append(attr_TYPE_BLO)
				   

		#Recuperation des types BLO colonne 0
		for typeblo in Liste_TYPE_BLO:
			Liste_TYPE_BLO_Nat.append(typeblo[0])

		#1.Creation de la list des boites pour commencer les traitements 
		list_Boite_For_Compare=[]
		for shape_pbos in layershape_boite.getFeatures():
			
			nbre_log=0
			if shape_pbos[Nom_Colonne_nbrloge] != NULL:
				nbre_log=shape_pbos[Nom_Colonne_nbrloge]
				
			Compare_Max_Capa_rent=shape_pbos[Nom_Colonne_capacite_cable_rentrant]
			Compare_Max_Episssure= shape_pbos[Nom_Colonne_Nbre_EPISSURE]
			Compare_Max_NB_CB_Passage=shape_pbos[Nom_Colonne_nbre_cable_passage]
			Compare_Max_NB_CB_Sortant=shape_pbos[Nom_Colonne_nbre_cable_derivation]
			Compare_Max_NB_Log=nbre_log
			mod_pose=shape_pbos[Nom_Colonne_mode_pose_BOITE]
			nature_pt=shape_pbos[Nom_Colonne_mode_pose_nature_BOITE]
			#print nature_pt,';','MDP_NAT'
			#for TYPE_BLO in Liste_TYPE_BLO:
			if nature_pt not in Liste_TYPE_BLO_Nat:
				a= nature_pt
				
			
			attr_boite_compare=[shape_pbos[Nom_Colonne_capacite_cable_rentrant],shape_pbos[Nom_Colonne_Nbre_EPISSURE],shape_pbos[Nom_Colonne_nbre_cable_passage],shape_pbos[Nom_Colonne_nbre_cable_derivation],nbre_log,shape_pbos[shape_pbo_Nom_Colonne_Nom],mod_pose,'-1',nature_pt,'-1']
			#print attr_boite_compare
			list_Boite_For_Compare.append(attr_boite_compare)
			

		#2.Choix des ref_boites qui sont possibles avec creation dune liste de toutes les possibilites
		list_choix_ref_boite=[]
		for i in list_Boite_For_Compare:
			mdp_nat='-1'
			for fo_list in Liste_BPE_DEF:
				if fo_list[3] ==Nom_entite_MDP_ref_boite_souterrain and i[6] == Nom_Colonne_PT_STRUC_CHAMBRE and i[8] in Liste_TYPE_BLO_Nat:
					if int(i[0]) <= int(float(fo_list[4])) and int(i[1]) <= int(float(fo_list[5])) and int(i[2]) <= int(float(fo_list[6])) and int(i[3]) <= int(float(fo_list[7])) and int(i[4]) <= int(float(fo_list[8])):
						sum_boite=int(i[0])+int(i[1]) +int(i[2]) + int(i[3])+int(i[4]) 
						sum_ref=int(float(fo_list[4]))+int(float(fo_list[5]))+int(float(fo_list[6]))+int(float(fo_list[7]))+int(float(fo_list[8]))
						if sum_boite <= sum_ref:
							for counter, head_blo in enumerate(list_header_typblo):
								if fo_list[2] == head_blo:
									for TYPE_BLO in Liste_TYPE_BLO:
										if int(float(TYPE_BLO[counter])) != 0:
											attr=[i[5],i[6],sum_boite,sum_ref,fo_list[3],fo_list[0]]#[i_5,i_6,sum_boite,sum_ref,fo_list_3,fo_list_0]       
											list_choix_ref_boite.append(attr)

				elif fo_list[3] ==Nom_entite_MDP_ref_boite_aerien and i[6] == Nom_Colonne_PT_STRUC_POTEAU:
					if int(i[0]) <= int(float(fo_list[4])) and int(i[1]) <= int(float(fo_list[5])) and int(i[2]) <= int(float(fo_list[6])) and int(i[3]) <= int(float(fo_list[7])) and int(i[4]) <= int(float(fo_list[8])):
						sum_boite=int(i[0])+int(i[1]) +int(i[2]) + int(i[3])+int(i[4]) 
						sum_ref=int(float(fo_list[4]))+int(float(fo_list[5]))+int(float(fo_list[6]))+int(float(fo_list[7]))+int(float(fo_list[8]))
						if sum_boite <= sum_ref:
							attr=[i[5],i[6],sum_boite,sum_ref,fo_list[3],fo_list[0]]
							list_choix_ref_boite.append(attr)
				
				elif fo_list[3] ==Nom_entite_MDP_ref_boite_facade and i[6] == Nom_Colonne_PT_STRUC_FACADE:
					if int(i[0]) <= int(float(fo_list[4])) and int(i[1]) <= int(float(fo_list[5])) and int(i[2]) <= int(float(fo_list[6])) and int(i[3]) <= int(float(fo_list[7])) and int(i[4]) <= int(float(fo_list[8])):
						sum_boite=int(i[0])+int(i[1]) +int(i[2]) + int(i[3])+int(i[4]) 
						sum_ref=int(float(fo_list[4]))+int(float(fo_list[5]))+int(float(fo_list[6]))+int(float(fo_list[7]))+int(float(fo_list[8]))
						if sum_boite <= sum_ref:
							attr=[i[5],i[6],sum_boite,sum_ref,fo_list[3],fo_list[0]]
							list_choix_ref_boite.append(attr)
				
				elif fo_list[3] ==Nom_entite_MDP_ref_boite_immeuble and i[6] == Nom_Colonne_PT_STRUC_IMMEUBLE:
					if int(i[0]) <= int(float(fo_list[4])) and int(i[1]) <= int(float(fo_list[5])) and int(i[2]) <= int(float(fo_list[6])) and int(i[3]) <= int(float(fo_list[7])) and int(i[4]) <= int(float(fo_list[8])):
						sum_boite=int(i[0])+int(i[1]) +int(i[2]) + int(i[3])+int(i[4]) 
						sum_ref=int(float(fo_list[4]))+int(float(fo_list[5]))+int(float(fo_list[6]))+int(float(fo_list[7]))+int(float(fo_list[8]))
						if sum_boite <= sum_ref:
							attr=[i[5],i[6],sum_boite,sum_ref,fo_list[3],fo_list[0]]
							list_choix_ref_boite.append(attr)
		#3.Creation dun dictionnaire pour recuperer lunicite des boites ainsi que les references des boites possibles en se basant sur la somme minimum de la ref_boite
		#list_choix_ref_boite_Triee= sorted(list_choix_ref_boite,key=lambda colonnes: colonnes[3]) 
			#print mdp_nat,';',i[5]
		dict_nbre_cable_sortant=defaultdict(list)#{}
		for choix_ref_boite in list_choix_ref_boite:
			#a= choix_ref_boite[0],';',choix_ref_boite[1],';',choix_ref_boite[2],';',choix_ref_boite[3],';',choix_ref_boite[4],';',choix_ref_boite[5]
			dict_nbre_cable_sortant[choix_ref_boite[0]].append(choix_ref_boite[3])

		#4.Transfert de linfo dans la liste initiale des boites creer dans 1.
		for key, value in dict_nbre_cable_sortant.items():
			for choix_ref_boite in list_choix_ref_boite:
				if choix_ref_boite[0] == key and min(value) == choix_ref_boite[3]:
					for boite in list_Boite_For_Compare:
						if boite[5] == key:
							#Affecttation de la referne de la boite 
							boite[7]=choix_ref_boite[5]
							#print key,';',value,';',min(value),';',choix_ref_boite[4],';',choix_ref_boite[5],';',boite[6],';',boite[7]
							

		#5.Transfert dans le shape boite
		for boite in list_Boite_For_Compare:
			a=  boite[5],';',boite[1],';',boite[2],';',boite[3],';',boite[4],';',boite[5],';',boite[6],';',boite[7],';',boite[8]
			
		layershape_boite.startEditing()
		indexe_Nom_Colonne_REF_BOITE=layershape_boite.fieldNameIndex(Nom_Colonne_REF_BOITE)
		for shape_pbos in layershape_boite.getFeatures():
			for boite in list_Boite_For_Compare:
				if boite[5]==shape_pbos[shape_pbo_Nom_Colonne_Nom]:
					layershape_boite.changeAttributeValue(shape_pbos.id(),indexe_Nom_Colonne_REF_BOITE, unicode(boite[7]))

		layershape_boite.commitChanges()
		
		


	#Execution de la fonction ajout des champs
	#ajout_champs()
	#Execution de la fonction remplissage shape_boite
	TYPE_PROD_1()
	#Calcul prod2
	Type_prod_2()
	#Execution de la fonction du calcul du nombre de cassette
	calc_nbre_cassette()
	#Calcul type_fonc
	type_foncc()
	#Execution de la fonction calcul distance PBO_SRO
	Distance_PBO_SRO()
	#Execution de la fonction de distances PM_PBO_PTO dans sites
	distance_PM_PBO_PTO_SITES()
	#Execution de la fonction de calcul de la distance PBO_PTO a voil doiseau
	calcul_dist_PBO_PTO_VOl_OISEAU()
	"""#Execution de la fonction du calcul de statut isole du cable
	get_st_isole_boite()
	#Execution de la fonction du calcul de statut isole de la boite
	get_st_isole_cable()
	"""
	#Execution de la fonction calcul reference de la boite
	choix_ref_boite()

	QMessageBox.information(w, "Message-Execution-Plugin", succesMsg)