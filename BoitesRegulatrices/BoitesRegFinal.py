#!/usr/bin/python3
#coding: utf-8
__author__="Kevin Rayas"

#Library import
from collections import defaultdict
from copy import deepcopy
import os
import gzip
import logging
from posixpath import join
import re
import sys
import json
import argparse
import urllib
from urllib import request
import ftplib 

#Library Class import
from collections import defaultdict
from Position import Position
from CtcfBindingsite import CtcfBindingsite
from OpenChromatineRegion import OpenChromatineRegion
from Enhancer import Enhancer
from Promoter import Promoter
from PromoterFlank import PromoterFlank
from TfBindingSite import TfBindingSite
from ValueBoxes import ValueBoxes

def download(espece,result):
	ftp = ftplib.FTP('ftp.ensembl.org')
	ftp.login()
	ftp.cwd('/pub/release-104/regulation/'+espece)
	files=ftp.nlst()
	
	local_Destination_Path = result+"/"+espece +"/"
	urlName='http://ftp.ensembl.org/pub/release-104/regulation/'+espece+'/'
	print(local_Destination_Path)
	

	if not os.path.exists(local_Destination_Path):
		os.makedirs(local_Destination_Path)
	else:
		logging.info(local_Destination_Path,"The directory is already created")

	os.chdir(local_Destination_Path)

	for fichier in files:
		if fichier.endswith('.gz'):
			regulatory=fichier
			regulatoryshort = os.path.splitext(regulatory)[0]
			local_filename=os.listdir(local_Destination_Path)

			if regulatoryshort in local_filename:
				print(regulatoryshort,"is already downloaded")
			else:
				logging.info("Opening",(urlName)+ ":::"+regulatory)

				try:
					with urllib.request.urlopen(urlName+regulatory) as response:

						try :
							with gzip.GzipFile(fileobj=response) as uncompressed:
								file_content = uncompressed.read()
							fileOutName=os.path.splittext(regulatory)
							print(fileOutName)
												
							logging.info("Loading and decompression successful",regulatoryshort)
						except :
							logging.error("Unable to decompress file",regulatoryshort)
					try :
						with open(regulatoryshort, 'wb') as f:
							f.write(file_content)
					except :
						logging.error("Error opening file for output",regulatoryshort)
				
				except:
					logging.error("Error at opening url request : ",urlName)

	
	return str(local_Destination_Path)


def FillDicoJson(dico,dicoGlobPlageType,cle):
		dicoResult=defaultdict(int)
		for plage,listReg in dico.items():
			NumberPlage=len(listReg)
			dicoResult[plage]+=NumberPlage

			for regul in listReg:
				regulVal=regul.obj_dict()
				dicoGlobPlageType[plage][cle].append(regulVal)

		return dicoResult

