#!/usr/bin/envpython3
#coding: utf-8                                                                                                                                                                                                                                                                                                                          


import requests, sys
#sys.path.append('/../BoitesFonctionelles/')
import json
import os
import argparse
import logging
import time
import re
from collections import defaultdict



def cleanspace(text):
    """What this function does?
    inputs:
        text with space
    output:
        same text without space
    """
    m_space=re.compile("\s+")
    text_clean=re.sub(m_space,'',text)
    return text_clean

if __name__ == "__main__":

    parser = argparse.ArgumentParser ( description="")
    parser.add_argument('-c', '--chromosome', dest="chromosome", default='',help="Enter the path to the file which contain the configuration of all program")
    parser.add_argument('-p','--plage',dest="plage", type=int, nargs='+', action='append', 
    help='file list')
    parser.add_argument('-j','--json',dest="json",default='',help="Enter the path to the file which contain the exit of chromosome.json")
    parser.add_argument('-t','--table',dest="table",default='',help="Enter the path to the file which contain the configuration of all program")
    parser.add_argument('-r','--result',dest="result",default='',help="Enter the path to the file which contain the result of all program")

    args=parser.parse_args()
    chromosome=args.chromosome
    chromosome=chromosome.split("/")[-1]
    chromosome=chromosome.split(".")[-3:-1]
    chromosome="".join(chromosome)+'.json'
    pathJson=args.json
    listPlage=args.plage
    pathTableInteractants=args.table
    pathResult=args.result
    nombreGeneCodant=0
    listIdTranscrit=()
    pathResult=cleanspace(pathResult +"/"+str(listPlage)+"/")
    if not os.path.exists(pathResult):
      os.makedirs(pathResult)
    

    with open(pathJson+chromosome,"r") as json_data:
        data=json.load(json_data)
        for plage,boite in data.items():
            if 'Mrna' in list(data[plage].keys()):
                for i in data[plage]['Mrna']:
                    listIdTranscrit+=(i['Id_transcrit'].split('.')[0],)
                    print("coucou")
                    print(listIdTranscrit,"List Id Transcrit")
                    
    dicoIdEnst_Uniprot=defaultdict(list)
    

    with open(pathTableInteractants,"r") as f1:
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
                dicoIdEnst_Uniprot[idTranscrit].append(UniProtKBGeneNameID)

    dicoResult=defaultdict(list)
    print(dicoResult,"DicoResult")

    for i in listIdTranscrit:
        if i in list(dicoIdEnst_Uniprot.keys()):
          for j in dicoIdEnst_Uniprot[i]:
            dicoResult[j].append(i)
    lenDico=0
    for i in dicoResult:
      lenDico+=len(dicoResult[i])

    print(dicoResult)
 
    dicoIdProtInteract=defaultdict()  
    
    for i in dicoResult:
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/interaction/"
        requestURL+=i
        r = requests.get(requestURL, headers={ "Accept" : "application/json"})

        if not r.ok:
            continue

        responseBody = r.text
        data=json.loads(responseBody)

        dicoInteractant=data[0]
        dicoInteractant['idTranscrit']=dicoResult[i]
        
        with open(pathResult+i+".json","w") as result:
            json.dump(dicoInteractant,result,indent=2)
            result.close()

      
      

