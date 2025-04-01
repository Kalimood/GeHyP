#!/usr/bin/envpython3
#coding: utf-8
import json
import os
import re
import sys
import time
import copy
import csv
import logging
from numpy.core.numeric import NaN
import pandas as pd
import argparse
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t Protein -e  homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat -p  1 600000 -p 750000 900000 -p 950000 1500000 -j /home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/ -i /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab -r /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/ResultJson
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/Scripttest/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 11000000 12000000 -p 5900000 6000000 -p 11000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/TableENSG-MIR.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json/ -r /home/kevin/Bureau/StageM2/Scripttest/Result
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/Scripttest/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 5000000 7000000 -p 10000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/TableENSG-MIR.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json/ -r /home/kevin/Bureau/StageM2/Scripttest/Result -n /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/Table_ENSG_NCBI.txt -u /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tabpython3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/Scripttest/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 5000000 7000000 -p 10000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/TableENSG-MIR.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json/ -r /home/kevin/Bureau/StageM2/Scripttest/Result -n /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/Table_ENSG_NCBI.txt -u /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab
# Position miRNA Chromosome 2: 11767444..11767525 ; 5974662..5974732 ; 11836933..11836986
#Position 
if __name__ == "__main__":
    parser = argparse.ArgumentParser ( description="")
    parser.add_argument('-c', '--chromosome', dest="chromosome", default='',help="Enter the path to the file which contain the chromosome files downloaded from Ensembl")
    parser.add_argument('-p','--plage',dest="plage", type=int, nargs='+', action='append', 
    help='Enter the plage(s) you want to parse like -p 1 10000 -p 20000 450000')
    parser.add_argument('-j','--json',dest="json",default='',help="Enter the path to the file which contain the result from the parsing of the script Boite Fonctionelle")
    parser.add_argument('-t','--table',dest="table",default='',help="Enter the path to the file which contain the conversion table between ENSG ID and Mir ID, available at Biomart")
    parser.add_argument('-n','--ncbi',dest="ncbi",default='',help="Enter the path to the file which contain the conversion table between ENSG ID and NCBI ID, available at Biomart ")
    parser.add_argument('-u','--uniprot',dest="uniprot",default='',help="Enter the path to the file which contain the conversion table between ENST ID and UniProt ID, available at Biomart")
    parser.add_argument('-r','--result',dest="result",default='',help="Enter the path to the file which contain the result of the program")

    
    args=parser.parse_args()

    chromosome=args.chromosome
    chromosome=chromosome.split("/")[-1]
    chromosome=chromosome.split(".")[-3:-1]
    chromosome="".join(chromosome)+'.json'
    result=args.result
    listPlage=args.plage
    pathTableInteractants=args.table
    pathTableEnstNcbi=args.ncbi
    pathTableEnstUniprot=args.uniprot

    #Probleme de chemin du json(un espace en trop)
    #/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/[[1, 600000], [750000, 900000]] --> /home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/[[1,600000],[750000,900000]]/
   
    # m_space=re.compile("\s+")
    # pathJson=args.json+str(listPlage)+'/'
    # pathJson=re.sub(m_space,'',pathJson)
    pathJson=args.json
    

    #localfilesJson=os.listdir(pathJson)
    #print(localfilesJson)

    dicoMirCorr=defaultdict(list)
    listDicoMirJson=[]
    #print(chromosome)

    with open(pathJson+chromosome,'r',encoding='utf-8') as json_data:
        data=json.load(json_data)
        #print(data)

        for plage,boite in data.items():
            #data={['plage']:{'Type':[{TypeBoite:Val ,Nom:Val , Positions:[[Val]],Locus:Val, Note:Val, NumberBoxe:Val}]}}
            for i in range(len(data[plage]['Misc_rna'])):
                if data[plage]['Misc_rna'][i]["Note"]=='miRNA':
                    data[plage]['Misc_rna'][i]["Id_gene"]=data[plage]['Misc_rna'][i]["Id_gene"].split(".")[0]
                    
                    #print(data[plage]['Misc_rna'][i]["Id_gene"])
                    listDicoMirJson.append(copy.deepcopy(data[plage]['Misc_rna'][i]))
                    #On utilise deepcopy pour copier le dico et les rendre indépendant(pas de modification de l'un si l'autre est modifié)

    

    #pathTableMir='/home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw'
    #os.chdir(pathTableMir)
    #dataMir=os.listdir(pathTableMir)
    #print(dataMir)


    dicoEnsgMir=defaultdict(list)
    listDico=[]

    #with open("TableENSG-MIR.tab","r") as f1:
    with open(pathTableInteractants,"r") as f1:
        for li in f1:
            ln=li.rstrip("\n")
            ls=ln.split("\t")
            #print(ls)
            idENSG=ls[0]
            idVersENSG=ls[1]
            idTranscrit=ls[2]
            idTranscritVersion=ls[3]
            mirBaseAccession=ls[4]
            mirBaseId=ls[5]
            if len(mirBaseId)>0:
                dicoEnsgMir[idENSG].append(mirBaseId)

    

    #print(dicoIdUniprot_Ensg)
    for i in listDicoMirJson:
        print(i["Id_gene"])
        for j in dicoEnsgMir:
            if i["Id_gene"]==j:
                dicoMirCorr[i["Id_gene"]]=(dicoEnsgMir[j])
                break


    listmir2=[]
    for listmir in dicoMirCorr.values():
        for mir in listmir:
            listmir2.append(mir)
    
    mir=", ".join(listmir2)
     

#Envoi de la Requête a mirdb
urlMining='http://mirdb.org/mirdb/mining.html'
urlTableau='http://mirdb.org/cgi-bin/mining.cgi'
#print(listmir2)