if __name__ == "__main__":
	parser = argparse.ArgumentParser ( description="")
	parser.add_argument('-c', '--chromosome', dest="chromosome", default='/home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat', help="Enter the path to the file which contain all the data of chromosome ending by.dat from Ensembl (/pub/current_embl/'+espece)")
	parser.add_argument('-e', '--espece', dest="espece", default='homo_sapiens',help="""Enter the name of the specie you want to study""")
	parser.add_argument('-p','--plage',dest="plage",type=int, nargs='+', action='append', help='enter the plage you want like -p 1 4000000 -p 400500 990000')
	parser.add_argument('-r', '--result', dest="result", help="""Enter the path of the result you want t""")
	parser.add_argument('-f', '--fichier', dest="fichier", help="""Enter the path of the file you want to parse""")
	args=parser.parse_args()

	chromosome=args.chromosome
	espece=args.espece
	listPlage=args.plage
	result=args.result
	fichier=args.fichier

	
	#exit(args)
	dico_Position=defaultdict(dict)
	dicoBoitesReg=defaultdict(list)
	dicoCtcfPlage=defaultdict(list)
	dicoTfBindSitePlage=defaultdict(list)
	dicoOpenChromPlage=defaultdict(list)
	dicoEnhancePlage=defaultdict(list)
	dicoPromPlage=defaultdict(list)
	dicoPromFlankPlage=defaultdict(list)

	listPositions=[]
	listObjects=[]
	listCTCF_binding_site=[]
	listTF_binding_site=[]
	listOpen_chromatin_region=[]
	listEnhancer=[]
	listPromoter=[]
	listPromoter_flanking_region=[]
	m_Chromosome=re.compile("^\d+|^[X]|^[Y]")

	retourdwnlod=download(espece,result)

	
	'''
	for i in range(2,len(sys.argv)):
		#print(i)
		plage=sys.argv[i]
		plage=plage.split(",")
		start=int(plage[0])
		end=int(plage[1])
		listPlage.append([start,end])
	'''

	with open (fichier,mode="rt") as f1:
		for li in f1:
			li = li.rstrip("\n")
			ls=li.split("\t")
			Chromosome=m_Chromosome.search(ls[0])

			if Chromosome:
				numChr=ls[0]

				if numChr==chromosome:						
					typeBoite=ls[2]
					startBoitesReg=ls[3]
					endBoitesReg=ls[4]
					listPositions.clear()
					listPositions.append(startBoitesReg)
					listPositions.append(endBoitesReg)
					infos=ls[8].split(";")
					idEnsr=infos[0].split(":")
					idEnsr=idEnsr[1]

					for i in range(len(listPlage)):
						start=listPlage[i][0]
						end=listPlage[i][1]

						if typeBoite=="CTCF_binding_site":							
							CtcfBind=CtcfBindingsite(numChr,list(listPositions),idEnsr,typeBoite)
							if CtcfBind.inRange(start,end):
								dicoCtcfPlage[str(listPlage[i])].append(CtcfBind)

						elif typeBoite=="TF_binding_site":
							TFBindSite=TfBindingSite(numChr,list(listPositions),idEnsr,typeBoite)
							if TFBindSite.inRange(start,end):
								dicoTfBindSitePlage[str(listPlage[i])].append(TFBindSite)
								print("coucou2")
								print(dicoTfBindSitePlage)

						elif typeBoite=="open_chromatin_region":
							OpenChromRegion=OpenChromatineRegion(numChr,list(listPositions),idEnsr,typeBoite)
							if OpenChromRegion.inRange(start,end):
								dicoOpenChromPlage[str(listPlage[i])].append(OpenChromRegion)
								listOpen_chromatin_region.append(OpenChromRegion)


						
						elif typeBoite=="enhancer":
							Enhance=Enhancer(numChr,list(listPositions),idEnsr,typeBoite)
							if Enhance.inRange(start,end):
								dicoEnhancePlage[str(listPlage[i])].append(Enhance)
								listEnhancer.append(Enhance)

						elif typeBoite=="promoter":
							Promote=Promoter(numChr,list(listPositions),idEnsr,typeBoite)
							if Promote.inRange(start,end):
								dicoPromPlage[str(listPlage[i])].append(Promote)
								listPromoter.append(Promote)
									
						elif typeBoite=="promoter_flanking_region":
							PromoterFlan=PromoterFlank(numChr,list(listPositions),idEnsr,typeBoite)
							if PromoterFlan.inRange(start,end):
								dicoPromFlankPlage[str(listPlage[i])].append(PromoterFlan)
								listPromoter_flanking_region.append(PromoterFlan)

						else:
							logging.info("Autre boite")
		
	
	dicoGlobRegPlageType=defaultdict(lambda:defaultdict(list))
	listCtcfPlageNum=[]
	listTfBindPlageNum=[]
	listOpenChromPlageNum=[]
	listEnhancePlageNum=[]
	listPromPlageNum=[]
	listPromFlkPlageNum=[]

	dicoPlageCtCf_num=defaultdict(int)
	dicoPlageTfBind_num=defaultdict(int)
	dicoPlageOpenChromBind_num=defaultdict(int)
	dicoPlageEnhance_num=defaultdict(int)
	dicoPlageProm_num=defaultdict(int)
	dicoPlagePromFlk_num=defaultdict(int)

	compteur= 0

	dicoPlageCtCf_num=deepcopy(FillDicoJson(dicoCtcfPlage,dicoGlobRegPlageType,"Ctcf"))
	dicoPlageTfBind_num=deepcopy(FillDicoJson(dicoTfBindSitePlage,dicoGlobRegPlageType,"TfBindingSite"))
	dicoPlageOpenChromBind_num=deepcopy(FillDicoJson(dicoOpenChromPlage,dicoGlobRegPlageType,"OpenChromatine"))
	dicoPlageEnhance_num=deepcopy(FillDicoJson(dicoEnhancePlage,dicoGlobRegPlageType,"Enhancer"))
	dicoPlageProm_num=deepcopy(FillDicoJson(dicoPromPlage,dicoGlobRegPlageType,"Promoter"))
	dicoPlagePromFlk_num=deepcopy(FillDicoJson(dicoPromFlankPlage,dicoGlobRegPlageType,"Promoter_Flanking_Region"))


	for plage in listPlage:
		plage='['+', '.join(map(str,plage))+']'
		CtcfNumber=[0,plage]
		TfNumber=[0,plage]
		OpenChromNumber=[0,plage]
		EnhancNumber=[0,plage]
		PromoteNumber=[0,plage]
		PromoteFlkNumber=[0,plage]
		
		if plage in dicoPlageCtCf_num.keys():
			CtcfNumber=[dicoPlageCtCf_num[plage],plage]

		if plage in dicoPlageTfBind_num.keys():
			TfNumber=[dicoPlageTfBind_num[plage],plage]

		if plage in dicoPlageOpenChromBind_num.keys():
			OpenChromNumber=[dicoPlageOpenChromBind_num[plage],plage]

		if plage in dicoPlageEnhance_num.keys():
			EnhancNumber=[dicoPlageEnhance_num[plage],plage]

		if plage in dicoPlageProm_num.keys():
			PromoteNumber=[dicoPlageProm_num[plage],plage]

		if plage in dicoPlagePromFlk_num.keys():
			PromoteFlkNumber=[dicoPlagePromFlk_num[plage],plage]
	
		totalNumberRegulBox=CtcfNumber+TfNumber+OpenChromNumber+EnhancNumber+PromoteNumber+PromoteFlkNumber
		regulatoryValues=ValueBoxes(CtcfNumber,TfNumber,OpenChromNumber,EnhancNumber,PromoteNumber,PromoteFlkNumber,totalNumberRegulBox)
		jsonRegulatoryValues=regulatoryValues.obj_dict()
		dicoGlobRegPlageType[plage]["RegulatoryValues"].append(jsonRegulatoryValues)

	print('--------------------------------------------Ecriture JSON Du Parsing----------------------------------------------------------')
	
	print(result,"result")
	localPathExit = result+"/"+str(listPlage)+"/"
	print(localPathExit,"localPathExit")
	if not os.path.exists(localPathExit):
		os.makedirs(localPathExit)
		logging.info("Le fichier de sortie Json est creer")

	os.chdir(localPathExit)
	try:
		with open("Regulatory Chromosome"+chromosome+".json","w",encoding="utf-8") as fichier:
			json.dump(dicoGlobRegPlageType,fichier,indent=2)
			fichier.close()

	except:
		logging.error("Error Writting Files")
	
	