requests.get(urlMining)
interMir={'searchType':'miRNA','excludeGene':'ON','minScore':'90','excludeMir':'ON','maxTarget':'2000','species':'Human','miRsample':'on','searchBox':mir,'submitButton':'Go'}
print(interMir)
reponse=requests.post(urlTableau,data=interMir)

#print(reponse.text)

dfs=pd.read_html(reponse.text,header=None)
dfInteract=dfs[1]
#print(dfInteract)
header=dfInteract.head(1)
header=header.values.tolist()[0]

#print(header)

#dfInteract=pd.DataFrame([dfInteract],columns=header)
dfInteract.columns=header
dfInteract.drop(0,0,inplace=True)
del dfInteract['Target Detail']
#print(dfInteract.head(10))


#print(dfInteract)

#print(dfInteract.columns)
GeneNcbi=dfInteract.iloc[:,[3]].values.tolist()

#print(listGeneNcbi)
#exit(GeneNcbi)
dicoNcbi_Enst=defaultdict(list)
with open(pathTableEnstNcbi,mode="r") as f1:
    for li in f1:
        ln=li.rstrip("\n")
        ls=ln.split("\t")
        #print(ls)
        idENSG=ls[0]
        idVersENSG=ls[1]
        idTranscrit=ls[2]
        idTranscritVersion=ls[3]
        NcbigeneId=ls[4]
        #print(idTranscrit)
        if len(NcbigeneId)>0:
            dicoNcbi_Enst[NcbigeneId].append(idTranscrit)



dicoEnst_Uniprot=defaultdict(list)
#print(pathTableEnstUniprot)    


with open(pathTableEnstUniprot,"r") as f1:
    for li in f1:
        ln=li.rstrip("\n")
        ls=ln.split("\t")
        idENSG=ls[0]
        idVersENSG=ls[1]
        idTranscrit=ls[2]
        idTranscritVersion=ls[3]
        UniProtKBGeneNameID=ls[4]
        UniprotKbSwissProtId=ls[5]
        if len(UniProtKBGeneNameID)>0:
            dicoEnst_Uniprot[idTranscrit].append(UniProtKBGeneNameID)

#print(ValueGeneNcbi)
#print(GeneNcbi)
#print(dfInteract['Gene Symbol'])
#exit(dicoEnst_Uniprot)
dicoNcbiUniprot=defaultdict(set)


#print(len(dicoNcbi_Enst))
compteur=0
#print("coucou")
#Compteur pour reduire temps de script 
for ncbi in dicoNcbi_Enst:
    compteur+=1
    if compteur== 200:
        break
    for i in dicoNcbi_Enst[ncbi]:
        if i in list((dicoEnst_Uniprot.keys())):
            dicoNcbiUniprot[ncbi]=set.union(set(dicoEnst_Uniprot[i]),set(dicoNcbiUniprot[ncbi]))
#Probleme de Longeur de liste des valeurs du dicoNCBIuniprot!!!
exit(dicoResult)
#print(dicoNcbiUniprot)
for i in dicoNcbiUniprot:
    #print("{} : \t {}".format(i,dicoNcbiUniprot[i][0:7]))
    dicoNcbiUniprot[i]=[list(dicoNcbiUniprot[i])]
#print(dicoNcbiUniprot['FCAR'])


dfNcbiUniprot=pd.DataFrame.from_dict(dicoNcbiUniprot,orient='index')

dfNcbiUniprot.index.name='Gene Symbol'
#print(dfNcbiUniprot)
dfNcbiUniprot.reset_index(inplace=True)
#dfNcbiUniprot.drop[0,1]
dfResult=pd.merge(dfInteract,dfNcbiUniprot,on="Gene Symbol",how='left')

dfResult.rename(columns={0:'Id Uniprot'},inplace=True)
#exit(dfResult)
dfResult.to_csv(path_or_buf=result, sep='\t',index=False)
#print('yo')
#Ecriture du dataFrame
#dicoResult=dfResult.set_index("Gene Symbol").to_dict()[0]
dicoResult=dfResult.set_index("Gene Symbol").to_dict()['Id Uniprot']

#print(dfResult.iloc[:,[3]])
#print(dfNcbiUniprot.head())
print("DicoResult")
print(dicoResult)

#localPathExit = result+"/"+str(listPlage)+"/"
if not os.path.exists(result):
    os.makedirs(result)
    os.chdir(result)

for i in dicoResult:
    #print(dicoResult[i],'dicoResult[i]')
    #print(i)
    #print(type(dicoResult[i]))
    #print(type(0.1))
    if type(0.1) ==type(dicoResult[i]):
        continue

    for j in dicoResult[i]:
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/interaction/"
        requestURL+=j
        print(requestURL)
        r = requests.get(requestURL, headers={ "Accept" : "application/json"})


        #print(j)
        if not r.ok:
            #r.raise_for_status()
            continue

        responseBody = r.text
        data=json.loads(responseBody)

        dicoInteractant=data[0]
        #print(dicoInteractant)
        dicoInteractant['idGeneNcbi']=i

        with open(result+i+".json","w") as sortie:
            json.dump(dicoInteractant,sortie,indent=2)
            sortie.close()

    


'''
données formulaire
searchType	"miRNA"
FuncMir	"ON"
excludeGene	"ON"
minScore	"60"
excludeMir	"ON"
maxTarget	"2000"
species	"Human"
miRsample	"on"
searchBox	"hsa-let-7a-5p,+hsa-miR-1-3p,+hsa-miR-9-3p"
submitButton	"Go"
'''
